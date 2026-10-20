"""Tests for continuity_v1 condition structure."""

from __future__ import annotations

import json
from pathlib import Path

BENCH_DIR = Path("benchmarks/continuity_v1")


def _load_jsonl(name):
    items = []
    with open(BENCH_DIR / name, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


class TestConditions:
    def test_retrieval_sets_structure(self):
        sets = _load_jsonl("retrieval_sets.jsonl")
        for rs in sets:
            for cond in ["correct_retrieval", "matched_decoy", "no_memory"]:
                assert cond in rs["conditions"]
                assert "episode_ids" in rs["conditions"][cond]
                assert "episodes" in rs["conditions"][cond]

    def test_correct_has_target(self):
        scenarios = _load_jsonl("scenarios.jsonl")
        sets = _load_jsonl("retrieval_sets.jsonl")
        set_map = {rs["scenario_id"]: rs for rs in sets}
        for s in scenarios:
            rs = set_map[s["scenario_id"]]
            correct_ids = rs["conditions"]["correct_retrieval"]["episode_ids"]
            assert s["target_episode_id"] in correct_ids

    def test_decoy_has_decoy(self):
        scenarios = _load_jsonl("scenarios.jsonl")
        sets = _load_jsonl("retrieval_sets.jsonl")
        set_map = {rs["scenario_id"]: rs for rs in sets}
        for s in scenarios:
            rs = set_map[s["scenario_id"]]
            decoy_ids = rs["conditions"]["matched_decoy"]["episode_ids"]
            assert s["decoy_episode_id"] in decoy_ids

    def test_no_memory_lacks_target(self):
        scenarios = _load_jsonl("scenarios.jsonl")
        sets = _load_jsonl("retrieval_sets.jsonl")
        set_map = {rs["scenario_id"]: rs for rs in sets}
        for s in scenarios:
            rs = set_map[s["scenario_id"]]
            no_mem_ids = rs["conditions"]["no_memory"]["episode_ids"]
            assert s["target_episode_id"] not in no_mem_ids

    def test_no_condition_label_in_prompts(self):
        # Verified at generation time; check scenarios don't contain labels
        scenarios = _load_jsonl("scenarios.jsonl")
        for s in scenarios:
            task = s["task"].lower()
            for label in ["correct_retrieval", "matched_decoy", "no_memory"]:
                assert label not in task
