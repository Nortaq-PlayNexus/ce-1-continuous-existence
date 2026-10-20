"""Analysis logic for the model qualification suite.

Produces a model verdict: QUALIFIED, NOT_QUALIFIED, or INVALID_RUN.
No model calls are made.
"""

from __future__ import annotations

from .scoring import compute_qualification_metrics

# Qualification thresholds (from the instruction file)
QUALIFICATION_THRESHOLDS = {
    "truncation_rate": 0.0,       # 0/24 truncations
    "valid_json_rate": 23 / 24,   # at least 23/24 valid JSON/schema
    "evidence_extraction_rate": 21 / 24,  # at least 21/24 correct extraction
    "source_id_invention_max": 1 / 24,    # no more than 1/24 invented
    "normal_completion_rate": 23 / 24,    # at least 23/24 normal-stop
    "parseable_rate": 23 / 24,            # at least 23/24 parseable
}

MIN_TRIALS = 24


def analyze_qualification(scores: list, metrics: dict) -> dict:
    """Analyze qualification results and produce a model verdict.

    Returns a dict with:
        - verdict: QUALIFIED, NOT_QUALIFIED, or INVALID_RUN
        - reasons: list of reasons for the verdict
        - metrics: the computed metrics
        - threshold_checks: dict of threshold name -> (passed, actual, required)
    """
    reasons = []
    threshold_checks = {}

    total = metrics.get("total_trials", 0)

    # Check minimum trial count
    if total < MIN_TRIALS:
        return {
            "verdict": "INVALID_RUN",
            "reasons": ["insufficient trials: %d < %d" % (total, MIN_TRIALS)],
            "metrics": metrics,
            "threshold_checks": {},
        }

    # Check truncation rate
    trunc_rate = metrics.get("truncation_rate", 1.0)
    trunc_ok = trunc_rate <= QUALIFICATION_THRESHOLDS["truncation_rate"]
    threshold_checks["truncation_rate"] = {
        "passed": trunc_ok,
        "actual": trunc_rate,
        "required": QUALIFICATION_THRESHOLDS["truncation_rate"],
    }
    if not trunc_ok:
        reasons.append("truncation rate %.3f exceeds threshold %.3f" % (trunc_rate, QUALIFICATION_THRESHOLDS["truncation_rate"]))

    # Check valid JSON rate
    json_rate = metrics.get("valid_json_rate", 0.0)
    json_ok = json_rate >= QUALIFICATION_THRESHOLDS["valid_json_rate"]
    threshold_checks["valid_json_rate"] = {
        "passed": json_ok,
        "actual": json_rate,
        "required": QUALIFICATION_THRESHOLDS["valid_json_rate"],
    }
    if not json_ok:
        reasons.append("valid JSON rate %.3f below threshold %.3f" % (json_rate, QUALIFICATION_THRESHOLDS["valid_json_rate"]))

    # Check pass rate (evidence extraction)
    pass_rate = metrics.get("pass_rate", 0.0)
    pass_ok = pass_rate >= QUALIFICATION_THRESHOLDS["evidence_extraction_rate"]
    threshold_checks["evidence_extraction_rate"] = {
        "passed": pass_ok,
        "actual": pass_rate,
        "required": QUALIFICATION_THRESHOLDS["evidence_extraction_rate"],
    }
    if not pass_ok:
        reasons.append("pass rate %.3f below threshold %.3f" % (pass_rate, QUALIFICATION_THRESHOLDS["evidence_extraction_rate"]))

    # Check parseable rate
    parseable = (metrics.get("valid_pass", 0) + metrics.get("valid_fail", 0)) / total if total > 0 else 0.0
    parseable_ok = parseable >= QUALIFICATION_THRESHOLDS["parseable_rate"]
    threshold_checks["parseable_rate"] = {
        "passed": parseable_ok,
        "actual": parseable,
        "required": QUALIFICATION_THRESHOLDS["parseable_rate"],
    }
    if not parseable_ok:
        reasons.append("parseable rate %.3f below threshold %.3f" % (parseable, QUALIFICATION_THRESHOLDS["parseable_rate"]))

    # Determine verdict
    if trunc_rate > 0:
        verdict = "NOT_QUALIFIED"
        if "truncation rate" not in " ".join(reasons):
            reasons.append("any truncation disqualifies the model")
    elif all(v["passed"] for v in threshold_checks.values()):
        verdict = "QUALIFIED"
    else:
        verdict = "NOT_QUALIFIED"

    # Check for INVALID_RUN (too many invalid trials)
    invalid_rate = metrics.get("invalid_trials", 0) / total if total > 0 else 0.0
    if invalid_rate > 0.25:  # more than 25% invalid
        verdict = "INVALID_RUN"
        reasons.append("too many invalid trials: %d/%d" % (metrics.get("invalid_trials", 0), total))

    return {
        "verdict": verdict,
        "reasons": reasons,
        "metrics": metrics,
        "threshold_checks": threshold_checks,
    }
