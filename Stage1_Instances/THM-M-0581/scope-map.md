# Scope map

## Included root

- A closed, connected, orientable topological or smooth `3`-manifold `M`.
- Prime decomposition along embedded essential `2`-spheres.
- The subsequent characteristic/JSJ decomposition of irreducible pieces along incompressible
  embedded `2`-tori, with the exact uniqueness convention to be selected from the audited source.
- A geometric structure on every final piece, modeled on one of `S^3`, `E^3`, `H^3`,
  `S^2 x R`, `H^2 x R`, the universal cover of `SL(2,R)`, `Nil`, or `Sol`.
- The completeness, quotient, and finite-volume/boundary behavior required by the selected precise
  source formulation.

## Statement-phase decisions

The exact source statement must settle whether geometrization is formulated for the manifold
interior, for prime components, or after both sphere and torus cuts; whether finite volume or a
standard boundary behavior is part of each geometric piece; and how spherical space-form and
Seifert-fibered cases are represented. The formal target must then freeze the manifold category,
embedded-submanifold API, essentiality/incompressibility predicates, cutting and gluing objects,
canonicity up to isotopy, model geometries, group actions, quotient metrics, binder order,
universes, and all typeclass hypotheses.

Boundary cases needing explicit treatment include an empty cutting family, already-geometric
manifolds, reducible manifolds, exceptional Seifert pieces, and the interaction between prime and
JSJ decompositions.

## Explicit exclusions

- The Poincare conjecture alone or only the simply connected/spherical branch.
- Hyperbolization of atoroidal pieces alone.
- A Ricci-flow existence, surgery, or finite-extinction theorem without the topological bridge.
- Classification of only irreducible, atoroidal, Haken, or Seifert-fibered special cases.
- An abstract structure that contains the geometrization conclusion as assumed data.
- Noncompact, boundary, or nonorientable generalizations without a checked transport to this root.

The legacy `S1_M_128.lean` file is discovery material only. Its `GeometrizationPackage` makes the
missing decomposition and conclusion proposition-valued fields and therefore cannot establish the
root frozen here.
