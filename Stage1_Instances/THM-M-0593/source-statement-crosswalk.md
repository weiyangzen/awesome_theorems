# Source-statement crosswalk

## Repository record and primary-source candidate

`Docs/researches/math_theorems.md` records the title "Sard's theorem", Arthur Sard, 1942, and only
the sentence "the critical values of a smooth map have measure zero". Stage0 repeats that sentence
and explicitly leaves precise definitions, prerequisites, proof history, formal artifacts, and
axioms to be supplied. Its `已验证` field is untrusted metadata under rev-5.6.

The primary-source candidate is Arthur Sard, *The measure of the critical values of differentiable
maps*, **Bulletin of the American Mathematical Society** 48 (1942), 883-890. This intake has not
independently inspected a pinned scan, theorem locator, definitions, corrections, or errata.
Accordingly the citation is a discovery anchor rather than `H0` evidence. In particular, its
Euclidean differentiability formulation must not be represented as a source-stated manifold
theorem without an explicit chartwise transport and countability argument.

## Crosswalk

| Repository/source phrase | Mathematical component to freeze | Required Lean component | Intake status |
|---|---|---|---|
| "smooth map" | map between finite-dimensional real smooth manifolds | `ContMDiff`/selected smooth-map predicate and manifold instances | family frozen; exact regularity context open |
| "critical" | derivative is not surjective (rank below target dimension) | tangent derivative and `Function.Surjective` or checked rank equivalent | meaning frozen; encoding open |
| "values" | image in `N` of the critical-point locus | set image or existentially defined subset of `N` | meaning frozen; binder form open |
| "measure zero" | null for the target smooth measure class/chartwise Lebesgue measure | `MeasureTheory.IsNullMeasurableSet`/measure-zero formulation selected from actual API | conclusion family frozen; measure convention open |
| Sard / 1942 | historical theorem and primary-paper locator | provenance only; no machine-proof credit | candidate article identified |
| finite differentiability | classical sharp threshold relating `k`, `m`, and `n` | differentiability-order hypothesis and implication to the smooth case | alternate source form; exact threshold review open |

## Source and machine boundary

The repository-wide intake search found references to missing Sard/Hausdorff-dimension
infrastructure in separately owned Whitney-embedding work, but no theorem-specific Lean source for
`THM-M-0593`. This negative search is not the downstream formal-anchor audit and says nothing
conclusive about external Lean 4 projects. No neighboring target's artifact supplies proof credit.

Before `H0`, an independent reviewer must inspect an immutable copy of the selected source, record
the exact theorem/page and definitions, verify the differentiability threshold and dimensional
cases, check corrections and errata, and approve the Euclidean-to-manifold relationship. Before
statement credit, every row must map to an elaborated Lean expression, with checked transports for
alternate criticality and null-set encodings.
