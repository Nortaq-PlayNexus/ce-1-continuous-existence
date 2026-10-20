#!/usr/bin/env python3
"""Score qualification run results.

Usage:
    python score_qualification.py --results results.jsonl --suite qualification_suite.jsonl --output scores.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from ce1.qualification.scoring import score_run, compute_qualification_metrics


def load_jsonl(path: Path) -> list[dict]:
    items = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def main():
    parser = argparse.ArgumentParser(description="Score qualification results")
    parser.add_argument("--results", required=True, help="Path to results JSONL")
    parser.add_argument("--suite", default=str(Path(__file__).resolve().parent / "qualification_suite.jsonl"),
                        help="Path to suite JSONL")
    parser.add_argument("--output", default="qualification_scores.json", help="Output path")
    args = parser.parse_args()

    results = load_jsonl(Path(args.results))
    suite = load_jsonl(Path(args.suite))

    scores = score_run(results, suite)
    metrics = compute_qualification_metrics(scores)

    # Serialize scores
    score_dicts = []
    for s in scores:
        score_dicts.append({
            "trial_id": s.trial_id,
            "status": s.status,
            "reason": s.reason,
            "parsed_answer": s.parsed_answer,
            "parsed_evidence_id": s.parsed_evidence_id,
            "parsed_confidence": s.parsed_confidence,
            "expected_answer": s.expected_answer,
            "expected_evidence_id": s.expected_evidence_id,
            "answer_correct": s.answer_correct,
            "evidence_correct": s.evidence_correct,
            "confidence_valid": s.confidence_valid,
        })

    output = {
        "scores": score_dicts,
        "metrics": metrics,
    }

    Path(args.output).write_text(json.dumps(output, indent=2), encoding="utf-8")
    print("Scored %d trials" % len(scores))
    print("VALID_PASS: %d, VALID_FAIL: %d, INVALID_TRIAL: %d" % (
        metrics["valid_pass"], metrics["valid_fail"], metrics["invalid_trials"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
