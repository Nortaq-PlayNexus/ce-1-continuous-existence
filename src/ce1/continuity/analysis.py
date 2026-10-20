"""Preregistered analysis for the continuity_v1 benchmark.

`experiments/continuity_v1/preregistration_h8.md` specifies, for the primary
comparison (correct_retrieval - matched_decoy, paired by scenario):

  * a paired permutation test, seeded and reproducible;
  * a bootstrap confidence interval, scenario-level, seeded, with the
    resample count recorded;
  * invalid trials excluded, never scored as zero;
  * INVALID_RUN when more than 5% of trials are invalid or when there are
    insufficient paired observations.

The preregistration does not fix the seed or the resample count, so both are
chosen here and written into the analysis output: seed 20261020 (the
benchmark seed) and 10000 resamples.
"""

from __future__ import annotations

import random
from typing import Iterable, Sequence

SEED = 20261020
N_RESAMPLES = 10000
MAX_INVALID_RATE = 0.05
ALPHA = 0.05


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values)


def paired_permutation_test(diffs: Sequence[float], n_resamples: int = N_RESAMPLES,
                            seed: int = SEED) -> dict:
    """Two-sided sign-flip permutation test on paired differences.

    Under the null the sign of each paired difference is exchangeable, so
    flipping signs at random preserves the paired design.
    """
    if not diffs:
        return {"p_value": None, "observed_mean": None, "n_resamples": n_resamples,
                "seed": seed, "n_pairs": 0, "note": "no paired observations"}
    observed = _mean(diffs)
    rng = random.Random(seed)
    at_least_as_extreme = 0
    for _ in range(n_resamples):
        total = 0.0
        for d in diffs:
            total += -d if rng.random() < 0.5 else d
        if abs(total / len(diffs)) >= abs(observed) - 1e-12:
            at_least_as_extreme += 1
    return {
        "p_value": (at_least_as_extreme + 1) / (n_resamples + 1),
        "observed_mean": observed,
        "n_resamples": n_resamples,
        "seed": seed,
        "n_pairs": len(diffs),
    }


def bootstrap_ci(values: Sequence[float], n_resamples: int = N_RESAMPLES,
                 seed: int = SEED, alpha: float = ALPHA) -> dict:
    """Percentile bootstrap confidence interval for the mean.

    Resampling is over the scenario-level values (the independent unit), not
    over trials.
    """
    if not values:
        return {"lower": None, "upper": None, "n_resamples": n_resamples,
                "seed": seed, "n": 0, "note": "no observations"}
    rng = random.Random(seed)
    n = len(values)
    means = []
    for _ in range(n_resamples):
        total = 0.0
        for _ in range(n):
            total += values[rng.randrange(n)]
        means.append(total / n)
    means.sort()
    lower = _percentile(means, 100 * alpha / 2)
    upper = _percentile(means, 100 * (1 - alpha / 2))
    return {"lower": lower, "upper": upper, "n_resamples": n_resamples,
            "seed": seed, "n": n, "alpha": alpha, "point_estimate": _mean(values)}


def _percentile(sorted_values: Sequence[float], pct: float) -> float:
    if not sorted_values:
        raise ValueError("empty sample")
    if len(sorted_values) == 1:
        return sorted_values[0]
    pos = (len(sorted_values) - 1) * (pct / 100.0)
    low = int(pos)
    high = min(low + 1, len(sorted_values) - 1)
    frac = pos - low
    return sorted_values[low] * (1 - frac) + sorted_values[high] * frac


def paired_differences(scores: Iterable[dict], condition_a: str, condition_b: str,
                       by: str = "scenario_id") -> dict[str, float]:
    """Pair condition_a and condition_b scores by `by`, keeping valid trials only.

    A scenario contributes a pair only when both conditions produced a valid
    scored trial.
    """
    buckets: dict[str, dict[str, float]] = {}
    for s in scores:
        if s.get("score") is None:
            continue
        key = s[by]
        buckets.setdefault(key, {})[s["condition"]] = float(s["score"])
    out = {}
    for key, per_cond in buckets.items():
        if condition_a in per_cond and condition_b in per_cond:
            out[key] = per_cond[condition_a] - per_cond[condition_b]
    return out


def invalid_rate(trials: Sequence[dict]) -> float:
    if not trials:
        return 1.0
    invalid = sum(1 for t in trials if t.get("score") is None)
    return invalid / len(trials)


def min_required_pairs(n_scenarios: int) -> int:
    """Paired observations needed for the run to count (90% of scenarios)."""
    return -(-(9 * n_scenarios) // 10)


def decide_verdict(primary_diff: float | None, permutation_p: float | None,
                   ci_lower: float | None, invalid_rate: float,
                   n_pairs: int, min_pairs: int, min_effect: float,
                   alpha: float = ALPHA) -> tuple[str, list[str]]:
    """Apply the validity gate and the decision rule.

    Returns (verdict, gate_failures). Verdicts: INVALID_RUN, SUPPORTED,
    INCONCLUSIVE, NOT_SUPPORTED.
    """
    gate_failures = []
    if invalid_rate > MAX_INVALID_RATE:
        gate_failures.append("invalid_rate_%.4f_above_%.2f" % (invalid_rate, MAX_INVALID_RATE))
    if n_pairs < min_pairs:
        gate_failures.append("insufficient_paired_observations_%d_below_%d" % (n_pairs, min_pairs))

    effect_met = primary_diff is not None and primary_diff >= min_effect
    p_ok = permutation_p is not None and permutation_p <= alpha
    ci_ok = ci_lower is not None and ci_lower > 0

    if gate_failures:
        return "INVALID_RUN", gate_failures
    if effect_met and p_ok and ci_ok:
        return "SUPPORTED", gate_failures
    if effect_met:
        return "INCONCLUSIVE", gate_failures
    return "NOT_SUPPORTED", gate_failures

