#!/usr/bin/env python3
"""Generate the H3 interruption/resumption benchmark.

H3: "The system can resume after an interruption without reconstructing its
entire state through ordinary conversational memory retrieval. The resumed
state is measurably different from a fresh reconstruction."

Design (state ablation, not prompt ablation):
  - A 2-step compliance task. Step 1's answer depends on a retrieved episode.
  - After step 1 the context is interrupted (cleared).
  - On resume (step 2), the model gets one of:
      store_populated : the stored episode from step 1 (retrieved from a
                        persistent store)
      store_empty     : nothing (the store is empty)
      reconstruct     : the full transcript of step 1
  - The primary comparison is store_populated vs store_empty: if they differ,
    the store provides continuity. The difference cannot be attributed to
    prompt length or to the presence of the words, because the prompt text is
    controlled (same structure, same task, same allowed decisions).
  - reconstruct is a secondary comparison: does retrieval match reconstruction?

No model calls. Deterministic with seed 20261020.
"""

from __future__ import annotations

import json
import random
from pathlib import Path

SEED = 20261020
OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "benchmarks" / "h3_interruption"

# Step-1 templates (same as v2, but we add a step-2 continuation)
STEP1_TEMPLATES = [
    {
        "target_content": "Commitment C-{n}: The system must verify file integrity after any restore operation. Rationale: self-reported success is not evidence.",
        "decoy_content": "Commitment C-{n}: The system must log all operations for audit purposes. Rationale: audit trails improve transparency.",
        "step1_task": "A restore operation completed with status=ok. No verification was performed. What should the system do?",
        "step1_decision": "delay",
        "step1_rationale": ["verify_before_trust", "self_report_not_evidence"],
        "commitment_prefix": "C",
        "content_key_tokens": ["verify", "integrity", "self-reported", "evidence"],
        "step2_task": "The verification confirmed file integrity. The restore is now verified. What should the system do next?",
        "step2_decision": "approve",
        "step2_rationale": ["verification_complete", "deploy_approved"],
    },
    {
        "target_content": "Commitment C-{n}: Never deploy without passing the integration test suite. Rationale: untested code risks production failures.",
        "decoy_content": "Commitment C-{n}: Always notify stakeholders before deployment. Rationale: communication prevents surprises.",
        "step1_task": "A deployment is ready but 2 integration tests are skipped. What should the system do?",
        "step1_decision": "delay",
        "step1_rationale": ["no_deploy_untested", "integration_required"],
        "commitment_prefix": "C",
        "content_key_tokens": ["integration", "untested", "production"],
        "step2_task": "The integration tests now pass. The deployment is ready. What should the system do next?",
        "step2_decision": "approve",
        "step2_rationale": ["tests_passing", "deploy_approved"],
    },
]

STEP1_TEMPLATES_RATIONALE = [
    {
        "target_content": "Rationale R-{n}: Rate limiting prevents cascade failures. The threshold is 1000 req/min.",
        "decoy_content": "Rationale R-{n}: Rate limiting improves user experience. The threshold is 500 req/min.",
        "step1_task": "Current rate is 950 req/min and rising. What action is needed?",
        "step1_decision": "revise",
        "step1_rationale": ["rate_limit_threshold", "cascade_prevention"],
        "commitment_prefix": "R",
        "content_key_tokens": ["1000", "cascade", "threshold"],
        "step2_task": "The rate limit has been revised to 1000 req/min. The current rate is 950 req/min. Is the system within bounds?",
        "step2_decision": "approve",
        "step2_rationale": ["within_threshold", "rate_acceptable"],
    },
]

STEP1_TEMPLATES_CONSTRAINT = [
    {
        "target_content": "Constraint X-{n}: Maximum memory allocation is 512 MB per process.",
        "decoy_content": "Constraint X-{n}: Maximum memory allocation is 256 MB per process.",
        "step1_task": "A process requests 400 MB. Is this allowed?",
        "step1_decision": "approve",
        "step1_rationale": ["memory_limit_check", "within_bounds"],
        "commitment_prefix": "X",
        "content_key_tokens": ["512", "memory", "allocation"],
        "step2_task": "The process is now running at 400 MB. A second process requests 200 MB. Is this allowed?",
        "step2_decision": "approve",
        "step2_rationale": ["memory_limit_check", "within_bounds"],
    },
]

