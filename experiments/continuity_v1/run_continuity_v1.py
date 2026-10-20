#!/usr/bin/env python3
"""Run the continuity_v1 benchmark.

Dry-run by default. Use --live for actual model calls (Ollama, local).

The live path reproduces the recorded confirmatory run exactly: scenarios are
shuffled with the benchmark seed (20261020), conditions are run in the order
correct_retrieval, matched_decoy, no_memory, and every trial is recorded with
its prompt hash, done_reason, truncation flag and elapsed time.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

BENCH_DIR = ROOT / "benchmarks" / "continuity_v1"
SCENARIOS_PATH = BENCH_DIR / "scenarios.jsonl"
RETRIEVAL_PATH = BENCH_DIR / "retrieval_sets.jsonl"
ANSWER_KEYS_PATH = BENCH_DIR / "answer_keys.jsonl"

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
CONDITIONS = ["correct_retrieval", "matched_decoy", "no_memory"]
SEED = 20261020


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


def call_ollama(prompt: str, model: str, temperature: float, num_predict: int,
                timeout: int = 300) -> tuple[str, str | None, bool]:
    """Call Ollama. Returns (raw_response, done_reason, is_truncated).

    The default timeout is generous because the first call for a model pays
    the load cost (a 3 GB model took 121 s to load on this box).
    """
    """Call Ollama. Returns (raw_response, done_reason, is_truncated)."""
    body = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "options": {"temperature": temperature, "num_predict": num_predict},
    }).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    raw = result.get("response", "")
    done_reason = result.get("done_reason")
    return raw, done_reason, done_reason == "length"


def main():
    parser = argparse.ArgumentParser(description="Run continuity_v1 benchmark")
    parser.add_argument("--scenarios", default=str(SCENARIOS_PATH))
    parser.add_argument("--retrieval", default=str(RETRIEVAL_PATH))
    parser.add_argument("--output", default="continuity_v1_results.jsonl")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--model", default="gemma3:4b")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--num-predict", type=int, default=300)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--limit", type=int, default=0,
                        help="stop after N scenarios (0 = all)")
    args = parser.parse_args()

    scenarios = load_jsonl(Path(args.scenarios))
    retrieval_sets = {rs["scenario_id"]: rs for rs in load_jsonl(Path(args.retrieval))}
    random.Random(args.seed).shuffle(scenarios)
    if args.limit:
        scenarios = scenarios[:args.limit]

    print("Scenarios: %d" % len(scenarios))
    print("Mode: %s" % ("LIVE" if args.live else "DRY-RUN"))
    print("Model: %s  temperature: %s  num_predict: %s  seed: %s" % (
        args.model, args.temperature, args.num_predict, args.seed))

    if not args.live:
        run_id = "dry-run-%s" % time.strftime("%Y%m%d%H%M%S")
        records = []
        for s in scenarios:
            rs = retrieval_sets[s["scenario_id"]]
            for cond in CONDITIONS:
                prompt = build_prompt(s, cond, rs)
                records.append({
                    "scenario_id": s["scenario_id"],
                    "category": s["category"],
                    "condition": cond,
                    "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16],
                    "raw_response": "",
                    "done_reason": None,
                    "is_truncated": False,
                    "run_id": run_id,
                    "model": args.model,
                    "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                })
        Path(args.output).write_text(
            "\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")
        print("Wrote %d trial records (dry run, no model calls)" % len(records))
        return 0

    run_id = args.run_id or "confirmatory-%s" % time.strftime("%Y%m%d%H%M%S")
    print("run_id: %s" % run_id)
    records = []
    n = len(scenarios)
    for i, s in enumerate(scenarios):
        rs = retrieval_sets[s["scenario_id"]]
        for cond in CONDITIONS:
            prompt = build_prompt(s, cond, rs)
            t0 = time.time()
            try:
                raw, done_reason, is_truncated = call_ollama(
                    prompt, args.model, args.temperature, args.num_predict)
                err = None
            except (urllib.error.URLError, OSError, ValueError) as e:
                raw, done_reason, is_truncated = "", "error", False
                err = str(e)
            elapsed = time.time() - t0
            record = {
                "scenario_id": s["scenario_id"],
                "category": s["category"],
                "condition": cond,
                "prompt_hash": hashlib.sha256(prompt.encode()).hexdigest()[:16],
                "raw_response": raw,
                "done_reason": done_reason,
                "is_truncated": is_truncated,
                "elapsed": round(elapsed, 3),
                "run_id": run_id,
                "model": args.model,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                "temperature": args.temperature,
                "num_predict": args.num_predict,
                "seed": args.seed,
            }
            if err:
                record["error"] = err
            records.append(record)
            print("  [%d/%d] %s %s done_reason=%s %.1fs" % (
                i + 1, n, s["scenario_id"], cond, done_reason, elapsed))

    Path(args.output).write_text(
        "\n".join(json.dumps(r) for r in records) + "\n", encoding="utf-8")
    print("Wrote %d trial records to %s" % (len(records), args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
