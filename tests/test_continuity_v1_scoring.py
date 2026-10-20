"""Tests for continuity_v1 scoring."""

from __future__ import annotations

import json
from pathlib import Path

sys_path = Path(__file__).resolve().parent.parent
import sys
sys.path.insert(0, str(sys_path))

from experiments.continuity_v1.score_continuity_v1 import score_response


class TestScoring:
    def _make_ak(self, decision="approve", commitment_id="C-1", codes=None, sources=None):
        return {"answer_key": {
            "decision": decision,
            "commitment_id": commitment_id,
            "rationale_codes": codes or ["verify_before_trust"],
            "source_episode_ids": sources or ["ep_target_001"],
            "memory_conflict_detected": False,
            "confidence": 0.9,
        }}

    def test_perfect_score(self):
        resp = {
            "decision": "approve",
            "commitment_id": "C-1",
            "rationale_codes": ["verify_before_trust"],
            "source_episode_ids": ["ep_target_001"],
        }
        assert score_response(resp, self._make_ak()) == 5

    def test_wrong_decision(self):
        resp = {
            "decision": "reject",
            "commitment_id": "C-1",
            "rationale_codes": ["verify_before_trust"],
            "source_episode_ids": ["ep_target_001"],
        }
        assert score_response(resp, self._make_ak()) == 4

    def test_missing_rationale_code(self):
        resp = {
            "decision": "approve",
            "commitment_id": "C-1",
            "rationale_codes": [],
            "source_episode_ids": ["ep_target_001"],
        }
        assert score_response(resp, self._make_ak()) <= 4

    def test_invalid_response_zero(self):
        assert score_response(None, self._make_ak()) == 0
        assert score_response("bad", self._make_ak()) == 0
        assert score_response({}, self._make_ak()) <= 1
