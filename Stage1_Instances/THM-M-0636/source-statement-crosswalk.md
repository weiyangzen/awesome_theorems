# Source-statement crosswalk

## Repository source

The tracked inventory at `Docs/researches/math_theorems.md:4713-4718` contains exactly the following
theorem metadata: title `不动点定理`, attribution to Luitzen Brouwer, year 1910, the gloss
`紧凸集上连续映射有不动点`, high importance, and status `已验证`. All six lines originate in the
repository's initial source-record commit, and the record gives no citation.

`Docs/Stage0_Blueprint.md:17395-17420` repeats the gloss while explicitly leaving exact definitions
and premises, proof route, dependencies, equivalent forms, axioms, machine status, and artifact
links unresolved. Thus the catalog identifies a theorem family but not a source-complete proposition.
The inherited status is untrusted under rev-5.6 and earns no `H`, `M`, or receipt credit.

## Source candidates and identity boundary

The attribution and year point toward Brouwer's classical fixed-point work. A historical source lead
is L. E. J. Brouwer, *Uber Abbildung von Mannigfaltigkeiten*, *Mathematische Annalen* 71
(1911), 97-115. This bibliographic lead is recorded only to guide later source audit: no immutable
copy, exact proposition/page, original terminology, definition chain, assumptions, translation,
proof boundary, or errata has been admitted here.

A modern authoritative source stating the exact compact-convex formulation may instead be selected
by the statement/source-review lane. It must explain the relationship to the historical formulation
and to ball or simplex versions. A broad citation or the fame of the theorem is not `H0`.

## Crosswalk

| Catalog phrase | Candidate mathematical component | Required Lean component | Intake status |
|---|---|---|---|
| `紧凸集` / compact convex set | a nonempty compact convex subset of a source-selected finite-dimensional real space | `K.Nonempty`, `IsCompact K`, `Convex Real K`, and a concrete ambient-space encoding | family identified; dimension, scalar, topology, and nonemptiness not stated by catalog |
| `连续映射` / continuous map | a continuous self-map of that set | subtype `Continuous` map or ambient `ContinuousOn` plus `Set.MapsTo` | self-map and continuity encoding open |
| `有不动点` / has a fixed point | existence of a member fixed by the map | `Exists fun x => x in K and Function.IsFixedPt f x`, or checked subtype equivalent | conclusion family identified; exact binders open |
| Brouwer / 1910 | historical theorem identity | source edition, theorem/page, assumptions, definitions, proof boundary, errata, reviewer | bibliographic family lead only |
| `已验证` | inherited catalog status | no formal component and no proof credit | explicitly untrusted |

## Neighbor crosswalk

| Target | Catalog wording | Relationship and boundary |
|---|---|---|
| `THM-M-0319` | fixed-point theorem on compact convex subsets of Euclidean space | likely overlapping compact-convex Brouwer formulation, but separate target ownership and no shared evidence or state |
| `THM-M-0640` | every continuous self-map of an n-dimensional ball has a fixed point | ball formulation in the same family; requires a checked relationship rather than silent identification |
| `THM-M-0637` | fixed point for a compact map on a Banach space | Schauder family; stronger/infinite-dimensional scope and not a substitute |
| `THM-M-0638` | fixed point on a locally convex space | Tychonoff family; stronger ambient scope and not a substitute |

## Human-source and machine boundary

The provisional `H1` means only that a well-known published theorem family and bibliographic lead
are known. Before `H0`, an independent source reviewer must approve an immutable edition, exact
theorem/page, every material premise and incorporated definition, formulation transports, proof
boundaries, translation issues, and errata.

The pinned Lean probe authenticates adjacent vocabulary only. A bounded case-insensitive search of
pinned mathlib found no declaration or module named for Brouwer and no terminal compact-convex
fixed-point theorem. That negative observation is not an exhaustive anchor audit. The later anchor
phase must search repo-local Lean, pinned mathlib, and credible external Lean 4 projects at immutable
revisions, then record exact declarations, types, terminal bodies, axioms, licenses, and dependency
feasibility.
