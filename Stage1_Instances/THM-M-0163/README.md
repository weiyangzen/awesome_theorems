# THM-M-0163 rev-5.6 intake

This directory is the `planned` intake for the mathematical target "geodesic equation". The terse
repository gloss says only "the differential equation of shortest curves on a surface." The intake
freezes the standard Riemannian interpretation while preserving the important boundary: the
affinely parametrized geodesic equation is not an unrestricted characterization of global shortest
curves.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Geometric setting | A finite-dimensional smooth real Riemannian manifold, hence also a regular surface as a special case | Exact Lean manifold, chart, and universe parameters remain open |
| Intrinsic root | A `C2` curve is geodesic when its Levi-Civita covariant acceleration vanishes | No Lean predicate or elaborated expression is credited |
| Coordinate root | In a chart, every component obeys `gamma''^k + sum_ij Gamma^k_ij(gamma) gamma'^i gamma'^j = 0` | Christoffel-symbol conventions and the chart-to-intrinsic transport require checking |
| Variational bridge | A regular locally length-minimizing curve, parametrized at constant speed, obeys the equation | Arbitrary parametrizations do not obey the affine form |
| Minimization boundary | Sufficiently short geodesic segments are locally minimizing | A geodesic need not minimize globally; conjugate points and cut loci are outside this root |
| Neighboring target | Riemannian differential geometry | The relativistic free-particle equation is the distinct physics item `THM-P-0639` |
| Formal substrate | Lean 4 and repository-pinned mathlib | Intake search found covariant-derivative infrastructure but no exact geodesic-equation declaration; anchor audit is a later phase |

The ordered mathematical scope is recorded in `intake.json`. The repository wording, source
candidates, assumptions, and Lean boundary are reconciled in `source_statement_crosswalk.md`.

## Intake verdict

Lifecycle is `planned`; the provisional root vector is `[H2, M4, R3]`. `H2` is intentional: two
credible textbook sources have been identified, but a primary-source genealogy, exact
edition/theorem/page pin, errata review, assumption-level crosswalk, and independent review have not
passed. The first failed theorem gate is the exact Lean statement gate. No module, declaration,
expression hash, checked transport, or mutation certificate exists yet.

## Open task DAG

`INTAKE -> STATEMENT -> ANCHOR_AUDIT -> OBLIGATION_TREE -> PROOF -> VALIDATION -> RELEASE`.

The next phase must choose a precise Lean representation for curves, the Levi-Civita connection,
covariant acceleration along a curve, coordinate charts, and Christoffel symbols without replacing
the equation by a bare definition or silently asserting global minimality.

## Validation

`validation.md` records the exact commands and results. The self-test covers target membership,
manifest/blueprint agreement, dossier schema invariants, local references, and clean text layout.
It is intake evidence only and gives no Lean statement or proof credit.