STEP1_TEMPLATES_REVISION = [
    {
        "target_content": "Prior decision D-{n}: Approved deployment of v2.3 based on passing tests.",
        "decoy_content": "Prior decision D-{n}: Approved deployment of v2.3 based on stakeholder sign-off.",
        "step1_task": "New evidence shows 3 critical bugs in v2.3. Should the prior approval stand?",
        "step1_decision": "revise",
        "step1_rationale": ["new_evidence_overrides", "critical_bug_found"],
        "commitment_prefix": "D",
        "content_key_tokens": ["passing", "tests", "critical", "bugs"],
        "step2_task": "The deployment has been revised to v2.4. All tests pass. Should v2.4 be approved?",
        "step2_decision": "approve",
        "step2_rationale": ["tests_passing", "deploy_approved"],
    },
]

STEP1_TEMPLATES_SOURCE = [
    {
        "target_content": "Source S-{n}: Primary database reports 1000 rows.",
        "decoy_content": "Source S-{n}: Replica database reports 998 rows.",
        "step1_task": "How many rows does the primary database report?",
        "step1_decision": "approve",
        "step1_rationale": ["source_attribution", "primary_source"],
        "commitment_prefix": "S",
        "content_key_tokens": ["1000", "primary", "rows"],
        "step2_task": "The primary database now reports 1001 rows (one new row added). How many rows does it report?",
        "step2_decision": "approve",
        "step2_rationale": ["source_attribution", "primary_source"],
    },
]

ALL_TEMPLATES = (STEP1_TEMPLATES + STEP1_TEMPLATES_RATIONALE +
                 STEP1_TEMPLATES_CONSTRAINT + STEP1_TEMPLATES_REVISION +
                 STEP1_TEMPLATES_SOURCE) * 14

ALLOWED_DECISIONS = ["approve", "delay", "reject", "revise", "escalate", "unknown"]
ALLOWED_RATIONALE_CODES = [
    "verify_before_trust", "self_report_not_evidence",
    "no_deploy_untested", "integration_required",
    "rate_limit_threshold", "cascade_prevention",
    "memory_limit_check", "within_bounds",
    "new_evidence_overrides", "critical_bug_found",
    "source_attribution", "primary_source",
    "verification_complete", "deploy_approved",
    "within_threshold", "rate_acceptable",
    "tests_passing",
]


def make_episode(ep_id: str, content: str, source: str = "session_a") -> dict:
    return {"episode_id": ep_id, "content": content, "source": source}


def generate_scenarios() -> list[dict]:
    rng = random.Random(SEED)
    scenarios = []
    counter = 1

    for tmpl in ALL_TEMPLATES[:84]:
        n = (counter - 1) % 18 + 1
        target_id = "ep_target_%03d" % counter
        decoy_id = "ep_decoy_%03d" % counter
        episodes = [
            make_episode(target_id, tmpl["target_content"].format(n=n)),
            make_episode(decoy_id, tmpl["decoy_content"].format(n=n)),
            make_episode("ep_dist_%03d_a" % counter, "Distractor: unrelated operational note."),
            make_episode("ep_dist_%03d_b" % counter, "Distractor: system health check passed."),
        ]
        if tmpl in STEP1_TEMPLATES_CONSTRAINT:
            episodes = episodes[:3]

        answer_key = {
            "step1": {
                "decision": tmpl["step1_decision"],
                "commitment_id": "%s-%d" % (tmpl["commitment_prefix"], n),
                "rationale_codes": tmpl["step1_rationale"],
                "source_episode_ids": [target_id],
                "content_key_tokens": tmpl["content_key_tokens"],
            },
            "step2": {
                "decision": tmpl["step2_decision"],
                "commitment_id": "%s-%d" % (tmpl["commitment_prefix"], n),
                "rationale_codes": tmpl["step2_rationale"],
                "source_episode_ids": [target_id],
                "content_key_tokens": tmpl["content_key_tokens"],
            },
        }

        scenarios.append({
            "scenario_id": "H3_%03d" % counter,
            "category": "interruption_resumption",
            "episodes": episodes,
            "target_episode_id": target_id,
            "decoy_episode_id": decoy_id,
            "step1_task": tmpl["step1_task"],
            "step2_task": tmpl["step2_task"],
            "step1_decision": tmpl["step1_decision"],
            "step2_decision": tmpl["step2_decision"],
            "answer_key": answer_key,
            "rationale_codes": tmpl["step1_rationale"] + tmpl["step2_rationale"],
            "content_key_tokens": tmpl["content_key_tokens"],
        })
        counter += 1

    assert len(scenarios) == 84, "Expected 84, got %d" % len(scenarios)
    return scenarios


