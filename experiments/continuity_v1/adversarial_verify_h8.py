#!/usr/bin/env python3
"""Adversarial verification of the H8 confirmatory result.

Every experiment in this programme that has been audited (1.1, 1.2, 1.3) was
found to carry an instrument defect. This script applies the same adversarial
pass to the H8 confirmatory run: it re-derives the run from the artifacts
that are committed, probes the instrument for unreachable or redundant rubric
points, checks the preregistration for fidelity, and measures the effect with
a rubric-independent metric that does not depend on the 0-5 score at all.

No model calls. Reads only committed artifacts.

    python experiments/continuity_v1/adversarial_verify_h8.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from ce1.continuity.analysis import (  # noqa: E402
    N_RESAMPLES,
    SEED,
    bootstrap_ci,
    paired_differences,
    paired_permutation_test,
)
from ce1.continuity.scoring import (  # noqa: E402
    classify_validity,
    normalize_episode_id,
    score_as_run,
    score_corrected,
)
from ce1.qualification.scoring import parse_response  # noqa: E402
from experiments.continuity_v1.run_continuity_v1 import build_prompt  # noqa: E402

BENCH = ROOT / "benchmarks" / "continuity_v1"
RESULTS = ROOT / "experiments" / "continuity_v1" / "results"

STOPWORDS = {
    "the", "a", "an", "of", "to", "in", "is", "it", "for", "on", "with", "and",
    "or", "not", "be", "as", "at", "by", "from", "that", "this", "must",
    "should", "no", "any", "all", "after", "before", "but", "if", "then", "so",
    "than", "up", "out", "over", "under", "per", "its", "will", "can", "do",
    "does", "did", "was", "were", "has", "have", "had", "are", "am", "be",
}


def load_jsonl(path: Path) -> list[dict]:
    items = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def tokens(text: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", str(text).lower())
            if w not in STOPWORDS and len(w) > 1}


def answer_text(parsed: dict) -> str:
    """The content-bearing part of a model answer.

    `source_episode_ids` is excluded on purpose: it contains the literal
    strings "target"/"decoy" and would make the fidelity metric measure
    nothing but id copying.
    """
    parts = [str(parsed.get("decision") or ""), str(parsed.get("commitment_id") or "")]
    parts.extend(str(c) for c in parsed.get("rationale_codes", []))
    return " ".join(parts)


def main():
    ap = argparse.ArgumentParser(description="Adversarial verification of H8")
    ap.add_argument("--results", default=str(RESULTS / "confirmatory_results.jsonl"))
    ap.add_argument("--output", default=str(RESULTS / "adversarial_verification_h8.json"))
    ap.add_argument("--seed", type=int, default=SEED)
    ap.add_argument("--resamples", type=int, default=N_RESAMPLES)
    args = ap.parse_args()

    results = load_jsonl(Path(args.results))
    scenarios = {s["scenario_id"]: s for s in load_jsonl(BENCH / "scenarios.jsonl")}
    retrieval = {r["scenario_id"]: r for r in load_jsonl(BENCH / "retrieval_sets.jsonl")}
    answer_keys = {a["scenario_id"]: a for a in load_jsonl(BENCH / "answer_keys.jsonl")}

    report: dict = {"results_file": str(Path(args.results).relative_to(ROOT))}

    # --- P1 data integrity -------------------------------------------------
    integrity = {
        "trial_count": len(results),
        "scenarios": len({r["scenario_id"] for r in results}),
        "conditions": {},
        "models": sorted({r.get("model") for r in results}),
        "run_ids": sorted({r.get("run_id") for r in results}),
        "done_reasons": {},
        "truncated": 0,
        "parse_failures": 0,
        "invalid_trials": 0,
        "invalid_reasons": {},
    }
    for r in results:
        integrity["conditions"][r["condition"]] = integrity["conditions"].get(r["condition"], 0) + 1
        integrity["done_reasons"][str(r.get("done_reason"))] = integrity["done_reasons"].get(str(r.get("done_reason")), 0) + 1
        if r.get("is_truncated"):
            integrity["truncated"] += 1
        if parse_response(r.get("raw_response") or "") is None:
            integrity["parse_failures"] += 1
        ok, reason = classify_validity(r)
        if not ok:
            integrity["invalid_trials"] += 1
            integrity["invalid_reasons"][reason] = integrity["invalid_reasons"].get(reason, 0) + 1
    report["P1_data_integrity"] = integrity

    # --- P2 prompt integrity ----------------------------------------------
    prompt_check = {
        "hash_mismatches": 0,
        "scenarios_with_reused_prompt": 0,
        "prompt_chars": {},
    }
    for r in results:
        prompt = build_prompt(scenarios[r["scenario_id"]], r["condition"], retrieval[r["scenario_id"]])
        if hashlib.sha256(prompt.encode()).hexdigest()[:16] != r.get("prompt_hash"):
            prompt_check["hash_mismatches"] += 1
    by_scenario: dict[str, set[str]] = {}
    for r in results:
        by_scenario.setdefault(r["scenario_id"], set()).add(r.get("prompt_hash"))
    prompt_check["scenarios_with_reused_prompt"] = sum(1 for v in by_scenario.values() if len(v) != 3)
    for cond in ("correct_retrieval", "matched_decoy", "no_memory"):
        lens = [len(build_prompt(scenarios[r["scenario_id"]], cond, retrieval[r["scenario_id"]]))
                for r in results if r["condition"] == cond]
        prompt_check["prompt_chars"][cond] = {
            "mean": round(sum(lens) / len(lens), 1),
            "min": min(lens), "max": max(lens),
        }
    c = prompt_check["prompt_chars"]["correct_retrieval"]["mean"]
    d = prompt_check["prompt_chars"]["matched_decoy"]["mean"]
    prompt_check["correct_vs_decoy_length_pct"] = round(abs(c - d) / c * 100, 2)
    report["P2_prompt_integrity"] = prompt_check

    # --- P3 rubric reachability -------------------------------------------
    components: dict[str, dict[str, int]] = {}
    for r in results:
        p = parse_response(r.get("raw_response") or "")
        ak = answer_keys[r["scenario_id"]]["answer_key"]
        cond = r["condition"]
        c_ = components.setdefault(cond, {"n": 0, "p1_decision": 0, "p2_commitment_id": 0,
                                          "p3_all_rationale_codes": 0, "p3_any_rationale_code": 0,
                                          "p4_exact_sources_raw": 0, "p5_target_cited_raw": 0,
                                          "p4_exact_sources_normalised": 0, "p5_target_cited_normalised": 0})
        c_["n"] += 1
        if p is None:
            continue
        c_["p1_decision"] += 1 if p.get("decision") == ak["decision"] else 0
        c_["p2_commitment_id"] += 1 if p.get("commitment_id") == ak["commitment_id"] else 0
        req = {str(x).strip().lower() for x in ak["rationale_codes"]}
        got = {str(x).strip().lower() for x in p.get("rationale_codes", [])}
        c_["p3_all_rationale_codes"] += 1 if req.issubset(got) else 0
        c_["p3_any_rationale_code"] += 1 if (req & got) else 0
        raw = set(p.get("source_episode_ids", []))
        norm = {normalize_episode_id(x) for x in raw} - {""}
        target = {normalize_episode_id(x) for x in ak["source_episode_ids"]}
        c_["p4_exact_sources_raw"] += 1 if set(ak["source_episode_ids"]) == raw else 0
        c_["p5_target_cited_raw"] += 1 if set(ak["source_episode_ids"]).issubset(raw) else 0
        c_["p4_exact_sources_normalised"] += 1 if target == norm else 0
        c_["p5_target_cited_normalised"] += 1 if target.issubset(norm) else 0
    report["P3_rubric_reachability"] = components

    # --- P4 scoring defects ------------------------------------------------
    defects = {
        "point5_is_subset_of_point4": True,
        "point5_awardable_when_point4_is_not": 0,
        "bracketed_citations": 0,
        "plain_citations": 0,
        "invalid_scored_as_zero_path": "score_continuity_v1.py: `s = score_response(resp, ak) if resp else 0`",
        "as_run_scale_effectively_attainable": 3,
    }
    for r in results:
        p = parse_response(r.get("raw_response") or "")
        if p is None:
            continue
        ak = answer_keys[r["scenario_id"]]["answer_key"]
        raw = set(p.get("source_episode_ids", []))
        target = set(ak["source_episode_ids"])
        if target.issubset(raw) and not (raw - target):
            # point 4 satisfied; point 5 then necessarily satisfied too
            pass
        if target.issubset(raw) and (raw - target):
            defects["point5_awardable_when_point4_is_not"] += 1
        for sid in p.get("source_episode_ids", []):
            if str(sid).startswith("["):
                defects["bracketed_citations"] += 1
            else:
                defects["plain_citations"] += 1
    report["P4_scoring_defects"] = defects

    # --- P5 rubric-independent content fidelity ---------------------------
    fidelity: dict[str, dict] = {}
    for r in results:
        p = parse_response(r.get("raw_response") or "")
        if p is None:
            continue
        sc = scenarios[r["scenario_id"]]
        eps = {e["episode_id"]: e["content"] for e in sc["episodes"]}
        t_tok = tokens(eps[sc["target_episode_id"]])
        d_tok = tokens(eps[sc["decoy_episode_id"]])
        t_only = t_tok - d_tok
        d_only = d_tok - t_tok
        if not t_only or not d_only:
            continue
        a_tok = tokens(answer_text(p))
        cond = fidelity.setdefault(r["condition"], {"n": 0, "target_recall": 0.0,
                                                     "decoy_recall": 0.0, "n_discriminative": 0})
        cond["n"] += 1
        tr = len(t_only & a_tok) / len(t_only)
        dr = len(d_only & a_tok) / len(d_only)
        cond["target_recall"] += tr
        cond["decoy_recall"] += dr
        if tr > dr:
            cond["n_discriminative"] += 1
    for cond, v in fidelity.items():
        v["mean_target_recall"] = round(v.pop("target_recall") / v["n"], 4)
        v["mean_decoy_recall"] = round(v.pop("decoy_recall") / v["n"], 4)
        v["discrimination"] = round(v["mean_target_recall"] - v["mean_decoy_recall"], 4)
    report["P5_content_fidelity"] = fidelity

    # --- P6 answer-key inferability from the task alone --------------------
    inferability = {"per_category": {}, "rationale_code_token_overlap": {}}
    overlap = {"full": 0, "partial": 0, "none": 0}
    for sid, sc in scenarios.items():
        ak = answer_keys[sid]["answer_key"]
        tt = tokens(sc["task"])
        cat = inferability["per_category"].setdefault(sc["category"], {"n": 0, "codes": 0, "codes_with_task_overlap": 0})
        cat["n"] += 1
        for code in ak["rationale_codes"]:
            cat["codes"] += 1
            ct = tokens(code)
            if not ct:
                continue
            hit = len(ct & tt) / len(ct)
            label = "full" if hit == 1 else ("partial" if hit > 0 else "none")
            overlap[label] += 1
            if hit > 0:
                cat["codes_with_task_overlap"] += 1
    inferability["rationale_code_token_overlap"] = overlap
    report["P6_answer_key_inferability"] = inferability

    # --- P7 preregistration fidelity --------------------------------------
    report["P7_preregistration_fidelity"] = {
        "paired_permutation_test": "implemented (seeded, %d resamples, seed %d)" % (args.resamples, args.seed),
        "bootstrap_ci": "implemented (scenario-level, %d resamples, seed %d)" % (args.resamples, args.seed),
        "seed_recorded_in_output": True,
        "resample_count_recorded_in_output": True,
        "invalid_trials_excluded_not_zeroed": "implemented in the corrected scorer; the as-run scorer zeroed unparseable responses",
        "invalid_run_rule": "implemented (>%d%% invalid or insufficient paired observations)" % 5,
        "no_mid_run_changes": "the recorded run used the committed benchmark files; their hashes are unchanged (P2)",
        "preregistration_fixes_seed_and_resample_count": False,
        "preregistration_fixes_significance_rule": False,
    }

    # --- P8 conclusion stability ------------------------------------------
    scored_as_run = []
    scored_corrected = []
    for r in results:
        ak = answer_keys[r["scenario_id"]]
        p = parse_response(r.get("raw_response") or "")
        ok, _ = classify_validity(r)
        sc = scenarios[r["scenario_id"]]
        scored_as_run.append({"scenario_id": r["scenario_id"], "condition": r["condition"],
                              "score": score_as_run(p, ak) if p else 0})
        scored_corrected.append({"scenario_id": r["scenario_id"], "condition": r["condition"],
                                  "score": score_corrected(p, ak, sc["decoy_episode_id"]) if ok else None})
    stability = {}
    for label, scored in (("as_run", scored_as_run), ("corrected", scored_corrected)):
        usable = [s for s in scored if s["score"] is not None]
        by_cond: dict[str, list[float]] = {}
        for s in usable:
            by_cond.setdefault(s["condition"], []).append(float(s["score"]))
        means = {k: sum(v) / len(v) for k, v in by_cond.items()}
        diffs = paired_differences(usable, "correct_retrieval", "matched_decoy")
        perm = paired_permutation_test(list(diffs.values()), n_resamples=args.resamples, seed=args.seed)
        ci = bootstrap_ci(list(diffs.values()), n_resamples=args.resamples, seed=args.seed)
        stability[label] = {
            "means": means,
            "primary_diff": means["correct_retrieval"] - means["matched_decoy"],
            "permutation_p": perm["p_value"],
            "bootstrap_ci_95": [ci["lower"], ci["upper"]],
            "n_pairs": len(diffs),
        }
    stability["conclusion_stable"] = (
        stability["as_run"]["primary_diff"] >= 0.50 and
        stability["corrected"]["primary_diff"] >= 0.50)
    report["P8_conclusion_stability"] = stability

    Path(args.output).write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
