#!/usr/bin/env python3
"""Model qualification runner.

Records qualification trial data. Dry-run by default; --live makes Ollama calls.

Usage:
    python run_qualification.py --suite qualification_suite.jsonl --output results.jsonl
    python run_qualification.py --suite qualification_suite.jsonl --output results.jsonl --live --model gemma3:4b
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import urllib.request
import urllib.error
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

SUITE_PATH = Path(__file__).resolve().parent / "qualification_suite.jsonl"
OLLAMA_URL = "http://127.0.0.1:11434/api/generate"


def load_suite(path: Path) -> list[dict]:
    items = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def compute_manifest_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def build_trial_record(item, raw_response="", done_reason=None, is_truncated=False,
                       elapsed=0.0, run_id="", model="", prompt_hash="", code_revision=""):
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
    parser.add_argument("--suite", default=str(SUITE_PATH))
    parser.add_argument("--output", default="qualification_results.jsonl")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--model", default="gemma3:4b")
    args = parser.parse_args()

    suite_path = Path(args.suite)
    suite = load_suite(suite_path)
    manifest_hash = compute_manifest_hash(suite_path)

    print("Qualification suite: %d items" % len(suite))
    print("Manifest hash: %s" % manifest_hash)

    run_id = "run-%s" % time.strftime("%Y%m%d%H%M%S")
    records = []

    if args.live:
        print("LIVE MODE: Making Ollama calls for %d items with %s" % (len(suite), args.model))
        for i, item in enumerate(suite):
            prompt = item["prompt"]
            t0 = time.time()
            try:
                body = json.dumps({
                    "model": args.model,
                    "prompt": prompt,
                    "stream": False,
                    "think": False,
                    "options": {"temperature": 0.0, "num_predict": 300},
                }).encode("utf-8")
                req = urllib.request.Request(OLLAMA_URL, data=body,
                                            headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=300) as resp:
                    result = json.loads(resp.read().decode("utf-8"))
                raw = result.get("response", "")
                done_reason = result.get("done_reason")
                is_truncated = (done_reason == "length")
                elapsed = time.time() - t0
                print("  [%d/%d] %s: done_reason=%s truncated=%s %.1fs" % (
                    i + 1, len(suite), item["id"], done_reason, is_truncated, elapsed))
            except Exception as e:
                raw = ""
                done_reason = "error"
                is_truncated = False
                elapsed = time.time() - t0
                print("  [%d/%d] %s: ERROR %s" % (i + 1, len(suite), item["id"], e))

            record = build_trial_record(
                item=item, raw_response=raw, done_reason=done_reason,
                is_truncated=is_truncated, elapsed=elapsed, run_id=run_id,
                model=args.model,
                prompt_hash=hashlib.sha256(item["prompt"].encode()).hexdigest()[:16],
                code_revision="live-run",
            )
            records.append(record)
    else:
        print("DRY-RUN MODE: No model calls")
        run_id = "dry-run-%s" % time.strftime("%Y%m%d%H%M%S")
        for item in suite:
            record = build_trial_record(
                item=item, raw_response="", done_reason=None, is_truncated=False,
                elapsed=0.0, run_id=run_id, model=args.model,
                prompt_hash=hashlib.sha256(item["prompt"].encode()).hexdigest()[:16],
                code_revision="unknown",
            )
            records.append(record)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for r in records:
            f.write(json.dumps(r) + "\n")

    print("Wrote %d trial records to %s" % (len(records), output_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
