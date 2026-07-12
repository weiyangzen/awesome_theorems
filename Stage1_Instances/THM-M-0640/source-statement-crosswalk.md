# Source-statement crosswalk

## Repository sources inspected

`Docs/researches/math_theorems.md:4741-4746` is the complete repository research record. It gives
the Chinese name, Luitzen Brouwer, 1910, the gloss
`n维球到自身的连续映射有不动点`, importance "high", and `已验证`. Git history traces all six
uncited lines to commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. This establishes
repository provenance, not a mathematical source or binder-complete proposition.

`Docs/Stage0_Blueprint.md:17503-17528` repeats the gloss while explicitly leaving precise
definitions and premises, proof history and route, dependencies, equivalent forms, axioms,
machine-checked status, and artifact links open. The rev-5.6 manifest preserves `已验证` only as
`source_status_untrusted` and resets the target to `L0 / rework_required`.

No repository-local exact source quotation, theorem locator, definition chain, assumption list,
errata disposition, translation review, or independent source review was found for this target.

## Primary-source discovery lead

Crossref bibliographic metadata identifies L. E. J. Brouwer, "Uber Abbildung von
Mannigfaltigkeiten", *Mathematische Annalen* **71** (1911), 97-115, DOI
`10.1007/BF01456931`. The author and historical period fit the theorem family, but the repository's
1910 date is not itself a proposition locator. This intake does not admit the paper text, select an
exact theorem/page, or credit any incorporated definitions, assumptions, translation, correction,
erratum, or independent review. The citation is a discovery lead only and does not establish H0.

## Crosswalk

| Repository phrase | Possible mathematical component | Prospective Lean component | Intake assessment |
|---|---|---|---|
| `布劳威尔不动点定理` | the classical finite-dimensional Brouwer family | future source-selected declaration | recognizable family, not exact identity |
| `n维球` | in the classical named theorem, usually a closed topological ball in real n-space | likely a subtype of `Metric.closedBall` in `EuclideanSpace` | closed/open/sphere, model, center, radius, and dimension range absent |
| `到自身` | a self-map preserving the selected ball | subtype map or ambient map plus `Set.MapsTo` | representation and binder order absent |
| `连续映射` | continuity on the selected carrier | `Continuous` or `ContinuousOn` | domain convention absent |
| `有不动点` | existence of a point in the ball fixed by the map | `Exists (Function.IsFixedPt f)` with membership as required | exact conclusion and equality orientation absent |
| Luitzen Brouwer, 1910 | historical attribution | source provenance only | 1911 bibliographic lead found; pinpoint identity open |
| `已验证` | catalog classification | no Lean proposition or proof object | explicitly rejected as evidence |

## Neighbor crosswalk

| Target | Repository wording | Relationship and boundary |
|---|---|---|
| `THM-M-0319` | fixed-point theorem on compact convex subsets of Euclidean space | same title and related Brouwer family, but distinct target ownership; no statement, state, receipt, or proof credit transfers |
| `THM-M-0636` | continuous map on a compact convex set has a fixed point | generic fixed-point/Brouwer family with unresolved scope; it explicitly treats this target as the separate ball wording |
| `THM-M-0637` / `THM-M-0638` | Schauder / Tychonoff fixed-point formulations | broader ambient families and not substitutes for the n-ball theorem |
| `THM-M-0639` | Kakutani set-valued fixed-point theorem | changes a single-valued self-map to a correspondence and is not a substitute |

## Pinned Lean boundary

The discovery-only probe elaborates the Euclidean-space type constructor, closed-ball membership, continuity,
maps into a set, and fixed-point vocabulary from pinned mathlib. These APIs show that pieces of a
future encoding exist. They do not choose the source statement or supply Brouwer's terminal
theorem. A bounded case-insensitive search over `Formalizations/Lean/AwesomeTheorems` and pinned
mathlib Lean sources found no terminal Brouwer fixed-point declaration. This is a feasibility
boundary, not the scheduled immutable anchor audit and not an absence claim beyond the searched
trees.

Before H0 or the statement gate can pass, accountable reviewers must preserve an immutable primary
or authoritative edition; identify the exact theorem and incorporated definitions by page; map
every domain, dimension, ball, self-map, continuity, conclusion, and degenerate-case clause; inspect
corrections and errata; resolve the 1910/1911 and neighbor-target boundaries; approve the
translation; and independently review the result.
