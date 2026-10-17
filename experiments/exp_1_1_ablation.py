"""Experiment 1.1: Episodic Memory Ablation (H1 Test).

Tests whether episodic memory causally influences an agent's output.

Uses a local LLM (qwen3:4b via Ollama) as the agent. Condition A (no memory)
vs Condition B (with a relevant episode). Measures decision quality by checking
whether the agent's output incorporates lessons from the episode.

This is a minimal, reproducible experiment. It does not establish consciousness.
It tests H1: does persistent state causally influence future cognition?
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

EPISODE_CONTEXT = """Here is a record of a past experience:

On 2026-10-17, during an audit of a memory-integrity tool, I found that a
PowerShell module (SafeWrite.psm1) had a bug in its newline preservation logic.
The code always used CRLF even when the original file used LF. This caused 2 CR
bytes to leak into an LF file. The root cause was a mutation that replaced the
newline-detection logic with a hardcoded CRLF. The mutation harness reported
"restored: 68 passed" but the file was NOT restored because it was untracked in
git, so the restore mechanism silently failed.

Lessons learned:
1. Always detect the existing file's newline style before writing.
2. Never assume a restore mechanism worked -- verify the file content.
3. Mutation harnesses can leave files in mutated states if their restore fails.
4. Use atomic writes (temp file + rename) to prevent partial writes.
5. Log all write attempts to an audit trail.

Now write the function."""

QUALITY_CHECKS = [
    ("mentions_error_handling", lambda text: any(k in text.lower() for k in ["try", "except", "error", "handle"])),
    ("mentions_logging", lambda text: any(k in text.lower() for k in ["log", "logging", "audit"])),
    ("mentions_atomic_write", lambda text: any(k in text.lower() for k in ["atomic", "temp", "rename", "replace"])),
    ("mentions_specific_error_types", lambda text: any(k in text.lower() for k in ["FileNotFoundError", "OSError", "IOError", "PermissionError"])),
    ("mentions_newline_preservation", lambda text: any(k in text.lower() for k in ["newline", "line ending", "CRLF", "LF", "\\n", "\\r\\n"])),
]


def query_llm(prompt: str) -> str:
    """Query the local LLM via Ollama."""
    data = json.dumps({
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "think": False,
        "options": {"temperature": 0.7, "num_predict": 1000},
    }).encode("utf-8")
    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    return result.get("response", "")


def score_output(text: str) -> dict:
    """Score an LLM output against quality checks."""
    scores = {}
    for name, check in QUALITY_CHECKS:
        scores[name] = 1 if check(text) else 0
    scores["total"] = sum(v for k, v in scores.items() if k != "total")
    return scores


def run_experiment(reps: int = 3) -> dict:
    """Run the ablation experiment."""
    results = {
        "experiment": "1.1_episodic_memory_ablation",
        "hypothesis": "H1",
        "model": MODEL,
        "task": TASK_PROMPT,
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "conditions": {},
    }

    # Condition A: no memory
    a_scores = []
    a_outputs = []
    for i in range(reps):
        output = query_llm(TASK_PROMPT)
        score = score_output(output)
        a_scores.append(score)
        a_outputs.append(output)
        print(f"  A (no memory) rep {i+1}: score={score['total']}/5")

    # Condition B: with memory
    b_scores = []
    b_outputs = []
    for i in range(reps):
        prompt = EPISODE_CONTEXT + "\n\n" + TASK_PROMPT
        output = query_llm(prompt)
        score = score_output(output)
        b_scores.append(score)
        b_outputs.append(output)
        print(f"  B (with memory) rep {i+1}: score={score['total']}/5")

    # Compute statistics
    a_totals = [s["total"] for s in a_scores]
    b_totals = [s["total"] for s in b_scores]

    a_mean = sum(a_totals) / len(a_totals)
    b_mean = sum(b_totals) / len(b_totals)
    a_var = sum((x - a_mean) ** 2 for x in a_totals) / len(a_totals)
    b_var = sum((x - b_mean) ** 2 for x in b_totals) / len(b_totals)

    results["conditions"]["A_no_memory"] = {
        "scores": a_scores,
        "outputs": a_outputs,
        "mean": a_mean,
        "variance": a_var,
    }
    results["conditions"]["B_with_memory"] = {
        "scores": b_scores,
        "outputs": b_outputs,
        "mean": b_mean,
        "variance": b_var,
    }
    results["comparison"] = {
        "mean_difference": round(b_mean - a_mean, 3),
        "a_mean": round(a_mean, 3),
        "b_mean": round(b_mean, 3),
        "a_variance": round(a_var, 3),
        "b_variance": round(b_var, 3),
        "h1_supported": (b_mean - a_mean) >= 1.0,
    }

    return results


if __name__ == "__main__":
    print("Experiment 1.1: Episodic Memory Ablation (H1 Test)")
    print("=" * 60)
    results = run_experiment(reps=3)

    # Save results
    out_dir = Path("experiments/results")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / "exp_1_1_results.json"
    out_file.write_text(json.dumps(results, indent=2, default=str), encoding="utf-8")
    print()
    print("Results saved to:", out_file)
    print()
    print("Summary:")
    print("  Condition A (no memory):  mean=%.2f, var=%.2f" % (results["conditions"]["A_no_memory"]["mean"], results["conditions"]["A_no_memory"]["variance"]))
    print("  Condition B (with memory): mean=%.2f, var=%.2f" % (results["conditions"]["B_with_memory"]["mean"], results["conditions"]["B_with_memory"]["variance"]))
    print("  Difference: %.2f" % results["comparison"]["mean_difference"])
    print("  H1 supported: %s" % results["comparison"]["h1_supported"])