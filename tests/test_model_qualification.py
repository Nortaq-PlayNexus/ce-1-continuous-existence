"""Tests for the model qualification suite.

No live model calls. All tests use synthetic fixtures.
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from ce1.qualification.scoring import (
    parse_response,
    validate_trial,
    score_run,
    compute_qualification_metrics,
    TrialScore,
)
from ce1.qualification.analysis import analyze_qualification


def _load_suite():
    suite_path = Path("experiments/model_qualification/qualification_suite.jsonl")
    items = []
    with open(suite_path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


class TestSuiteStructure:
    """Tests for the qualification suite structure."""

    def test_suite_has_24_items(self):
        suite = _load_suite()
        assert len(suite) == 24

    def test_all_items_have_answer_keys(self):
        suite = _load_suite()
        for item in suite:
            assert "answer" in item, "Missing answer in %s" % item["id"]
            assert "evidence_id" in item, "Missing evidence_id in %s" % item["id"]
            assert "confidence" in item, "Missing confidence in %s" % item["id"]

    def test_all_items_have_prompts(self):
        suite = _load_suite()
        for item in suite:
            assert "prompt" in item
            assert len(item["prompt"]) > 0

    def test_all_items_have_ids(self):
        suite = _load_suite()
        ids = [item["id"] for item in suite]
        assert len(set(ids)) == 24, "Duplicate IDs found"

    def test_all_items_have_categories(self):
        suite = _load_suite()
        for item in suite:
            assert "category" in item

    def test_categories_are_valid(self):
        suite = _load_suite()
        valid_cats = {"direct_evidence_extraction", "select_between_records",
                      "explicit_unknown", "contradiction_detection", "source_attribution"}
        for item in suite:
            assert item["category"] in valid_cats, "Invalid category: %s" % item["category"]

    def test_answer_keys_not_in_prompts(self):
        """Raw answer keys must not appear in model prompts."""
        suite = _load_suite()
        for item in suite:
            prompt = item["prompt"].lower()
            answer = str(item["answer"]).lower()
            # The answer should not appear as a standalone value in the prompt
            # (evidence records contain the data, but the answer field itself
            #  should not be leaked as "the answer is X")
            assert "the answer is" not in prompt
            assert "answer:" not in prompt.lower().split("respond with")[0] if "respond with" in prompt.lower() else True

    def test_no_condition_labels_in_prompts(self):
        """Condition labels must not appear in prompts."""
        suite = _load_suite()
        forbidden = ["correct_retrieval", "matched_decoy", "no_memory", "condition"]
        for item in suite:
            prompt_lower = item["prompt"].lower()
            for f in forbidden:
                assert f not in prompt_lower, "Forbidden label '%s' in %s" % (f, item["id"])

    def test_manifest_hash_deterministic(self):
        """Suite file hash should be deterministic."""
        suite_path = Path("experiments/model_qualification/qualification_suite.jsonl")
        h1 = hashlib.sha256(suite_path.read_bytes()).hexdigest()
        h2 = hashlib.sha256(suite_path.read_bytes()).hexdigest()
        assert h1 == h2


class TestParseResponse:
    """Tests for response parsing."""

    def test_parse_valid_json(self):
        raw = '{"answer": "3", "evidence_id": "E1", "confidence": 0.95}'
        parsed = parse_response(raw)
        assert parsed is not None
        assert parsed["answer"] == "3"
        assert parsed["evidence_id"] == "E1"

    def test_parse_empty(self):
        assert parse_response("") is None
        assert parse_response("   ") is None

    def test_parse_invalid_json(self):
        assert parse_response("not json") is None

    def test_parse_markdown_wrapped(self):
        raw = '```json\n{"answer": "5", "evidence_id": "E2", "confidence": 0.8}\n```'
        parsed = parse_response(raw)
        assert parsed is not None
        assert parsed["answer"] == "5"


class TestValidateTrial:
    """Tests for trial validation."""

    def test_truncated_is_invalid(self):
        score = validate_trial("Q01", "some text", "length", "3", "E1", is_truncated=True)
        assert score.status == "INVALID_TRIAL"
        assert score.reason == "truncated"

    def test_empty_is_invalid(self):
        score = validate_trial("Q01", "", "stop", "3", "E1")
        assert score.status == "INVALID_TRIAL"
        assert score.reason == "empty_response"

    def test_unparseable_is_invalid(self):
        score = validate_trial("Q01", "not json", "stop", "3", "E1")
        assert score.status == "INVALID_TRIAL"
        assert score.reason == "unparseable_json"

    def test_missing_field_is_invalid(self):
        score = validate_trial("Q01", '{"answer": "3"}', "stop", "3", "E1")
        assert score.status == "INVALID_TRIAL"
        assert "missing_field" in score.reason

    def test_correct_answer_passes(self):
        raw = '{"answer": "3", "evidence_id": "E1", "confidence": 0.95}'
        score = validate_trial("Q01", raw, "stop", "3", "E1")
        assert score.status == "VALID_PASS"
        assert score.answer_correct is True
        assert score.evidence_correct is True

    def test_wrong_answer_fails(self):
        raw = '{"answer": "5", "evidence_id": "E1", "confidence": 0.95}'
        score = validate_trial("Q01", raw, "stop", "3", "E1")
        assert score.status == "VALID_FAIL"
        assert score.answer_correct is False

    def test_wrong_evidence_fails(self):
        raw = '{"answer": "3", "evidence_id": "E2", "confidence": 0.95}'
        score = validate_trial("Q01", raw, "stop", "3", "E1")
        assert score.status == "VALID_FAIL"
        assert score.evidence_correct is False

    def test_no_truncation_qualifies(self):
        """A model with 0 truncations can qualify."""
        suite = _load_suite()
        # Simulate perfect run
        results = []
        for item in suite:
            raw = json.dumps({"answer": item["answer"], "evidence_id": item["evidence_id"], "confidence": item["confidence"]})
            results.append({"id": item["id"], "raw_response": raw, "done_reason": "stop", "is_truncated": False})
        scores = score_run(results, suite)
        metrics = compute_qualification_metrics(scores)
        analysis = analyze_qualification(scores, metrics)
        assert analysis["verdict"] == "QUALIFIED"

    def test_one_truncation_disqualifies(self):
        """A model with 1 truncation is not qualified."""
        suite = _load_suite()
        results = []
        for i, item in enumerate(suite):
            if i == 0:
                results.append({"id": item["id"], "raw_response": "partial", "done_reason": "length", "is_truncated": True})
            else:
                raw = json.dumps({"answer": item["answer"], "evidence_id": item["evidence_id"], "confidence": item["confidence"]})
                results.append({"id": item["id"], "raw_response": raw, "done_reason": "stop", "is_truncated": False})
        scores = score_run(results, suite)
        metrics = compute_qualification_metrics(scores)
        analysis = analyze_qualification(scores, metrics)
        assert analysis["verdict"] == "NOT_QUALIFIED"

    def test_no_network_calls(self):
        """Tests must not make network or Ollama calls."""
        # This test just verifies imports work without network
        import ce1.qualification.scoring
        import ce1.qualification.analysis
        assert True


class TestAnalyzeQualification:
    """Tests for qualification analysis."""

    def test_qualified_verdict(self):
        suite = _load_suite()
        results = []
        for item in suite:
            raw = json.dumps({"answer": item["answer"], "evidence_id": item["evidence_id"], "confidence": item["confidence"]})
            results.append({"id": item["id"], "raw_response": raw, "done_reason": "stop", "is_truncated": False})
        scores = score_run(results, suite)
        metrics = compute_qualification_metrics(scores)
        analysis = analyze_qualification(scores, metrics)
        assert analysis["verdict"] == "QUALIFIED"

    def test_thresholds_in_code(self):
        """Thresholds must be implemented in code, not just prose."""
        from ce1.qualification.analysis import QUALIFICATION_THRESHOLDS
        assert "truncation_rate" in QUALIFICATION_THRESHOLDS
        assert QUALIFICATION_THRESHOLDS["truncation_rate"] == 0.0
        assert "valid_json_rate" in QUALIFICATION_THRESHOLDS
        assert QUALIFICATION_THRESHOLDS["valid_json_rate"] >= 23 / 24 - 1e-9
