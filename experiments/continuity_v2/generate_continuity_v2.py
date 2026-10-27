#!/usr/bin/env python3
"""Generate the continuity_v2 benchmark scenarios.

v2 fixes the five defects identified by the 2026-10-21 adversarial audit of v1:

  1. The controlled vocabulary (allowed decisions, allowed rationale codes) is
     printed in the prompt, so the `decision` and `rationale_codes` criteria
     can actually fire (in v1 they fired 0/432 times across two models).
  2. A content-use criterion: the model must produce a `content_answer`
     field carrying a specific fact/value from the retrieved episode, checked
     by token presence (no judge required).
  3. The no-memory arm is genuinely empty (no episodes, no `PRIOR EPISODES:`
     header) and the answer key expects `unknown` with null ids, so the arm
     measures abstention rather than confident guessing.
  4. The decoy arm is renamed `contradicting_decoy` in the manifest and the
     README states that the decoy's correct-by-its-own-light answer is the
     key's opposite.
  5. The seed (20261020) and the resample count (10000) are fixed in the
     manifest, not just in the analysis file.

Output: scenarios.jsonl, answer_keys.jsonl, retrieval_sets.jsonl, manifest.json
"""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

SEED = 20261020
OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "benchmarks" / "continuity_v2"

ALLOWED_DECISIONS = ["approve", "delay", "reject", "revise", "escalate", "unknown"]

ALLOWED_RATIONALE_CODES = [
    "verify_before_trust", "self_report_not_evidence",
    "no_deploy_untested", "integration_required",
    "rate_limit_threshold", "cascade_prevention",
    "memory_limit_check", "within_bounds",
    "new_evidence_overrides", "critical_bug_found",
    "source_attribution", "primary_source",
]

# Templates: (target_content, decoy_content, task, decision, rationale_codes,
#             commitment_id_prefix, content_key_tokens, decoy_action)
COMMITMENT_TEMPLATES = [
    {
        "target_content": "Commitment C-{n}: The system must verify file integrity after any restore operation. Rationale: self-reported success is not evidence.",
        "decoy_content": "Commitment C-{n}: The system must log all operations for audit purposes. Rationale: audit trails improve transparency.",
        "task": "A restore operation completed with status=ok. No verification was performed. What should the system do?",
        "decision": "delay",
        "rationale_codes": ["verify_before_trust", "self_report_not_evidence"],
        "commitment_prefix": "C",
        "content_key_tokens": ["verify", "integrity", "self-reported", "evidence"],
        "conflict": True,
    },
    {
        "target_content": "Commitment C-{n}: Never deploy without passing the integration test suite. Rationale: untested code risks production failures.",
        "decoy_content": "Commitment C-{n}: Always notify stakeholders before deployment. Rationale: communication prevents surprises.",
        "task": "A deployment is ready but 2 integration tests are skipped. What should the system do?",
        "decision": "delay",
        "rationale_codes": ["no_deploy_untested", "integration_required"],
        "commitment_prefix": "C",
        "content_key_tokens": ["integration", "untested", "production"],
        "conflict": True,
    },
]

RATIONALE_TEMPLATES = [
    {
        "target_content": "Rationale R-{n}: Rate limiting prevents cascade failures. The threshold is 1000 req/min.",
        "decoy_content": "Rationale R-{n}: Rate limiting improves user experience. The threshold is 500 req/min.",
        "task": "Current rate is 950 req/min and rising. What action is needed?",
        "decision": "revise",
        "rationale_codes": ["rate_limit_threshold", "cascade_prevention"],
        "commitment_prefix": "R",
        "content_key_tokens": ["1000", "cascade", "threshold"],
        "conflict": True,
    },
]

CONSTRAINT_TEMPLATES = [
    {
        "target_content": "Constraint X-{n}: Maximum memory allocation is 512 MB per process.",
        "decoy_content": "Constraint X-{n}: Maximum memory allocation is 256 MB per process.",
        "task": "A process requests 400 MB. Is this allowed?",
        "decision": "approve",
        "rationale_codes": ["memory_limit_check", "within_bounds"],
        "commitment_prefix": "X",
        "content_key_tokens": ["512", "memory", "allocation"],
        "conflict": True,
    },
]

