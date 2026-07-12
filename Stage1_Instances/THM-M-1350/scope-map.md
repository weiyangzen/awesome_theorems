# Scope map

## Preserved catalog scope

The intake preserves target `THM-M-1350`, the title `指标理论` (index theory), the gloss `闭曲线的指标`
(the index of a closed curve), the attribution Henri Poincare, and the year 1885. Importance
`high` and status `已验证` are catalog metadata, not source-fidelity or Lean evidence.

The record's ODE category and its placement near Poincare-Bendixson and Bendixson-Dulac suggest
planar dynamics, but the literal wording also admits the topological winding number of a curve.
Context is not an exact source statement.

## Candidate families not credited

The following are distinct discovery hypotheses, not accepted formulations of the target:

1. Define the winding number of a closed planar or complex curve about a point outside its image,
   perhaps by a lift, degree, homotopy class, or contour integral, and prove a source-selected
   property of it.
2. Define the Poincare index of a continuous nonzero planar vector field along an oriented closed
   curve and prove a source-selected invariance or computation theorem.
3. Prove an index-sum theorem relating the field's index on a boundary curve to local indices of
   isolated zeros enclosed by the curve.
4. Apply an index result to an ODE phase portrait, periodic orbit, equilibrium classification, or
   existence/nonexistence argument selected by an exact source.

A definition alone, an integer-valuedness result, homotopy invariance, a normalization for a circle,
an argument-principle formula, and an enclosed-zero sum are not interchangeable conclusions.

## Proposition-changing decisions

Before the statement phase can close, an immutable source and independent review must fix:

- which candidate family and which truth-valued theorem, rather than merely an index definition;
- the ambient carrier: real plane, complex plane, punctured plane, manifold, or another space;
- the curve representation, parameter domain, continuity or differentiability, closedness,
  orientation, piecewise regularity, and whether constant or self-intersecting curves are allowed;
- the reference point and avoidance hypothesis for winding number, or the vector field and
  nonvanishing-on-the-curve hypothesis for Poincare index;
- whether the curve is Jordan, whether it bounds an approved domain, and whether zeros inside are
  finite and isolated with source-defined multiplicities or local indices;
- the index convention: degree, lift endpoint, angle increment, normalized contour integral, sign,
  normalization, and proof of equivalence for every credited alternate encoding;
- all ordered binders, domain and regularity hypotheses, exact conclusion, and incorporated
  definitions, proof boundary, correction history, and errata; and
- degenerate cases such as constant curves, the reference point on the image, zeros on the curve,
  reversed orientation, empty interiors, repeated traversal, no enclosed zeros, and trivial fields.

## Explicit exclusions

- A definition of an integer called `index` presented as a proved theorem.
- The index of a convenient circle about its center as a substitute for a general closed curve.
- Complex winding number substituted for vector-field index, or conversely, without a checked
  source-faithful transport.
- The argument principle, residue theorem, Brouwer degree, fixed-point index, rotation number, or
  Euler characteristic substituted merely because it uses related terminology.
- An index-sum theorem with isolated-zero and domain assumptions omitted.
- A structure that assumes the requested index value, invariance, or sum formula as a field.
- A numerical angle-unwrapping computation, plot, floating-point contour integral, or sampled
  trajectory offered as theorem evidence.
- The repository's `已验证` label offered as human-source or kernel credit.

## Formal boundary

Pinned mathlib has genuine adjacent path/homotopy, covering-map lifting, complex exponential-cover,
and parametrized-circle interfaces, authenticated by the intake probe. The bounded lexical search
did not locate an exact target declaration. These facts neither identify the intended mathematics
nor freeze minimal imports, an expression fingerprint, checked transports, mutations, discovery
protocol, obligation registry, proof graph, or proof state.
