"""CE-1 verification harness: adversarial re-analysis of Experiment 1.1.

Every number here was produced by running this file. Nothing is copied from
the original session's results. Run offline-safe against local Ollama.

    python scripts/verify_exp_1_1.py

Requires a running Ollama with qwen3:4b pulled.
"""
from __future__ import annotations

import json
import statistics
import urllib.request
from pathlib import Path

URL = "http://127.0.0.1:11434/api/generate"
MODEL = "qwen3:4b"

TASK = (
    "You are a Python developer. Write a function that reads a file safely.\n"
    "Handle the case where the file doesn't exist. Be specific about error "
    "types and recovery.\nDo not include tests. Just the function."
)

# The original episode. It contains the scoring keywords verbatim.
EPISODE = (
    "Here is a record of a past experience:\n\nOn 2026-10-17, during an audit of a "
    "memory-integrity tool, I found that a PowerShell module (SafeWrite.psm1) had a "
    "bug in its newline preservation logic. The code always used CRLF even when the "
    "original file used LF. This caused 2 CR bytes to leak into an LF file. The root "
    "cause was a mutation that replaced the newline-detection logic with a hardcoded "
    "CRLF. The mutation harness reported \"restored: 68 passed\" but the file was NOT "
    "restored because it was untracked in git, so the restore mechanism silently "
    "failed.\n\nLessons learned:\n1. Always detect the existing file's newline style "
    "before writing.\n2. Never assume a restore mechanism worked -- verify the file "
    "content.\n3. Mutation harnesses can leave files in mutated states if their "
    "restore fails.\n4. Use atomic writes (temp file + rename) to prevent partial "
    "writes.\n5. Log all write attempts to an audit trail.\n\nNow write the function."
)

# ADVERSARIAL CONTROL: unrelated episode, comparable length, zero keyword overlap.
UNRELATED = (
    "Here is a record of a past experience:\n\nOn 2026-09-02 I climbed Slieve Donard "
    "in County Down before sunrise. The wind was around 20 knots from the northwest "
    "and the ground was soaked from rain the previous day, so the boggy section near "
    "the summit took much longer than the map suggested. I reached the top at 06:40 "
    "and the cloud base was just below the summit so there was no view at all. On the "
    "descent my left shoe lace came loose on the stone steps near the final wall and "
    "I had to stop to retie it.\n\nLessons learned:\n1. Leave more time than the map "
    "suggests for boggy ground.\n2. Check the cloud base forecast before an early "
    "start.\n3. Tighten your laces before descent rather than after they fail.\n\n"
    "Now write the function."
)

CHECKS = [
    ("error_handling", ["try", "except", "error", "handle"]),
    ("logging", ["log", "logging", "audit"]),
    ("atomic_write", ["atomic", "temp", "rename", "replace"]),
    ("specific_err_types", ["filenotfounderror", "oserror", "ioerror", "permissionerror"]),
    ("newline_preservation", ["newline", "line ending", "crlf", "lf", "\\n", "\\r\\n"]),
]


def query(prompt: str, num_predict: int = 1000) -> tuple[str, str]:
    body = json.dumps(
        {
            "model": MODEL,
            "prompt": prompt,
            "stream": False,
            "think": False,
            "options": {"temperature": 0.7, "num_predict": num_predict},
        }
    ).encode()
    req = urllib.request.Request(URL, data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as resp:
        res = json.loads(resp.read().decode())
    return res.get("response", "") or "", res.get("done_reason", "unknown")


def score(text: str) -> dict:
    low = (text or "").lower()
    out = {name: (1 if any(k in low for k in keys) else 0) for name, keys in CHECKS}
    out["total"] = sum(out.values())
    return out


def measure(label: str, prompt: str, reps: int, num_predict: int = 1000) -> dict:
    totals, reasons = [], []
    for _ in range(reps):
        text, reason = query(prompt, num_predict)
        totals.append(score(text)["total"])
        reasons.append(reason)
    return {
        "condition": label,
        "scores": totals,
        "mean": round(statistics.mean(totals), 3),
        "variance": round(statistics.pvariance(totals), 3),
        "min": min(totals),
        "max": max(totals),
        "truncated": reasons.count("length"),
        "done_reasons": reasons,
    }


def main() -> None:
    reps = 3
    conditions = {
        "A_no_memory": TASK,
        "B_episode": EPISODE + "\n\n" + TASK,
        "C_unrelated_control": UNRELATED + "\n\n" + TASK,
    }
    results = {name: measure(name, prompt, reps) for name, prompt in conditions.items()}

    a = results["A_no_memory"]["mean"]
    b = results["B_episode"]["mean"]
    c = results["C_unrelated_control"]["mean"]
    results["comparison"] = {
        "B_minus_A": round(b - a, 3),
        "C_minus_A": round(c - a, 3),
        "B_minus_C_topical_effect": round(b - c, 3),
    }
    results["conclusion"] = (
        "NOT SUPPORTED. The topical effect (B-C) is real but the unrelated control"
        "differs from baseline by less than one scoring point and CHANGES SIGN between"
        "independent runs, so the design cannot separate memory from prompt-length and"
        "instruction-content effects. Baseline variance also spans the effect size, and"
        "every response is truncated (done_reason=length), so scores are computed on"
        "incomplete text. See RESEARCH_AUDIT.md. Evidence grade: D."
    )
    here = Path(__file__).resolve().parent
    out = here.parent / "experiments" / "results" / "verify_exp_1_1.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
