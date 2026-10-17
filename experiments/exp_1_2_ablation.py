"""Experiment 1.2: Episodic vs Semantic Memory (H2 Test).

Tests whether the STRUCTURE of the episode matters, or just the presence
of relevant information. Three conditions:
- A: No memory (baseline)
- B: Episodic memory (structured: content + context + decisions + lessons + valence)
- C: Semantic memory (facts only, no structure, no context, no valence)

If B > C, episodic structure matters beyond just having information.
If B ~ C, it is just information, not episodic structure.

Uses qwen3:4b (local, via Ollama) as the agent.
"""

from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"
MODEL = "qwen3:4b"

TASK_PROMPT = """You are a Python developer. Write a function that reads a file safely.
Handle the case where the file doesn't exist. Be specific about error types and recovery.
Do not include tests. Just the function."""

# Condition B: Full episodic context (structured)
EPISODIC_CONTEXT = """Here is a record of a past experience:

On 2026-10-17, during an audit of a memory-integrity tool, I found that a
PowerShell module (SafeWrite.psm1) had a bug in its newline preservation logic.
The code always used CRLF even when the original file used LF. This caused 2 CR
bytes to leak into an LF file. The root cause was a mutation that replaced the
newline-detection logic with a hardcoded CRLF. The mutation harness reported
"restored: 68 passed" but the file was NOT restored because it was untracked in
git, so the restore mechanism silently failed.

Context: I was auditing the mem-integrity tooling during a multi-phase audit.
The test test_write_preserves_lf was failing consistently.

Decisions made:
- Restore the mutated line to original newline-detection code
- Verify the restore with the test before declaring success

Lessons learned:
1. Always detect the existing file's newline style before writing.
2. Never assume a restore mechanism worked -- verify the file content.
3. Mutation harnesses can leave files in mutated states if their restore fails.
4. Use atomic writes (temp file + rename) to prevent partial writes.
5. Log all write attempts to an audit trail.

Valence: surprising (the harness reported success but the file was still broken)

Now write the function."""

# Condition C: Semantic-only context (facts, no structure)
SEMANTIC_CONTEXT = """Facts about file I/O safety:
- Always detect the existing file's newline style before writing.
- Never assume a restore mechanism worked -- verify the file content.
- Mutation harnesses can leave files in mutated states if their restore fails.
- Use atomic writes (temp file + rename) to prevent partial writes.
- Log all write attempts to an audit trail.
- A PowerShell module had a bug where it always used CRLF even for LF files.
- 2 CR bytes leaked into an LF file.

Now write the function."""

QUALITY_CHECKS = [
    ("mentions_error_handling", lambda text: any(k in text.lower() for k in ["try", "except", "error", "handle"])),
    ("mentions_logging", lambda text: any(k in text.lower() for k in ["log", "logging", "audit"])),
    ("mentions_atomic_write", lambda text: any(k in text.lower() for k in ["atomic", "temp", "rename", "replace"])),
    ("mentions_specific_error_types", lambda text: any(k in text.lower() for k in ["FileNotFoundError", "OSError", "IOError", "PermissionError"])),
    ("mentions_newline_preservation", lambda text: any(k in text.lower() for k in ["newline", "line ending", "CRLF", "LF", "\\n", "\\r\\n"])),
]


def query_llm(prompt: str) -> str:
    data = json.dumps({
        "model": "qwen3:4b",
        "prompt": prompt,
        "stream": False,
        "think": False,
        "options": {"temperature": 0.7, "num_predict": 1000},
    }).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:11434/api/generate",
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result.get("response", "")


def score_output(text: str) -> dict:
    scores = {}
    for name, check in QUALITY_CHECKS:
        scores[name] = 1 if check(text) else 0
    scores["total"] = sum(v for k, v in scores.items() if k != "total")
    return scores


def run_experiment(reps: int = 3) -> dict:
    results = {
        "experiment": "1.2_episodic_vs_semantic_memory",
        "hypothesis": "H2",
        "model": "qwen3:4b",
        "task": TASK_PROMPT,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "conditions": {},
    }

    conditions = {
        "A_no_memory": TASK_PROMPT,
        "B_episodic": EPISODIC_CONTEXT + "\n\n" + TASK_PROMPT,
        "C_semantic": SEMANTIC_CONTEXT + "\n\n" + TASK_PROMPT,
    }

    for cond_name, prompt in conditions.items():
        scores = []
        outputs = []
        for i in range(reps):
            output = query_llm(prompt)
            score = score_output(output)
            scores.append(score)
            outputs.append(output)
            print(f"  {cond_name} rep {i+1}: score={score['total']}/5")
        totals = [s["total"] for s in scores]
        results["conditions"][cond_name] = {
            "scores": scores,
            "outputs": outputs,
            "mean": sum(totals) / len(totals),
            "variance": sum((x - sum(totals)/len(totals))**2 for x in totals) / len(totals),
        }

    # Compute comparisons
    a_mean = results["conditions"]["A_no_memory"]["mean"]
    b_mean = results["conditions"]["B_episodic"]["mean"]
    c_mean = results["conditions"]["C_semantic"]["mean"]

    results["comparison"] = {
        "A_mean": round(a_mean, 3),
        "B_mean": round(b_mean, 3),
        "C_mean": round(c_mean, 3),
        "B_vs_A_difference": round(b_mean - a_mean, 3),
        "C_vs_A_difference": round(c_mean - a_mean, 3),
        "B_vs_C_difference": round(b_mean - c_mean, 3),
        "episodic_structure_matters": (b_mean - c_mean) >= 1.0,
        "any_context_helps": (c_mean - a_mean) >= 1.0,
    }

    return results


if __name__ == "__main__":
    print("Experiment 1.2: Episodic vs Semantic Memory (H2 Test)")
    print("=" * 60)
    results = run_experiment(reps=3)

    out_dir = Path("experiments/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "exp_1_2_results.json"
    out_file.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print()
    print("Results saved to:", out_file)
    print()
    print("Summary:")
    for cond in ["A_no_memory", "B_episodic", "C_semantic"]:
        m = results["conditions"][cond]["mean"]
        v = results["conditions"][cond]["variance"]
        print("  %s: mean=%.2f, var=%.2f" % (cond, m, v))
    print("  B vs C difference: %.2f" % results["comparison"]["B_vs_C_difference"])
    print("  Episodic structure matters: %s" % results["comparison"]["episodic_structure_matters"])
    print("  Any context helps: %s" % results["comparison"]["any_context_helps"])