## H8: Content-specific episodic continuity

**Status:** SUPPORTED (confirmatory, 2026-10-20)

**Operational definition:** After a context reset, correctly retrieved prior
episodes improve objective trajectory-continuity performance relative to
token-matched decoy episodes and a no-memory baseline.

**Falsification:** If correctly retrieved episodes do not produce a measurable
improvement over matched decoy episodes, H8 is falsified.

**Result:** SUPPORTED. Primary comparison (correct - decoy) = 0.819 on 0-5 scale,
exceeding minimum meaningful effect of 0.50. 216 trials, 0 truncations, 0 invalid.
All 5 categories show positive correct-decoy differences.

**What this does NOT establish:**
- Consciousness or subjective experience
- Genuine reliving or autonoetic awareness
- Metaphysical continuous existence
- Moral patienthood
- Generalization to other models or tasks

**Evidence:** Zenodo DOI 10.5281/zenodo.23489491, confirmatory_results.jsonl,
confirmatory_scores.jsonl, confirmatory_analysis.json

**Model:** gemma3:4b (qualified 23/24, 95.8%)

**Preregistration:** experiments/continuity_v1/preregistration_h8.md

---

## Connection to episodic memory

The episodic memory system (`C:\Users\natha\projects\episodic-memory`) provides
the data layer for testing H1-H5:

- **H1 test:** Ablate episodic memory, measure decision quality change.
- **H2 test:** Before/after decision patterns with episodic memory enabled vs disabled.
- **H3 test:** Interrupt, resume, measure state continuity vs retrieval-based reconstruction.
- **H4 test:** Ablate recurrent connections between memory and reasoning, measure.
- **H5 test:** Self-model accuracy measurement with episodic memory as the self-model's data source.

H6 and H7 require architectural work beyond episodic memory alone.

## Episodic memory as necessary but insufficient

Episodic memory (Tulving) is a necessary component of subjective experience:
- Without episodic memory, there is no "mental time travel" — no reliving of past events.
- Without reliving, there is no autobiographical self.
- Without an autobiographical self, there is no continuous identity.

But episodic memory is not sufficient:
- A database of past events is not a memory (it is storage).
- Retrieval of an episode is not reliving it (it is recognition).
- Behavioral consistency with past episodes is not identity (it is reconstruction).

The gap between storage and experience is the gap between data and consciousness.
This hypothesis register documents that gap and provides the ladder (H1-H6) for
investigating it.

## H8 (supported 2026-10-20)

H8 extends the programme with a functional, content-specific test of episodic
continuity. Unlike H1-H5 (which test architectural properties), H8 tests whether
correctly retrieved episodic content produces measurable behavioural benefit
over matched decoy content. H8 is supported (primary diff = 0.819, threshold 0.50)
but does not establish consciousness, subjective experience, or metaphysical
continuous existence. H8 is a behavioural benchmark, not a consciousness claim.
