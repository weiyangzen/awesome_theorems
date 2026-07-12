# Anchor-audit validation

Item: `S56-M-1026-ANCHOR_AUDIT`  
Base revision: `f8f0785bee9e7e4be4cc3096162cde337683261a`

## Result

The exact local target remains `M4`: no Lean proof candidate for the stable-law/domain-of-attraction
biconditional was found. Pinned mathlib supplies characteristic functions of convolutions, Levy
convergence, and the ordinary finite-variance Gaussian CLT. These are useful infrastructure but do
not establish stability, the necessity direction, or the converse attraction construction.

The four Sourcegraph responses and four GitHub repository responses were captured and content
hashed on 2026-07-12. They returned no candidate. GitHub code search returned HTTP 401, so this audit
records that lane as blocked rather than treating it as negative evidence. No dependency was fetched,
cloned, installed, updated, or built.

## Commands and results

| Command | Exit/result |
|---|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0; 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0; 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1026` | 0; rank 502, planned, hard anchor/wrapper lane, theorem incomplete |
| `rg -n -i 'stable law|stable distribution|domain.?of.?attraction|generalized central limit' Formalizations/Lean/.lake/packages/mathlib/Mathlib Stage1_Instances --glob '*.lean'` | 0; no exact mathlib theorem; local hits are statements and unrelated uses of "stable" |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1026/AnchorAudit.lean` | 0; all five declarations resolved; printed axiom sets contain only `propext`, `Classical.choice`, and `Quot.sound` |
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1026/Statement.lean` | 0; frozen exact target still elaborates |
| Four Sourcegraph archived/fork-inclusive public Lean queries recorded in `anchor-audit.json` | HTTP 200; every response reports `matchCount=0`; exact response hashes recorded |
| Four GitHub REST repository queries recorded in `anchor-audit.json` | HTTP 200; every response reports `total_count=0`, `incomplete_results=false`; response hash recorded |
| GitHub REST code query `"stable distribution" language:Lean` | HTTP 401 `Requires authentication`; blocked, not counted as a negative result |
| `python3 -m json.tool Stage1_Instances/THM-M-1026/anchor-audit.json >/dev/null` | 0; structured audit is valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1026 .stage1-worker-selftest.json` | 0; no whitespace errors |

This completes only the bounded formal-anchor audit, pending master acceptance. Human primary-source
pinpointing remains open, as do the obligation tree, proof, theorem validation, and release gates.
