# ACCESS_LIMITATIONS.md — what CE-1 could not reach, and why

**Date:** 2026-10-18
**Directive requirement:** section 5 — "If a website, repository, or database
cannot be accessed, record that limitation and continue with available
sources." and "Do not state that the entire internet has been searched."

## Coverage is currently very narrow, and that is a finding

The source manifest contains **4 records**. The master directive (section 4)
names **six** research areas and dozens of specific systems. Four sources do not
constitute a literature review. This file records exactly what is missing so
nobody mistakes a thin manifest for a finished one.

## What was verified (see `SOURCE_MANIFEST.jsonl`)

| Source | Status | Verification |
|---|---|---|
| Butlin et al. 2023, AI consciousness indicators | verified, DOI confirmed | abstract read |
| Cogitate Consortium 2025, Nature, IIT vs GNWT | verified, DOI confirmed | full text read |
| Albantakis et al. 2023, IIT 4.0 | verified, DOI confirmed | abstract read |
| Packer et al. 2023, MemGPT | verified, DOI confirmed | full text read |

## Not yet searched — required by directive section 4

| Area | Required by | Status |
|---|---|---|
| Recurrent Processing Theory primary literature (Lamme) | 4A | **not searched** |
| Attention Schema Theory (Graziano) | 4A | **not searched** |
| Higher-Order Theories (Rosenthal, Lau) | 4A | **not searched** |
| Predictive processing / active inference (Friston, Clark) | 4A | **not searched** |
| Biological naturalism (Searle) and other competing positions | 4A | **not searched** |
| Embodied / enactive approaches (Thompson, Di Paolo) | 4A | **not searched** |
| Butlin et al. 2024 "Taking AI Welfare Seriously" | 4B, 10 | **not searched** |
| Post-2025 adversarial-collaboration responses and replications | 4B | **not searched** |
| Mem0, Zep/Graphiti — cited in RESEARCH_MAP.md with **no citation at all** | 4C | **not searched** |
| Letta (as distinct from MemGPT) current documentation | 4C | **not searched** |
| Catastrophic forgetting / continual learning literature | 4D | **not searched** |
| Sleep, memory consolidation, disorders of consciousness | 4E | **not searched** |

## Access limitations encountered

1. **No scholarly database access.** No Scopus, Web of Science, PubMed
   subscription, or institutional proxy was used or available. Verification
   relied on open sources: arXiv, publisher landing pages, Crossref-style DOIs,
   PubMed Central, and preprint servers.
2. **Two grade-A-eligible sources were only read at abstract level** (IIT 4.0
   and Butlin 2023). They are graded B accordingly. Reaching grade A requires
   reading the full formal derivation / full report.
3. **Paywalled full texts were not obtained** for works referenced by the
   sources above. Their bibliographies are recorded as leads, not as verified
   entries.
4. **No claim is made about non-indexed or paywalled grey literature**, which
   is extensive in this field.
5. **arXiv DOIs (10.48550/arXiv.*) are DataCite-issued**, not publisher DOIs.
   They are stable identifiers but do not indicate peer review.

## Two specific factual errors found in the inherited documents

1. **IIT was silently miscategorised.** `research/RESEARCH_MAP.md` lists IIT
   alongside GWT, HOT, RPT and PP as a parallel candidate theory without
   recording that the principal AI-consciousness indicator framework (Butlin
   et al. 2023) *deliberately excludes* IIT on the grounds that IIT is
   incompatible with computational functionalism. Those are different
   theoretical commitments, not adjacent options.

2. **IIT is described as merely "controversial".** The map does not record that
   the 2025 preregistered adversarial collaboration found IIT's posterior-cortex
   synchrony prediction was **not met** (Bayes factor 1.15–4.9 for the null) —
   a stronger statement than "controversial".

## Standing caveat

No source in this manifest concerns an artificial system achieving subjective
experience. `butlin2023cai` concludes no current AI system is a strong
candidate; `cogitate2025` challenged both leading theories rather than
validating either. **Nothing found so far supports the H7 position, and
nothing falsifies it.** The programme must not present this thin, early-stage
coverage as a completed review.