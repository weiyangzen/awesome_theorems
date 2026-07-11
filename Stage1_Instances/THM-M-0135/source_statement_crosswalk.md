# Source-statement crosswalk

| Claim component | Human source anchor | Lean candidate | Intake assessment |
|---|---|---|---|
| Affine-root-system identity family | I. G. Macdonald, *Affine root systems and Dedekind's eta-function*, Inventiones Mathematicae 15 (1972), 91-143, DOI `10.1007/BF01418931` | no exact declaration selected | Primary bibliographic source identified, but the repository wording gives no theorem/equation/page pinpoint; `H2` only |
| Root data and multiplicities | Definitions and conventions in the same paper | legacy `AffineRootDatum` in `S1_M_051.lean` | Local wrapper is discovery material; field-for-field source fidelity is unaudited |
| Infinite denominator product | A numbered source formula must determine roots, multiplicities, coefficient ring, and completion | legacy `ExpressionRing := AddMonoidAlgebra Z Weight` | Finite-support algebra cannot by itself represent the completed infinite product; not an exact encoding |
| Alternating Weyl expression | A numbered source formula must determine action, sign, shift, and normalization | `CoxeterSystem.length_mul_mod_two` is only an adjacent parity anchor | Ingredient-level candidate, not root closure |
| Eta-function specialization | Paper title and identity family indicate specializations | none | Possible alternate theorem, not interchangeable until a checked transport is supplied |
| Equality shape | Product side equals sum/specialized side | legacy `StatementShape D` | Shape only: both sides are unconstrained structure fields, so it neither constructs nor proves the classical identity |

The metadata phrase "Macdonald identity" is underdetermined. The statement phase must choose one
numbered identity and record the scanned/digital edition hash, exact pages/equation, definitions,
assumptions, errata search, and a node-by-node premise crosswalk. It must then choose a formal-series
completion in which both sides are defined and prove checked transports for any specialization.

No claim of `H0` or exact Lean elaboration is made. The legacy source label `已验证` and historical
Lean file are discovery inputs only. No public machine-checked full Macdonald identity has been
established by this intake, so the current machine classification remains formalization debt rather
than repo-local closure.
