#!/usr/bin/env python3
"""Run the H3 interruption/resumption benchmark."""

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

BENCH_DIR = ROOT / "benchmarks" / "h3_interruption"
SCENARIOS_PATH = BENCH_DIR / "scenarios.jsonl"
RETRIEVAL_PATH = BENCH_DIR / "retrieval_sets.jsonl"

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
CONDITIONS = ["store_populated", "store_empty", "reconstruct"]
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
    cond_data = retrieval_set["conditions"][condition]
    episodes = cond_data["episodes"]
    transcript = cond_data.get("step1_transcript")
    episode_block = ""
    if episodes:
        episode_block = "\n\nPRIOR EPISODES (retrieved from persistent store):\n" + "\n".join(
            "- [%s] %s" % (ep["episode_id"], ep["content"]) for ep in episodes
        )
    elif condition == "store_empty":
        episode_block = "\n\nPRIOR EPISODES (retrieved from persistent store):\n(none available)"
    if transcript:
        episode_block = "\n\nPRIOR TRANSCRIPT (full reconstruction):\n" + transcript

    allowed_decisions = "approve | delay | reject | revise | escalate | unknown"
    allowed_codes = ", ".join([
        "verify_before_trust", "self_report_not_evidence",
        "no_deploy_untested", "integration_required",
        "rate_limit_threshold", "cascade_prevention",
        "memory_limit_check", "within_bounds",
        "new_evidence_overrides", "critical_bug_found",
        "source_attribution", "primary_source",
        "verification_complete", "deploy_approved",
        "within_threshold", "rate_acceptable",
        "tests_passing",
    ])
    return (
        "You are evaluating a decision task. You are resuming after an interruption.\n"
        "%s\n\n"
        "TASK: %s\n\n"
        "ALLOWED DECISIONS: %s\n"
        "ALLOWED RATIONALE CODES: %s\n\n"
        "Respond with JSON only:\n"
        '{"decision": "<one of the allowed decisions>", "commitment_id": "<string or null>", '
        '"rationale_codes": ["<subset of allowed codes>"], "source_episode_ids": ["<episode ids>"], '
        '"memory_conflict_detected": true/false, "confidence": 0.0-1.0, '
        '"content_answer": "<the specific fact or value from the retrieved episode that supports your decision>"}'
    ) % (episode_block, scenario["step2_task"], allowed_decisions, allowed_codes)


def call_ollama(prompt: str, model: str, temperature: float, num_predict: int,
                timeout: int = 300) -> tuple[str, str | None, bool]:
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
    parser = argparse.ArgumentParser(description="Run H3 interruption benchmark")
    parser.add_argument("--scenarios", default=str(SCENARIOS_PATH))
    parser.add_argument("--retrieval", default=str(RETRIEVAL_PATH))
    parser.add_argument("--output", default="h3_results.jsonl")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--model", default="gemma3:4b")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--num-predict", type=int, default=300)
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--run-id", default=None)
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--offset", type=int, default=0)
    args = parser.parse_args()

    scenarios = load_jsonl(Path(args.scenarios))
    retrieval_sets = {rs["scenario_id"]: rs for rs in load_jsonl(Path(args.retrieval))}
    random.Random(args.seed).shuffle(scenarios)
    if args.offset:
        scenarios = scenarios[args.offset:]
    if args.limit:
        scenarios = scenarios[:args.limit]

    print("Scenarios: %d" % len(scenarios))
    print("Mode: %s" % ("LIVE" if args.live else "DRY-RUN"))

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
        print("Wrote %d trial records (dry run)" % len(records))
        return 0

    run_id = args.run_id or "h3-%s" % time.strftime("%Y%m%d%H%M%S")
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
                "is_truncated": bool(is_truncated),
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
