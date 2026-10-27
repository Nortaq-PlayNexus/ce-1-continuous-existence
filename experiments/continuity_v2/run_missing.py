#!/usr/bin/env python3
"""Run only the missing v2 scenarios."""
from __future__ import annotations
import argparse, hashlib, json, random, sys, time, urllib.error, urllib.request
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
BENCH = ROOT / "benchmarks" / "continuity_v2"
SCN = BENCH / "scenarios.jsonl"
RET = BENCH / "retrieval_sets.jsonl"
OLLAMA = "http://127.0.0.1:11434/api/generate"
MISSING = ["CO_004","CO_037","CO_038","CO_045","JU_053","JU_057","RA_033",
           "SA_074","SA_075","SA_077","SA_079","SA_083","SO_063","SO_071"]
def load(p): return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]
scns={s["scenario_id"]:s for s in load(SCN)}
rs={r["scenario_id"]:r for r in load(RET)}
from experiments.continuity_v2.run_continuity_v2 import build_prompt
CONDITIONS=["correct_retrieval","contradicting_decoy","no_memory"]
records=[]
for sid in MISSING:
    s=scns[sid]; r=rs[sid]
    for cond in CONDITIONS:
        prompt=build_prompt(s,cond,r)
        t0=time.time()
        try:
            body=json.dumps({"model":"gemma3:4b","prompt":prompt,"stream":False,"think":False,"options":{"temperature":0.0,"num_predict":300}}).encode()
            req=urllib.request.Request(OLLAMA,data=body,headers={"Content-Type":"application/json"})
            with urllib.request.urlopen(req,timeout=300) as resp:
                res=json.loads(resp.read().decode())
            raw=res.get("response",""); dr=res.get("done_reason"); trunc=dr=="length"
        except Exception as e:
            raw,dr,trunc="", "error", False
        records.append({"scenario_id":sid,"category":s["category"],"condition":cond,
            "prompt_hash":hashlib.sha256(prompt.encode()).hexdigest()[:16],
            "raw_response":raw,"done_reason":dr,"is_truncated":trunc,
            "elapsed":round(time.time()-t0,3),"run_id":"v2-missing","model":"gemma3:4b",
            "timestamp":time.strftime("%Y-%m-%dT%H:%M:%SZ",time.gmtime()),
            "temperature":0.0,"num_predict":300,"seed":20261020})
        print(f"  {sid} {cond} {dr} {round(time.time()-t0,1)}s",flush=True)
Path("experiments/continuity_v2/results/chunk_missing.jsonl").write_text("\n".join(json.dumps(r) for r in records)+"\n",encoding="utf-8")
print("Wrote",len(records),"records")
PY