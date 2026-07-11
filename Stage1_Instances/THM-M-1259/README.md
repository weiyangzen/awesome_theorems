# THM-M-1259 rev-5.6 intake

This directory is the `planned` instance for Hormander's theorem (subelliptic). The legacy Chinese
label and one-line description do not uniquely choose among the sum-of-squares hypoellipticity
theorem, the quantitative subelliptic estimate used in its proof, later finite-type variants, and
boundary formulations. Intake therefore records that ambiguity rather than inventing a precise
root.

## Scope map

| Surface | Provisional in-scope object | Intake boundary |
|---|---|---|
| Root family | Hormander's bracket-generating theorem for smooth real vector fields and a sum-of-squares second-order operator | Exact 1967 operator convention and theorem wording require source-page verification |
| Geometry | Open subsets of Euclidean space; Lie brackets span the tangent space locally | Manifolds may be a checked transport later, not a silent domain substitution |
| Analytic objects | Smooth vector fields, distributions, local Sobolev regularity, differential operators | A Lean object model has not been selected or elaborated |
| Quantitative branch | A localized subelliptic estimate with positive Sobolev gain | Gain, norms, compact supports, and lower-order terms must be stated exactly |
| Qualitative branch | Hypoellipticity: local smoothness of `P u` forces local smoothness of `u` | Equivalence with the estimate is not credited without a checked bridge |
| Exclusions | Boundary-value theorems, complex vector-field variants, elliptic special cases, finite-dimensional approximations | None may substitute for the root theorem |

The future proof architecture must expose at least: vector-field/differential-operator definitions,
iterated-bracket rank condition, localization, commutator estimates, the subelliptic estimate, the
Sobolev regularity bootstrap, and the final hypoellipticity wrapper. These are scope seeds only; the
obligation registry is intentionally deferred to its dependent phase.

## Intake verdict

Lifecycle is `planned` and the provisional root vector is `[H2, M4, R3]`. The first failed gate is
exact source-statement identification: the manifest name is underdetermined and no canonical Lean
expression exists. The statement phase must resolve the root against an immutable primary-source
copy before elaboration. This intake is self-tested, but the theorem is not complete.

## Validation

The exact commands and results for manifest membership, repository consistency, JSON parsing,
reference integrity, and whitespace checks are recorded in `validation.md`.
