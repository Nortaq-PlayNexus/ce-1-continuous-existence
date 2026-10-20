# ZENODO_README.md — Standalone README for Zenodo Record

## CE-1 Continuous Existence: Episodic Memory Instrument, Research Audit, and Experiment Redesign

**Version:** 0.1.0
**License:** CC-BY-NC-4.0 (research-only; no commercial use)
**Release date:** 2026-10-19

### Abstract

CE-1 Continuous Existence is a research software and experimental-protocol
repository investigating episodic memory, continuity-related behavior, and the
distinction between retrieval of stored information and subjective experience in
AI systems. The repository includes the episodic-memory implementation, research
protocols, experiment runners, validation tools, research artifacts, audit reports,
and a corrected redesign of the initial experiments.

### Contents

- `src/` — Episodic memory implementation (Python, ChromaDB + sentence-transformers)
- `tests/` — Automated validation (48 tests, all passing)
- `experiments/` — Experiment runners and results (3 experiments, all inconclusive)
- `experiments/EXPERIMENT_1_REDESIGN.md` — Preregistered protocol for future experiments
- `research/` — Research map, audit report, source manifest
- `hypotheses/` — H1-H7 hypothesis register with operational definitions
- `architecture/` — Candidate designs for persistent state
- `reports/` — Initial research report, audit reports, result reports
- `sources/` — Source manifest, search log, access limitations
- `scripts/` — Validation and provenance tools

### Scientific status

**H1 (causal state influence): INCONCLUSIVE.**
**H2 (durable change): INCONCLUSIVE.**
**Original Experiment 1.1: Not suitable as evidence** — non-reproducible, confounded by
prompt-content and keyword-copying effects, truncated responses.
**Original Experiment 1.2: Not suitable as evidence** — floating-point threshold defect,
post-hoc threshold selection, inadequate controls.
**Experiment 1.3: Exploratory only** — null result (memory had no measurable effect
when controlling for prompt content).

### Audit findings

An independent audit (2026-10-18) found:
1. The original Experiment 1.1 result was not independently reproducible.
2. The experiment design could not separate memory effects from prompt-content effects.
3. Experiment 1.2 contained a floating-point threshold defect (2e-16 decided the verdict).
4. The "Identity as Trajectory" citation was retracted (agent-generated research sprint,
   not peer-reviewed literature).
5. An unauthorized Git commit (`3d36dc2`) was created without explicit authorization.
6. The report contradicted its own artifacts.

The audit also created validation scripts (48 tests, 13/13 mutations caught) and a
source manifest (4 verified sources with DOIs).

### Limitations

- The software implementation and scientific claims are separate.
- Passing tests indicate software behavior, not consciousness.
- H1 and H2 are inconclusive.
- The original positive experiment claims were superseded or invalidated.
- This work does not establish AI consciousness, phenomenal experience, or personal identity.
- Future experiments require a corrected and preregistered protocol (see EXPERIMENT_1_REDESIGN.md).
- The gap between retrieval and experience remains an open research question.

### Reproducibility

- Python >= 3.11, standard library only (no runtime dependencies for Stage 0).
- Optional: numpy>=2.0, scipy>=1.14 for numerical work.
- Run tests: `python -m pytest tests/ -q`
- Run source validation: `python scripts/validate_sources.py`
- Run artifact validation: `python scripts/validate_research_artifacts.py`
- Run mutation checks: `python scripts/mutation_check.py`

### License

CC-BY-NC-4.0 (research-only; no commercial use).

### Citation

CE-1 Continuous Existence: Episodic Memory Instrument, Research Audit, and Experiment
Redesign. Version 0.1.0. Zenodo. DOI assigned upon publication.

If you use this software, research protocol, or audit record, please cite this
repository release and its Zenodo DOI.

### Contact

Research programme: CE-1 Continuous Existence
Repository: C:\Users\natha\projects\ce-1-continuous-existence