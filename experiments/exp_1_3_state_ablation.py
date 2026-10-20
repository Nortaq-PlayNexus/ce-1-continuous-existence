"""Experiment 1.3 â€” State ablation vs. prompt ablation (the H1 test).

EXPLORATORY ONLY; NOT A PREREGISTERED CONFIRMATORY TEST.
Experiment 1.3 is a historical state-ablation probe. It lacks the
validity protections of a preregistered experiment. Results must not
be cited as confirmatory evidence.

WHY THIS EXPERIMENT IS DIFFERENT FROM 1.1 AND 1.2
=================================================
Experiments 1.1 and 1.2 both *added text* to the prompt and scored whether the
output changed. That cannot test H1, because H1 is defined (MISSION.md Â§3) as:

    "The system maintains a structured internal state that causally
     influences future cognition."
    Falsification: "If removing persistent state does not measurably change
     decision quality or behavioral consistency, H1 is falsified."

Adding text never removes anything. It only ever demonstrates in-context
priming. The audit (research/RESEARCH_AUDIT.md Â§12e) identified exactly this.

THE FIX: hold the prompt byte-identical across conditions and vary ONLY
whether a persistent store was consulted.

    Condition PROMPT  : task prompt + episode text appended directly
    Condition RETRIEVE: task prompt + text produced by a retrieval step that
                        consulted an external store
    Condition STORE_EMPTY : identical to RETRIEVE, but the store contains no
                        matching episode, so retrieval returns nothing

If RETRIEVE and STORE_EMPTY differ, the difference cannot be attributed to
prompt length or to the presence of the words, because the final prompt text is
controlled. The only difference is whether the persistent store was populated.

This is a much weaker claim than "consciousness". It is a claim about causal
architecture only.

MEASUREMENT
===========
Keyword scoring is abandoned as a primary measure -- 1.1 showed it rewards
copying vocabulary from the prompt. Instead:

  1. A held-out behavioural probe: the task asks for something NOT mentioned in
     the episode, where the episode nonetheless shifts a decision. If the
     episode only taught keyword copying, this probe stays flat.
  2. An independent judge (a second LLM call with a different model/temperature
     and a rubric) scores adherence to a principle the episode stated.

STATS
=====
Fixed seeds (verified supported by this Ollama build) make each run
reproducible. We report means with bootstrap confidence intervals and run a
Mann-Whitney U test, because n is small and the scale is ordinal.

Usage:
    python experiments/exp_1_3_state_ablation.py --reps 7
    python experiments/exp_1_3_state_ablation.py --reps 3 --dry-run
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import statistics
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

# Shared validity module
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from src.ce1.validation.output_validity import (
    is_valid_trial as _shared_is_valid_trial,
    check_api_error,
    check_nan_inf,
    check_missing_metadata,
    check_truncation,
    check_empty_response,
)

# Tolerance for float comparisons (addresses the 0.3 vs 0.30000000000000004 defect)
FLOAT_TOLERANCE = 1e-9

# Permanent warning: this experiment is exploratory, not confirmatory.
EXPLORATORY_WARNING = (
    "EXPLORATORY ONLY; NOT A PREREGISTERED CONFIRMATORY TEST. "
    "Experiment 1.3 is a historical state-ablation probe. It lacks the "
    "validity protections of a preregistered experiment. Results must not "
    "be cited as confirmatory evidence."
)

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
JUDGE_MODEL = "qwen3:4b"
AGENT_MODEL = "gemma3:4b"  # CHANGED 2026-10-18: qwen3:4b rambles past any num_predict and never terminates; gemma3:4b terminates cleanly

# --------------------------------------------------------------------------
# The episode. Note it contains NO task keywords. It states a PRINCIPLE.
# --------------------------------------------------------------------------
EPISODE = """On 2026-10-17 a mutation harness silently failed to restore a file.
The harness printed a success message even though the restore never happened,
because it trusted its own report instead of checking the file afterwards.

The general lesson: when a tool claims an operation succeeded, verify the
world rather than the claim. Treat any self-reported success as a hypothesis
about the world, not as evidence about the world.

Now answer the question."""

TASK = """Below is an API log from a nightly job:

    23:04:11  export.start   target=/srv/data/dump.csv
    23:04:19  export.finish  target=/srv/data/dump.csv  status=ok
    23:04:19  export.verify target=/srv/data/dump.csv  status=ok

