# Source-statement crosswalk

## Repository source and provenance

`Docs/researches/math_theorems.md:1536-1541` is the complete repository source record. It supplies
the Chinese title "hyperbolic parallel postulate", the Lobachevsky/Bolyai attribution, the year
1830, the one-line statement "through a point outside a line, infinitely many parallel lines can
be drawn", high importance, and status `已验证`. Git provenance attributes all six uncited lines to
repository commit `bcf3f9fa79ab8c2b6610c9875668c2589b35b74f`. The record contains no publication,
edition, section, page, axiom system, definition, proof, correction history, reviewer, or formal
artifact.

`Docs/Stage0_Blueprint.md:5919-5944` repeats the gloss while explicitly leaving the formal system,
logical foundation, precise definitions and premises, proof route, dependencies, equivalent
forms, axioms, machine status, and artifact links open. Its generic planning text that a closed
result is believed to exist is not evidence. The rev-5.6 manifest carries `已验证` only as
`source_status_untrusted` and resets this target to `L0 / rework_required`.

No immutable primary or authoritative source was identified and inspected during intake. The
attribution and year are discovery metadata only; they do not select a Lobachevsky or Bolyai
edition, passage, translation, or modern equivalent. Human-source status is therefore `H5` for the
received target wording: it is not yet a stable proposition. This neither refutes nor declares open
the source-selected theorem that a later review may establish.

## Literal crosswalk

| Repository phrase | Mathematical decision required | Prospective Lean component | Intake result |
|---|---|---|---|
| "line" | complete synthetic line or model geodesic; equality and incidence | a source-selected `Line` type and `On : Point -> Line -> Prop` | carrier and equality open |
| "point outside a line" | nonincidence in a nondegenerate plane | `p : Point`, `l : Line`, and `not (On p l)` plus any ambient axioms | premise shape only; axioms open |
| "through" | incidence of the same point with each candidate line | `On p m` | predicate not selected |
| "parallel" | disjoint, limiting/asymptotic, ultraparallel, or a defined union | `Parallel l m` with an exact intersection/ideal-boundary convention | materially ambiguous |
| "lines" | distinct geometric objects rather than duplicate parameters | extensional line equality or a quotient plus pairwise distinctness | identity policy open |
| "infinitely many" | Dedekind/set infinitude, unbounded finite families, or cardinal claim | `Set.Infinite {m | On p m && Parallel l m}` or a checked alternate | relationship not selected |
| Lobachevsky/Bolyai / 1830 | historical genealogy | immutable source revision and pinpoint locators | uncited catalog metadata only |
| `已验证` | untrusted inventory label | inspectable human proof and kernel evidence would be required | no H or M credit |

## Nearby mathematical formulations

Modern summaries often distinguish two limiting parallels from the open fan of other disjoint
lines through the external point, and sometimes call only the limiting lines "parallel" while
calling the rest ultraparallel. Other presentations state only that more than one parallel exists,
or use the negation of Playfair uniqueness. These are useful search aliases, not interchangeable
statements by default. The catalog's literal infinite-family wording cannot be replaced by a
two-line existence axiom, and a stronger cardinality claim cannot be added, without an accepted
source crosswalk and the required implication/equivalence witnesses.

## Pinned Lean substrate crosswalk

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

| Pinned interface | Checked library role | Why it does not close the root |
|---|---|---|
| `UpperHalfPlane` | complex points with positive imaginary part | carrier for one analytic model only; no source-selected line predicate |
| `MetricSpace UpperHalfPlane` | Poincare distance on that carrier | metric structure alone does not define or classify complete geodesics |
| `UpperHalfPlane.dist_eq` | exact formula for the pinned distance | no parallel, incidence, or infinitude conclusion |
| `UpperHalfPlane.isometry_vertical_line` | an isometric parametrization of each vertical line | one vertical-line metric interface, not a geodesic classification or parallel postulate |
| `AffineMap.lineMap` / `AffineMap.lineMap_injective` | ordinary affine line interpolation and injectivity | Euclidean/affine substrate, not hyperbolic geodesic parallelism |
| `Set.Infinite` / `Set.Infinite.natEmbedding` | generic set infinitude and a natural-number embedding | conclusion vocabulary only; the set of candidate hyperbolic lines is absent |

The API probe and bounded name search are intake discovery evidence, not the later exhaustive
anchor audit. They supply no canonical expression, statement fingerprint, formal target match, or
proof credit.

## Next source and statement gates

Before ordinary theorem execution can leave `H5`, an accountable reviewer must preserve a lawful
immutable primary or authoritative source, select one exact proposition and all incorporated
definitions and axioms, record edition/section/page locators, map every binder, premise, conclusion,
and exceptional case, audit translations, corrections, and errata, reconcile the neighboring model
targets, and obtain an independent source review.

The statement phase must then choose minimal pinned imports, elaborate that exact Lean expression,
record normalized expression and environment fingerprints, compile every required synthetic/model
and alternate-infinitude transport, and mutation-test removed hypotheses, changed domains, binder
scope, the external-point condition, line identity, and boundary cases. Until these gates pass, the
canonical statement, obligation registry, proof tree, and all proof credit remain open.
