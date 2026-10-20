#!/usr/bin/env python3
"""Score continuity_v1 results. Blinded: no condition labels required.

Two instruments are available:

  --scoring as_run     the instrument used for the recorded confirmatory run
                       (commit dd5f188). Default, and byte-compatible with the
                       committed confirmatory_scores.jsonl.
  --scoring corrected  the amended instrument (episode-id normalisation, a
                       real decoy-contamination check). Invalid trials are
                       recorded with a reason and are NOT scored as zero.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from ce1.continuity.scoring import (  # noqa: E402
    classify_validity,
    score_as_run,
    score_corrected,
)
from ce1.qualification.scoring import parse_response  # noqa: E402

ANSWER_KEYS_PATH = ROOT / "benchmarks" / "continuity_v1" / "answer_keys.jsonl"
SCENARIOS_PATH = ROOT / "benchmarks" / "continuity_v1" / "scenarios.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    items = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def score_response(response: dict, answer_key: dict) -> int:
    """Score a single response against an answer key. Returns 0-5."""
    return score_as_run(response, answer_key)


def main():
    parser = argparse.ArgumentParser(description="Score continuity_v1 results")
    parser.add_argument("--results", required=True)
    parser.add_argument("--answers", default=str(ANSWER_KEYS_PATH))
    parser.add_argument("--output", default="continuity_v1_scores.jsonl")
    parser.add_argument("--scoring", choices=["as_run", "corrected"], default="as_run")
    args = parser.parse_args()

    results = load_jsonl(Path(args.results))
    answer_keys = {ak["scenario_id"]: ak for ak in load_jsonl(Path(args.answers))}
    decoys = {}
    if args.scoring == "corrected":
        decoys = {s["scenario_id"]: s.get("decoy_episode_id")
                  for s in load_jsonl(SCENARIOS_PATH)}

    scored = []
    for r in results:
        ak = answer_keys.get(r["scenario_id"])
        if ak is None:
            scored.append({"scenario_id": r["scenario_id"], "condition": r["condition"],
                           "score": None, "error": "missing answer key"})
            continue
        raw = r.get("raw_response", "")
        resp = parse_response(raw) if raw else None
        if args.scoring == "as_run":
            s = score_response(resp, ak) if resp else 0
            scored.append({
                "scenario_id": r["scenario_id"],
                "category": r.get("category"),
                "condition": r["condition"],
                "score": s,
                "raw_response": raw,
            })
            continue
        valid, reason = classify_validity(r)
        s = score_corrected(resp, ak, decoys.get(r["scenario_id"])) if valid else None
        scored.append({
            "scenario_id": r["scenario_id"],
            "category": r.get("category"),
            "condition": r["condition"],
            "score": s,
            "valid": valid,
            "invalid_reason": reason,
            "raw_response": raw,
        })

    Path(args.output).write_text(
        "\n".join(json.dumps(s) for s in scored) + "\n", encoding="utf-8")
    print("Scored %d trials (%s)" % (len(scored), args.scoring))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
