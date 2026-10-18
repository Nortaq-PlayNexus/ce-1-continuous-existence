# datasets/ — external data CE-1 would need

**Status: EMPTY BY DESIGN, documented per master directive §7**
("Do not create empty files merely to satisfy a checklist" — the same principle
applied to directories.)

## Why there is no data here yet

Every experiment run so far in CE-1 has been **prompt-based**: a fixed task
prompt, scored by keyword presence. No dataset is required to run them, and
none was used. `scripts/validate_research_artifacts.py` flags this directory as
empty so the gap stays visible rather than being forgotten.

## What Stage 1+ will actually need

Adding any of the following requires recording: source URL, licence, version,
content hash, and access date, in a manifest — not just dropping a file here.

| Candidate | Why CE-1 would want it | Licence / access concern |
|---|---|---|
| Long-horizon conversational agent benchmarks (e.g. LoCoMo-style multi-session chat) | H2, H3 — measuring durable change and resumption needs multi-session ground truth | **Check each licence individually.** Some are research-only; several require registration. |
| Narrative/story comprehension sets with human annotations | Gives the "reliving" claim something external to compare against | Varies; some are non-commercial. |
| Code-repair corpora (e.g. BugsInPy-style) | H1/H2 — tasks with objectively checkable outcomes, unlike keyword scoring | BugsInPy is MIT; confirm per project. |
| Anesthesia / disorders-of-consciousness EEG or imaging datasets | E-section ground truth for what unconsciousness looks like | **Frequently restricted.** Human-subject data often requires a data-use agreement. Not appropriate for this programme without review. |
| Any dataset containing personal data | — | **Directive §10 forbids copying personal data into CE-1.** Do not. |

## Explicit non-goals

- No large model checkpoints. Directive §7: "Do not download enormous datasets
  or install large model dependencies without justification."
- No scraped conversation logs of real users. That is private data.
- No dataset acquired before a protocol states which hypothesis it serves.

## Rule

A dataset enters this directory only with a row in
`sources/SOURCE_MANIFEST.jsonl` (as `source_type: "dataset"`) recording its
licence, hash, and access date. If it cannot be licensed, it does not enter.