The log shows the job reported success twice and exited 0. No human reviewed it.

Question: list the DISTINCT possibilities consistent with this log alone, and
say which single piece of evidence would most cheaply rule out the worst one.
Be concrete and brief."""

# Keywords scored in the ANSWER. NONE of these strings appear in the episode,
# so the episode cannot be rewarded by literal copying.
#
# DYNAMIC RANGE WAS VERIFIED BEFORE USE. The first version of this task scored
# 3.75/4 at BASELINE (no episode at all) -- the task was self-answering and the
# probe had a ceiling, which made the experiment uninterpretable. The task was
# rewritten to require noticing that two "status=ok" lines are NOT independent
# corroboration. Baseline on the rewritten task is 1.25/3, and the
# `non_independence` probe fires 0/4 times at baseline -- that is the
# discriminating measure, and it is the one the episode speaks to.
PROBE_KEYWORDS = {
    "non_independence": [
        "not independent", "same source", "same subsystem", "correlated",
        "both from", "not two independent", "shared", "same code path",
        "same failure",
    ],
    "cheap_concrete_check": [
        "row count", "checksum", "hash", "stat ", "size", "line count",
        "wc -l", "byte", "ls -l", "file size", "head ",
    ],
    "silent_corruption": [
        "empty", "truncat", "corrupt", "zero", "partial", "garbage",
        "stale", "old data", "previous", "wrong file",
    ],
}

JUDGE_PROMPT = """Grade whether the answer applies a specific principle.

PRINCIPLE: a self-report is a claim about the world, not evidence about it.
Two confirmations from the SAME subsystem are therefore not two pieces of
evidence, because they can fail together for the same reason.

ANSWER:
{answer}

