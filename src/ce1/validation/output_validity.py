"""Output validity gate for CE-1 experiments.

Every model response used as an experimental observation must pass this
gate before it can enter analysis. A response that fails any check is
INVALID and must not be scored or included in any mean.

Design principle: fail loudly, never silently. An invalid trial is recorded
with its invalidity reason, not dropped or scored as zero.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from typing import Any


@dataclass
class TrialValidity:
    """Result of validating a single model response."""
    valid: bool
    reason: str  # empty string if valid
    response_text: str = ""
    done_reason: str | None = None
    eval_count: int | None = None
    metadata_complete: bool = True
    missing_fields: list[str] = field(default_factory=list)


# Required metadata fields for a trial to be considered complete.
REQUIRED_TRIAL_FIELDS = ["condition", "attempt_index", "seed", "prompt_hash",
                        "done_reason", "response", "timestamp_started",
                        "timestamp_finished"]

# Required top-level result fields.
REQUIRED_RESULT_FIELDS = ["experiment", "protocol_version", "experiment_version",
                         "model", "timestamp", "reps_requested", "threshold",
                         "tolerance", "conditions"]


def is_valid_trial(response: dict, required_fields: list[str] | None = None) -> TrialValidity:
    """Validate a single model response.

    Returns a TrialValidity with valid=True only if ALL of the following hold:
    1. response is a dict
    2. response text is present and non-empty (not whitespace-only)
    3. done_reason is present and is "stop" (not "length", not None, not unexpected)
    4. response is not an API error payload
    5. all required metadata fields are present

    Conservative policy: missing done_reason → invalid (not assumed valid).
    """
    if required_fields is None:
        required_fields = []

    if not isinstance(response, dict):
        return TrialValidity(valid=False, reason="invalid_response_type",
                            response_text="", done_reason=None)

    text = response.get("response")
    if text is None:
        return TrialValidity(valid=False, reason="missing_response",
                            response_text="", done_reason=response.get("done_reason"))
    if not isinstance(text, str) or not text.strip():
        return TrialValidity(valid=False, reason="empty_response",
                            response_text=text or "", done_reason=response.get("done_reason"))

    done_reason = response.get("done_reason")
    if done_reason is None:
        return TrialValidity(valid=False, reason="missing_done_reason",
                            response_text=text, done_reason=None)
    if done_reason == "length":
        return TrialValidity(valid=False, reason="truncated_length",
                            response_text=text, done_reason=done_reason)
    if done_reason not in ("stop",):
        return TrialValidity(valid=False, reason="unexpected_done_reason",
                            response_text=text, done_reason=done_reason)

    # Check for API error payload
    if "error" in response and isinstance(response.get("error"), str):
        return TrialValidity(valid=False, reason="api_error",
                            response_text=text, done_reason=done_reason)

    # Check required metadata fields
    missing = [f for f in required_fields if f not in response or response.get(f) is None]
    if missing:
        return TrialValidity(valid=False, reason="missing_required_metadata",
                            response_text=text, done_reason=done_reason,
                            metadata_complete=False, missing_fields=missing)

    # Check for NaN/infinity in numeric fields
    for key in ("eval_count",):
        val = response.get(key)
        if isinstance(val, float) and (math.isnan(val) or math.isinf(val)):
            return TrialValidity(valid=False, reason="nan_or_inf_value",
                                response_text=text, done_reason=done_reason)

    return TrialValidity(valid=True, reason="", response_text=text,
                        done_reason=done_reason,
                        eval_count=response.get("eval_count"))


def is_valid_result(result: dict) -> tuple[bool, str]:
    """Validate a complete experiment result file.

    Returns (valid, reason). Checks:
    1. All required top-level fields present
    2. At least one condition with trials
    3. No condition has all-invalid trials without reporting
    4. No verdict claim of "supported" with insufficient valid trials
    """
    if not isinstance(result, dict):
        return False, "result is not a dict"

    missing = [f for f in REQUIRED_RESULT_FIELDS if f not in result]
    if missing:
        return False, "missing top-level fields: %s" % missing

    conditions = result.get("conditions", {})
    if not conditions:
        return False, "no conditions present"

    for cond_name, cond in conditions.items():
        if not isinstance(cond, dict):
            return False, "condition %s is not a dict" % cond_name
        trials = cond.get("trials", [])
        if not isinstance(trials, list):
            return False, "condition %s trials is not a list" % cond_name
        # Check that invalid trials have invalidity reasons
        for trial in trials:
            if not trial.get("valid", True) and not trial.get("invalidity_reason"):
                return False, "invalid trial in %s has no invalidity reason" % cond_name

    # Check comparison/verdict
    comparison = result.get("comparison", {})
    if isinstance(comparison, dict):
        verdict = comparison.get("verdict")
        if verdict is not None and verdict not in ("INCONCLUSIVE", "INVALID_RUN", "VALID_SUPPORTING_RESULT", "VALID_NULL_RESULT"):
            return False, "invalid verdict value: %s" % verdict

    return True, "ok"


def check_truncation(response: dict) -> bool:
    """Return True if the response was truncated."""
    return response.get("done_reason") == "length"


def check_empty_response(response: dict) -> bool:
    """Return True if the response is empty or whitespace-only."""
    text = response.get("response", "")
    return not text or not text.strip()


def check_api_error(response: dict) -> bool:
    """Return True if the response contains an API error."""
    return "error" in response and isinstance(response.get("error"), str)


def check_missing_metadata(response: dict, required: list[str]) -> list[str]:
    """Return list of missing required metadata fields."""
    return [f for f in required if f not in response or response.get(f) is None]


def check_nan_inf(values: list) -> bool:
    """Return True if any value is NaN or infinity."""
    for v in values:
        if isinstance(v, float) and (math.isnan(v) or math.isinf(v)):
            return True
    return False


def check_overlap(episode_text: str, scoring_keywords: list[str]) -> list[str]:
    """Check if any scoring keyword appears in the episode text.

    Returns list of overlapping keywords. Empty list means no overlap.
    This is a simple substring check (case-insensitive).
    """
    lower = episode_text.lower()
    return [kw for kw in scoring_keywords if kw.lower() in lower]


def validate_experiment_result(result: dict) -> tuple[bool, list[str]]:
    """Validate a complete experiment result file.

    Returns (valid, list of issues).
    """
    issues = []
    ok, reason = is_valid_result(result)
    if not ok:
        issues.append(reason)
        return False, issues

    # Check that no condition has all-invalid trials without reporting
    for cond_name, cond in result.get("conditions", {}).items():
        trials = cond.get("trials", [])
        invalid = [t for t in trials if not t.get("valid", True)]
        if len(invalid) == len(trials) and len(trials) > 0:
            issues.append("condition %s has ALL invalid trials" % cond_name)

    # Check that verdict is not 'supported' when there are invalid trials
    comparison = result.get("comparison", {})
    verdict = comparison.get("verdict", "")
    if "supported" in verdict.lower():
        for cond in result.get("conditions", {}).values():
            if any(not t.get("valid", True) for t in cond.get("trials", [])):
                issues.append("verdict claims support but some trials are invalid")

    # Check reproducibility metadata
    required_top = ["protocol_version", "experiment_version", "model", "timestamp"]
    for field in required_top:
        if field not in result:
            issues.append("missing reproducibility field: %s" % field)

    return len(issues) == 0, issues

