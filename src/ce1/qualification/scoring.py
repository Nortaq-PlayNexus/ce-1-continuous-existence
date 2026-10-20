"""Scoring logic for the model qualification suite.

Classifies each trial as VALID_PASS, VALID_FAIL, or INVALID_TRIAL.
No model calls are made.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from typing import Any


@dataclass
class TrialScore:
    """Score result for a single qualification trial."""
    trial_id: str
    status: str  # VALID_PASS, VALID_FAIL, INVALID_TRIAL
    reason: str  # empty if VALID_PASS or VALID_FAIL; invalidity reason if INVALID_TRIAL
    parsed_answer: str | None = None
    parsed_evidence_id: str | None = None
    parsed_confidence: float | None = None
    expected_answer: str | None = None
    expected_evidence_id: str | None = None
    answer_correct: bool = False
    evidence_correct: bool = False
    confidence_valid: bool = False


def parse_response(raw: str) -> dict | None:
    """Parse a raw model response as JSON. Returns None if unparseable."""
    if not raw or not raw.strip():
        return None
    text = raw.strip()
    # Try to extract JSON from markdown code blocks
    if text.startswith("```"):
        lines = text.split("\n")
        json_lines = []
        in_block = False
        for line in lines:
            if line.strip().startswith("```"):
                if in_block:
                    break
                in_block = True
                continue
            if in_block:
                json_lines.append(line)
        if json_lines:
            text = "\n".join(json_lines).strip()
    try:
        return json.loads(text)
    except (json.JSONDecodeError, ValueError):
        return None


def validate_trial(
    trial_id: str,
    raw_response: str,
    done_reason: str | None,
    expected_answer: str,
    expected_evidence_id: str | None,
    is_truncated: bool = False,
) -> TrialScore:
    """Validate and score a single qualification trial.

    Returns a TrialScore with status VALID_PASS, VALID_FAIL, or INVALID_TRIAL.
    """
    # Check truncation first
    if is_truncated or done_reason == "length":
        return TrialScore(
            trial_id=trial_id,
            status="INVALID_TRIAL",
            reason="truncated",
            expected_answer=expected_answer,
            expected_evidence_id=expected_evidence_id,
        )

    # Check empty response
    if not raw_response or not raw_response.strip():
        return TrialScore(
            trial_id=trial_id,
            status="INVALID_TRIAL",
            reason="empty_response",
            expected_answer=expected_answer,
            expected_evidence_id=expected_evidence_id,
        )

    # Check unexpected done_reason
    if done_reason is not None and done_reason not in ("stop",):
        return TrialScore(
            trial_id=trial_id,
            status="INVALID_TRIAL",
            reason="unexpected_done_reason",
            expected_answer=expected_answer,
            expected_evidence_id=expected_evidence_id,
        )

    # Parse JSON
    parsed = parse_response(raw_response)
    if parsed is None:
        return TrialScore(
            trial_id=trial_id,
            status="INVALID_TRIAL",
            reason="unparseable_json",
            expected_answer=expected_answer,
            expected_evidence_id=expected_evidence_id,
        )

    # Check required fields
    if not isinstance(parsed, dict):
        return TrialScore(
            trial_id=trial_id,
            status="INVALID_TRIAL",
            reason="not_a_dict",
            expected_answer=expected_answer,
            expected_evidence_id=expected_evidence_id,
        )

    for field in ("answer", "evidence_id", "confidence"):
        if field not in parsed:
            return TrialScore(
                trial_id=trial_id,
                status="INVALID_TRIAL",
                reason="missing_field_%s" % field,
                expected_answer=expected_answer,
                expected_evidence_id=expected_evidence_id,
            )

    # Extract parsed values
    answer = str(parsed.get("answer", "")).strip()
    evidence_id = parsed.get("evidence_id")
    # Handle string "null" as None
    if isinstance(evidence_id, str) and evidence_id.lower() in ("null", "none", ""):
        evidence_id = None
    if evidence_id is not None:
        evidence_id = str(evidence_id).strip()
    confidence = parsed.get("confidence")

    # Validate confidence
    confidence_valid = False
    if isinstance(confidence, (int, float)) and not isinstance(confidence, bool):
        if not (isinstance(confidence, float) and (math.isnan(confidence) or math.isinf(confidence))):
            if 0.0 <= confidence <= 1.0:
                confidence_valid = True

    # Normalize answers for comparison (case-insensitive, strip units/prefixes)
    def _normalize(s):
        s = str(s).lower().strip()
        # Remove common prefixes
        for prefix in ("job ", "task ", "service ", "module ", "disk ", "the "):
            if s.startswith(prefix):
                s = s[len(prefix):]
        # Remove trailing units for numeric answers
        s = s.split()[0] if s and s[0].isdigit() else s
        return s

    # Score answer and evidence
    answer_correct = (_normalize(answer) == _normalize(expected_answer))

    # For contradiction items, evidence citation is flexible (citing conflicting sources is valid)
    if expected_answer and _normalize(expected_answer) == "contradiction":
        evidence_correct = True
    elif expected_evidence_id is not None:
        evidence_correct = (evidence_id == expected_evidence_id)
    else:
        # expected None: model should not cite a source
        evidence_correct = (evidence_id is None)

    # Determine pass/fail
    if answer_correct and evidence_correct:
        status = "VALID_PASS"
        reason = ""
    else:
        status = "VALID_FAIL"
        reason = "answer_mismatch" if not answer_correct else "evidence_mismatch"

    return TrialScore(
        trial_id=trial_id,
        status=status,
        reason=reason,
        parsed_answer=answer,
        parsed_evidence_id=evidence_id,
        parsed_confidence=confidence if confidence_valid else None,
        expected_answer=expected_answer,
        expected_evidence_id=expected_evidence_id,
        answer_correct=answer_correct,
        evidence_correct=evidence_correct,
        confidence_valid=confidence_valid,
    )


def score_run(results: list[dict], suite: list[dict]) -> list[TrialScore]:
    """Score a complete qualification run.

    Args:
        results: List of trial result dicts with keys: id, raw_response, done_reason, is_truncated
        suite: List of suite items with keys: id, answer, evidence_id

    Returns:
        List of TrialScore objects.
    """
    suite_map = {item["id"]: item for item in suite}
    scores = []
    for result in results:
        item = suite_map.get(result["id"])
        if item is None:
            scores.append(TrialScore(
                trial_id=result["id"],
                status="INVALID_TRIAL",
                reason="unknown_trial_id",
            ))
            continue
        score = validate_trial(
            trial_id=result["id"],
            raw_response=result.get("raw_response", ""),
            done_reason=result.get("done_reason"),
            expected_answer=item["answer"],
            expected_evidence_id=item.get("evidence_id"),
            is_truncated=result.get("is_truncated", False),
        )
        scores.append(score)
    return scores


def compute_qualification_metrics(scores: list[TrialScore]) -> dict:
    """Compute qualification metrics from a list of TrialScore objects."""
    total = len(scores)
    invalid = [s for s in scores if s.status == "INVALID_TRIAL"]
    valid_pass = [s for s in scores if s.status == "VALID_PASS"]
    valid_fail = [s for s in scores if s.status == "VALID_FAIL"]

    truncation_count = sum(1 for s in invalid if s.reason == "truncated")
    json_fail_count = sum(1 for s in invalid if s.reason in ("unparseable_json", "not_a_dict", "missing_field_answer", "missing_field_evidence_id", "missing_field_confidence"))
    evidence_invention_count = 0  # would need expected to check; placeholder

    return {
        "total_trials": total,
        "valid_pass": len(valid_pass),
        "valid_fail": len(valid_fail),
        "invalid_trials": len(invalid),
        "truncation_count": truncation_count,
        "json_fail_count": json_fail_count,
        "truncation_rate": truncation_count / total if total > 0 else 0.0,
        "valid_json_rate": (len(valid_pass) + len(valid_fail)) / total if total > 0 else 0.0,
        "pass_rate": len(valid_pass) / total if total > 0 else 0.0,
    }
