# Statement validation record

Item: `S56-M-1241-STATEMENT`  
Base revision: `d1615c5f63fce7e4aa25060da18e8fa27ebf3c9e`

## Frozen target

`Stage1Instances.THM_M_1241.GagliardoNirenbergTarget` is a transcription of Nirenberg's theorem
on page 125, formulae (2.2)--(2.3), in *On elliptic partial differential equations*, Annali della
Scuola Normale Superiore di Pisa (3) 13(2), 1959, 115--162. The stable NUMDAM scan has SHA-256
`cd76d6de19f77a7f27d44909c2c00cafbb5fb165a6587b4ff8d86dd13ff7eb3e`.

The Lean target fixes real functions on `EuclideanSpace Real (Fin n)`, classical iterated partial
derivatives, Lebesgue `eLpNorm`, the source's scaling equation and interval `j/m <= a <= 1`, a
constant uniform in `u`, and both printed exceptional cases. Source fidelity and errata review are
not promoted here; they remain work for the dependent anchor/source audit.

## Commands and results

All commands ran inside this worker clone. Lean commands ran from `Formalizations/Lean` using the
existing pinned `.lake` environment; no dependency update or fetch was performed.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1241/Statement.lean` | 0 | exact target, checked reflexive expansion, and four structural mutations elaborated; explicit target expression printed |
| `python3 ../../Stage1_Instances/THM-M-1241/check_statement.py` | 0 | expression SHA-256 `bf613985e300aa3a5b5e8299a1e0e0e059369387e17c7f0d2c92dc8d8190eb82`; all four mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `git -C .lake/packages/mathlib rev-parse HEAD` | 0 | pinned mathlib `8a178386ffc0f5fef0b77738bb5449d50efeea95` |
| `python3 -m json.tool Stage1_Instances/THM-M-1241/statement.json` | 0 | structured statement artifact is valid JSON |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets validated |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-1241` | 0 | rank 422, planned, L0/rework-required, theorem incomplete |
| `git diff --check -- Stage1_Instances/THM-M-1241 .stage1-worker-selftest.json` | 0 | no whitespace errors |

The validator rejects removal of the lower `a` bound, specialization to one dimension, moving the
constant under the function binder, and deleting the endpoint exceptions. This is statement-only
evidence pending master acceptance. It does not prove the inequality or advance any dependent node.
