# Statement validation record

Item: `S56-M-1026-STATEMENT`  
Base revision: `97a7eb41befd3d09707663f246a3133706a9be08`

## Frozen target

`Stage1Instances.THM_M_1026.Statement` freezes the one-dimensional generalized central limit
theorem at the law level: a nondegenerate Borel probability law on `Real` is stable exactly when
it attracts the positively scaled and centered convolution powers of some Borel probability law.
Weak convergence is expressed by convergence of integrals of every bounded continuous real test
function. Stability quantifies over every convolution power `n >= 2`; scales are strictly positive.

The sole direct import is `Mathlib.MeasureTheory.Integral.BoundedContinuousFunction`. Removing it
fails because the bounded-continuous-function/integration surface is unavailable. The convolution
API is already transitively available, so a separate convolution import was tested and removed.

## Commands and results

All commands ran in this worker clone on 2026-07-12. Lean used the existing pinned Lake artifacts;
no dependency was fetched, updated, or built.

| Command | Exit | Result |
|---|---:|---|
| `cd Formalizations/Lean && lake env lean ../../Stage1_Instances/THM-M-1026/Statement.lean` | 0 | target, definitional transport, and four mutations elaborated and printed |
| `python3 Stage1_Instances/THM-M-1026/check_statement.py` | 0 | expression SHA-256 `e39476697d12d054b84ab39c07251418d449ba5ea094c2bb37df9850c7caff93`; four mutations distinguished |
| `cd Formalizations/Lean && lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1026` | 0 | rank 502, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1026/statement.json` | 0 | structured statement record is valid JSON |
| `! rg -n '\b(sorry\|admit\|axiom)\b\|sorryAx' Stage1_Instances/THM-M-1026/Statement.lean` | 0 | no proof-gap declaration in the Lean source; the validator independently enforces the same policy |
| `git diff --check -- Stage1_Instances/THM-M-1026 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Mutation and status boundary

The validator fingerprints Lean's printed elaborated root and distinguishes removal of the
nondegeneracy hypothesis, admission of zero scales, substitution of a degenerate point-mass target,
and replacement of the biconditional by its necessity direction. The fully expanded encoding is
connected to the public target by the checked theorem `statement_iff_expanded`.

The exact primary-source edition, theorem/page, assumption crosswalk, and errata review remain open
on the H axis. So do the anchor audit, obligation registry, proof, hermetic replay, and independent
review. This node supplies statement elaboration only, pending master acceptance.
