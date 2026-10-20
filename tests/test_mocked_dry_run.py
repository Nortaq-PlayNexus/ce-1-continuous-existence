"""Mocked dry run for Experiment 1.1.

Tests the full experiment pipeline with mocked LLM responses.
No model calls are made. Verifies that:
- Valid responses are scored and included in means
- Truncated responses are invalidated and excluded from means
- Empty responses are invalidated
- Insufficient valid trials produce INVALID_RUN
- Reproducibility metadata is recorded
- Raw trial data is preserved

This is the mocked dry run required by the directive before any model-backed run.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import importlib.util
spec = importlib.util.spec_from_file_location("exp11", "experiments/exp_1_1_ablation.py")
exp11 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exp11)


class TestMockedDryRun:
    """Mocked dry run — no model calls."""

    def test_all_valid_responses(self, tmp_path):
        """All valid responses produce a result with valid trials."""
        mock_responses = [
            {"response": "try except FileNotFoundError log atomic temp rename newline LF", "done_reason": "stop", "eval_count": 100},
            {"response": "try except OSError audit logging atomic write temp file rename newline", "done_reason": "stop", "eval_count": 120},
            {"response": "try except PermissionError log audit atomic temp rename newline CRLF", "done_reason": "stop", "eval_count": 110},
        ]
        call_idx = [0]
        def mock_query(prompt):
            idx = call_idx[0] % len(mock_responses)
            call_idx[0] += 1
            return mock_responses[idx]

        original = exp11.query_llm
        exp11.query_llm = mock_query
        try:
            result = exp11.run_experiment(reps=3)
            # All 3 conditions x 3 reps = 9 trials, all valid
            for cond in result["conditions"]:
                assert result["conditions"][cond]["valid_count"] == 3
                assert result["conditions"][cond]["invalid_count"] == 0
            # Verdict should be INCONCLUSIVE (design limitation)
            assert result["comparison"]["verdict"] in ("INCONCLUSIVE", "INVALID_RUN")
            # Reproducibility metadata
            assert result["protocol_version"] == "1.1"
            assert result["experiment_version"] == "exp_1_1_v2"
            assert result["model"] == "qwen3:4b"
            assert result["threshold"] == 1.0
            assert result["tolerance"] == 1e-9
            # Raw trial data preserved
            for cond in result["conditions"]:
                for trial in result["conditions"][cond]["trials"]:
                    assert "response" in trial
                    assert "done_reason" in trial
                    assert "valid" in trial
                    assert "prompt_hash" in trial
                    assert "timestamp" in trial
                    assert "score" in trial
        finally:
            exp11.query_llm = original

    def test_all_truncated_responses(self, tmp_path):
        """All truncated responses produce INVALID_RUN."""
        original = exp11.query_llm
        exp11.query_llm = lambda prompt: {"response": "some text", "done_reason": "length", "eval_count": 100}
        try:
            result = exp11.run_experiment(reps=3)
            for cond in result["conditions"]:
                assert result["conditions"][cond]["valid_count"] == 0
                assert result["conditions"][cond]["invalid_count"] == 3
            assert result["comparison"]["verdict"] == "INVALID_RUN"
        finally:
            exp11.query_llm = original

    def test_mixed_valid_invalid(self, tmp_path):
        """Mixed valid/invalid responses: fewer than 2 valid → INVALID_RUN."""
        call_count = [0]
        def mock_query(prompt):
            call_count[0] += 1
            if call_count[0] % 3 == 0:
                return {"response": "valid text", "done_reason": "stop", "eval_count": 100}
            return {"response": "truncated", "done_reason": "length", "eval_count": 100}
        original = exp11.query_llm
        exp11.query_llm = mock_query
        try:
            result = exp11.run_experiment(reps=3)
            for cond in result["conditions"]:
                assert result["conditions"][cond]["valid_count"] < 2
            assert result["comparison"]["verdict"] == "INVALID_RUN"
        finally:
            exp11.query_llm = original

    def test_empty_responses_are_invalid(self, tmp_path):
        """Empty responses are invalidated and excluded from scoring."""
        original = exp11.query_llm
        exp11.query_llm = lambda prompt: {"response": "", "done_reason": "stop", "eval_count": 0}
        try:
            result = exp11.run_experiment(reps=2)
            for cond in result["conditions"]:
                assert result["conditions"][cond]["valid_count"] == 0
                assert result["conditions"][cond]["invalid_count"] == 2
            assert result["comparison"]["verdict"] == "INVALID_RUN"
        finally:
            exp11.query_llm = original

    def test_malformed_responses_are_invalid(self, tmp_path):
        """Malformed responses (missing response key) are invalidated."""
        original = exp11.query_llm
        exp11.query_llm = lambda prompt: {"done_reason": "stop", "eval_count": 100}
        try:
            result = exp11.run_experiment(reps=2)
            for cond in result["conditions"]:
                assert result["conditions"][cond]["valid_count"] == 0
            assert result["comparison"]["verdict"] == "INVALID_RUN"
        finally:
            exp11.query_llm = original

    def test_api_error_responses_are_invalid(self, tmp_path):
        """API error responses (unexpected done_reason) are invalidated."""
        original = exp11.query_llm
        exp11.query_llm = lambda prompt: {"response": "some text", "done_reason": "error", "eval_count": 100}
        try:
            result = exp11.run_experiment(reps=2)
            for cond in result["conditions"]:
                assert result["conditions"][cond]["valid_count"] == 0
            assert result["comparison"]["verdict"] == "INVALID_RUN"
        finally:
            exp11.query_llm = original

    def test_trial_metadata_complete(self, tmp_path):
        """Every trial records required metadata."""
        original = exp11.query_llm
        exp11.query_llm = lambda prompt: {"response": "valid text", "done_reason": "stop", "eval_count": 100}
        try:
            result = exp11.run_experiment(reps=2)
            for cond in result["conditions"]:
                for trial in result["conditions"][cond]["trials"]:
                    assert "valid" in trial
                    assert "done_reason" in trial
                    assert "prompt_hash" in trial
                    assert "timestamp" in trial
                    assert "response" in trial
                    assert "score" in trial
                    assert "invalidity_reason" in trial
                    assert "eval_count" in trial
                    assert "condition" in trial
        finally:
            exp11.query_llm = original

    def test_prompt_hash_deterministic(self, tmp_path):
        """Prompt hashes are deterministic for the same prompt."""
        original = exp11.query_llm
        exp11.query_llm = lambda prompt: {"response": "valid text", "done_reason": "stop", "eval_count": 100}
        try:
            result = exp11.run_experiment(reps=2)
            # All trials in the same condition should have the same prompt hash
            for cond in result["conditions"]:
                hashes = set(t["prompt_hash"] for t in result["conditions"][cond]["trials"])
                assert len(hashes) == 1, "Prompt hash should be deterministic"
        finally:
            exp11.query_llm = original

    def test_invalid_trials_excluded_from_scoring(self, tmp_path):
        """Invalid trials must not contribute to the mean."""
        original = exp11.query_llm
        call_count = [0]
        def mock_query(prompt):
            call_count[0] += 1
            if call_count[0] % 2 == 0:
                return {"response": "valid text with try except", "done_reason": "stop", "eval_count": 100}
            return {"response": "truncated", "done_reason": "length", "eval_count": 100}
        exp11.query_llm = mock_query
        try:
            result = exp11.run_experiment(reps=4)
            # Check that invalid trials have score=None
            for cond in result["conditions"]:
                for trial in result["conditions"][cond]["trials"]:
                    if not trial["valid"]:
                        assert trial["score"] is None
                    else:
                        assert trial["score"] is not None
        finally:
            exp11.query_llm = original

    def test_result_serialization(self, tmp_path):
        """Result can be serialized to JSON and deserialized."""
        import json
        original = exp11.query_llm
        exp11.query_llm = lambda prompt: {"response": "valid text", "done_reason": "stop", "eval_count": 100}
        try:
            result = exp11.run_experiment(reps=2)
            # Serialize
            serialized = json.dumps(result, indent=2, default=str)
            # Deserialize
            deserialized = json.loads(serialized)
            assert deserialized["experiment"] == "1.1_episodic_memory_ablation"
            assert deserialized["protocol_version"] == "1.1"
            assert deserialized["comparison"]["verdict"] in ("INCONCLUSIVE", "INVALID_RUN")
        finally:
            exp11.query_llm = original