"""Tests for the continuity_v1 analysis instrument.

Covers the validity gate, the as-run and corrected scorers, the preregistered
statistics, and the decision rule.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from ce1.continuity.analysis import (  # noqa: E402
    bootstrap_ci,
    decide_verdict,
    min_required_pairs,
    paired_differences,
    paired_permutation_test,
)
from ce1.continuity.scoring import (  # noqa: E402
    classify_validity,
    normalize_episode_id,
    score_as_run,
    score_corrected,
)

RESULTS = ROOT / "experiments" / "continuity_v1" / "results"
COMMITTED_RESULTS = RESULTS / "confirmatory_results.jsonl"
COMMITTED_SCORES = RESULTS / "confirmatory_scores.jsonl"

AK = {"answer_key": {
    "decision": "delay",
    "commitment_id": "C-1",
    "rationale_codes": ["verify_before_trust", "self_report_not_evidence"],
    "source_episode_ids": ["ep_target_001"],
    "memory_conflict_detected": False,
    "confidence": 0.9,
}}


def load_jsonl(path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


class TestEpisodeIdNormalisation:
    def test_strips_brackets_and_whitespace(self):
        assert normalize_episode_id("[ep_target_001]") == "ep_target_001"
        assert normalize_episode_id("  ep_target_001 ") == "ep_target_001"
        assert normalize_episode_id("EP_Target_001") == "ep_target_001"

    def test_handles_none_and_empty(self):
        assert normalize_episode_id(None) == ""
        assert normalize_episode_id("") == ""


class TestScorers:
    def test_as_run_ignores_brackets(self):
        resp = {"decision": "delay", "commitment_id": "C-1",
                "rationale_codes": ["verify_before_trust", "self_report_not_evidence"],
                "source_episode_ids": ["[ep_target_001]"]}
        # raw comparison fails, so the source points are not awarded
        assert score_as_run(resp, AK) == 3
        # normalised comparison awards them
        assert score_corrected(resp, AK, "ep_decoy_001") == 5

    def test_corrected_rejects_decoy_citation(self):
        resp = {"decision": "delay", "commitment_id": "C-1",
                "rationale_codes": ["verify_before_trust", "self_report_not_evidence"],
                "source_episode_ids": ["ep_target_001", "ep_decoy_001"]}
        # point 4 (exact set) fails, point 5 (decoy contamination) fails
        assert score_corrected(resp, AK, "ep_decoy_001") == 3

    def test_corrected_awards_point5_when_target_cited_with_extras(self):
        resp = {"decision": "delay", "commitment_id": "C-1",
                "rationale_codes": ["verify_before_trust", "self_report_not_evidence"],
                "source_episode_ids": ["ep_target_001", "ep_dist_001_a"]}
        # point 4 fails (not the exact set), point 5 passes (no decoy)
        assert score_corrected(resp, AK, "ep_decoy_001") == 4

    def test_as_run_point5_is_a_duplicate_of_point4(self):
        """The as-run point 5 fires whenever point 4's set condition holds."""
        resp = {"decision": "x", "commitment_id": "y", "rationale_codes": [],
                "source_episode_ids": ["ep_target_001"]}
        assert score_as_run(resp, AK) == 2  # p4 + p5, neither p1/p2/p3

    def test_corrected_ignores_case_and_whitespace(self):
        resp = {"decision": " Delay ", "commitment_id": "c-1",
                "rationale_codes": ["verify_before_trust", "self_report_not_evidence"],
                "source_episode_ids": ["ep_target_001"]}
        assert score_corrected(resp, AK, "ep_decoy_001") == 5
        assert score_as_run(resp, AK) == 3  # raw comparison rejects " Delay " and "c-1"


class TestValidityGate:
    def _record(self, **kw):
        base = {"raw_response": '{"decision": "delay", "commitment_id": "C-1", '
                               '"rationale_codes": [], "source_episode_ids": []}',
                "done_reason": "stop", "is_truncated": False}
        base.update(kw)
        return base

    def test_valid_response(self):
        assert classify_validity(self._record()) == (True, "")

    def test_truncated(self):
        ok, reason = classify_validity(self._record(done_reason="length"))
        assert not ok and reason == "truncated_length"

    def test_unparseable(self):
        ok, reason = classify_validity(self._record(raw_response="not json"))
        assert not ok and reason == "unparseable_json"

    def test_empty_response(self):
        ok, reason = classify_validity(self._record(raw_response=""))
        assert not ok and reason == "empty_response"

    def test_missing_field(self):
        ok, reason = classify_validity(self._record(raw_response='{"decision": "delay"}'))
        assert not ok and reason.startswith("missing_field_")


