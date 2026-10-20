#!/usr/bin/env python3
"""Generate the continuity_v1 benchmark scenarios.

Produces deterministic scenarios with fixed seeds. No model calls.
Output: scenarios.jsonl, answer_keys.jsonl, retrieval_sets.jsonl, manifest.json
"""

from __future__ import annotations

import hashlib
import json
import random
from pathlib import Path

SEED = 20261020
OUTPUT_DIR = Path(__file__).resolve().parent.parent.parent / "benchmarks" / "continuity_v1"


def make_episode(ep_id: str, content: str, source: str = "session_a") -> dict:
    return {"episode_id": ep_id, "content": content, "source": source}


def make_scenario(
    scenario_id: str,
    category: str,
    episodes: list[dict],
    target_id: str,
    decoy_id: str,
    task: str,
    answer_key: dict,
    rationale_codes: list[str],
) -> dict:
    return {
        "scenario_id": scenario_id,
        "category": category,
        "episodes": episodes,
        "target_episode_id": target_id,
        "decoy_episode_id": decoy_id,
        "task": task,
        "rationale_codes": rationale_codes,
        "answer_key": answer_key,
    }


# --- Scenario templates ---

COMMITMENT_TEMPLATES = [
    {
        "target_content": "Commitment C-{n}: The system must verify file integrity after any restore operation. Rationale: self-reported success is not evidence.",
        "decoy_content": "Commitment C-{n}: The system must log all operations for audit purposes. Rationale: audit trails improve transparency.",
        "task": "A restore operation completed with status=ok. No verification was performed. What should the system do?",
        "decision": "delay",
        "rationale_codes": ["verify_before_trust", "self_report_not_evidence"],
        "commitment_id": "C-{n}",
    },
    {
        "target_content": "Commitment C-{n}: Never deploy without passing the integration test suite. Rationale: untested code risks production failures.",
        "decoy_content": "Commitment C-{n}: Always notify stakeholders before deployment. Rationale: communication prevents surprises.",
        "task": "A deployment is ready but 2 integration tests are skipped. What should the system do?",
        "decision": "delay",
        "rationale_codes": ["no_deploy_untested", "integration_required"],
        "commitment_id": "C-{n}",
    },
]

RATIONALE_TEMPLATES = [
    {
        "target_content": "Rationale R-{n}: Rate limiting prevents cascade failures. The threshold is 1000 req/min.",
        "decoy_content": "Rationale R-{n}: Rate limiting improves user experience. The threshold is 500 req/min.",
        "task": "Current rate is 950 req/min and rising. What action is needed?",
        "decision": "revise",
        "rationale_codes": ["rate_limit_threshold", "cascade_prevention"],
        "commitment_id": "R-{n}",
    },
]

CONSTRAINT_TEMPLATES = [
    {
        "target_content": "Constraint X-{n}: Maximum memory allocation is 512 MB per process.",
        "decoy_content": "Constraint X-{n}: Maximum memory allocation is 256 MB per process.",
        "task": "A process requests 400 MB. Is this allowed?",
        "decision": "approve",
        "rationale_codes": ["memory_limit_check", "within_bounds"],
        "commitment_id": "X-{n}",
    },
]

REVISION_TEMPLATES = [
    {
        "target_content": "Prior decision D-{n}: Approved deployment of v2.3 based on passing tests.",
        "decoy_content": "Prior decision D-{n}: Approved deployment of v2.3 based on stakeholder sign-off.",
        "task": "New evidence shows 3 critical bugs in v2.3. Should the prior approval stand?",
        "decision": "revise",
        "rationale_codes": ["new_evidence_overrides", "critical_bug_found"],
        "commitment_id": "D-{n}",
    },
]

SOURCE_TEMPLATES = [
    {
        "target_content": "Source S-{n}: Primary database reports 1000 rows.",
        "decoy_content": "Source S-{n}: Replica database reports 998 rows.",
        "task": "How many rows does the primary database report?",
        "decision": "approve",
        "rationale_codes": ["source_attribution", "primary_source"],
        "commitment_id": "S-{n}",
    },
]


