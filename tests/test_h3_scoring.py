"""Tests for the H3 scoring instrument."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from experiments.h3_interruption.score_h3 import score_response  # noqa: E402

AK = {"answer_key": {
    "step1": {
        "decision": "delay",
        "commitment_id": "C-1",
        "rationale_codes": ["verify_before_trust", "self_report_not_evidence"],
        "source_episode_ids": ["ep_target_001"],
        "content_key_tokens": ["verify", "integrity"],
    },
    "step2": {
        "decision": "approve",
        "commitment_id": "C-1",
        "rationale_codes": ["verification_complete", "deploy_approved"],
        "source_episode_ids": ["ep_target_001"],
        "content_key_tokens": ["verify", "integrity"],
    },
}}


def _resp(**kw):
    base = {
        "decision": "approve",
        "commitment_id": "C-1",
        "rationale_codes": ["verification_complete", "deploy_approved"],
        "source_episode_ids": ["ep_target_001"],
        "memory_conflict_detected": False,
        "confidence": 0.9,
        "content_answer": "file integrity verified",
    }
    base.update(kw)
    return base


class TestH3Scoring:
    def test_perfect_score(self):
        assert score_response(_resp(), AK, "store_populated") == 5

    def test_wrong_decision(self):
        r = _resp(decision="delay")
        assert score_response(r, AK, "store_populated") == 4

    def test_abstention_in_store_empty(self):
        r = {"decision": "unknown", "commitment_id": None,
             "rationale_codes": [], "source_episode_ids": [],
             "memory_conflict_detected": False, "confidence": 0.1,
             "content_answer": None}
        assert score_response(r, AK, "store_empty") == 1

    def test_abstention_fails_if_model_answers(self):
        r = _resp(decision="approve")
        assert score_response(r, AK, "store_empty") == 5

    def test_invalid_response_zero(self):
        assert score_response(None, AK, "store_populated") == 0
        assert score_response("bad", AK, "store_populated") == 0

    def test_content_use_fails_without_key_token(self):
        r = _resp(content_answer="log all operations")
        assert score_response(r, AK, "store_populated") == 4
