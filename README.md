# CE-1 — Continuous Existence Research Programme

> *"Establish a rigorous, reproducible, independently auditable scientific research programme investigating whether an artificial cognitive system could genuinely experience continuous existence and subjective experience."*

**Status:** Stage 0 — Research baseline (documentation + provenance engineering)
**Started:** 2026-10-17
**Location:** `C:\Users\natha\projects\ce-1-continuous-existence`
**License:** CC-BY-NC-4.0 (research-only; no commercial use)

---

## 1. What this is

CE-1 is a **long-term scientific research programme**, not a product. Its goal is
to investigate the engineering and scientific requirements for an artificial
cognitive system whose ongoing internal state develops through experience,
persists through time, and could — in principle — provide evidence relevant to
subjective experience.

**What it is NOT:**
- Not a chatbot that claims to be conscious.
- Not a memory-retrieval system or a roleplay persona.
- Not a system that merely simulates autobiographical continuity.
- Not a claim that consciousness is achievable, impossible, or already demonstrated.

## 2. How to read this repository

| Path | Purpose |
|---|---|
| `MISSION.md` | The full research charter (verbatim from the directive). |
| `RESEARCH_PRINCIPLES.md` | Evidence grading, provenance, and audit rules. |
| `CONTRIBUTING.md` | How to add a source, an experiment, or a finding. |
| `research/` | The Stage 0 research baseline: literature, theories, implementations. |
| `hypotheses/` | H1–H7 register with operational definitions and falsification criteria. |
| `experiments/` | Roadmap, protocols, templates, control designs, metrics. |
| `architecture/` | Candidate designs for persistent state, continual learning, self-models. |
| `sources/` | Provenance: source manifest, search log, access limitations. |
| `prototypes/` | Small, testable implementations — each with its own README. |
| `tests/` | Automated validation of the provenance and research-artifact machinery. |
| `scripts/` | Deterministic validation scripts. |
| `reports/` | The initial research report and next-step plan. |

## 3. Current stage

**Stage 0 — Research baseline** is in progress. The deliverables required by
the directive are listed in `reports/NEXT_STEPS.md`; each is marked
COMPLETE, PARTIAL, or NOT STARTED. Nothing here is a placeholder — every file
contains substantive content or explicitly documents why it is incomplete.

## 4. Isolation guarantees

This repository is **independent** of all other work on this machine:

- Own Git history (initialised separately; the home directory is an unrelated
  accidental worktree and is *not* this repo's parent).
- Own virtual environment when dependencies are added (none yet).
- No modification to global OpenCode configuration, shared memory, system
  Python, or any other project's dependencies or processes.
- No credentials, private data, or unrelated experiment outputs are copied in.

## 5. Reproducibility

Every source in `sources/SOURCE_MANIFEST.jsonl` is recorded with its DOI or
canonical URL, access date, evidence grade, and verification status. Scripts
in `scripts/` are deterministic and fail visibly on missing data. See
`RESEARCH_PRINCIPLES.md` for the full provenance policy.

## 6. Citation

If you use this work, cite the repository and the specific files. This is a
living document; the current report is `reports/INITIAL_RESEARCH_REPORT.md`.