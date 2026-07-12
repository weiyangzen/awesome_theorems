# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md` supplies the title, Pierre de Fermat, 1643, the exact phrase
`三角形内到三顶点距离之和最小的点`, importance `中`, and the untrusted status `已验证`.
The record was introduced at repository commit
`bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. `Docs/Stage0_Blueprint.md` repeats the phrase and
explicitly leaves precise definitions and premises, equivalent statements, axioms, machine status,
and artifact links open. Neither file cites a mathematical source.

| Repository phrase | Information plausibly indicated | Information not fixed | Intake result |
|---|---|---|---|
| `三角形` (triangle) | three vertices in Euclidean geometry | ambient space, distinctness, noncollinearity, open/closed triangular region | unresolved |
| `内` (inside) | some relationship between the sought point and triangle | strict interior, relative interior, closed triangle, or merely a theorem that a global minimizer lies there | unresolved |
| `到三顶点距离之和` | candidate objective `dist P A + dist P B + dist P C` | metric, weights, comparison domain, Lean encoding | candidate only |
| `最小的点` | a minimizer is intended | existence, uniqueness, universal inequality, construction, or characterization | unresolved |
| Fermat / 1643 | historical attribution metadata | pinpoint correspondence, edition, page, exact wording, Torricelli's proof boundary | unresolved |
| `已验证` | repository metadata | human proof crosswalk or kernel evidence | no credit |

## Inspected modern source lead

Boris S. Mordukhovich and Nguyen Mau Nam, *The Fermat-Torricelli Problem and Weiszfeld's
Algorithm in the Light of Convex Analysis*, arXiv `1302.5244v4` (23 December 2019), was inspected
as a source-family discriminator. Its abstract and Section 1 formulate the problem as minimizing
the sum of Euclidean distances from a point in the plane to three given points. Section 1 then
states the two classical branches: a triangle angle at least 120 degrees gives the corresponding
vertex; otherwise there is a unique interior solution with three 120-degree angles. Section 2,
equations (2.1)-(2.2), Proposition 2.2, Proposition 2.3, Proposition 2.7, and Example 2.8 separate
existence, uniqueness, analytic optimality conditions, and the planar construction.

The inspected PDF has SHA-256
`6d7d80758d515659bd93397afb2aaea5db9db6478e2ae12bbc1f320ad9a20645`. It is a credible modern
expository source lead, but the repository does not cite or select it. This intake has not admitted
it as immutable H0 evidence, mapped its complete assumptions and proof body, checked its errata,
or obtained independent source review. Its broader `R^n` and finite-point formulations must not be
substituted for the unresolved catalog target.

## Crosswalk to a future statement

| Candidate component | Modern-source role | Required Lean surface | Status |
|---|---|---|---|
| Objective function | equation (2.1) sums Euclidean norms/distances | a transparent three-distance function | API feasibility only |
| Global minimization | equation (2.2) minimizes over the ambient Euclidean space | `IsMinOn` on `Set.univ` or a universal inequality | source selection open |
| Existence | Proposition 2.2 for a finite distinct point family | quantified minimizer and membership/domain data | not credited to catalog claim |
| Uniqueness | Proposition 2.3 under noncollinearity; surrounding text discusses the three-point case | exact triangle nondegeneracy and unique-existence encoding | assumptions open |
| Interior 120-degree branch | Section 1 and Example 2.8 | affine interior plus three angle equalities | source-to-root decision open |
| Vertex branch | Section 1, Proposition 2.7(ii), Example 2.8 | angle threshold and vertex `IsMinOn` claim | omitted by literal gloss |

## Human and machine boundary

Before `H0`, an accountable reviewer must select an immutable primary or authoritative source,
pinpoint the exact theorem and incorporated definitions, audit corrections and errata, and approve
a row-by-row assumption/conclusion map. The historical Fermat attribution, the modern source lead,
and Torricelli's solution must remain distinct provenance records.

A bounded exact-name search found no Fermat-point, Torricelli-point, or geometric-median declaration
in pinned mathlib or repository-local Lean sources. Generic Euclidean distance, convex-hull,
angle, compact-minimum, and convex-distance APIs elaborate in `IntakeProbe.lean`; this is only
feasibility evidence. The dependent anchor audit must later search declarations and external Lean 4
projects at immutable revisions after the exact statement is frozen. No formal proof body or
machine-completion evidence is credited here.
