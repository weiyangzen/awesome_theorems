# THM-M-1243 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Nash inequality. It starts at the uniform
`L0 / rework_required` baseline and does not inherit proof credit from the Stage0 label
`已验证`.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Historical root | Nash's Euclidean interpolation inequality relating the `L1`, `L2`, and Dirichlet-energy quantities of a function | The Stage0 phrase “entropy and energy” is too imprecise to freeze a normalization |
| Function class | Real-valued functions on Euclidean `R^n`, initially smooth and compactly supported; later extension to the appropriate Sobolev intersection | Exact measurability, integrability, weak-derivative, and dimension hypotheses belong to the statement phase |
| Quantitative content | Existence of a dimension-dependent positive constant; sharp-constant variants are excluded unless independently sourced | Constant normalization and exponent encoding remain open |
| Equivalent forms | Norm form and squared/integral form | Equivalence requires checked Lean transports; none is credited here |
| Degenerate cases | Zero function should satisfy the inequality; dimension zero and infinite quantities require explicit treatment | Boundary behavior must be mutation-tested before statement acceptance |
| Foundations | Lean 4 kernel, pinned mathlib analysis/measure/Sobolev APIs | Exact imports, toolchain, axioms, and dependency closure remain open |

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The primary historical paper is
identified, but the source pinpoint, assumptions, errata, and normalization have not been audited.
The first failed gate is exact-statement identification: neither the Stage0 wording nor this intake
chooses among mathematically related normalizations. Consequently there is no Lean declaration,
kernel closure, or theorem-completion claim.

The structured scope is in `intake.json`; source-to-statement ambiguity is recorded in
`source_statement_crosswalk.md`; exact self-test commands are in `validation.md`.
