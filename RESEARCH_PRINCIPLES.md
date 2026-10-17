# RESEARCH_PRINCIPLES.md — Evidence grading, provenance, and audit rules

This file defines how CE-1 judges evidence. It is the normative backbone of
every claim in this repository.

---

## 1. Evidence grades

Grades are a **working framework**, not a universal scientific standard. Criteria:

| Grade | Definition | Required |
|---|---|---|
| **A** | Direct, relevant empirical evidence with strong methodology and reproducible support. | Independent replication; published or publicly verifiable data. |
| **B** | Relevant empirical evidence with meaningful limitations. | Methodology sound enough to be informative despite limits. |
| **C** | Theoretical work, formal models, or indirect evidence. | Clear reasoning; testable predictions or formal structure. |
| **D** | Speculation, opinion, unverified claims, or insufficiently supported assertions. | Recorded as such; never cited as support for a positive claim. |

A highly cited paper is **not** automatically correct. A paper proposing an
architecture is **not** evidence that the architecture creates consciousness.

## 2. Per-source attributes

Every source in `sources/SOURCE_MANIFEST.jsonl` records:

- Stable source ID
- Title, authors
- Publication year and date
- DOI or canonical URL
- Source type (journal, preprint, conference, repository, dataset, report, book)
- Publication status (peer-reviewed / preprint / published / withdrawn)
- Access date
- Relevant research questions
- Evidence grade (A–D)
- Short factual summary
- Limitations
- Verification status (abstract read / full text read / code inspected / not inspected)

## 3. Peer-review status

Record separately: peer-review status, methodological quality, independent
replication, relevance to artificial systems, conflicts of interest where
documented, contradictory findings, and confidence in the interpretation.

## 4. Provenance rules

- **Freeze before you measure.** Establish the baseline and freeze it before
  running anything. A baseline is never refreshed to make a run pass.
- **Pin by content hash**, not by file path or modification time.
- If a pin must evolve, pin a frozen *historical prefix* whose digest is
  verified against the original whole-file digest. Record that you did this.
- **Append, do not rewrite history.** DECISIONS.md-style logs are append-only;
  supersede, never delete.
- **Preserve source provenance** so every important conclusion can be traced to
  its supporting evidence.

## 5. Research rigour expectations

- Check estimator applicability preconditions before trusting output; distinguish
  real findings from numerical artifacts in both directions.
- Want adversarial falsification of own results, cross-validation, and
  sensitivity sweeps.
- **Null results are acceptable and must be stated plainly, never softened into
  weak positives.**
- "No supported connection found" is a legitimate, publishable outcome. State it
  plainly and quantify what was ruled out.

## 6. Scope every claim

- Separate **per-test claims** from **family-level verdicts**. A defect in one
  test does not invalidate the family verdict unless it actually propagates.
- State scope explicitly: what the result covers and what it does not.
- Supersede, never rewrite. When a conclusion changes, keep the original visible
  and record what changed and why.

## 7. Reporting rules

- Numbers with units and uncertainty. Never a bare decimal.
- The actual command run and its actual output.
- Failed checks reported as failures, with their count.
- Confidence stated honestly: verified, probable, or unknown. Not false
  precision, not hedging every sentence.

## 8. Audit mechanism limits

Append-only logs are used where appropriate **without claiming they are tamper-proof**.
The limits of the audit mechanism are documented. Scripts must be deterministic
where feasible and must fail visibly when required information is missing.

## 9. Anti-anthropomorphism

- Do not infer subjective experience from external measurements.
- Use neuroscience as evidence and inspiration, **not as proof** that a
  computational imitation produces equivalent subjective experience.
- Do not falsely classify all memory retrieval as incompatible with consciousness.
  The actual question is whether the architecture's operation and causal
  organization are sufficient for the properties under investigation.
- Do not claim to have inspected a repository's code unless the code was
  actually inspected.
- Do not claim an experiment was reproduced unless it was actually executed and
  its results recorded.
- Do not invent search results, citations, paper contents, URLs, or publication
  details.
- Do not state that the entire internet has been searched. Describe the actual
  scope of coverage and what remains inaccessible.