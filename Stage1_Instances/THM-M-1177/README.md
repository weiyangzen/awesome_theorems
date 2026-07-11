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

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first failed theorem gate is
the exact Lean statement gate: this intake supplies no elaborated expression, environment
fingerprint, checked transport, or mutation result. The theorem is not complete.

## Validation

The commands and results in `validation.md` establish target membership, standard consistency,
JSON syntax, and dossier-local hygiene only. Master acceptance and all dependent phases remain open.
