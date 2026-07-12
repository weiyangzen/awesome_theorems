# Scope map

## Received scope

The repository record fixes only a title, attribution, date, and the phrase "the theory of
fixed-point classes." Stage0 explicitly leaves precise definitions and premises, proof route,
equivalent forms, axioms, machine status, and formal artifacts open. The catalog's `已验证` label
is untrusted metadata under rev-5.6.

The phrase is not a theorem statement. It gives no class of spaces, maps, equivalence relation,
index convention, quantifier order, hypotheses, or conclusion.

## Candidate mathematical components

An accepted source might connect some or all of these components, but the intake credits none as
the canonical root:

- fixed points of a continuous self-map partitioned into Nielsen fixed-point classes, defined by
  paths/homotopies or by lifts and Reidemeister classes;
- a fixed-point index attached to each class and the designation of nonzero-index classes as
  essential;
- the Nielsen number `N(f)`, counting essential fixed-point classes;
- homotopy invariance of `N(f)`;
- the lower bound `N(f) <= #Fix(g)` for every map `g` homotopic to `f`, under a source-fixed
  finiteness and space category;
- a minimum theorem realizing that bound, potentially only under surface, manifold, dimension,
  or Wecken-type hypotheses.

These are not interchangeable. A definition, an invariance theorem, a lower bound, and a
realization theorem have different binders and proof obligations.

## Proposition-changing decisions

Before statement freeze, an admitted source and reviewer must fix:

1. The domain category: closed surface, compact connected polyhedron, ANR/ENR, manifold, or
   another class, including dimension, boundary, connectedness, and local hypotheses.
2. Whether maps are continuous self-maps and whether the homotopy is free, relative, based, or
   subject to another constraint.
3. The path versus lift/Reidemeister definition of a fixed-point class and a checked relationship
   if both encodings receive credit.
4. The fixed-point index normalization, its domain of definition, and the definition of an
   essential class and `N(f)`.
5. The exact theorem family and quantifier order: class decomposition, finiteness, invariance,
   lower bound, equality/minimum realization, or a conjunction explicitly present in the source.
6. Whether cardinality is a natural number, finite cardinal, or cardinal, and how infinite fixed
   sets and empty fixed sets are represented.
7. Every compactness, finiteness, triangulability, connectedness, boundary, orientation, and
   dimension hypothesis, plus every correction or erratum.

## Boundary and degenerate cases

No boundary case is silently excluded. Source review must decide empty and singleton spaces;
disconnected spaces; maps with no fixed points; maps with infinitely many fixed points or
fixed-point classes; inessential zero-index classes; the identity and constant maps; boundary
fixed points; noncompact spaces; and maps homotopic to fixed-point-free representatives.

## Explicit exclusions

- Wecken's realization/equality theorem (`THM-M-0643`) as a substitute for a Nielsen lower bound.
- The Lefschetz fixed-point theorem (`THM-M-0641`) or Brouwer fixed-point theorem
  (`THM-M-0640`) merely because they concern fixed points.
- The unrelated Nielsen-Schreier theorem (`THM-M-0079`).
- A fixed-point set, homotopy relation, fundamental group, or covering-space API presented as if
  it already defined Nielsen classes, their indices, or the Nielsen number.
- A structure whose fields assume the desired lower bound, invariance, or realization result.
- A theorem restricted to a convenient finite type or interval when the approved source has a
  topological surface/polyhedron domain.
- The catalog's title, date, attribution, or `已验证` label used as proof evidence.

## Lean boundary

Pinned mathlib provides `Function.IsFixedPt`, `Function.fixedPoints`, continuous maps, and
`ContinuousMap.Homotopy`/`ContinuousMap.Homotopic`. The bounded intake search found no relevant
Nielsen fixed-point, fixed-point-class, Nielsen-number, or Reidemeister-class declaration. These
generic APIs are useful substrate only; they neither select nor prove the target.

## Retry condition

Select an immutable primary or authoritative source and one exact proposition; record its
edition/scan, theorem or page-level locator, incorporated definitions, ordered binders,
hypotheses, conclusion, proof boundary, corrections, and neighbor ownership; then obtain an
independent source review. The statement phase may only then encode that proposition, select
minimal pinned imports, serialize the expression and environment fingerprints, check alternate
transports, and execute the required statement mutations.
