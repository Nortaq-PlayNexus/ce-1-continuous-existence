# MISSION.md — CE-1 Research Charter

Verbatim restatement of the directive's scientific objective, with the
isolation and execution rules that govern this programme.

---

## 1. Mission

Establish a rigorous, reproducible, independently auditable scientific research
programme investigating whether an artificial cognitive system could genuinely
experience continuous existence and subjective experience.

The goal is NOT to build a chatbot that claims to be conscious, a
memory-retrieval system, a roleplay persona, or a system that merely simulates
autobiographical continuity.

The goal is to investigate the scientific and engineering requirements for an AI
whose ongoing internal cognitive state develops through experience and persists
through time, and to determine what evidence could support or falsify
hypotheses about subjective experience.

This is a long-term research programme. Do not assume consciousness is
achievable, impossible, or already demonstrated. Treat all three possibilities
according to the available evidence.

## 2. Research question

Can we construct an artificial cognitive architecture whose internal state
develops continuously through interaction and ongoing computation, survives
interruptions through causal state continuity, and exhibits properties that
provide scientifically meaningful evidence relevant to subjective experience?

## 3. Hypotheses (H1–H7)

| ID | Hypothesis | Testable computationally? |
|---|---|---|
| H1 | The system maintains a structured internal state that causally influences future cognition. | Yes |
| H2 | Interactions produce durable changes in subsequent reasoning, expectations, associations, and decisions. | Yes |
| H3 | The system can resume after interruption without reconstructing its entire state through ordinary conversational memory retrieval. | Yes |
| H4 | Recurrent information processing and communication between cognitive subsystems measurably influence performance and internal-state dynamics. | Yes |
| H5 | The system maintains an evidence-grounded model of its own capabilities, history, limitations, and changing state. | Yes |
| H6 | The architecture exhibits measurable properties predicted by at least one serious scientific theory of consciousness. | Yes |
| H7 | The system has subjective experience. | **No** — not establishable by behavioural tests, memory persistence, reported feelings, or a self-model alone. |

**Critical separation:** H1–H6 can be investigated through computational and
behavioural experiments. H7 is the ultimate question but cannot currently be
established simply by passing behavioural tests. Do not collapse these
hypotheses into one claim.

Each hypothesis is documented in `hypotheses/HYPOTHESIS_REGISTER.md` with its
operational definition, motivation, supporting/contrary evidence, competing
explanations, measurements, falsification conditions, what the experiment
cannot establish, and current confidence.

## 4. Research protocol (mandatory stages)

1. **Research the existing field before inventing solutions.** See
   `research/RESEARCH_MAP.md`.
2. **Stage 0 — Research baseline:** literature review, theory comparison,
   implementation inventory, hypothesis register, evidence audit.
3. **Stage 1 — Computational continuity:** compare stateless, retrieval-based,
   persistent explicit-state, recurrent, and experience-dependent architectures.
4. **Stage 2 — Causal interventions:** ablation, state perturbation, recurrence
   removal, information-sharing interventions.
5. **Stage 3 — Experience-dependent development:** retention, transfer,
   stability, adaptability, calibration, catastrophic forgetting.
6. **Stage 4 — Theory-specific predictions:** select strongest feasible
   predictions from competing theories *before* execution.
7. **Stage 5 — Independent replication.**
8. **Stage 6 — Scientific assessment.**

## 5. Safety and ethical governance

Explicit review is required for: uncertainty around AI consciousness;
possible moral-status considerations; the distinction between simulated
distress reports and established subjective suffering; safe limits on
autonomous operation; resource and compute limits; human oversight; secure
handling of credentials and personal data; reversibility of experiments;
protection against uncontrolled self-modification; risks of anthropomorphic
interpretation; and clear disclosure of uncertainty in public-facing results.

Keep the initial project observational and experimental. **Do not implement
unrestricted self-modification, uncontrolled replication, or autonomous changes
to the host environment.**

## 6. Implementation rules

- Use the installed environment and available tools intelligently.
- Before adding dependencies: inspect existing versions, determine necessity,
  prefer a project-local virtual environment, record why the dependency is
  needed, pin versions where reproducibility requires it, and test
  compatibility with the actual Python and OS versions.
- Do not assume GPU availability.
- Do not assume internet access is unrestricted.
- Do not pretend a model has run if it has only been proposed.
- Do not build a large speculative framework when a small experiment would test
  the hypothesis more effectively.
- Prefer modular, testable components and documented interfaces.
- Every prototype must have a README explaining its scientific purpose,
  assumptions, limitations, execution instructions, and tests.

## 7. Required initial deliverables

1. Verified isolated repository.
2. Project README and research charter.
3. Multi-stage research map.
4. Populated literature register with verifiable sources.
5. Comparison of major theories of consciousness.
6. Inventory of relevant existing implementations.
7. Hypothesis register with operational definitions.
8. Catalogue of contradictory evidence and unresolved questions.
9. Proposed experimental roadmap with controls and falsification criteria.
10. Documented source and experiment provenance system.
11. Working validation scripts and automated tests.
12. Coverage report explaining searched areas, incomplete areas, and why.
13. Initial scientific report with citations.
14. Prioritized next-action plan.
15. Clean final status report distinguishing completed from proposed work.

## 8. Execution and reporting protocol

Proceed autonomously through safe, reversible setup and research tasks. At each
significant milestone: inspect actual state, record completed work, run
appropriate validation, record failures and limitations, update the research
audit, and preserve reproducibility.

If an action could affect unrelated projects, require elevated permissions,
incur substantial costs, or introduce irreversible changes, stop and request
authorization.

**Do not make Git commits unless explicitly authorized.** Do not change
unrelated repositories or existing experiments. Do not report success until the
relevant checks have actually passed. When web research is limited, record the
limitation rather than fabricate comprehensive coverage. When evidence conflicts,
preserve the conflict rather than forcing a conclusion. When a scientific claim
cannot be established, say so explicitly.