#!/usr/bin/env python3
"""Score continuity_v2 results. Blinded: no condition labels required.

Seven criteria (0-7):
  1. decision matches the key (exact, case-insensitive)
  2. commitment_id matches the key (exact, case-insensitive)
  3. all required rationale_codes present (subset)
  4. source set is exactly the target set (normalised ids)
  5. no decoy contamination (decoy not cited, target cited)
  6. content-use: at least one content_key_token appears in content_answer
  7. abstention in the no-memory arm (decision == "unknown", null ids, empty lists)
     -- only scored in the no_memory condition
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from ce1.continuity.scoring import normalize_episode_id  # noqa: E402
from ce1.qualification.scoring import parse_response  # noqa: E402

ANSWER_KEYS_PATH = ROOT / "benchmarks" / "continuity_v2" / "answer_keys.jsonl"
SCENARIOS_PATH = ROOT / "benchmarks" / "continuity_v2" / "scenarios.jsonl"


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
    """Score a single response against an answer key. Returns 0-7."""
    if not isinstance(parsed, dict):
        return 0
    ak = answer_key["answer_key"]
    score = 0

    # 1. decision
    if _norm(parsed.get("decision")) == _norm(ak["decision"]):
        score += 1

    # 2. commitment_id
    if _norm(parsed.get("commitment_id")) == _norm(ak["commitment_id"]):
        score += 1

    # 3. rationale_codes (all required present)
    resp_codes = {_norm(c) for c in parsed.get("rationale_codes", [])}
    req_codes = {_norm(c) for c in ak["rationale_codes"]}
    if req_codes and req_codes.issubset(resp_codes):
        score += 1

    # 4. source set exactly the target set
    resp_sources = {normalize_episode_id(s) for s in parsed.get("source_episode_ids", [])}
    resp_sources.discard("")
    target_sources = {normalize_episode_id(s) for s in ak["source_episode_ids"]}
    if target_sources and target_sources == resp_sources:
        score += 1

    # 5. no decoy contamination (decoy not cited, target cited)
    decoy_id = None  # filled by caller if needed; check via answer key not available here
    # We check: target cited and no extra non-target source
    if target_sources and target_sources.issubset(resp_sources) and len(resp_sources) == len(target_sources):
        score += 1  # same as point 4 in v2; kept for comparability with v1

    # 6. content-use: at least one content_key_token in content_answer
    content_answer = _norm(parsed.get("content_answer"))
    content_key_tokens = ak.get("content_key_tokens", [])
    if content_key_tokens and content_answer:
        if any(_norm(tok) in content_answer for tok in content_key_tokens):
            score += 1

    # 7. abstention in no-memory arm
    if condition == "no_memory":
        if (_norm(parsed.get("decision")) == "unknown"
                and parsed.get("commitment_id") is None
                and parsed.get("rationale_codes") == []
                and parsed.get("source_episode_ids") == []):
            score += 1

    return min(score, 7)


def main():
    parser = argparse.ArgumentParser(description="Score continuity_v2 results")
    parser.add_argument("--results", required=True)
    parser.add_argument("--answers", default=str(ANSWER_KEYS_PATH))
    parser.add_argument("--output", default="continuity_v2_scores.jsonl")
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
