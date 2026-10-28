#!/usr/bin/env python3
"""Analyze H3 interruption/resumption results."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from ce1.continuity.analysis import (  # noqa: E402
    N_RESAMPLES,
    SEED,
    bootstrap_ci,
    decide_verdict,
    min_required_pairs,
    paired_differences,
    paired_permutation_test,
)
from ce1.continuity.scoring import classify_validity  # noqa: E402

MIN_MEANINGFUL_EFFECT = 0.50
PRIMARY_A = "store_populated"
PRIMARY_B = "store_empty"
ALPHA = 0.05


def load_jsonl(path: Path) -> list[dict]:
    items = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def main():
    parser = argparse.ArgumentParser(description="Analyze H3 results")
    parser.add_argument("--scores", required=True)
    parser.add_argument("--results", required=True)
    parser.add_argument("--output", default="h3_analysis.json")
    parser.add_argument("--seed", type=int, default=SEED)
    parser.add_argument("--resamples", type=int, default=N_RESAMPLES)
    parser.add_argument("--min-effect", type=float, default=MIN_MEANINGFUL_EFFECT)
    args = parser.parse_args()

    scores = load_jsonl(Path(args.scores))
    results = load_jsonl(Path(args.results))
    validity = {}
    for r in results:
        ok, reason = classify_validity(r)
        validity[(r["scenario_id"], r["condition"])] = (ok, reason)

    usable = []
    invalid_by_condition: dict[str, int] = {}
    for s in scores:
        key = (s["scenario_id"], s["condition"])
        ok, reason = validity.get(key, (False, "missing_result_record"))
        if s.get("score") is None:
            ok, reason = False, reason or "unscored"
        if not ok:
            invalid_by_condition[s["condition"]] = invalid_by_condition.get(s["condition"], 0) + 1
            continue
        usable.append(s)

    total_trials = len(scores)
    n_invalid = total_trials - len(usable)
    invalid_rate = n_invalid / total_trials if total_trials else 1.0

    by_cond: dict[str, list[float]] = {}
    for s in usable:
        by_cond.setdefault(s["condition"], []).append(float(s["score"]))
    means = {c: sum(v) / len(v) if v else None for c, v in by_cond.items()}

    # Primary: store_populated vs store_empty
    diffs = paired_differences(usable, PRIMARY_A, PRIMARY_B)
    diff_values = list(diffs.values())
    n_scenarios = len({s["scenario_id"] for s in scores})
    min_pairs = min_required_pairs(n_scenarios)

    permutation = paired_permutation_test(diff_values, n_resamples=args.resamples, seed=args.seed)
    ci = bootstrap_ci(diff_values, n_resamples=args.resamples, seed=args.seed, alpha=ALPHA)
    primary_diff = (means.get(PRIMARY_A) - means.get(PRIMARY_B)
                    if means.get(PRIMARY_A) is not None and means.get(PRIMARY_B) is not None
                    else None)

    # Secondary: store_populated vs reconstruct
    secondary = {}
    if means.get("store_populated") is not None and means.get("reconstruct") is not None:
        secondary["store_populated - reconstruct"] = means["store_populated"] - means["reconstruct"]
    if means.get("store_empty") is not None and means.get("reconstruct") is not None:
        secondary["store_empty - reconstruct"] = means["store_empty"] - means["reconstruct"]

    per_category: dict[str, dict] = {}
    for s in usable:
        cat = s.get("category") or "unknown"
        per_category.setdefault(cat, {}).setdefault(s["condition"], []).append(float(s["score"]))
    per_category_out = {}
    for cat, conds in sorted(per_category.items()):
        cat_means = {c: sum(v) / len(v) for c, v in conds.items()}
        row = {"means": cat_means, "n": len(conds.get(PRIMARY_A, []))}
        if PRIMARY_A in cat_means and PRIMARY_B in cat_means:
            row["diff"] = cat_means[PRIMARY_A] - cat_means[PRIMARY_B]
        per_category_out[cat] = row

    verdict, gate_failures = decide_verdict(
        primary_diff=primary_diff,
        permutation_p=permutation.get("p_value"),
        ci_lower=ci.get("lower"),
        invalid_rate=invalid_rate,
        n_pairs=len(diff_values),
        min_pairs=min_pairs,
        min_effect=args.min_effect,
        alpha=ALPHA,
    )

    result = {
        "means": means,
        "primary_comparison": "%s - %s" % (PRIMARY_A, PRIMARY_B),
        "primary_diff": primary_diff,
        "min_meaningful_effect": args.min_effect,
        "meets_threshold": primary_diff is not None and primary_diff >= args.min_effect,
        "trial_count": total_trials,
        "valid_trial_count": len(usable),
        "invalid_trial_count": n_invalid,
        "invalid_rate": invalid_rate,
        "invalid_by_condition": invalid_by_condition,
        "n_paired_observations": len(diff_values),
        "n_scenarios": n_scenarios,
        "min_required_pairs": min_pairs,
        "paired_permutation_test": permutation,
        "bootstrap_ci": ci,
        "secondary_comparisons": secondary,
        "per_category": per_category_out,
        "gate_failures": gate_failures,
        "verdict": verdict,
        "analysis_parameters": {
            "seed": args.seed,
            "n_resamples": args.resamples,
            "alpha": ALPHA,
        },
    }

    Path(args.output).write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("Primary diff (%s): %s" % (result["primary_comparison"], primary_diff))
    print("Permutation p: %s   bootstrap 95%% CI: [%s, %s]" % (
        permutation.get("p_value"), ci.get("lower"), ci.get("upper")))
    print("Valid trials: %d/%d (invalid rate %.4f)" % (
        len(usable), total_trials, invalid_rate))
    print("Verdict: %s" % verdict)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
