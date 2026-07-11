# THM-M-1528 rev-5.6 intake

This directory is the rev-5.6 `planned` instance for the Einstein field equations. It treats the
generated phrase "the basic equations of general relativity" as a theorem-family label, not as a
proof or as a uniquely specified theorem. Historical Stage1 artifacts are discovery inputs only.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Equation family | `G + Lambda g = kappa T`, with `G = Ric - (R/2)g` | Sign, curvature, metric-signature, units, dimension, and constant conventions remain to be frozen |
| Geometric objects | smooth Lorentzian spacetime, Levi-Civita connection, Ricci and scalar curvature | Exact regularity, universes, tensor bundles, and nondegeneracy predicates are open |
| Matter side | supplied symmetric stress-energy tensor, possibly with conservation/field-model assumptions | No particular matter model or field equations are selected |
| Logical force | an equation/predicate on supplied geometric and matter data | The label alone does not say existence, uniqueness, derivation from an action, or equivalence to a PDE system |
| Degenerate branches | vacuum (`T = 0`) and zero cosmological constant (`Lambda = 0`) as specializations | These are not substitutes for the general equation |
| Lean discovery | legacy `AwesomeTheorems.Stage1.S1_M_196` pointwise algebra and abstract statement shape | No legacy declaration or proof credit is inherited; exact elaboration belongs to the statement phase |
| Trust boundary | Lean 4 kernel plus pinned mathlib | Toolchain, dependency, foundation, TCB, and computation fingerprints remain open |

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H2, M3, R3]`. The human statement is not yet
unique because the repository label omits conventions and logical force. The first failed gate is
the exact-source statement gate; consequently no canonical Lean expression, proof closure, or
theorem completion is claimed. The dependent statement phase must either freeze a sourced equation
predicate with explicit conventions or keep `M3/M4` and report the ambiguity.

## Open task DAG

`statement -> anchor audit -> obligation tree -> proof -> validation -> release`. Each edge is the
corresponding dependency in `Docs/Stage1_Blueprint_rev-5.6.md`; this intake closes none of those
nodes. Source and statement decisions are itemized in `source_statement_crosswalk.md`.