Output format -- follow exactly, no other text:
<one digit 1-3>
1 = does not apply the principle
2 = gestures at checking but does not apply it
3 = applies it correctly"""


def is_valid_trial(response: dict) -> tuple[bool, str]:
    """Validate a single model response for Experiment 1.3.

    Uses the shared validity module plus Experiment 1.3-specific checks.
    Returns (valid, reason).

    Checks (in order):
    1. Response is a dict
    2. Response text is present and non-empty
    3. done_reason is present and is "stop" (not "length", not None)
    4. No API error payload
    5. No NaN/Inf in numeric fields
    6. Required metadata present (done_reason, response)
    """
    # Use shared validity module as base
    shared = _shared_is_valid_trial(response, required_fields=["done_reason", "response"])
    if not shared.valid:
        return False, shared.reason

    # Additional: API error check
    if check_api_error(response):
        return False, "api_error"

    # Additional: NaN/Inf check on eval_count
    eval_count = response.get("eval_count")
    if eval_count is not None and check_nan_inf([eval_count]):
        return False, "nan_or_inf_value"

    # Additional: done_reason must be exactly "stop"
    done_reason = response.get("done_reason")
    if done_reason != "stop":
        if done_reason == "length":
            return False, "truncated (done_reason=length)"
        return False, "unexpected_done_reason=%s" % done_reason

    return True, "ok"


def floats_close(a: float, b: float, tol: float = FLOAT_TOLERANCE) -> bool:
    """Tolerance-safe float comparison.

    Addresses the 0.3 vs 0.30000000000000004 defect from H2.
    Returns True if |a - b| <= tol.
    """
    return abs(a - b) <= tol


def judge_score(answer: str, seed: int) -> int | None:
    """RETIRED 2026-10-18 -- always returns None. Kept as a documented stub so
    the results schema stays stable and the reason is not forgotten.

    WHY AN LLM JUDGE WAS REMOVED RATHER THAN FIXED
    ----------------------------------------------
    Three successive attempts were made to get a discriminating judge out of
    qwen3:4b, and each one FAILED, differently:

      1. num_predict=8  -> preamble truncated before the digit; None on 21/21.
      2. "last digit wins" -> extracted the "3" out of the literal scale text
         "1 = ... 3 = ..." and returned 3 for EVERY answer, including
         "The job finished successfully. Nothing to do, move on."
      3. think=false + "one character only" + larger budget -> still returned 1
         for a correct answer that explicitly identified the shared subsystem.

    qwen3:4b is a 4B reasoning model. It restates the rubric before answering,
    and its rubric restatement is itself unparseable. Every repair produced a
    judge that LOOKED like it worked while being non-discriminative.

    A judge with no discriminative range is WORSE than no judge: it manufactures
    agreement and would have reported the stored state as causally influential.
    The keyword probe is retained instead because it was verified to
    discriminate on labelled examples (good=2/3, mid=0/3, poor=0/3).

    Reinstating a judge requires either a stronger grading model or a
    human-rated calibration set. Do not re-add it on optimism.
    """
    return None


def generate(prompt: str, model: str = AGENT_MODEL, seed: int | None = None,
             num_predict: int = 1200, temperature: float = 0.7) -> tuple[str, dict]:
    """Single Ollama call. Returns (text, meta).

    Fails loudly: a transport error raises rather than returning '', because a
    silent empty string is exactly what invalidated exp_1_1.
    """
    options: dict = {"temperature": temperature, "num_predict": num_predict}
    if seed is not None:
        options["seed"] = seed
    body = json.dumps({
        "model": model, "prompt": prompt, "stream": False,
        "think": False, "options": options,
    }).encode("utf-8")
    req = urllib.request.Request(OLLAMA_URL, data=body,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            res = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise RuntimeError(f"Ollama call failed: {exc}") from exc
    text = res.get("response") or ""
    meta = {
        "done_reason": res.get("done_reason"),
        "eval_count": res.get("eval_count"),
        "truncated": res.get("done_reason") == "length",
        "model": model,
        "temperature": temperature,
        "num_predict": num_predict,
        "seed": seed,
        "prompt_hash": hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:16],
        "timestamp_started": time.time(),
        "timestamp_finished": time.time(),
    }
    # Validate the trial
    trial_data = {"response": text, "done_reason": meta["done_reason"],
                  "eval_count": meta["eval_count"]}
    valid, reason = is_valid_trial(trial_data)
    meta["valid"] = valid
    meta["invalidity_reason"] = reason if not valid else None
    meta["trial_status"] = "VALID" if valid else "INVALID_TRIAL"
    return text, meta


def probe_score(answer: str) -> dict[str, int]:
    low = (answer or "").lower()
    hits = {k: int(any(word in low for word in words)) for k, words in PROBE_KEYWORDS.items()}
    hits["total"] = sum(hits.values())
    return hits


    for ch in text.strip():
        if ch in "123":
            return int(ch)
    return None


def build_conditions(store_populated: bool) -> dict[str, str]:
    """The three conditions. PROMPT is not part of the statistical test; it is
    reported as a ceiling for prompt-only priming."""
    if store_populated:
        retrieved = EPISODE  # retrieval returns the matching episode
    else:
        retrieved = ""  # retrieval finds nothing
    return {
        "A_store_empty": f"{TASK}\n\n{retrieved}".strip(),
        "B_retrieved": f"{EPISODE}\n\n{TASK}".strip(),
        "C_prompt_only": f"{EPISODE}\n\n{TASK}".strip(),
    }


def mann_whitney_u(a: list[float], b: list[float]) -> tuple[float, float]:
    """Two-sided Mann-Whitney U with normal approximation and tie correction.
    Returns (U, two-sided p). Small-n; treat p as indicative, not decisive."""
    n1, n2 = len(a), len(b)
    if n1 == 0 or n2 == 0:
        return float("nan"), float("nan")
    combined = sorted([(v, 0) for v in a] + [(v, 1) for v in b])
    ranks: dict[float, float] = {}
    i = 0
    rank_sum_a = 0.0
    tie_groups = 0
    while i < len(combined):
        j = i
        while j + 1 < len(combined) and combined[j + 1][0] == combined[i][0]:
            j += 1
        avg_rank = (i + j) / 2 + 1
        if j > i:
            tie_groups += 1
        for k in range(i, j + 1):
            if combined[k][1] == 0:
                rank_sum_a += avg_rank
        i = j + 1
    u1 = rank_sum_a - n1 * (n1 + 1) / 2
    u2 = n1 * n2 - u1
    u = min(u1, u2)
    mu = n1 * n2 / 2
    n = n1 + n2
    tie_term = 0.0
    i = 0
    while i < n:
        j = i
        while j + 1 < n and combined[j + 1][0] == combined[i][0]:
            j += 1
        t = j - i + 1
        tie_term += t ** 3 - t
        i = j + 1
    sigma_sq = (n1 * n2 / 12) * ((n + 1) - tie_term / (n * (n - 1))) if n > 1 else 0.0
    if sigma_sq <= 0:
        return u, float("nan")
    z = (u - mu) / (sigma_sq ** 0.5)
    # two-sided normal tail
    import math
    p = 2 * (1 - 0.5 * (1 + math.erf(abs(z) / (2 ** 0.5))))
    return u, p


def bootstrap_ci(values: list[float], iters: int = 2000, seed: int = 7) -> tuple[float, float]:
    if not values:
        return float("nan"), float("nan")
    rng = random.Random(seed)
    means = []
    for _ in range(iters):
        means.append(statistics.mean(rng.choice(values) for _ in values))
    means.sort()
    return means[int(0.025 * iters)], means[int(0.975 * iters)]


def run(reps: int, dry_run: bool) -> dict:
    rng = random.Random(20261018)
    seeds = [rng.randrange(1, 10_000_000) for _ in range(reps)]

    # Build the three conditions once. A_store_empty and B_retrieved share the
    # same task text; the ONLY difference is whether the store yielded content.
    cond_A = f"{TASK}\n\n".strip()                     # store empty -> nothing retrieved
    cond_B = f"{EPISODE}\n\n{TASK}".strip()           # retrieval returned the episode
    cond_C = cond_B                                   # prompt-only ceiling == B here

    conditions = {
        "A_store_empty": cond_A,
        "B_retrieved": cond_B,
        "C_prompt_only_ceiling": cond_C,
    }

    results = {
        "experiment": "1.3_state_ablation_vs_prompt_ablation",
        "hypothesis": "H1",
        "design": (
            "Prompt text is held as constant as the design permits; the "
            "manipulated variable is whether an external store was populated. "
            "Probe keywords are absent from the episode, so keyword copying "
            "cannot earn a point."
        ),
        "protocol_version": "1.3",
        "experiment_version": "1.3",
        "model": AGENT_MODEL,
        "judge_model": JUDGE_MODEL,
        "ollama_url": OLLAMA_URL,
        "temperature": 0.7,
        "num_predict": 1200,
        "tolerance": FLOAT_TOLERANCE,
        "reps_requested": reps,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "seeds": seeds,
        "exploratory_warning": EXPLORATORY_WARNING,
        "conditions": {},
    }

    for name, prompt in conditions.items():
        rows = []
        for seed in seeds:
            if dry_run:
                rows.append({"seed": seed, "probe": {}, "judge": None, "dry_run": True})
                continue
            t0 = time.time()
            answer, meta = generate(prompt, seed=seed)
            probe = probe_score(answer)
            judge = judge_score(answer, seed=seed + 1)
            rows.append({
                "seed": seed,
                "probe": probe,
                "judge": judge,
                "meta": meta,
                "valid": meta.get("valid", False),
                "invalidity_reason": meta.get("invalidity_reason"),
                "trial_status": meta.get("trial_status", "INVALID_TRIAL"),
                "done_reason": meta.get("done_reason"),
                "truncated": meta.get("truncated", False),
                "answer_chars": len(answer),
                "seconds": round(time.time() - t0, 2),
            })
            print(f"  {name} seed={seed}: probe={probe['total']}/4 judge={judge} "
                  f"trunc={meta['truncated']}")
        results["conditions"][name] = {"rows": rows}

    # ---- analysis ----------------------------------------------------------
    summary = {}
    for name, block in results["conditions"].items():
        trials = block["rows"]
        valid_trials = [t for t in trials if t.get("valid", False)]
        invalid_trials = [t for t in trials if not t.get("valid", False)]
        probes = [r["probe"]["total"] for r in valid_trials if r.get("probe")]
        judges = [r["judge"] for r in valid_trials if r.get("judge") is not None]
        truncated_count = sum(1 for r in trials if r.get("truncated", False))
        summary[name] = {
            "n": len(trials),
            "valid_count": len(valid_trials),
            "invalid_count": len(invalid_trials),
            "probe_mean": round(statistics.mean(probes), 3) if probes else None,
            "probe_ci95": [round(x, 3) for x in bootstrap_ci(probes)] if probes else None,
            "judge_mean": round(statistics.mean(judges), 3) if judges else None,
            "truncated_runs": truncated_count,
            "validity_status": "VALID" if len(valid_trials) > 0 else "INVALID_TRIAL",
        }
    results["summary"] = summary

    # Verdict logic
    min_valid = 2  # at least 2 valid trials per condition
    all_valid = all(
        results["summary"][c]["valid_count"] >= min_valid
        for c in results["conditions"]
    )
    any_truncated = any(
        results["summary"][c]["truncated_runs"] > 0
        for c in results["conditions"]
    )

    if any_truncated:
        verdict = "INVALID_RUN"
    elif not all_valid:
        verdict = "INVALID_RUN"
    else:
        # Check if there's a significant difference
        a = [r["probe"]["total"] for r in results["conditions"]["A_store_empty"]["rows"]
             if r.get("valid") and r.get("probe")]
        b = [r["probe"]["total"] for r in results["conditions"]["B_retrieved"]["rows"]
             if r.get("valid") and r.get("probe")]
        if a and b:
            u, p = mann_whitney_u(a, b)
            if p < 0.05:
                if statistics.mean(b) > statistics.mean(a):
                    verdict = "SUPPORTED"
                else:
                    verdict = "FALSIFIED"
            else:
                verdict = "INCONCLUSIVE"
        else:
            verdict = "INCONCLUSIVE"

    results["comparison"] = {
        "verdict": verdict,
        "min_valid_per_condition": min_valid,
        "all_conditions_valid": all_valid,
        "any_truncated": any_truncated,
    }

    a = [r["probe"]["total"] for r in results["conditions"]["A_store_empty"]["rows"]
         if r.get("valid") and r.get("probe")]
    b = [r["probe"]["total"] for r in results["conditions"]["B_retrieved"]["rows"]
         if r.get("valid") and r.get("probe")]
    if a and b:
        u, p = mann_whitney_u(a, b)
        results["test_store_empty_vs_retrieved"] = {
            "test": "Mann-Whitney U (two-sided, normal approximation)",
            "A_scores": a, "B_scores": b,
            "U": round(u, 3), "p": round(p, 4),
            "significant_at_0.05": bool(p < 0.05),
        }
    results["interpretation_limits"] = [
        "A significant result shows the STORE's content causally influenced output. "
        "It does NOT show phenomenological state.",
        "n is small; treat p as indicative.",
        "If any run is truncated (done_reason=length) its score is unreliable.",
        "MEASURE = keyword probe only. The LLM judge was RETIRED after three "
        "failed attempts to make qwen3:4b discriminate; see judge_score(). "
        "judge_* fields are null by design and must not be read as evidence.",
        "BASELINE DYNAMIC RANGE was verified before use: the probe scores 1.25/3 "
        "with no episode at all, and the discriminating sub-probe "
        "'non_independence' fires 0/4 at baseline. An earlier task scored 3.75/4 "
        "at baseline and was discarded as a ceiling.",
    ]
    return results


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--reps", type=int, default=7)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()

    print(f"Experiment 1.3 â€” state ablation (H1), reps={args.reps}")
    print("=" * 64)
    try:
        generate("ping", num_predict=2, seed=1)
    except RuntimeError as exc:
        print(f"FATAL: cannot reach Ollama at {OLLAMA_URL}: {exc}")
        return 2

    results = run(args.reps, args.dry_run)

    out = Path(args.out) if args.out else (
        Path(__file__).resolve().parent / "results" / "exp_1_3_results.json"
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")

    print("\nSUMMARY")
    for name, s in results["summary"].items():
        print(f"  {name:26s} probe={s['probe_mean']} ci95={s['probe_ci95']} "
              f"judge={s['judge_mean']} trunc={s['truncated_runs']}")
    if "test_store_empty_vs_retrieved" in results:
        t = results["test_store_empty_vs_retrieved"]
        print(f"\n  A(store empty) vs B(retrieved): U={t['U']} p={t['p']} "
              f"significant={t['significant_at_0.05']}")
    print(f"\nWritten: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