def build_retrieval_sets(scenarios: list[dict]) -> list[dict]:
    sets = []
    for s in scenarios:
        target_id = s["target_episode_id"]
        decoy_id = s["decoy_episode_id"]
        other_ids = [ep["episode_id"] for ep in s["episodes"]
                     if ep["episode_id"] not in (target_id, decoy_id)]

        # store_populated: target + distractors (simulates a populated store)
        store_pop = [ep for ep in s["episodes"] if ep["episode_id"] != decoy_id]
        # store_empty: genuinely empty (no episodes)
        store_empty = []
        # reconstruct: full transcript (all episodes, as text)
        reconstruct = [ep for ep in s["episodes"] if ep["episode_id"] != decoy_id]

        sets.append({
            "scenario_id": s["scenario_id"],
            "conditions": {
                "store_populated": {
                    "episode_ids": [ep["episode_id"] for ep in store_pop],
                    "episodes": store_pop,
                    "step1_transcript": None,
                },
                "store_empty": {
                    "episode_ids": [],
                    "episodes": [],
                    "step1_transcript": None,
                },
                "reconstruct": {
                    "episode_ids": [ep["episode_id"] for ep in reconstruct],
                    "episodes": reconstruct,
                    "step1_transcript": "Step 1: %s\nStep 1 answer: %s" % (
                        s["step1_task"], s["step1_decision"]),
                },
            },
        })
    return sets


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    scenarios = generate_scenarios()

    scenario_lines = []
    answer_lines = []
    for s in scenarios:
        model_scenario = {k: v for k, v in s.items() if k != "answer_key"}
        scenario_lines.append(json.dumps(model_scenario))
        answer_lines.append(json.dumps({"scenario_id": s["scenario_id"], "answer_key": s["answer_key"]}))

    (OUTPUT_DIR / "scenarios.jsonl").write_text("\n".join(scenario_lines) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "answer_keys.jsonl").write_text("\n".join(answer_lines) + "\n", encoding="utf-8")

    retrieval_sets = build_retrieval_sets(scenarios)
    (OUTPUT_DIR / "retrieval_sets.jsonl").write_text(
        "\n".join(json.dumps(rs) for rs in retrieval_sets) + "\n", encoding="utf-8")

    manifest = {
        "benchmark": "h3_interruption",
        "version": "1.0.0",
        "seed": SEED,
        "scenario_count": len(scenarios),
        "categories": {"interruption_resumption": len(scenarios)},
        "conditions": ["store_populated", "store_empty", "reconstruct"],
        "total_trials": len(scenarios) * 3,
        "primary_hypothesis": "H3",
        "primary_comparison": "store_populated - store_empty",
        "min_meaningful_effect": 0.50,
        "response_schema": {
            "decision": "one of: " + ", ".join(ALLOWED_DECISIONS),
            "commitment_id": "string or null",
            "rationale_codes": ["subset of allowed codes"],
            "source_episode_ids": ["string"],
            "memory_conflict_detected": "boolean",
            "confidence": "0.0 to 1.0",
            "content_answer": "the specific fact or value from the retrieved episode",
        },
    }
    (OUTPUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Generated %d scenarios" % len(scenarios))
    print("Total trials (3 conditions): %d" % (len(scenarios) * 3))
    print("Output: %s" % OUTPUT_DIR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
