# Model Qualification Results — 2026-10-21

## Purpose
The model qualification suite is a **gate**, not an experiment. It establishes
that a model can complete short structured-output tasks without truncation
before that model is used in a confirmatory run. It is evidence about
instruction following, not about memory, continuity, consciousness or selfhood.

Protocol: `experiments/model_qualification/qualification_protocol.md`.
Suite: 24 fixed items, 6 categories, frozen.

## Results

| Model | Verdict | Valid pass | Valid fail | Invalid | Truncated | Wall clock |
|---|---|---:|---:|---:|---:|---:|
| gemma3:4b (2026-10-20) | **QUALIFIED** | 23/24 | 1 | 0 | 0 | ~2 min |
| qwen3:4b (2026-10-21) | **INVALID_RUN** | 0/24 | 0 | 24 | 12 | 74 min |
| dolphin-llama3:latest (2026-10-21) | **QUALIFIED** | 21/24 | 3 | 0 | 0 | ~4 min |

Artifacts: `experiments/model_qualification/results/{model}_verdict.json`.

## qwen3:4b — why it is INVALID_RUN, not merely weak

The run produced 12 trials with `done_reason="length"`, 10 with
`done_reason="error"` (300 s timeout) and 2 with `done_reason="stop"`.

The cause is visible in the raw responses: qwen3 is a *reasoning* model. It
opens a long deliberation before producing the JSON object, exhausts the
`num_predict: 300` budget, and the response is truncated before the answer
arrives. The protocol's disqualification rule is explicit — "if a model
truncates even once, it is not qualified" — and raising the token budget to
accommodate it is explicitly ruled out. Every trial is therefore INVALID, and
the run is INVALID_RUN rather than NOT_QUALIFIED because there is no valid
data left to judge.

The second-order cost was throughput: 74 minutes for 24 trials on this
CPU-only host, because every truncated trial still had to generate its full
300 tokens. At that rate the 216-trial continuity_v1 replication would have
taken roughly 11 hours.

## dolphin-llama3:latest — the second model

dolphin-llama3 passes the gate with 21/24 valid passes, 3 valid failures, 0
invalid trials and 0 truncations, meeting every threshold
(evidence extraction 21/24 = 87.5% against a required 21/24; valid JSON 24/24
against a required 23/24).

It is a Llama-3 8B model, instruction-tuned, non-reasoning: it answers in
the requested JSON shape directly, which is why it neither truncates nor
stalls.

## Host constraint discovered on 2026-10-21

Ollama 0.34.2 on this machine **hangs during GPU discovery** (`discovering
available GPUs...` never completes against the GTX 1080), after which it
accepts generation requests and never answers them. The server runs
correctly with:

```
OLLAMA_LLM_LIBRARY=cpu
OLLAMA_NUM_GPU=0
OLLAMA_VULKAN=false
OLLAMA_NO_CLOUD=1
OLLAMA_CONTEXT_LENGTH=131072
```

The context length is set to 131072 to match the configuration used for the
recorded 2026-10-20 confirmatory run, so the replication is not confounded by
a different context window. Note that the recorded 2026-10-20 run was produced
with the GPU-enabled server; the 2026-10-21 runs used CPU-only inference. This
is recorded as a configuration difference between the original and the
replications.

## Consequence for the research programme

- **gemma3:4b** — qualified, used for the confirmatory H8 run and its
  same-model reproduction.
- **dolphin-llama3:latest** — qualified, used for the preregistered H8
  second-model replication.
- **qwen3:4b** — disqualified. It remains the model of record for the
  voided Experiments 1.1 and 1.2, where the same truncation behaviour was
  observed (all 30 trials truncated at num_predict=1000). That is a
  consistent, independently observed property of the model, not a fluke.
