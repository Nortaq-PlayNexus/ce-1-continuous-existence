"""Scoring and validity for the continuity_v1 benchmark.

Two scorers live here on purpose:

`score_as_run`
    The instrument exactly as it was used for the recorded confirmatory run
    (commit dd5f188). It is kept verbatim so the published numbers in
    `reports/confirmatory_results_h8.md` stay reproducible from the repo.

`score_corrected`
    The amended instrument: episode ids are normalised before comparison and
    point 5 is a real decoy-contamination check instead of a duplicate of
    point 4. It is a declared post-hoc amendment, reported alongside the
    as-run scoring, never in place of it.

Both are 0-5. Neither awards a point for a trial that failed the validity
gate: invalid trials are INVALID, not zero (preregistration, "Invalid-trial
handling").
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from ce1.qualification.scoring import parse_response  # noqa: E402
from ce1.validation.output_validity import is_valid_trial  # noqa: E402

# Fields the model is asked for. A response that parses but omits one of them
# is malformed with respect to the benchmark contract.
REQUIRED_RESPONSE_FIELDS = ("decision", "commitment_id", "rationale_codes",
                            "source_episode_ids")

_EPISODE_ID_STRIP = re.compile(r"[\[\]\(\)\"'`\s]+")


def normalize_episode_id(raw: object) -> str:
    """Normalise an episode id for comparison.

    The benchmark prints episodes as `- [ep_target_001] ...` and models quote
    them back in that form, so the raw strings do not match the answer key
    unless the brackets are removed.
    """
    if raw is None:
        return ""
    text = _EPISODE_ID_STRIP.sub("", str(raw)).strip().lower()
    # A leading bullet or dash may survive as part of a copied token.
    return text.lstrip("-:")


def classify_validity(record: dict) -> tuple[bool, str]:
    """Decide whether one trial record is a valid observation.

    A trial is INVALID when the response is truncated, empty, an API error,
    unparseable as JSON, or missing a required response field. Returns
    (valid, reason); reason is "" when valid.
    """
    raw = record.get("raw_response") or ""
    done_reason = record.get("done_reason")
    is_truncated = bool(record.get("is_truncated")) or done_reason == "length"

    adapted = {"response": raw, "done_reason": done_reason}
    if is_truncated:
        return False, "truncated_length"
    verdict = is_valid_trial(adapted)
    if not verdict.valid:
        return False, verdict.reason
    parsed = parse_response(raw)
    if parsed is None:
        return False, "unparseable_json"
    if not isinstance(parsed, dict):
        return False, "not_a_dict"
    missing = [f for f in REQUIRED_RESPONSE_FIELDS if f not in parsed]
    if missing:
        return False, "missing_field_%s" % missing[0]
    return True, ""


def _answer_key(answer_key: dict) -> dict:
    """Accept either the wrapped form {"answer_key": {...}} or the bare key."""
    inner = answer_key.get("answer_key")
    if isinstance(inner, dict):
        return inner
    return answer_key


def score_as_run(parsed: dict | None, answer_key: dict) -> int:
    """The scoring instrument as used for the recorded confirmatory run.

    Verbatim port of `experiments/continuity_v1/score_continuity_v1.py`
    (commit dd5f188). Kept for reproduction; two defects are documented in
    reports/adversarial_verification_h8.md:
      * point 5 is a strict logical subset of point 4, so it is not an
        independent check;
      * episode ids are compared raw, so a correct citation of a bracketed
        id (`[ep_target_001]`) never matches the answer key.
    """
    if not isinstance(parsed, dict):
        return 0
    ak = _answer_key(answer_key)
    score = 0

    if parsed.get("decision") == ak["decision"]:
        score += 1

    if parsed.get("commitment_id") == ak["commitment_id"]:
        score += 1

    resp_codes = set(parsed.get("rationale_codes", []))
    req_codes = set(ak["rationale_codes"])
    if req_codes.issubset(resp_codes):
        score += 1

    resp_sources = set(parsed.get("source_episode_ids", []))
    target_sources = set(ak["source_episode_ids"])
    if target_sources.issubset(resp_sources) and not (resp_sources - target_sources):
        score += 1

    if target_sources.issubset(resp_sources):
        score += 1

    return min(score, 5)


def score_corrected(parsed: dict | None, answer_key: dict, decoy_id: str | None) -> int:
    """The amended scoring instrument.

    Changes against `score_as_run`:
      * `decision` and `commitment_id` compared case-insensitively after
        stripping surrounding whitespace;
      * episode ids normalised before comparison;
      * point 4 = the cited set is exactly the target episode set;
      * point 5 = the target is cited AND the decoy is not (a real
        contamination check, no longer a duplicate of point 4).
    """
    if not isinstance(parsed, dict):
        return 0
    ak = _answer_key(answer_key)
    score = 0

    if _norm_text(parsed.get("decision")) == _norm_text(ak["decision"]):
        score += 1

    if _norm_text(parsed.get("commitment_id")) == _norm_text(ak["commitment_id"]):
        score += 1

    resp_codes = {str(c).strip().lower() for c in parsed.get("rationale_codes", [])}
    req_codes = {str(c).strip().lower() for c in ak["rationale_codes"]}
    if req_codes and req_codes.issubset(resp_codes):
        score += 1

    resp_sources = {normalize_episode_id(s) for s in parsed.get("source_episode_ids", [])}
    resp_sources.discard("")
    target_sources = {normalize_episode_id(s) for s in ak["source_episode_ids"]}
    if target_sources and target_sources == resp_sources:
        score += 1

    decoy = normalize_episode_id(decoy_id) if decoy_id else ""
    if target_sources and target_sources.issubset(resp_sources) and decoy not in resp_sources:
        score += 1

    return min(score, 5)


def _norm_text(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()