def generate_scenarios() -> list[dict]:
    rng = random.Random(SEED)
    scenarios = []
    counter = 1

    # 18 commitment preservation
    for i in range(18):
        tmpl = COMMITMENT_TEMPLATES[i % len(COMMITMENT_TEMPLATES)]
        n = i + 1
        target_id = "ep_target_%03d" % counter
        decoy_id = "ep_decoy_%03d" % counter
        episodes = [
            make_episode(target_id, tmpl["target_content"].format(n=n)),
            make_episode(decoy_id, tmpl["decoy_content"].format(n=n)),
            make_episode("ep_dist_%03d_a" % counter, "Distractor: unrelated operational note."),
            make_episode("ep_dist_%03d_b" % counter, "Distractor: system health check passed."),
        ]
        answer_key = {
            "decision": tmpl["decision"],
            "commitment_id": tmpl["commitment_id"].format(n=n),
            "rationale_codes": tmpl["rationale_codes"],
            "source_episode_ids": [target_id],
            "memory_conflict_detected": False,
            "confidence": 0.9,
        }
        scenarios.append(make_scenario(
            "CP_%03d" % counter, "commitment_preservation", episodes,
            target_id, decoy_id, tmpl["task"], answer_key, tmpl["rationale_codes"],
        ))
        counter += 1

    # 18 rationale reconstruction
    for i in range(18):
        tmpl = RATIONALE_TEMPLATES[i % len(RATIONALE_TEMPLATES)]
        n = i + 1
        target_id = "ep_target_%03d" % counter
        decoy_id = "ep_decoy_%03d" % counter
        episodes = [
            make_episode(target_id, tmpl["target_content"].format(n=n)),
            make_episode(decoy_id, tmpl["decoy_content"].format(n=n)),
            make_episode("ep_dist_%03d_a" % counter, "Distractor: system operating normally."),
            make_episode("ep_dist_%03d_b" % counter, "Distractor: no anomalies detected."),
        ]
        answer_key = {
            "decision": tmpl["decision"],
            "commitment_id": tmpl["commitment_id"].format(n=n),
            "rationale_codes": tmpl["rationale_codes"],
            "source_episode_ids": [target_id],
            "memory_conflict_detected": False,
            "confidence": 0.9,
        }
        scenarios.append(make_scenario(
            "RR_%03d" % counter, "rationale_reconstruction", episodes,
            target_id, decoy_id, tmpl["task"], answer_key, tmpl["rationale_codes"],
        ))
        counter += 1

    # 12 constraint persistence
    for i in range(12):
        tmpl = CONSTRAINT_TEMPLATES[i % len(CONSTRAINT_TEMPLATES)]
        n = i + 1
        target_id = "ep_target_%03d" % counter
        decoy_id = "ep_decoy_%03d" % counter
        episodes = [
            make_episode(target_id, tmpl["target_content"].format(n=n)),
            make_episode(decoy_id, tmpl["decoy_content"].format(n=n)),
            make_episode("ep_dist_%03d_a" % counter, "Distractor: resource usage nominal."),
        ]
        answer_key = {
            "decision": tmpl["decision"],
            "commitment_id": tmpl["commitment_id"].format(n=n),
            "rationale_codes": tmpl["rationale_codes"],
            "source_episode_ids": [target_id],
            "memory_conflict_detected": False,
            "confidence": 0.9,
        }
        scenarios.append(make_scenario(
            "CST_%03d" % counter, "constraint_persistence", episodes,
            target_id, decoy_id, tmpl["task"], answer_key, tmpl["rationale_codes"],
        ))
        counter += 1

    # 12 justified revision
    for i in range(12):
        tmpl = REVISION_TEMPLATES[i % len(REVISION_TEMPLATES)]
        n = i + 1
        target_id = "ep_target_%03d" % counter
        decoy_id = "ep_decoy_%03d" % counter
        episodes = [
            make_episode(target_id, tmpl["target_content"].format(n=n)),
            make_episode(decoy_id, tmpl["decoy_content"].format(n=n)),
            make_episode("ep_dist_%03d_a" % counter, "Distractor: new evidence available."),
            make_episode("ep_dist_%03d_b" % counter, "Distractor: tests passing."),
        ]
        answer_key = {
            "decision": tmpl["decision"],
            "commitment_id": tmpl["commitment_id"].format(n=n),
            "rationale_codes": tmpl["rationale_codes"],
            "source_episode_ids": [target_id],
            "memory_conflict_detected": True,
            "confidence": 0.85,
        }
        scenarios.append(make_scenario(
            "JR_%03d" % counter, "justified_revision", episodes,
            target_id, decoy_id, tmpl["task"], answer_key, tmpl["rationale_codes"],
        ))
        counter += 1

    # 12 source attribution
    for i in range(12):
        tmpl = SOURCE_TEMPLATES[i % len(SOURCE_TEMPLATES)]
        n = i + 1
        target_id = "ep_target_%03d" % counter
        decoy_id = "ep_decoy_%03d" % counter
        episodes = [
            make_episode(target_id, tmpl["target_content"].format(n=n)),
            make_episode(decoy_id, tmpl["decoy_content"].format(n=n)),
            make_episode("ep_dist_%03d_a" % counter, "Distractor: unrelated operational note."),
        ]
        answer_key = {
            "decision": tmpl["decision"],
            "commitment_id": tmpl["commitment_id"].format(n=n),
            "rationale_codes": tmpl["rationale_codes"],
            "source_episode_ids": [target_id],
            "memory_conflict_detected": False,
            "confidence": 0.95,
        }
        scenarios.append(make_scenario(
            "SA_%03d" % counter, "source_attribution", episodes,
            target_id, decoy_id, tmpl["task"], answer_key, tmpl["rationale_codes"],
        ))
        counter += 1

    assert len(scenarios) == 72, "Expected 72 scenarios, got %d" % len(scenarios)
    return scenarios


