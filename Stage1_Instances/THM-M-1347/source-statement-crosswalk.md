# Source-statement crosswalk

## Repository record

`Docs/researches/math_theorems.md:9824-9829` supplies exactly the title `中心流形定理` (center
manifold theorem), attribution Jack Carr, date 1981, gloss `非双曲平衡点的约化` (reduction of
nonhyperbolic equilibria), importance "high," and status `已验证`. Git history places the uncited
record in commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. It contains no equation, theorem
locator, definitions, binders, hypotheses, conclusion, proof boundary, correction history, or
formal artifact.

`Docs/Stage0_Blueprint.md:36642-36667` repeats the gloss while explicitly leaving the formal system,
foundation, exact definitions and premises, proof route, dependencies, alternate forms, axioms,
machine status, and artifact links open. The rev-5.6 manifest retains `已验证` only as untrusted
metadata and resets the target to `L0 / rework_required`.

A separate source record, `Docs/researches/physics_theorems.md:6316-6322`, names a center-manifold
result attributed to Kelley/Pugh in 1967 with the gloss that system dynamics can be reduced to a
center manifold. It is not the provenance of `THM-M-1347` and must not silently fill its gaps.

## Primary-source lead, not credited

Jack Carr, *Applications of Centre Manifold Theory*, Applied Mathematical Sciences, Springer,
DOI `10.1007/978-1-4612-5929-9`, print ISBN `978-0-387-90577-8`, is a strong match to the catalog
author and year. Crossref reports 1981 book metadata. Springer reports the 1982 edition and gives
the following stable chapter metadata:

- Chapter 1, "Introduction to Centre Manifold Theory," DOI
  `10.1007/978-1-4612-5929-9_1`, pages 1-13. Its abstract says that it states the main results for
  finite-dimensional systems.
- Chapter 2, "Proofs of Theorems," DOI `10.1007/978-1-4612-5929-9_2`, pages 14-36.

An accessed two-page Chapter 1 preview contains only pages 1-2. It motivates invariant manifolds,
dimension reduction, and stability study for examples, but does not expose a complete numbered
theorem, all premises, or its conclusion. The full edition, theorem locator, definition chain,
assumption map, proof boundary, corrections or errata, and independent review remain open. The
lead is discovery evidence only and does not establish `H0`.

## Component crosswalk

| Catalog or source component | Prospective mathematical decision | Prospective Lean surface | Intake status |
|---|---|---|---|
| `中心流形定理` | select one theorem or explicit source conjunction | one exact proposition, not a family-name wrapper | open |
| "nonhyperbolic equilibrium" | system, equilibrium, derivative, and center spectral condition | normed space, vector field, derivative, spectrum/eigenspace predicates | all binders and hypotheses open |
| "center manifold" | local graph/submanifold, tangent space, regularity, and invariance | source-defined graph or manifold plus checked local invariance | definition and semantics open |
| "reduction" | induced equation, solution correspondence, tracking, or stability transfer | exact relation between full and reduced integral curves or flows | conclusion open |
| Carr/1981 | exact edition and result locator | provenance only | matching lead; not catalog-cited or accepted |
| `已验证` | no mathematical component | none | untrusted metadata; no H/M/R credit |

## Pinned Lean feasibility boundary

The current pinned environment exposes `IsIntegralCurveOn`, `IsInvariant`, `ContDiff`,
`HasFDerivAt`, `ContinuousLinearMap`, `Module.End.invtSubmodule`, and `spectrum`. These can support
parts of a future encoding, but they do not jointly supply a center manifold, its existence, its
local invariant semantics, or a reduction theorem. A bounded case-insensitive search for
`center/centre manifold` spellings found no exact-topic declaration in repo-local Lean or pinned
mathlib. That result is neither exhaustive external discovery nor proof that no formalization
exists.

## Required source-to-statement follow-up

Preserve and hash a lawfully accessible complete edition; select the exact numbered result and all
incorporated definitions; transcribe ordered binders, domains, spectral and regularity assumptions,
locality and nonuniqueness conventions, and every conclusion clause; inspect corrections and
errata; map each premise and conclusion to the canonical Lean expression; reconcile the separate
physics record and neighboring dynamical-systems targets; and obtain independent source review.
Until then the root remains `H1`, and no familiar textbook formulation may be substituted.
