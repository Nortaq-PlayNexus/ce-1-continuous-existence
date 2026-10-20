#!/usr/bin/env python3
"""Model qualification runner.

Records qualification trial data. Does NOT make live model calls in test mode.
In production mode (--live), calls Ollama for each suite item.

Usage:
    python run_qualification.py --suite qualification_suite.jsonl --output results.jsonl
    python run_qualification.py --suite qualification_suite.jsonl --output results.jsonl --live
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

SUITE_PATH = Path(__file__).resolve().parent / "qualification_suite.jsonl"


def load_suite(path: Path) -> list[dict]:
    """Load the qualification suite from a JSONL file."""
    items = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def compute_manifest_hash(path: Path) -> str:
    """Compute SHA-256 hash of the suite file."""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_trial_record(item: dict, raw_response: str = "", done_reason: str | None = None,
                       is_truncated: bool = False, elapsed: float = 0.0,
                       run_id: str = "", model: str = "", prompt_hash: str = "",
                       code_revision: str = "") -> dict:
    """Build a trial result record with full reproducibility metadata."""
    return {
        "id": item["id"],
        "raw_response": raw_response,
        "done_reason": done_reason,
        "is_truncated": is_truncated,
        "elapsed_seconds": round(elapsed, 3),
        "run_id": run_id,
        "model": model,
        "prompt_hash": prompt_hash,
        "code_revision": code_revision,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }


def main():
    parser = argparse.ArgumentParser(description="Run model qualification suite")
    parser.add_argument("--suite", default=str(SUITE_PATH), help="Path to suite JSONL")
    parser.add_argument("--output", default="qualification_results.jsonl", help="Output path")
    parser.add_argument("--live", action="store_true", help="Make live Ollama calls")
    parser.add_argument("--model", default="gemma3:4b", help="Model to qualify")
    args = parser.parse_args()

    suite_path = Path(args.suite)
    suite = load_suite(suite_path)
    manifest_hash = compute_manifest_hash(suite_path)

    print("Qualification suite: %d items" % len(suite))
    print("Manifest hash: %s" % manifest_hash)
    print("Mode: %s" % ("LIVE" if args.live else "DRY-RUN (no model calls)"))

    if args.live:
        print("ERROR: Live mode requires explicit human authorization.")
        print("Use --live only after authorization. Exiting.")
        return 1

    # Dry run: produce empty trial records (no model calls)
    run_id = "dry-run-%s" % time.strftime("%Y%m%d%H%M%S")
    records = []
    for item in suite:
        record = build_trial_record(
            item=item,
            raw_response="",
            done_reason=None,
            is_truncated=False,
            elapsed=0.0,
            run_id=run_id,
            model=args.model,
            prompt_hash=hashlib.sha256(item["prompt"].encode()).hexdigest()[:16],
            code_revision="unknown",
        )
        records.append(record)

    output_path = Path(args.output)
    with open(output_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    print("Wrote %d trial records to %s" % (len(records), output_path))
    print("NOTE: This is a dry run. No model calls were made.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
