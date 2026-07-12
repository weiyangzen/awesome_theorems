# Source-statement crosswalk

## Repository source

`Docs/researches/math_theorems.md` gives the Chinese title `亚瑟迹公式`, attributes it to James
Arthur, dates it to 1978, and supplies only `约化群的迹公式` ("the trace formula for reductive
groups"). `Docs/Stage0_Blueprint.md` repeats that gloss and explicitly leaves definitions,
hypotheses, proof route, equivalent formulations, axioms, and machine artifacts open. The rev-5.6
manifest preserves `已验证` only as `source_status_untrusted`.

Thus the repository record identifies a mathematical program, not an exact proposition. It gives
no base field, class of reductive groups, distribution, test-function space, truncation parameter,
normalization, indexing sets, convergence claim, theorem number, or page.

## Primary-source locators

The following publications are genuine primary-source locators, but are not yet accepted as an
exact theorem/page crosswalk:

- James Arthur, "A trace formula for reductive groups I: Terms associated to classes in
  `G(Q)`," *Duke Mathematical Journal* 45 (1978), 911-952,
  DOI `10.1215/S0012-7094-78-04540-9`.
- James Arthur, "A trace formula for reductive groups II: Applications of a truncation operator,"
  *Compositio Mathematica* 40 (1980), 87-121.

The title and date strongly suggest the first paper is the inventory's intended historical anchor,
while the second is part of the same construction. Intake does not guess that either entire paper,
or a theorem within it, is the canonical target. The statement/source-audit phases must inspect an
immutable copy, record the exact theorem or displayed identity and page, map definitions and
assumptions, check corrections or later reformulations, and obtain independent source review.

## Crosswalk

| Repository phrase | Mathematical data that must be frozen | Lean obligation | Intake status |
|---|---|---|---|
| "reductive groups" | field, connectedness, reductivity, adelic points and quotient | concrete algebraic/topological group encoding | absent |
| "trace formula" | chosen truncated, non-invariant, invariant, or stable distribution | exact `Prop`, not an assumed identity | ambiguous |
| geometric side | conjugacy classes/orbits, weighted orbital integrals, coefficients and measures | convergent indexed expression with definitions | absent |
| spectral side | automorphic representations, Levi/parabolic data, intertwining operators and measures | convergent indexed expression with definitions | absent |
| equality | parameter range and equality of distributions or evaluated expressions | elaborated equality with all binders | absent |
| `已验证` | untrusted inventory metadata | no proof credit | explicitly rejected |

## Lean boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the intake probe checks
only generic topological-group, Haar-measure, integration, and finite-sum APIs. These are necessary
ingredients at a very coarse level, not a formalization candidate. No repository-local declaration
for the Arthur trace formula was found by the bounded name search. A complete anchor audit remains
downstream and must not infer absence from this limited search.
