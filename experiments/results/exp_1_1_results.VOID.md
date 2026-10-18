# VOID — DO NOT CITE AS DATA

This file has been **withdrawn by the independent audit of 2026-10-18**.

It is retained unmodified for provenance (see `research/RESEARCH_AUDIT.md` §2),
but it is **not a result**. All six model outputs recorded below are the empty
string `""`, so every quality check scored 0 by construction:

    any(k in "" for k in [...])  ->  False, for every check

The recorded `h1_supported: false` therefore measures the instrument returning
nothing. It is **not** evidence about H1 in either direction.

Why the empty output is unexplained: running the script's own `query_llm()`
against the same model and daemon (Ollama 0.34.2, `qwen3:4b`) returns a
4,526-character response with `done_reason: "length"`. The code as it stands
does not reproduce this file. Either the daemon or model behaviour differed at
2026-10-18T07:32:05+1100, or the file was written without executing the queries.

Re-running the experiment **with the control the protocol omitted** (an
unrelated, length-comparable episode) shows the claimed effect does not
reproduce:

              run 1     run 2     run 3
    B - A    +1.33     +0.67     +0.67
    C - A    -0.67     +0.33     -0.67   <-- control changes sign
    B - C    +2.00     +1.33     +1.33

Baseline mean is 2.40 at both `num_predict=1000` and `num_predict=4000`, so the
effect lies inside baseline variance. Every response is truncated
(`done_reason=length`), so all scores are computed on incomplete text.

**Correct status: INCONCLUSIVE due to instrument defect.**
H1 is neither supported nor falsified by this experiment.

A working re-run with the control lives in `verify_exp_1_1.json` in this
directory, produced by `scripts/verify_exp_1_1.py`.