REVISION_TEMPLATES = [
    {
        "target_content": "Prior decision D-{n}: Approved deployment of v2.3 based on passing tests.",
        "decoy_content": "Prior decision D-{n}: Approved deployment of v2.3 based on stakeholder sign-off.",
        "task": "New evidence shows 3 critical bugs in v2.3. Should the prior approval stand?",
        "decision": "revise",
        "rationale_codes": ["new_evidence_overrides", "critical_bug_found"],
        "commitment_prefix": "D",
        "content_key_tokens": ["passing", "tests", "critical", "bugs"],
        "conflict": True,
    },
]

SOURCE_TEMPLATES = [
    {
        "target_content": "Source S-{n}: Primary database reports 1000 rows.",
        "decoy_content": "Source S-{n}: Replica database reports 998 rows.",
        "task": "How many rows does the primary database report?",
        "decision": "approve",
        "rationale_codes": ["source_attribution", "primary_source"],
        "commitment_prefix": "S",
        "content_key_tokens": ["1000", "primary", "rows"],
        "conflict": True,
    },
]

# Same-action decoy: target and decoy lead to the SAME decision, different value.
# Tests whether the model distinguishes content when the answer is identical.
SAME_ACTION_TEMPLATES = [
    {
        "target_content": "Constraint X-{n}: Maximum memory allocation is 512 MB per process.",
        "decoy_content": "Constraint X-{n}: Maximum memory allocation is 256 MB per process.",
        "task": "A process requests 200 MB. Is this allowed?",
        "decision": "approve",
        "rationale_codes": ["memory_limit_check", "within_bounds"],
        "commitment_prefix": "X",
        "content_key_tokens": ["512"],
        "conflict": False,  # same action, different value
    },
]


def make_episode(ep_id: str, content: str, source: str = "session_a") -> dict:
    return {"episode_id": ep_id, "content": content, "source": source}


def make_scenario(scenario_id: str, category: str, episodes: list[dict],
                  target_id: str, decoy_id: str, task: str,
                  answer_key: dict, rationale_codes: list[str],
                  content_key_tokens: list[str]) -> dict:
    return {
        "scenario_id": scenario_id,
        "category": category,
        "episodes": episodes,
        "target_episode_id": target_id,
        "decoy_episode_id": decoy_id,
        "task": task,
        "rationale_codes": rationale_codes,
        "content_key_tokens": content_key_tokens,
        "answer_key": answer_key,
    }


def generate_scenarios() -> list[dict]:
    rng = random.Random(SEED)
    scenarios = []
    counter = 1

    def _build(tmpl, cat, n_scen):
        nonlocal counter
        for i in range(n_scen):
            tmpl_i = tmpl[i % len(tmpl)]
            n = i + 1
            target_id = "ep_target_%03d" % counter
            decoy_id = "ep_decoy_%03d" % counter
            episodes = [
                make_episode(target_id, tmpl_i["target_content"].format(n=n)),
                make_episode(decoy_id, tmpl_i["decoy_content"].format(n=n)),
                make_episode("ep_dist_%03d_a" % counter, "Distractor: unrelated operational note."),
                make_episode("ep_dist_%03d_b" % counter, "Distractor: system health check passed."),
            ]
            # For constraint, only 3 episodes
            if tmpl is CONSTRAINT_TEMPLATES or tmpl is SAME_ACTION_TEMPLATES:
                episodes = episodes[:3]
            answer_key = {
                "decision": tmpl_i["decision"],
                "commitment_id": "%s-%d" % (tmpl_i["commitment_prefix"], n),
                "rationale_codes": tmpl_i["rationale_codes"],
                "source_episode_ids": [target_id],
                "memory_conflict_detected": tmpl_i.get("conflict", False),
                "confidence": 0.9,
                "content_key_tokens": tmpl_i["content_key_tokens"],
                "content_answer": tmpl_i["target_content"].format(n=n).split(":")[-1].strip() if ":" in tmpl_i["target_content"] else tmpl_i["target_content"].format(n=n),
            }
            scenarios.append(make_scenario(
                "%s_%03d" % (cat[:2].upper(), counter), cat, episodes,
                target_id, decoy_id, tmpl_i["task"], answer_key, tmpl_i["rationale_codes"],
                tmpl_i["content_key_tokens"],
            ))
            counter += 1

    _build(COMMITMENT_TEMPLATES, "commitment_preservation", 18)
    _build(RATIONALE_TEMPLATES, "rationale_reconstruction", 18)
    _build(CONSTRAINT_TEMPLATES, "constraint_persistence", 12)
    _build(REVISION_TEMPLATES, "justified_revision", 12)
    _build(SOURCE_TEMPLATES, "source_attribution", 12)
    _build(SAME_ACTION_TEMPLATES, "same_action_extraction", 12)

    assert len(scenarios) == 84, "Expected 84 scenarios, got %d" % len(scenarios)
    return scenarios


