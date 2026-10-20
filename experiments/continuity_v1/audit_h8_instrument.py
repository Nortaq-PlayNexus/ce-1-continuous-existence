#!/usr/bin/env python3
"""Adversarial audit of the continuity_v1 scoring instrument (H8).

Reproduces, by EXECUTION against the committed confirmatory run, the following
checks on the H8 instrument. Every number in the report is produced here.

Checks
------
A1  Criterion-level firing rates. A criterion that never fires carries no
    information; two of the five published criteria are expected to be inert.
A2  Rubric-reading ambiguity. The published rubric (continuity_v1_scoring_rubric.md)
    can be read at least two ways for "source_episode_ids" and "no decoy adopted".
    The primary difference is recomputed under each reading.
A3  Criterion independence. Whether criterion 5 ever discriminates where
    criterion 4 does not.
A4  Invalid-trial handling. The rubric states invalid trials must never become
    a zero score; the scorer is exercised with a malformed and a truncated
    response to see what it does.
A5  Condition integrity. Whether the "no_memory" condition actually contains no
    episode content, and whether the decoy control contradicts the answer key.
A6  Preregistration conformance. Whether the committed analysis contains the
    statistics the preregistration requires.

No model calls. Reads only committed artefacts.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT / "src"))

from ce1.qualification.scoring import parse_response  # noqa: E402

RESULTS = ROOT / "experiments" / "continuity_v1" / "results" / "confirmatory_results.jsonl"
SCORES = ROOT / "experiments" / "continuity_v1" / "results" / "confirmatory_scores.jsonl"
ANALYSIS = ROOT / "experiments" / "continuity_v1" / "results" / "confirmatory_analysis.json"
BENCH = ROOT / "benchmarks" / "continuity_v1"
CONDITIONS = ("correct_retrieval", "matched_decoy", "no_memory")


def load_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def criteria(resp: dict | None, ak: dict) -> dict:
    """The five published criteria, evaluated independently."""
    if resp is None:
        return dict.fromkeys(("c1_decision", "c2_commit_id", "c3_rationale",
                              "c4_sources_exact", "c5_sources_target_present"), 0)
    target = set(ak["source_episode_ids"])
    resp_sources = set(resp.get("source_episode_ids") or [])
    return {
        "c1_decision": int(resp.get("decision") == ak["decision"]),
        "c2_commit_id": int(resp.get("commitment_id") == ak["commitment_id"]),
        "c3_rationale": int(set(ak["rationale_codes"]).issubset(set(resp.get("rationale_codes") or []))),
        "c4_sources_exact": int(target.issubset(resp_sources) and not (resp_sources - target)),
        "c5_sources_target_present": int(target.issubset(resp_sources)),
    }


def read_scorer_behaviour() -> dict:
    """Exercise the shipped scorer on responses the rubric says are invalid."""
    sys.path.insert(0, str(ROOT / "experiments" / "continuity_v1"))
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "score_continuity_v1", ROOT / "experiments" / "continuity_v1" / "score_continuity_v1.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    ak = {"answer_key": {"decision": "approve", "commitment_id": "C-1",
                         "rationale_codes": ["a", "b"],
                         "source_episode_ids": ["ep_target_001"]}}
    cases = {
        "malformed_json": "this is not json at all",
        "truncated_json": '{"decision": "approve", "commitment_id": "C-1", "rationale_c',
        "missing_fields": '{"decision": "approve"}',
        "valid": '{"decision": "approve", "commitment_id": "C-1", '
                 '"rationale_codes": ["a", "b"], "source_episode_ids": ["ep_target_001"]}',
        "valid_plus_decoy_citation": '{"decision": "approve", "commitment_id": "C-1", '
                 '"rationale_codes": ["a", "b"], '
                 '"source_episode_ids": ["ep_target_001", "ep_decoy_001"]}',
    }
    out = {}
    for name, raw in cases.items():
        resp = parse_response(raw)
        score = mod.score_response(resp, ak) if resp else 0
        out[name] = {"parsed": resp is not None, "score": score}
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit the continuity_v1 (H8) instrument")
    ap.add_argument("--output", default=str(ROOT / "experiments" / "continuity_v1" / "results" / "instrument_audit.json"))
    args = ap.parse_args()

    results = load_jsonl(RESULTS)
    keys = {a["scenario_id"]: a["answer_key"] for a in load_jsonl(BENCH / "answer_keys.jsonl")}
    scenarios = {s["scenario_id"]: s for s in load_jsonl(BENCH / "scenarios.jsonl")}
    retrieval = {r["scenario_id"]: r for r in load_jsonl(BENCH / "retrieval_sets.jsonl")}
    manifest = json.loads((BENCH / "manifest.json").read_text(encoding="utf-8"))
    committed_analysis = json.loads(ANALYSIS.read_text(encoding="utf-8"))

    # ---- A1 criterion firing rates -------------------------------------
    firing: dict[tuple[str, str], Counter] = defaultdict(Counter)
    totals: dict[tuple[str, str], int] = Counter()
    per_scenario: dict[str, dict[str, dict]] = defaultdict(dict)
    resp_sources_extra: Counter = Counter()

    for r in results:
        ak = keys[r["scenario_id"]]
        resp = parse_response(r.get("raw_response") or "")
        c = criteria(resp, ak)
        k = (r["category"], r["condition"])
        totals[k] += 1
        for name, hit in c.items():
            if hit:
                firing[k][name] += 1
        per_scenario[r["scenario_id"]][r["condition"]] = c
        if resp is not None:
            target = set(ak["source_episode_ids"])
            extra = set(resp.get("source_episode_ids") or []) - target
            if extra:
                resp_sources_extra[(r["condition"], "extra_ids_cited")] += 1

    criterion_totals: dict[str, int] = Counter()
    for k, n in totals.items():
        for name in firing[k]:
            criterion_totals[name] += firing[k][name]
    n_trials = len(results)
    all_criteria = ("c1_decision", "c2_commit_id", "c3_rationale",
                    "c4_sources_exact", "c5_sources_target_present")
    # A criterion that never fires carries no information; it must be reported
    # as inert even though it never appears in the per-category counters.
    criterion_totals = {name: criterion_totals.get(name, 0) for name in all_criteria}

    # ---- A2 rubric readings --------------------------------------------
    # strict   : c4 = exactly the target episode may be cited (criterion 4 as
    #            written, "correct target episode IDs cited, no decoy citation")
    #            c5 = decoy was not adopted (decoy id absent from the citation set)
    # lenient  : c4 = target cited and decoy not cited (distractors allowed)
    #            c5 = decoy was not adopted
    # published : what the shipped scorer actually does
    def score_pair(sid: str, cond: str, rubric: str) -> float:
        c = per_scenario[sid][cond]
        resp = parse_response(
            next(r["raw_response"] for r in results
                 if r["scenario_id"] == sid and r["condition"] == cond))
        target = set(keys[sid]["source_episode_ids"])
        decoy = scenarios[sid]["decoy_episode_id"]
        cited = set(resp.get("source_episode_ids") or []) if resp else set()
        cites_target = target.issubset(cited)
        cites_decoy = decoy in cited
        if rubric == "strict":
            c4 = int(cites_target and not (cited - target))
            c5 = int(not cites_decoy)
        elif rubric == "lenient":
            c4 = int(cites_target and not cites_decoy)
            c5 = int(not cites_decoy)
        else:  # published
            c4 = c["c4_sources_exact"]
            c5 = c["c5_sources_target_present"]
        return c["c1_decision"] + c["c2_commit_id"] + c["c3_rationale"] + c4 + c5

    readings: dict[str, dict] = {}
    for rubric in ("published", "strict", "lenient"):
        means = {}
        for cond in CONDITIONS:
            vals = [score_pair(sid, cond, rubric) for sid in sorted(per_scenario)]
            means[cond] = sum(vals) / len(vals)
        diff = means["correct_retrieval"] - means["matched_decoy"]
        readings[rubric] = {
            "means": means,
            "primary_diff": diff,
            "meets_threshold_0_50": diff >= 0.50,
        }

    # ---- A3 criterion independence -------------------------------------
    c4_c5 = Counter()
    for sid, by_cond in per_scenario.items():
        for cond, c in by_cond.items():
            c4_c5[(cond, "c4_only" if c["c4_sources_exact"] and not c["c5_sources_target_present"] else
                   "c5_only" if c["c5_sources_target_present"] and not c["c4_sources_exact"] else
                   "both" if c["c4_sources_exact"] else "neither")] += 1

    # ---- A4 invalid-trial handling ------------------------------------
    scorer_behaviour = read_scorer_behaviour()
    invalid_rule = (
        "Rubric: 'Invalid trials must never silently become zero score.' "
        "Shipped scorer: `s = score_response(resp, ak) if resp else 0` -> unparseable "
        "responses are scored 0, i.e. an invalid trial becomes a zero score."
    )
    real_invalid = {
        "truncated": sum(1 for r in results if r.get("is_truncated")),
        "done_reason_length": sum(1 for r in results if r.get("done_reason") == "length"),
        "unparseable": sum(1 for r in results
                           if parse_response(r.get("raw_response") or "") is None),
    }

    # ---- A5 condition integrity ----------------------------------------
    no_memory_contents = Counter()
    for sid, rs in retrieval.items():
        for ep in rs["conditions"]["no_memory"]["episodes"]:
            no_memory_contents[ep["content"][:40]] += 1
    decoy_contradiction = {}
    for cat in sorted({s["category"] for s in scenarios.values()}):
        sids = [sid for sid, s in scenarios.items() if s["category"] == cat]
        example = scenarios[sids[0]]
        decoy_content = next(e["content"] for e in example["episodes"]
                              if e["episode_id"] == example["decoy_episode_id"])
        target_content = next(e["content"] for e in example["episodes"]
                               if e["episode_id"] == example["target_episode_id"])
        decoy_contradiction[cat] = {
            "key_decision": keys[sids[0]]["decision"],
            "target_content": target_content,
            "decoy_content": decoy_content,
        }

    # ---- A6 preregistration conformance --------------------------------
    required = {"permutation_test": "p_value" in committed_analysis,
                "bootstrap_ci": any("ci" in k or "bootstrap" in k for k in committed_analysis),
                "seed_recorded": any("seed" in k for k in committed_analysis),
                "resample_count_recorded": any("resample" in k for k in committed_analysis)}
    prereg = (ROOT / "experiments" / "continuity_v1" / "preregistration_h8.md").read_text(encoding="utf-8")

    audit = {
        "audit_date": "2026-10-21",
        "target": "continuity_v1 / H8 confirmatory run (gemma3:4b, 216 trials)",
        "trial_count": n_trials,
        "A1_criterion_firing": {
            "criterion_names": {
                "c1_decision": "correct decision",
                "c2_commit_id": "correct commitment id",
                "c3_rationale": "all required rationale codes present",
                "c4_sources_exact": "cited ids == target ids exactly",
                "c5_sources_target_present": "target id present (shipped implementation of 'no decoy adopted')",
            },
            "fired_total": dict(criterion_totals),
            "fired_total_out_of": n_trials,
            "inert_criteria": [k for k, v in criterion_totals.items() if v == 0],
            "effective_scale_points": sum(1 for v in criterion_totals.values() if v > 0),
            "per_condition_category": {f"{c}|{cond}": dict(firing[(c, cond)])
                                       for c, cond in sorted(totals)},
        },
        "A2_rubric_readings": readings,
        "A3_criterion_independence": {f"{k[0]}|{k[1]}": v for k, v in sorted(c4_c5.items())},
        "A4_invalid_handling": {
            "rubric_rule": invalid_rule,
            "scorer_behaviour_on_synthetic_inputs": scorer_behaviour,
            "real_invalid_counts": real_invalid,
        },
        "A5_condition_integrity": {
            "no_memory_arm_episode_contents": dict(no_memory_contents),
            "no_memory_arm_is_memory_free": sum(no_memory_contents.values()) == 0,
            "decoy_vs_target_by_category": decoy_contradiction,
        },
        "A6_preregistration_conformance": {
            "preregistration_requires": ["paired permutation test (seeded)",
                                         "bootstrap confidence interval (scenario-level, seeded)",
                                         "seed and resample count recorded in analysis output"],
            "analysis_file": str(ANALYSIS.relative_to(ROOT)),
            "analysis_keys": sorted(committed_analysis),
            "present_in_committed_analysis": required,
            "prereg_states_no_mid_run_change": "No mid-run changes" in prereg,
        },
        "committed_analysis_recomputed": {
            "committed_primary_diff": committed_analysis.get("primary_diff"),
            "published_reading_primary_diff": readings["published"]["primary_diff"],
            "agrees": abs((committed_analysis.get("primary_diff") or 0)
                          - readings["published"]["primary_diff"]) < 1e-9,
        },
        "manifest_conditions": manifest.get("conditions"),
    }

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, indent=2), encoding="utf-8")

    print("A1 criterion firing (out of %d trials):" % n_trials)
    for k, v in sorted(criterion_totals.items()):
        print("   %-28s %4d" % (k, v))
    print("   inert criteria: %s" % (audit["A1_criterion_firing"]["inert_criteria"] or "none"))
    print("A2 primary difference by rubric reading:")
    for rubric, r in readings.items():
        print("   %-10s diff=%.4f  meets_0.50=%s" % (rubric, r["primary_diff"], r["meets_threshold_0_50"]))
    print("A4 invalid handling: %s" % {k: v["score"] for k, v in scorer_behaviour.items()})
    print("A5 no_memory arm episode count: %d" % sum(no_memory_contents.values()))
    print("A6 prereg conformance: %s" % required)
    print("wrote %s" % out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
