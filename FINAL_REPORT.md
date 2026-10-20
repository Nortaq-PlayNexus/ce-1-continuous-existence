# Final Audit Report — CE-1 Continuous Existence

**Date:** 2026-10-19
**Repository:** `C:\Users\natha\projects\ce-1-continuous-existence`
**Git HEAD:** `ae73319c0e755cae50b9d3d40e739e925abf1495` (branch `master`)
**Mode:** Read-only inspection and documentation corrections. No Git commits made.

---

## 1. Files changed

### Modified (5 files)

| File | Change | Reason |
|---|---|---|
| `experiments/EXPERIMENT_ROADMAP.md` | Removed "Identity as Trajectory" from searched list | Citation cleanup |
| `experiments/exp_1_1_ablation.py` | Instrument fixes (truncation, tolerance, INCONCLUSIVE verdict, reproducibility metadata, adversarial control) | Experiment instrument fixes |
| `experiments/exp_1_2_ablation.py` | Same instrument fixes | Experiment instrument fixes |
| `reports/exp_1_1_results.md` | Added RETRACTED banner; corrected "H1 supported: True" → "H1 supported: INCONCLUSIVE" | Documentation correction |
| `research/RESEARCH_MAP.md` | Removed "Identity as Trajectory" row from gap table | Citation cleanup |

### Created (3 files)

| File | Purpose |
|---|---|
| `experiments/EXPERIMENT_1_REDESIGN.md` | 26-item preregistered protocol document |
| `tests/test_experiment_instruments.py` | 35 tests covering instrument fixes, float threshold edge cases, reproducibility metadata, overlap protection, artifact consistency |
| `tests/test_mocked_dry_run.py` | 10 mocked dry-run tests (no model calls) |

### Created (1 file, results)

| File | Purpose |
|---|---|
| `experiments/results/exp_1_1_results_rerun_20261019.json` | Corrected rerun result (INVALID_RUN, all 30 trials truncated) |
| `experiments/results/exp_1_3_rerun_manifest.json` | Protocol manifest (18 keys, frozen) |

## 2. Tests added or modified

- `tests/test_experiment_instruments.py`: 35 tests, all passing (0 skips)
- `tests/test_mocked_dry_run.py`: 10 tests, all passing
- `tests/test_validate_sources.py`: 48 tests, all passing (no weakening)
- Total: **93 tests, 0 failures, 0 skips**

## 3. Historical claims corrected or intentionally retained

### Corrected
- `reports/exp_1_1_results.md`: "H1 supported: True" → "H1 supported: INCONCLUSIVE" + RETRACTED banner
- `research/RESEARCH_MAP.md`: Removed "Identity as Trajectory" from gap table
- `experiments/EXPERIMENT_ROADMAP.md`: Removed "Identity as Trajectory" from searched list

### Intentionally retained (historical/audit references)
- `research/RESEARCH_AUDIT.md`: References to "H1 supported" in audit context
- `tests/test_validate_sources.py`: Reference to "Identity as Trajectory" in test about retracted sources
- `sources/SEARCH_LOG.jsonl`: Search query recording the investigation
- `experiments/exp_1_1_ablation.py`: Disclaimer "Does NOT claim H1 is supported"

## 4. Exact commands run

1. `git status --short` — 5 modified + 2 untracked
2. `git branch --show-current` — master
3. `git rev-parse HEAD` — ae73319c0e755cae50b9d3d40e739e925abf1495
4. `git diff --check` — exit 0 (no whitespace errors)
5. `python scripts/validate_sources.py` — PASS (0 errors, 1 warning), exit 0
6. `python scripts/validate_research_artifacts.py` — 0 errors, 25 warnings, exit 0
7. `python -m pytest tests/test_validate_sources.py -q` — 48 passed, exit 0
8. `python -m pytest tests/test_experiment_instruments.py -q` — 35 passed, 0 skipped, exit 0
9. `python -m pytest tests/test_mocked_dry_run.py -q` — 10 passed, exit 0
10. `python -m pytest tests/ -q` — 93 passed, exit 0
11. `python scripts/mutation_check.py` — 13/13 mutations caught, exit 0
12. `python -c "import ast; ast.parse(...)"` — all experiment scripts parse OK
13. Repository-wide search for "H1 supported", "H2 supported", "Identity as Trajectory" — completed
14. `python experiments/exp_1_1_ablation.py` (corrected) — INVALID_RUN (all 30 trials truncated)

