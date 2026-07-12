# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md` attributes the item to Hermann Minkowski, dates it to 1903, and
glosses it as the problem of prescribing the curvature measure of a convex body's surface. It gives
no dimension, measure condition, uniqueness clause, or bibliographic locator. Its `已验证` label is
untrusted under rev-5.6 and provides neither human-proof nor machine-proof credit.

## Candidate mathematical sources

- Hermann Minkowski, "Volumen und Oberfläche", *Mathematische Annalen* **57** (1903), 447-495.
  This is the primary historical candidate consistent with the repository date. The exact section,
  proposition, terminology, hypotheses, and relationship between its original formulation and the
  modern Borel-measure theorem have not yet been inspected.
- Rolf Schneider, *Convex Bodies: The Brunn-Minkowski Theory*, second expanded edition, Cambridge
  University Press (2014), the chapter on area measures and the Minkowski problem. This is a modern
  source candidate for the general measure formulation and normalization conventions. Exact
  theorem/page, cited dependencies, and errata remain to be checked.

These are discovery anchors, not `H0` evidence. An independent reviewer must verify an immutable
edition, pinpoint theorem/page, assumptions, definitions, proof dependencies, and errata.

## Crosswalk

| Source-side component | Mathematical role | Required Lean-side object | Intake status |
|---|---|---|---|
| Euclidean unit sphere | domain of prescribed normals | finite-dimensional real inner-product space and unit sphere | scope frozen; encoding open |
| finite Borel measure `mu` | prescribed area distribution | finite measure on the sphere with Borel measurable structure | scope frozen; API open |
| zero first moment | translation-invariant equilibrium condition | Bochner integral of sphere points into the ambient space | included; integrability encoding open |
| not on a great subsphere | excludes lower-dimensional degeneracy | support/non-concentration predicate and hyperplane sections | included; equivalent forms uncredited |
| convex body with interior | sought full-dimensional solution | compact convex set plus nonempty interior | scope frozen; representation open |
| surface-area measure | pushes boundary area through outer normals | concrete area measure/Gauss-map or equivalent standard definition | central missing formal interface |
| unique up to translation | sharp uniqueness conclusion | translation action and quotient/existential equality relation | included; binder form open |
| converse | necessity of balance and nondegeneracy | second implication or `Iff` transport | included; formal packaging open |

## Human and machine boundary

A repository-wide search found no theorem-specific Lean artifact for `THM-M-0189`. A narrow search
of the pinned mathlib source found no named Minkowski-problem or surface-area-measure declaration;
this is intake discovery only, not the exhaustive immutable candidate audit required later.

Before `H0`, the historical and modern formulations must be compared explicitly, including whether
the original source proves a polytopal or smooth precursor rather than the full Borel-measure form.
Before statement credit, every row above must map to an elaborated Lean target and any alternate
nondegeneracy, normalization, or uniqueness encoding must have a checked transport. No convenient
polytope or smooth special case may replace the frozen general claim.