class TestStatistics:
    def test_permutation_is_deterministic(self):
        diffs = [0.8] * 30 + [0.2] * 30
        a = paired_permutation_test(diffs, n_resamples=1000, seed=7)
        b = paired_permutation_test(diffs, n_resamples=1000, seed=7)
        assert a == b

    def test_permutation_detects_a_separated_effect(self):
        diffs = [1.0] * 40
        out = paired_permutation_test(diffs, n_resamples=1000, seed=7)
        assert out["p_value"] <= 0.01
        assert out["n_pairs"] == 40

    def test_permutation_on_zero_effect(self):
        out = paired_permutation_test([0.0] * 20, n_resamples=1000, seed=7)
        assert out["p_value"] == 1.0

    def test_bootstrap_is_deterministic_and_brackets_the_estimate(self):
        values = [0.2, 0.4, 0.6, 0.8, 1.0, 0.3, 0.9]
        a = bootstrap_ci(values, n_resamples=1000, seed=7)
        b = bootstrap_ci(values, n_resamples=1000, seed=7)
        assert a == b
        assert a["lower"] <= a["point_estimate"] <= a["upper"]

    def test_paired_differences_need_both_conditions(self):
        scores = [
            {"scenario_id": "A", "condition": "correct_retrieval", "score": 3},
            {"scenario_id": "A", "condition": "matched_decoy", "score": 1},
            {"scenario_id": "B", "condition": "correct_retrieval", "score": 2},
            {"scenario_id": "C", "condition": "no_memory", "score": 0},
        ]
        diffs = paired_differences(scores, "correct_retrieval", "matched_decoy")
        assert diffs == {"A": 2.0}


class TestDecisionRule:
    def test_supported(self):
        verdict, failures = decide_verdict(0.82, 0.0001, 0.67, 0.0, 72, 65, 0.50)
        assert verdict == "SUPPORTED" and failures == []

    def test_invalid_run_on_invalid_rate(self):
        verdict, failures = decide_verdict(0.82, 0.0001, 0.67, 0.2, 72, 65, 0.50)
        assert verdict == "INVALID_RUN" and failures

    def test_invalid_run_on_insufficient_pairs(self):
        verdict, failures = decide_verdict(0.82, 0.0001, 0.67, 0.0, 10, 65, 0.50)
        assert verdict == "INVALID_RUN" and failures

    def test_inconclusive_when_effect_met_but_inference_fails(self):
        verdict, _ = decide_verdict(0.82, 0.4, 0.1, 0.0, 72, 65, 0.50)
        assert verdict == "INCONCLUSIVE"

    def test_not_supported_below_threshold(self):
        verdict, _ = decide_verdict(0.2, 0.0001, 0.1, 0.0, 72, 65, 0.50)
        assert verdict == "NOT_SUPPORTED"

    def test_min_required_pairs(self):
        assert min_required_pairs(72) == 65
        assert min_required_pairs(10) == 9


class TestCommittedRunReproduces:
    """The as-run instrument must still reproduce the committed scores."""

    def test_as_run_scorer_reproduces_committed_scores(self):
        committed = load_jsonl(COMMITTED_SCORES)
        results = load_jsonl(COMMITTED_RESULTS)
        keys = {a["scenario_id"]: a for a in load_jsonl(
            ROOT / "benchmarks" / "continuity_v1" / "answer_keys.jsonl")}
        from ce1.qualification.scoring import parse_response
        recomputed = []
        for r in results:
            p = parse_response(r.get("raw_response") or "")
            ak = keys[r["scenario_id"]]
            recomputed.append((r["scenario_id"], r["condition"],
                               score_as_run(p, ak) if p else 0))
        original = [(s["scenario_id"], s["condition"], s["score"]) for s in committed]
        assert recomputed == original

    def test_committed_run_has_no_invalid_trials(self):
        results = load_jsonl(COMMITTED_RESULTS)
        for r in results:
            ok, _ = classify_validity(r)
            assert ok, "committed run contains an invalid trial: %s" % r["scenario_id"]