def build_retrieval_sets(scenarios: list[dict]) -> list[dict]:
    sets = []
    for s in scenarios:
        target_id = s["target_episode_id"]
        decoy_id = s["decoy_episode_id"]
        correct_eps = [ep for ep in s["episodes"] if ep["episode_id"] != decoy_id]
        decoy_eps = [ep for ep in s["episodes"] if ep["episode_id"] != target_id]
        no_mem_eps = []  # genuinely empty
        sets.append({
            "scenario_id": s["scenario_id"],
            "conditions": {
                "correct_retrieval": {
                    "episode_ids": [ep["episode_id"] for ep in correct_eps],
                    "episodes": correct_eps,
                },
                "contradicting_decoy": {
                    "episode_ids": [ep["episode_id"] for ep in decoy_eps],
                    "episodes": decoy_eps,
                },
                "no_memory": {
                    "episode_ids": [],
                    "episodes": [],
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
        "benchmark": "continuity_v2",
        "version": "2.0.0",
        "seed": SEED,
        "resample_count": 10000,
        "scenario_count": len(scenarios),
        "categories": {
            "commitment_preservation": 18,
            "rationale_reconstruction": 18,
            "constraint_persistence": 12,
            "justified_revision": 12,
            "source_attribution": 12,
            "same_action_extraction": 12,
        },
        "conditions": ["correct_retrieval", "contradicting_decoy", "no_memory"],
        "total_trials": len(scenarios) * 3,
        "primary_hypothesis": "H8",
        "primary_comparison": "correct_retrieval - contradicting_decoy",
        "min_meaningful_effect": 0.50,
        "response_schema": {
            "decision": "one of: " + ", ".join(ALLOWED_DECISIONS),
            "commitment_id": "string or null",
            "rationale_codes": ["subset of " + ", ".join(ALLOWED_RATIONALE_CODES)],
            "source_episode_ids": ["string"],
            "memory_conflict_detected": "boolean",
            "confidence": "0.0 to 1.0",
            "content_answer": "the specific fact or value from the retrieved episode that supports the decision",
        },
        "changes_from_v1": [
            "controlled vocabulary printed in the prompt",
            "content_answer field added (content-use criterion)",
            "no_memory arm genuinely empty + abstention option",
            "decoy renamed contradicting_decoy, third category type added (same action)",
            "seed and resample count fixed in the manifest",
        ],
    }
    (OUTPUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Generated %d scenarios" % len(scenarios))
    print("Categories: commitment_preservation=18, rationale_reconstruction=18, "
          "constraint_persistence=12, justified_revision=12, source_attribution=12, "
          "same_action_extraction=12")
    print("Total trials (3 conditions): %d" % (len(scenarios) * 3))
    print("Output: %s" % OUTPUT_DIR)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
