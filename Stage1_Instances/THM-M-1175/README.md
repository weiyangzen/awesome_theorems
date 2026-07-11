# THM-M-1175 rev-5.6 intake

This is a `planned` intake for the repository claim "Harnack inequality (divergence form)". The
metadata does not specify the operator, weak-solution space, ellipticity bounds, domain geometry,
or the two regions compared by the inequality. Those choices materially change the theorem, so
this intake does not silently select a textbook variant.

## Scope map

| Surface | In scope | Intake boundary |
|---|---|---|
| Equation | A second-order divergence-form elliptic equation, provisionally `div (A grad u) = 0` | Scalar/matrix coefficients, symmetry, measurability, and weak formulation remain to be frozen |
| Ellipticity | Uniform lower and upper bounds with positive constants | Exact norm, almost-everywhere quantification, and coefficient codomain remain open |
| Solution | Nonnegative weak solution | Sobolev space, representative, and whether positivity is strict remain open |
| Geometry | An interior subdomain or concentric smaller ball compactly contained in the equation domain | Shape, radii, dimension, and boundary distance must be sourced |
| Conclusion | An essential-supremum/essential-infimum comparison with a constant controlled by structural data | Ordinary versus essential extrema and exact constant dependencies remain open |
| Exclusions | Parabolic, non-divergence-form, boundary, discrete, and harmonic-function-only Harnack results | None may substitute for the divergence-form elliptic root |
| Formal system | Lean 4 plus pinned mathlib | No Lean declaration, imports, expression hash, or environment fingerprint is credited at intake |

The source-statement choices are itemized in `source_statement_crosswalk.md`. `task-dag.json`
keeps all dependent rev-5.6 phases open.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H3, M4, R3]`. The first failed theorem gate is
exact-source identification: the one-line repository gloss underdetermines the mathematical claim.
No statement elaboration, source acceptance, audit completion, or theorem completion is claimed.

