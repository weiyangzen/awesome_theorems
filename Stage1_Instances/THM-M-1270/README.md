# THM-M-1270 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for Ekeland's variational principle. It does not
inherit proof credit or accepted state from the generated source label `已验证`.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | The complete-metric-space, lower-semicontinuous, bounded-below variational principle | Parameter conventions and exact Lean expression belong to the dependent statement phase |
| Objects | A nonempty complete metric space `X`, an extended-real-valued objective `f`, and positive parameters `epsilon` and `lambda` | The codomain (`Real` versus `EReal`) and treatment of properness are not yet selected |
| Input | An `epsilon`-approximate minimizer `u` | The precise infimum inequality and strict/non-strict convention remain to be frozen |
| Witness | A point `v` no worse than `u`, within `lambda` of `u`, satisfying the strict perturbed-minimality inequality away from `v` | No witness construction or proof is credited |
| Equivalent forms | Caristi ordering, one-parameter normalization, minimization of a perturbed objective | Candidate transports only; none is accepted as equivalent at intake |
| Foundations | Lean 4 kernel, pinned mathlib, classical choice, completeness and extended-real order APIs | Exact toolchain, imports, axioms, and dependency closure remain open |

The scope deliberately concerns the abstract variational principle, not a PDE existence theorem or
an application obtained from it. The provisional human statement, ordered assumptions, exclusions,
and candidate formal shape are structured in `intake.json`. Source fidelity work is separated in
`source_statement_crosswalk.md`.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.
Only `INTAKE` is addressed here. All dependent nodes remain open and retain their rev-5.6 gates.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact-statement gate: there is no elaborated Lean declaration, normalized expression hash,
environment fingerprint, checked encoding transport, or mutation record. The theorem is not
complete.

## Validation

On base revision `61369637c5db864082a624c34c62a91e6741f9da`, the worker ran the commands recorded
in `validation.md`. They establish target membership, repository-standard consistency, JSON syntax,
and dossier-local integrity only.
