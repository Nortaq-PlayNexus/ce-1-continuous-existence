"""Tests for the continuity_v2 scoring instrument."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from experiments.continuity_v2.score_continuity_v2 import score_response  # noqa: E402

AK = {"answer_key": {
    "decision": "delay",
    "commitment_id": "C-1",
    "rationale_codes": ["verify_before_trust", "self_report_not_evidence"],
    "source_episode_ids": ["ep_target_001"],
    "memory_conflict_detected": False,
    "confidence": 0.9,
    "content_key_tokens": ["verify", "integrity", "self-reported", "evidence"],
    "content_answer": "self-reported success is not evidence.",
}}


def _resp(**kw):
    base = {
        "decision": "delay",
        "commitment_id": "C-1",
        "rationale_codes": ["verify_before_trust", "self_report_not_evidence"],
        "source_episode_ids": ["ep_target_001"],
        "memory_conflict_detected": False,
        "confidence": 0.9,
        "content_answer": "verify file integrity; self-reported success is not evidence",
    }
    base.update(kw)
    return base


class TestV2Scoring:
    def test_perfect_score(self):
        assert score_response(_resp(), AK, "correct_retrieval") == 6

    def test_content_use_passes_with_key_token(self):
        r = _resp(content_answer="the system must verify file integrity")
        assert score_response(r, AK, "correct_retrieval") == 6

    def test_content_use_fails_without_key_token(self):
        r = _resp(content_answer="log all operations for audit purposes")
        assert score_response(r, AK, "correct_retrieval") == 5

    def test_controlled_vocabulary_now_reachable(self):
        r = _resp(decision="delay", rationale_codes=["verify_before_trust", "self_report_not_evidence"])
        assert score_response(r, AK, "correct_retrieval") >= 3

    def test_abstention_in_no_memory(self):
        r = {"decision": "unknown", "commitment_id": None,
             "rationale_codes": [], "source_episode_ids": [],
             "memory_conflict_detected": False, "confidence": 0.1,
             "content_answer": None}
        assert score_response(r, AK, "no_memory") == 1

    def test_abstention_fails_if_model_answers(self):
        r = _resp(decision="delay")
        assert score_response(r, AK, "no_memory") == 6

    def test_decoy_contamination_penalised(self):
        r = _resp(source_episode_ids=["ep_target_001", "ep_decoy_001"])
        assert score_response(r, AK, "correct_retrieval") == 4

    def test_invalid_response_zero(self):
        assert score_response(None, AK, "correct_retrieval") == 0
        assert score_response("bad", AK, "correct_retrieval") == 0