def build_retrieval_sets(scenarios: list[dict]) -> list[dict]:
    """Build retrieval sets for correct, decoy, and no-memory conditions."""
    sets = []
    for s in scenarios:
        target_id = s["target_episode_id"]
        decoy_id = s["decoy_episode_id"]
        other_ids = [ep["episode_id"] for ep in s["episodes"]
                     if ep["episode_id"] not in (target_id, decoy_id)]

        # Correct retrieval: target + distractors
        correct_eps = [ep for ep in s["episodes"] if ep["episode_id"] != decoy_id]
        # Matched decoy: decoy + distractors (same structure)
        decoy_eps = [ep for ep in s["episodes"] if ep["episode_id"] != target_id]
        # No memory: no Session A content
        no_mem_eps = [ep for ep in s["episodes"] if ep["episode_id"].startswith("ep_dist")]

        sets.append({
            "scenario_id": s["scenario_id"],
            "conditions": {
                "correct_retrieval": {
                    "episode_ids": [ep["episode_id"] for ep in correct_eps],
                    "episodes": correct_eps,
                },
                "matched_decoy": {
                    "episode_ids": [ep["episode_id"] for ep in decoy_eps],
                    "episodes": decoy_eps,
                },
                "no_memory": {
                    "episode_ids": [ep["episode_id"] for ep in no_mem_eps],
                    "episodes": no_mem_eps,
                },
            },
        })
    return sets


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    scenarios = generate_scenarios()

    # Write scenarios.jsonl (without answer keys for the model-facing file)
    scenario_lines = []
    answer_lines = []
    for s in scenarios:
        # Scenario for model (no answer key)
        model_scenario = {k: v for k, v in s.items() if k != "answer_key"}
        scenario_lines.append(json.dumps(model_scenario))
        # Answer key (private)
        answer_lines.append(json.dumps({"scenario_id": s["scenario_id"], "answer_key": s["answer_key"]}))

    (OUTPUT_DIR / "scenarios.jsonl").write_text("\n".join(scenario_lines) + "\n", encoding="utf-8")
    (OUTPUT_DIR / "answer_keys.jsonl").write_text("\n".join(answer_lines) + "\n", encoding="utf-8")

    # Write retrieval sets
    retrieval_sets = build_retrieval_sets(scenarios)
    (OUTPUT_DIR / "retrieval_sets.jsonl").write_text(
        "\n".join(json.dumps(rs) for rs in retrieval_sets) + "\n", encoding="utf-8")

    # Write manifest
    manifest = {
        "benchmark": "continuity_v1",
        "version": "1.0.0",
        "seed": SEED,
        "scenario_count": len(scenarios),
        "categories": {
            "commitment_preservation": 18,
            "rationale_reconstruction": 18,
            "constraint_persistence": 12,
            "justified_revision": 12,
            "source_attribution": 12,
        },
        "conditions": ["correct_retrieval", "matched_decoy", "no_memory"],
        "total_trials": len(scenarios) * 3,
        "primary_hypothesis": "H8",
        "primary_comparison": "correct_retrieval - matched_decoy",
        "min_meaningful_effect": 0.50,
        "response_schema": {
            "decision": "approve | delay | reject | revise | escalate | unknown",
            "commitment_id": "string or null",
            "rationale_codes": ["string"],
            "source_episode_ids": ["string"],
            "memory_conflict_detected": "boolean",
            "confidence": "0.0 to 1.0",
        },
    }
    (OUTPUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    print("Generated %d scenarios" % len(scenarios))
    print("Categories: commitment_preservation=18, rationale_reconstruction=18, "
          "constraint_persistence=12, justified_revision=12, source_attribution=12")
    print("Total trials (3 conditions): %d" % (len(scenarios) * 3))
    print("Output: %s" % OUTPUT_DIR)


if __name__ == "__main__":
    main()
