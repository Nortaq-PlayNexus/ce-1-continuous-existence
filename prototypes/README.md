# prototypes/ — testable implementations

**Status: EMPTY BY DESIGN, documented per master directive §7.**

## Why there is nothing here yet

Directive §7 warns: *"Do not build a large speculative framework when a small
experiment would test the hypothesis more effectively."*

CE-1 has **not yet earned a prototype.** The audit
(`research/RESEARCH_AUDIT.md` §12e) established that the current experiments
measure *in-context priming*, not persistent cognitive state, because no state
is ever manipulated. Building a persistent-state architecture now — before the
programme can state what "state" means operationally and how it will be
ablated — would produce exactly the kind of unfalsifiable speculative artifact
the directive forbids.

The two experiments that exist (`exp_1_1_ablation.py`,
`exp_1_2_ablation.py`) live in `experiments/`, not here, because they are
instruments for testing claims, not candidate architectures.

## What must be true before anything lands here

1. **A falsifiable hypothesis.** Not "build a continuous-existence agent" but
   a specific claim with a stated measurement and a stated failure condition.
2. **An ablation that removes state.** Per `RESEARCH_AUDIT.md` §12e, a design
   that only ever *adds* context cannot test H1. The prototype must expose a
   switch that **removes or corrupts** persistent state and show behaviour
   changes.
3. **A preregistered protocol** in `experiments/` with thresholds fixed before
   execution — not the post-hoc `>= 1.0` that decided exp_1_2's verdict by
   2×10⁻¹⁶ of floating-point error.
4. **A README** stating scientific purpose, assumptions, limitations, execution
   instructions, and tests (directive §11).

## Candidate direction, for discussion only

The audit's §12e suggests the minimum viable H1 test: hold the prompt
byte-identical and vary only **whether retrieval populated it** — a populated
store, an emptied store, and an unrelated store. That is a harness, not an
architecture, and it would live in `experiments/`.

A genuine prototype would need state that is **causally upstream of
computation** rather than restatable as text. Whether that is achievable
without training a model is an open engineering question and is recorded in
`architecture/PERSISTENT_STATE_DESIGN.md`.

## Required layout for anything that does land here

```
prototypes/<name>/
  README.md        # purpose, assumptions, limitations, how to run, tests
  <implementation>
  test_<name>.py   # tests must be runnable and must pass
```

No prototype is committed without a passing test suite and a README that states
what it **cannot** establish.