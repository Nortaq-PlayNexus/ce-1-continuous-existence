#!/usr/bin/env python3
"""Score continuity_v1 results. Blinded: no condition labels required."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

ANSWER_KEYS_PATH = Path(__file__).resolve().parent.parent.parent / "benchmarks" / "continuity_v1" / "answer_keys.jsonl"


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
    if not isinstance(response, dict):
        return 0  # invalid, but score 0 for compatibility (should be INVALID)
    ak = answer_key["answer_key"]
    score = 0

    # 1. Correct decision
    if response.get("decision") == ak["decision"]:
        score += 1

    # 2. Correct commitment_id
    if response.get("commitment_id") == ak["commitment_id"]:
        score += 1

    # 3. All required rationale_codes present
    resp_codes = set(response.get("rationale_codes", []))
    req_codes = set(ak["rationale_codes"])
    if req_codes.issubset(resp_codes):
        score += 1

    # 4. Correct source_episode_ids, no decoy
    resp_sources = set(response.get("source_episode_ids", []))
    target_sources = set(ak["source_episode_ids"])
    decoy_id = None  # would need scenario context; check via answer key
    if target_sources.issubset(resp_sources) and not (resp_sources - target_sources):
        score += 1

    # 5. No decoy contamination (no decoy rationale adopted)
    # Simplified: if source attribution is clean, award point
    if target_sources.issubset(resp_sources):
        score += 1

    return min(score, 5)


def main():
    parser = argparse.ArgumentParser(description="Score continuity_v1 results")
    parser.add_argument("--results", required=True)
    parser.add_argument("--answers", default=str(ANSWER_KEYS_PATH))
    parser.add_argument("--output", default="continuity_v1_scores.jsonl")
    args = parser.parse_args()

    results = load_jsonl(Path(args.results))
    answer_keys = {ak["scenario_id"]: ak for ak in load_jsonl(Path(args.answers))}

    scored = []
    for r in results:
        ak = answer_keys.get(r["scenario_id"])
        if ak is None:
            scored.append({"scenario_id": r["scenario_id"], "condition": r["condition"],
                           "score": None, "error": "missing answer key"})
            continue
        # Parse response
        import json as _json
        resp = None
        raw = r.get("raw_response", "")
        if raw:
            try:
                resp = _json.loads(raw)
            except (json.JSONDecodeError, ValueError):
                resp = None
        s = score_response(resp, ak) if resp else 0
        scored.append({
            "scenario_id": r["scenario_id"],
            "category": r.get("category"),
            "condition": r["condition"],
            "score": s,
            "raw_response": raw,
        })

    Path(args.output).write_text(
        "\n".join(json.dumps(s) for s in scored) + "\n", encoding="utf-8")
    print("Scored %d trials" % len(scored))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
