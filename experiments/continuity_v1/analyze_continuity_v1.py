#!/usr/bin/env python3
"""Analyze continuity_v1 results."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))


def main():
    parser = argparse.ArgumentParser(description="Analyze continuity_v1 results")
    parser.add_argument("--scores", required=True)
    parser.add_argument("--output", default="continuity_v1_analysis.json")
    args = parser.parse_args()

    scores = []
    with open(args.scores, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                scores.append(json.loads(line))

    # Group by condition
    by_cond = {}
    for s in scores:
        by_cond.setdefault(s["condition"], []).append(s["score"])

    means = {}
    for cond, vals in by_cond.items():
        valid = [v for v in vals if v is not None]
        means[cond] = sum(valid) / len(valid) if valid else None

    # Primary comparison
    correct = means.get("correct_retrieval")
    decoy = means.get("matched_decoy")
    no_mem = means.get("no_memory")

    primary_diff = (correct - decoy) if (correct is not None and decoy is not None) else None

    result = {
        "means": means,
        "primary_comparison": "correct_retrieval - matched_decoy",
        "primary_diff": primary_diff,
        "min_meaningful_effect": 0.50,
        "meets_threshold": primary_diff is not None and primary_diff >= 0.50,
        "trial_count": len(scores),
    }

    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("Primary diff (correct - decoy): %s" % primary_diff)
    print("Meets threshold (>=0.50): %s" % result["meets_threshold"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
