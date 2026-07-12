# Statement validation record

Item: `S56-M-1526-STATEMENT`  
Base revision: `33a031b5238cc674b8e1073106bff2685c6bbbc4`

## Frozen target

`Stage1Instances.THM_M_1526.FreeDiracFactorizationTarget` is the exact intake-selected free
Dirac factorization and Klein-Gordon consequence. Its abstract complex-linear endomorphisms are a
deliberate domain-safe interface: a concrete function space must supply the Clifford and commuting
derivative laws rather than hiding the conclusion in a structure field. The target includes zero
mass and does not substitute the legacy finite Pauli-matrix leaf for the analytic claim.

The imports were narrowed to `Mathlib.LinearAlgebra.Matrix.ToLin` and
`Mathlib.Data.Complex.Basic`; the former is the smallest materialized pinned linear-map module found
in this worker cache. No dependency fetch or `.lake` mutation was performed.

## Commands and results

Commands ran in this worker clone. Lean commands used `Formalizations/Lean` as their working
directory and the existing pinned Lake environment.

| Command | Exit | Result |
|---|---:|---|
| `lake env lean ../../Stage1_Instances/THM-M-1526/Statement.lean` | 0 | canonical target, checked alternate name, four mutations, and zero-mass constructor elaborated; explicit expression printed |
| `python3 ../../Stage1_Instances/THM-M-1526/check_statement.py` | 0 | expression and file hashes matched; required hypothesis/domain/binder/boundary mutations distinguished |
| `lake env lean --version` | 0 | Lean 4.29.0, commit `98dc76e3c0a9b856c9b98726b713fb04fab16740` |
| `python3 Docs/tools/check_stage1_standard.py` | 0 | 15 assurance groups and 1546 uniform-L0 targets |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546 |
| `python3 scripts/stage1_target.py show THM-M-1526` | 0 | rank 194, planned, L0/rework-required, theorem incomplete |
| `python3 -m json.tool Stage1_Instances/THM-M-1526/statement.json` | 0 | valid JSON |
| `git diff --check -- Stage1_Instances/THM-M-1526` | 0 | no whitespace errors |

This is self-tested statement evidence pending master acceptance. The exact primary-source
equation/page and conventions remain at `H2`; proof, anchor audit, obligation tree, validation, and
release nodes remain open.
