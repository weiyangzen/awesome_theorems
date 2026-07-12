# Statement validation record

Item: `S56-M-0041-STATEMENT`  
Base revision: `0ea006c25dcbfe400adbb084c0a3476a9b271741` (tree
`ff2e3bde08d7f5d6c83519160a4a6bd2cb7526db`).

## Frozen target

`Stage1Instances.THM_M_0041.CayleyHamiltonTarget` quantifies over an arbitrary commutative ring,
arbitrary finite decidable index type, and arbitrary square matrix. Its conclusion is evaluation at
that matrix of `det (X I - A)`, equal to the zero matrix. Empty index types and the zero ring remain
in scope.

The target imports only `Mathlib.Algebra.Polynomial.AlgebraMap` and
`Mathlib.LinearAlgebra.Matrix.Determinant.Basic`. It does not import `Charpoly.Basic`; Lean therefore
confirms `Matrix.charpoly` and `Matrix.aeval_self_charpoly` are unavailable. The checked transport
and proof-body audit belong to the dependent anchor-audit node.

## Commands and results

All commands ran in this worker clone. Lean used the existing pinned Lake artifacts read-only. No
dependency update, build, clone, fetch, or other `.lake` mutation was performed.

| Command | Exit | Result |
|---|---:|---|
| `python3 Docs/tools/check_stage1_standard.py` | 0 | all 15 assurance groups and 1546 uniform-L0 targets passed |
| `python3 scripts/stage1_target.py check` | 0 | 1546 unique targets, ranks 1 through 1546, all L0/rework-required |
| `python3 scripts/stage1_target.py show THM-M-0041` | 0 | rank 1081, planned, legacy artifacts unaccepted, theorem incomplete |
| `lake env lean ../../Stage1_Instances/THM-M-0041/Statement.lean` from `Formalizations/Lean` | 0 | target and three structural mutations elaborated; expected identity and unavailable-candidate failures occurred; explicit target printed |
| `python3 ../../Stage1_Instances/THM-M-0041/check_statement.py` from `Formalizations/Lean` | 0 | expression SHA-256 `5aad8415...e711`; literal removed-hypothesis failure, three distinct mutations, both import deletions, boundaries, pins, metadata, receipt, and handoff agree |
| `lake env lean ../../Stage1_Instances/THM-M-0041/BoundaryProbe.lean` from `Formalizations/Lean` | 0 | exact expression elaborated for empty matrices and for matrices over the zero ring `PUnit`; empty output |
| `lake env lean --version` and `lake --version` | 0 | Lean 4.29.0 commit `98dc76e3...`; Lake `5.0.0-src+98dc76e` |
| `python3 -m json.tool Stage1_Instances/THM-M-0041/instance.json` and likewise for `task-dag.json`, `statement.json`, `statement-receipt.json`, and `.stage1-worker-selftest.json` | 0 | all five structured artifacts parse |
| `rg -n '\b(sorry\|admit\|sorryAx)\b\|^[[:space:]]*(axiom\|constant\|opaque\|unsafe)[[:space:]]' Stage1_Instances/THM-M-0041 -g '*.lean'` | 1 | expected no-match exit; no placeholder, custom axiom, opaque, or unsafe declaration |
| `git diff --check -- Stage1_Instances/THM-M-0041 .stage1-worker-selftest.json` | 0 | no whitespace errors |

## Mutation and evidence boundary

Removing `CommRing R` makes the exact expression ill-typed, and the validator requires Lean to
reject that literal mutation. The other fixtures specialize the coefficient domain to fields,
change the matrix binder to existential, or add `Nontrivial R` and `Nonempty n`; Lean rejects each
as an inhabitant of the canonical proposition, and their explicit expression hashes differ.

This is statement-only evidence pending master acceptance. It proves no inhabitant of the target
and gives no source-fidelity, anchor, proof, audit-completion, or theorem-completion credit. The old
intake checker binds the earlier nine-file intake snapshot and is not cited as current evidence.
