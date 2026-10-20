#!/usr/bin/env python3
"""Run the continuity_v1 benchmark.

Dry-run by default. Use --live for actual model calls (requires authorization).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

BENCH_DIR = Path(__file__).resolve().parent.parent.parent / "benchmarks" / "continuity_v1"
SCENARIOS_PATH = BENCH_DIR / "scenarios.jsonl"
RETRIEVAL_PATH = BENCH_DIR / "retrieval_sets.jsonl"
ANSWER_KEYS_PATH = BENCH_DIR / "answer_keys.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    items = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def build_prompt(scenario: dict, condition: str, retrieval_set: dict) -> str:
    """Build a model prompt for a given scenario and condition."""
    episodes = retrieval_set["conditions"][condition]["episodes"]
    episode_block = ""
    if episodes:
        episode_block = "\n\nPRIOR EPISODES:\n" + "\n".join(
            "- [%s] %s" % (ep["episode_id"], ep["content"]) for ep in episodes
        )
    return (
        "You are evaluating a decision task.\n"
        "%s\n\n"
        "TASK: %s\n\n"
        "Respond with JSON only:\n"
        '{"decision": "...", "commitment_id": "...", "rationale_codes": [...], '
        '"source_episode_ids": [...], "memory_conflict_detected": true/false, "confidence": 0.0-1.0}'
    ) % (episode_block, scenario["task"])


def main():
    parser = argparse.ArgumentParser(description="Run continuity_v1 benchmark")
    parser.add_argument("--scenarios", default=str(SCENARIOS_PATH))
    parser.add_argument("--retrieval", default=str(RETRIEVAL_PATH))
    parser.add_argument("--output", default="continuity_v1_results.jsonl")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--model", default="gemma3:4b")
    args = parser.parse_args()

    scenarios = load_jsonl(Path(args.scenarios))
    retrieval_sets = {rs["scenario_id"]: rs for rs in load_jsonl(Path(args.retrieval))}

    print("Scenarios: %d" % len(scenarios))
    print("Mode: %s" % ("LIVE" if args.live else "DRY-RUN"))

    if args.live:
        print("ERROR: Live mode requires explicit human authorization. Exiting.")
        return 1

    run_id = "dry-run-%s" % __import__("time").strftime("%Y%m%d%H%M%S")
    records = []
    for s in scenarios:
        rs = retrieval_sets[s["scenario_id"]]
        for cond in ["correct_retrieval", "matched_decoy", "no_memory"]:
            prompt = build_prompt(s, cond, rs)
            record = {
                "scenario_id": s["scenario_id"],
                "category": s["category"],
                "condition": cond,
                "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16],
                "raw_response": "",
                "done_reason": None,
                "is_truncated": False,
                "run_id": run_id,
                "model": args.model,
                "timestamp": __import__("time").strftime("%Y-%m-%dT%H:%M:%SZ", __import__("time").gmtime()),
            }
            records.append(record)

    Path(args.output).write_text(
        "\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")
    print("Wrote %d trial records (dry run, no model calls)" % len(records))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
