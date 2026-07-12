# THM-M-0550 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the Cartan formula target.
The repository source fixes the topic as the relation between cup products and
Steenrod operations. It does not fix the coefficient prime, operation family,
cohomology model, or whether the component or total-operation identity is the
root. Intake records those choices instead of silently substituting the most
convenient formula.

## Scope map

| Surface | In scope | Boundary at intake |
|---|---|---|
| Exact root | A Cartan product identity for a selected Steenrod-operation family | Exact source-backed formula is deferred to the statement phase |
| Inputs | Cohomology classes `x`, `y`, their degrees, a cup product, and an operation index | Space/cochain model, coefficient field, binders, and universes remain open |
| Mod-2 branch | Candidate formula `Sq^n(x cup y) = sum_{i+j=n} Sq^i(x) cup Sq^j(y)` | Conventional candidate, not yet the canonical target |
| Odd-prime branch | Reduced powers and any required Bockstein/sign variants | Analogue requiring a separate source decision; not folded into the mod-2 claim |
| Total operation | Multiplicativity of the total square or total reduced power | Equivalence to component identities requires a checked finite graded expansion |
| Proof architecture | cup product, cochain diagonal, operation definition, product compatibility, finite index decomposition | Scope nodes only; no obligation registry or proof credit is frozen |
| Boundaries | degree zero, unit, zero classes, instability range, and out-of-range indices | Must become explicit mutations after statement selection |
| Formal system | Lean 4 plus the repository's pinned mathlib environment | No declaration, minimal import, or expression fingerprint is claimed at intake |

The phrase "Cartan formula" can also name Cartan's homotopy formula in
differential geometry. That theorem is out of scope because this repository's
source text explicitly says cup product and Steenrod operations.

## Intake verdict

Lifecycle is `planned`; provisional root vector is `[H1, M4, R3]`. The first
open theorem gate is exact-statement identity. The dependent statement phase
must select and source one formula, then freeze coefficients, domains, ordered
binders, grading conventions, side conditions, boundaries, Lean imports, and
the normalized expression. No machine proof or theorem completion is claimed.

## Validation

The exact intake checks and results are recorded in `validation.md`. They cover
manifest membership, repository-standard consistency, JSON syntax, and
dossier-local hygiene only. Master acceptance remains outstanding.
