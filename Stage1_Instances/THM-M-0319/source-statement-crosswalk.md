# Source-statement crosswalk

## Repository source

The tracked discovery record at `Docs/researches/math_theorems.md` names Luitzen Brouwer, gives the
date 1910, and states `欧氏空间紧凸集上的不动点定理` (a fixed-point theorem on compact convex
subsets of Euclidean space). `Docs/Stage0_Blueprint.md` repeats that wording but explicitly leaves
the precise definitions, assumptions, proof route, formal system, and machine artifact unresolved.
The manifest label `已验证` is untrusted metadata under rev-5.6 and provides no `H`, `M`, or receipt
credit.

## Primary-source candidates

- L. E. J. Brouwer, "Uber Abbildung von Mannigfaltigkeiten," *Mathematische Annalen* 71
  (1911), 97-115. This is a historical source candidate associated with Brouwer's invariance and
  fixed-point work. The exact proposition, original terminology, assumptions, and relevant page
  have not yet been inspected in an immutable copy.
- A modern primary proof source stating the compact-convex Euclidean formulation must be selected
  during source audit, with edition, theorem number, page, assumptions, and errata recorded.

These entries are discovery anchors only. They justify `H1`, not `H0`. The spelling above is ASCII
transliteration for repository portability and is not presented as a verified transcription of the
paper's title page.

## Claim crosswalk

| Repository phrase | Frozen intake meaning | Formal component required later | Current status |
|---|---|---|---|
| Euclidean space | finite-dimensional real Euclidean space | concrete `R^n` representation | included; encoding open |
| compact convex set | subset `K` satisfying compactness and convexity | `IsCompact K` and `Convex R K` or checked equivalent | included |
| self-map | map whose domain and codomain are `K` | subtype map or ambient map plus `MapsTo` | included; choice open |
| continuous | continuity in the subspace topology | `Continuous` or `ContinuousOn` with checked equivalence | included; choice open |
| fixed point | an actual member `x` of `K` with `f x = x` | existential equality at the selected encoding | included |
| nonempty | necessary premise for the existential conclusion | `K.Nonempty` or subtype `Nonempty K` | made explicit |

## Review debt

Before `H0`, an independent reviewer must verify an immutable primary edition, pinpoint the theorem
and pages, map every source assumption to the Lean binders, check errata and translation issues, and
approve the relationship between ball/simplex and compact-convex formulations. Before any machine
credit, the anchor audit must inspect the pinned mathlib tree and any external Lean candidates by
exact declaration, type, revision, axioms, and terminal proof body.
