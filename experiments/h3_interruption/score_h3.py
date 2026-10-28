#!/usr/bin/env python3
"""Score H3 interruption/resumption results."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from ce1.qualification.scoring import parse_response  # noqa: E402

ANSWER_KEYS_PATH = ROOT / "benchmarks" / "h3_interruption" / "answer_keys.jsonl"


def load_jsonl(path: Path) -> list[dict]:
    items = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def _norm(value: object) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def score_response(parsed: dict | None, answer_key: dict, condition: str) -> int:
    """Score a single response against the step-2 answer key. Returns 0-6."""
    if not isinstance(parsed, dict):
        return 0
    ak = answer_key["answer_key"]["step2"]
    score = 0

    # 1. decision matches step2 key
    if _norm(parsed.get("decision")) == _norm(ak["decision"]):
        score += 1

    # 2. commitment_id matches
    if _norm(parsed.get("commitment_id")) == _norm(ak["commitment_id"]):
        score += 1

    # 3. rationale_codes (all required present)
    resp_codes = {_norm(c) for c in parsed.get("rationale_codes", [])}
    req_codes = {_norm(c) for c in ak["rationale_codes"]}
    if req_codes and req_codes.issubset(resp_codes):
        score += 1

    # 4. source set contains the target (normalised)
    resp_sources = {_norm(s) for s in parsed.get("source_episode_ids", [])}
    target_sources = {_norm(s) for s in ak["source_episode_ids"]}
    if target_sources and target_sources.issubset(resp_sources):
        score += 1

    # 5. content-use: at least one content_key_token in content_answer
    content_answer = _norm(parsed.get("content_answer"))
    content_key_tokens = ak.get("content_key_tokens", [])
    if content_key_tokens and content_answer:
        if any(_norm(tok) in content_answer for tok in content_key_tokens):
            score += 1

    # 6. abstention in store_empty arm
    if condition == "store_empty":
        if (_norm(parsed.get("decision")) == "unknown"
                and parsed.get("commitment_id") is None
                and parsed.get("rationale_codes") == []
                and parsed.get("source_episode_ids") == []):
            score += 1

    return min(score, 6)


def main():
    parser = argparse.ArgumentParser(description="Score H3 results")
    parser.add_argument("--results", required=True)
    parser.add_argument("--answers", default=str(ANSWER_KEYS_PATH))
    parser.add_argument("--output", default="h3_scores.jsonl")
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
        raw = r.get("raw_response", "")
        parsed = parse_response(raw) if raw else None
        s = score_response(parsed, ak, r["condition"]) if parsed else 0
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
