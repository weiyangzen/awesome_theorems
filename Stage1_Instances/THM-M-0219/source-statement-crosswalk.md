# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:1578-1583` supplies exactly the title `庞加莱半平面模型`,
Henri Poincare, 1882, the gloss `双曲几何的另一种模型`, importance "high," and status `已验证`.
Git blame attributes all six uncited lines to repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no bibliography, definition,
formula, quantifier, hypothesis, conclusion, proof boundary, correction history, or formal
artifact.

`Docs/Stage0_Blueprint.md:6081-6106` repeats the gloss and explicitly leaves the target formal
system, logical foundation, precise definitions and premises, proof route, dependencies,
equivalent forms, axioms, machine status, and artifact links open. Its generic planning statement
that a closed result is known is not source evidence. The rev-5.6 manifest carries `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

## Bibliographic discovery boundary

Crossref metadata was inspected for H. Poincare, *Theorie des groupes fuchsiens*, *Acta
Mathematica* **1** (1882), 1-62, DOI `10.1007/BF02592124`. The title, author, journal, volume,
year, and pages match the catalog's attribution and date, making this a plausible primary-work
lead. The catalog does not cite the work, however, and the linked Project Euclid scan was blocked
by its access-control page in this environment. No article text, exact model definition,
theorem/page locator, incorporated premise, proof boundary, correction, erratum, or translation
was inspected. This bibliography is discovery evidence only and receives no H credit.

## Literal crosswalk

| Repository element | Mathematical decision required | Prospective Lean component | Intake result |
|---|---|---|---|
| `庞加莱半平面模型` | choose one construction or theorem about the model | one exact canonical `Prop`, not a topic record | model label; root open |
| "half-plane" | strict complex upper half-plane, real coordinates, and boundary/ideal-point convention | `UpperHalfPlane` or a checked equivalent carrier | pinned carrier exists; source mapping open |
| "model" | metric/Riemannian construction, model-axiom satisfaction, or equivalence theorem | exact structures plus a truth-valued correctness conclusion | meaning and conclusion absent |
| "hyperbolic geometry" | distance or line element, scale, curvature, geodesics, incidence/congruence, and parallel convention | source-selected definitions and checked bridges | all proposition-changing choices open |
| "another" | likely comparison with a disk or other model | explicit Cayley map and equality, iff, implication, or isometry transport | comparison target and direction absent |
| Henri Poincare / 1882 | intended historical source and model genealogy | immutable source revision and pinpoint locators | Crossref lead only; no text inspected |
| `已验证` | untrusted inventory label | inspectable human proof and kernel evidence would be required | no H or M credit |

## Pinned Lean substrate crosswalk

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

| Pinned interface | Checked library role | Why it does not close this intake root |
|---|---|---|
| `UpperHalfPlane` | complex points with positive imaginary part | carrier only; catalog statement and source definition are not selected |
| `UpperHalfPlane.dist_eq` | `dist z w = 2 * arsinh (dist (z : C) w / (2 * sqrt (z.im * w.im)))` | one metric formula, not a source-mapped model theorem |
| `MetricSpace UpperHalfPlane` | checked symmetry, separation, and triangle-law packaging for that distance | does not establish which model properties the catalog intends |
| `ProperSpace UpperHalfPlane` | compactness of closed bounded metric sets | not a source-selected completeness/curvature/geodesic conclusion |
| `UpperHalfPlane.coe_specialLinearGroup_apply` | real `SL(2)` fractional-linear formula | action formula alone is not the full model claim |
| `IsIsometricSMul SL(2,R) UpperHalfPlane` | the special-linear action preserves the pinned metric | credible symmetry substrate but no exact canonical root match |
| `Complex.UnitDisc` | carrier for a neighboring disk-model encoding | no checked source-selected Cayley isometry was located in the bounded intake search |

The probe authenticates these interfaces with the pinned toolchain. It neither declares a target
theorem nor promotes the node to `M3`: without a stable canonical proposition, adjacent definitions
and theorems cannot be judged usable or source-identical.

## Source and statement gates

Before ordinary theorem execution can leave `H5`, an accountable reviewer must preserve a lawful
immutable primary or authoritative source, select one exact model theorem and all incorporated
definitions, record edition/section/page locators, map every binder, hypothesis, conclusion, and
exceptional case, audit corrections and errata, justify the boundary against the disk, Klein, and
area targets, and obtain an independent source review.

The statement phase must then choose minimal imports, elaborate the exact Lean expression, record
its environment and normalized-expression fingerprints, compile every required carrier/metric/
Riemannian/disk transport, and mutation-test hypotheses, domains, binder scope, normalization, and
boundary cases. Until those gates pass, the canonical statement, formal target, obligation
registry, proof tree, and all proof credit remain open.