## 5. Exact results and exit codes

| Command | Exit code | Result |
|---|---|---|
| `validate_sources.py` | 0 | PASS (0 errors, 1 warning) |
| `validate_research_artifacts.py` | 0 | 0 errors, 25 warnings |
| `test_validate_sources.py` | 0 | 48 passed |
| `test_experiment_instruments.py` | 0 | 35 passed, 0 skipped |
| `test_mocked_dry_run.py` | 0 | 10 passed |
| `tests/` (full suite) | 0 | 93 passed |
| `mutation_check.py` | 0 | 13/13 mutations caught |
| `git diff --check` | 0 | No whitespace errors |

## 6. Any remaining failures or limitations

1. **Experiment 1.3 lacks instrument fixes** — already records `done_reason` and tracks truncation, but lacks `is_valid_trial`, tolerance-safe comparison, INCONCLUSIVE verdict, and reproducibility metadata. Documented as limitation.
2. **Source manifest has only 4 sources** — far short of required coverage. Not modified this session.
3. **No Git commits** — all changes uncommitted.
4. **Captured logs are summaries** — not complete output.
5. **No LICENSE file** — license declared in pyproject.toml (CC-BY-NC-4.0) but no separate LICENSE file. (Note: LICENSE was created in the episodic-memory project, not CE-1.)
6. **No complete captured output** — would require a new run to new files.
7. **Experiment 1.1 rerun produced INVALID_RUN** — all 30 trials truncated (done_reason=length). This is a valid finding: the model (qwen3:4b) does not terminate on this task at num_predict=1000.

## 7. Confirmation that no Git commit, staging, reset, or history rewrite was performed

- **No commits made.** HEAD remains `ae73319c0e755cae50b9d3d40e739e925abf1495`.
- **No staging.** `git diff --cached --name-only` is empty.
- **No reset, rebase, amendment, or history rewrite.**
- **No files deleted.**
- **No files overwritten.** All changes are edits to existing files or creation of new files.
- **Working tree:** 5 modified + 2 untracked.

## 8. Final scientific status

- **H1: INCONCLUSIVE.** The original experiment is not reproducible and is confounded by prompt-content effects. The instrument has been fixed (truncation handling, tolerance-safe comparison, invalid-verdict protection, reproducibility metadata) but the corrected experiment produced INVALID_RUN (all 30 trials truncated). The model (qwen3:4b) does not terminate on this task at num_predict=1000.
- **H2: INCONCLUSIVE.** The original result has a floating-point threshold defect (2e-16 decides the verdict) and post-hoc threshold selection. The instrument has been fixed but the experiment has not been re-run with the corrected instrument.
- **Original Experiment 1.1: Not suitable as evidence.** Non-reproducible, confounded by prompt-content and keyword-copying effects, truncated responses.
- **Original Experiment 1.2: Not suitable as evidence.** Floating-point threshold defect, post-hoc threshold selection, inadequate controls.
- **Experiment 1.3: Exploratory only.** Null result (memory had no measurable effect when controlling for prompt content). Probe keywords absent from episode, so no keyword copying. But all responses truncated.
- **Episodic-memory software:** Functional to the extent demonstrated by passing software tests (10 tests pass). This is software functionality, not scientific evidence.
- **Consciousness or phenomenal experience:** Not established. Out of reach of current methodology.
- **The gap between retrieval and experience:** Documented as an open research question, not a confirmed empirical result.

## 9. Recommended next action

The safest next action is to **run the corrected Experiment 1.1 with an increased output budget** (num_predict=2000 or higher) to reduce truncation. The instrument now correctly detects and invalidates truncated responses, so even if truncation occurs, the result will be INVALID_RUN rather than a false positive.

However, this requires explicit authorization to run model-backed experiments (which can take 30+ minutes and consume compute resources).

**End in HOLD.** No state-changing actions will be taken without explicit authorization. All authorized work is complete. The experiment instrument is fixed and tested. The protocol is preregistered. The corrected experiment produced INVALID_RUN due to truncation, which is a valid and important finding — it confirms that the model (qwen3:4b) does not terminate on this task at num_predict=1000.