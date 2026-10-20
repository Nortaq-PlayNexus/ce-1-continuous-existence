"""Tests for the continuity_v1 generator."""

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


class TestGenerator:
    def test_scenario_count(self):
        scenarios = _load_jsonl("scenarios.jsonl")
        assert len(scenarios) == 72

    def test_answer_key_count(self):
        keys = _load_jsonl("answer_keys.jsonl")
        assert len(keys) == 72

    def test_retrieval_set_count(self):
        sets = _load_jsonl("retrieval_sets.jsonl")
        assert len(sets) == 72

    def test_categories(self):
        scenarios = _load_jsonl("scenarios.jsonl")
        cats = {}
        for s in scenarios:
            cats[s["category"]] = cats.get(s["category"], 0) + 1
        assert cats.get("commitment_preservation") == 18
        assert cats.get("rationale_reconstruction") == 18
        assert cats.get("constraint_persistence") == 12
        assert cats.get("justified_revision") == 12
        assert cats.get("source_attribution") == 12

    def test_each_scenario_has_target_and_decoy(self):
        scenarios = _load_jsonl("scenarios.jsonl")
        for s in scenarios:
            assert "target_episode_id" in s
            assert "decoy_episode_id" in s
            assert s["target_episode_id"] != s["decoy_episode_id"]

    def test_each_scenario_has_3_to_5_episodes(self):
        scenarios = _load_jsonl("scenarios.jsonl")
        for s in scenarios:
            assert 3 <= len(s["episodes"]) <= 5, "%s has %d episodes" % (s["scenario_id"], len(s["episodes"]))

    def test_each_scenario_has_task(self):
        scenarios = _load_jsonl("scenarios.jsonl")
        for s in scenarios:
            assert "task" in s
            assert len(s["task"]) > 0

    def test_answer_keys_match_scenarios(self):
        scenarios = _load_jsonl("scenarios.jsonl")
        keys = _load_jsonl("answer_keys.jsonl")
        scenario_ids = {s["scenario_id"] for s in scenarios}
        key_ids = {k["scenario_id"] for k in keys}
        assert scenario_ids == key_ids

    def test_retrieval_sets_have_3_conditions(self):
        sets = _load_jsonl("retrieval_sets.jsonl")
        for rs in sets:
            assert "correct_retrieval" in rs["conditions"]
            assert "matched_decoy" in rs["conditions"]
            assert "no_memory" in rs["conditions"]

    def test_manifest_exists(self):
        manifest = json.loads((BENCH_DIR / "manifest.json").read_text(encoding="utf-8"))
        assert manifest["scenario_count"] == 72
        assert manifest["total_trials"] == 216

    def test_no_answer_key_in_scenarios(self):
        scenarios = _load_jsonl("scenarios.jsonl")
        for s in scenarios:
            assert "answer_key" not in s
