# Scope map

## Received claim

`Docs/researches/math_theorems.md:1408-1413` supplies the title `欧拉线定理`, the attribution
Leonhard Euler, the year 1767, and the gloss `三角形垂心、重心、外心共线`. It supplies no
bibliography, definitions, ordered binders, hypotheses, theorem locator, proof boundary,
correction history, reviewer, or formal artifact. `Docs/Stage0_Blueprint.md:5428-5453` repeats the
gloss while explicitly leaving precise definitions and premises, proof route, equivalent forms,
axioms, machine status, and artifact links open.

The gloss identifies a recognizable classical theorem family, but it does not yet freeze one
source-faithful proposition.

## Candidate mathematical boundary

A familiar modern reading begins with a nondegenerate Euclidean triangle, lets `H`, `G`, and `O`
be its orthocenter, centroid, and circumcenter, and asserts that `{H, G, O}` is collinear. A
stronger Euler-line form locates the points by

```text
H = O + 3 (G - O), equivalently OG : GH = 1 : 2.
```

The stronger position formula implies bare collinearity, but the catalog states only collinearity.
It must not be silently substituted as the canonical root until a reviewed source and explicit
source-to-target decision establish the intended boundary.

## Proposition-changing decisions

Statement work must freeze all of the following:

- whether the ambient object is the ordinary Euclidean plane, a two-dimensional real affine inner-
  product space, or an arbitrary real inner-product affine space containing an affinely independent
  triple;
- whether a triangle is three distinct noncollinear points, an ordered affinely independent map
  `Fin 3 -> P`, or another construction, and how reorderings are transported;
- the definitions of orthocenter, centroid, and circumcenter, including existence and uniqueness
  hypotheses rather than assuming the desired centers as arbitrary points;
- whether the conclusion is bare set collinearity, membership of `H` in the affine span of `O` and
  `G`, an existential affine-parameter equation, the exact position formula, or a conjunction with
  order and ratio;
- whether the Euler-line name includes the degenerate equilateral case `H = G = O`, in which no
  unique geometric line is determined although three-point set collinearity remains true;
- the exact ordered binders, universes, typeclasses, hypotheses, conclusion, and all transports
  between synthetic, affine, vector, and coordinate encodings.

## Pinned Lean candidate boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the minimal candidate
module is `Mathlib.Geometry.Euclidean.MongePoint`.

- `Affine.Triangle ℝ P` abbreviates a `Simplex` of dimension two and stores three affinely
  independent points, so repeated and collinear vertices are excluded by the carrier itself.
- `Affine.Simplex.centroid` and `Affine.Simplex.circumcenter` supply the candidate `G` and `O`.
- `Affine.Triangle.orthocenter` is the triangle's Monge point, and
  `Affine.Triangle.orthocenter_mem_altitude` shows that it lies in every altitude.
- `Affine.Triangle.orthocenter_eq_smul_vsub_vadd_circumcenter` gives
  `H = 3 • (G - O) + O`.
- `Collinear ℝ s` means that the module rank of `vectorSpan ℝ s` is at most one.

A plausible future target is the collinearity of the set containing those three centers for every
`Affine.Triangle ℝ P`. It is recorded only as candidate text in `instance.json`, not as a canonical
target. Intake neither derives that target nor credits the existing position theorem as M0.

## Boundary and degenerate cases

- Repeated or collinear vertices do not form `Affine.Triangle`; a point-triple formulation would
  need explicit nondegeneracy hypotheses or separate conventions.
- In an equilateral triangle the three centers coincide. Rank-based set collinearity is true, but
  the phrase "the Euler line" does not identify a unique line.
- Right, obtuse, and acute nondegenerate triangles place the orthocenter on, outside, and inside the
  triangle respectively; none should be silently excluded by a bare collinearity statement.
- A triangle embedded in dimension greater than two spans a Euclidean affine plane and is covered
  by the candidate mathlib representation; a source may instead require the ambient plane itself
  to be two-dimensional.
- A coordinate theorem in `R^2`, a statement about slopes, and a synthetic incidence theorem are
  not definitionally identical to the affine rank-based form and require checked transports.

No boundary case is excluded at intake because no proposition has been selected.

## Explicit exclusions

- No substitution of the generalized Monge-point Euler line of an `n`-simplex for the triangle
  theorem.
- No substitution of the nine-point circle theorem, Feuerbach theorem, Sylvester theorem, or a
  theorem merely showing that the orthocenter lies in the triangle's affine span.
- No use of the stronger `H = O + 3 (G - O)` formula as the root without recording whether it is an
  alternate encoding, a strengthening, or a proof bridge.
- No structure or hypothesis that stores the desired collinearity or position equation as data.
- No diagram, floating-point coordinate check, theorem-name match, URL, untrusted catalog label,
  `#check`, or axiom report treated as proof credit.

## Statement retry condition

An independent Euclidean-geometry source reviewer must admit an immutable primary or authoritative
edition and exact result locator, map every incorporated definition, premise, conclusion, ratio or
order clause, proof boundary, translation, historical attribution, and correction status, and
approve one source-to-Lean root. Statement work may then elaborate that root with minimal imports,
serialize its expression and environment fingerprints, compile checked transports, and run the
required removed-hypothesis, changed-domain, binder-scope, and boundary mutations.
