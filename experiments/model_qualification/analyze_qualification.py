#!/usr/bin/env python3
"""Analyze qualification results and produce a model verdict.

Usage:
    python analyze_qualification.py --scores qualification_scores.json --output verdict.json
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "src"))

from ce1.qualification.analysis import analyze_qualification


def main():
    parser = argparse.ArgumentParser(description="Analyze qualification results")
    parser.add_argument("--scores", required=True, help="Path to scores JSON")
    parser.add_argument("--output", default="qualification_verdict.json", help="Output path")
    args = parser.parse_args()

    data = json.loads(Path(args.scores).read_text(encoding="utf-8"))
    metrics = data["metrics"]

    result = analyze_qualification(data.get("scores", []), metrics)

    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("Verdict: %s" % result["verdict"])
    for r in result["reasons"]:
        print("  - %s" % r)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
