# THM-M-1177 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Alexandrov-Bakelman-Pucci (ABP)
maximum estimate. It freezes one classical, drift-free linear form of the estimate; it does not
inherit proof credit from the Stage0 label `已验证`.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | ABP upper bound for a classical subsolution on a bounded domain in `R^n`, with measurable symmetric positive-definite coefficient field and zero boundary upper data | Constants, regularity encodings, and the contact-set definition must be elaborated in the statement phase |
| Geometry | Convex envelope of the positive part and its upper contact set; diameter and Lebesgue measure | No convex-envelope API or measurability result is credited |
| Analytic core | Gradient-image inclusion, area formula, Hessian determinant bound, and arithmetic-geometric mean | Architecture only; none is a closed Lean obligation |
| Coefficients | `A(x)` symmetric positive definite; estimate weighted by `(det A(x))^(-1/n)` | Uniform ellipticity and Pucci-extremal-operator corollaries are downstream variants, not the root |
| Boundary/degenerate cases | `u <= 0` on the boundary; empty domain and zero positive maximum must reduce trivially | Boundary topology and `n >= 1` require explicit Lean encodings |
| Foundations | Lean 4 kernel, pinned mathlib, classical finite-dimensional analysis and measure theory | Exact imports, choice use, TCB, and computation profile remain open |

The structured claim is in `intake.json`. Source genealogy and the component-level relationship to
the intended statement are recorded in `source_statement_crosswalk.md`.

## Statement freeze

`Statement.lean` now freezes and elaborates the exact classical ABP proposition selected here.
`statement.json` records the binder order, encoding decisions, pinned environment, expression hash,
and mutation results. This is a statement artifact only and contains no ABP proof.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact Lean statement gate in the intake record is superseded by the provisional statement
receipt, pending master acceptance. Source, proof, and release gates remain open, and the theorem is
not complete.

## Validation

The commands and results in `validation.md` establish target membership, standard consistency,
JSON syntax, and dossier-local hygiene only. Master acceptance and all dependent phases remain open.

## Obligation architecture

`obligation-registry.json` freezes the version-1 semantic denominator, while
`typed-graphs.json` keeps proof, refinement, provenance, evidence, trust, documentation, and
workflow edges distinct. `ObligationTree.lean` checks only the exact conditional composition of
the nonpositive-maximum and positive-maximum packages. The root remains open at `M4`; details and
the complete node ledger are in `obligation-tree.md`.
