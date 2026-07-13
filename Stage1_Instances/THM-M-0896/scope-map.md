# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-0896`, the label `有限几何`, the gloss
`有限几何与图论的联系`, the attribution "many mathematicians," and the twentieth century.
Importance `high` and status `已验证` are catalog metadata, not theorem or proof evidence. No
citation, definition, construction, parameter tuple, or named result accompanies the record.

The wording points toward a family of correspondences between finite incidence geometries and
graphs. A relationship between two fields is not itself a proposition.

## Proposition-changing decisions

An approved statement run must freeze all of the following from an immutable, independently
reviewed source:

- the geometry: projective or affine plane, higher-dimensional projective/affine geometry, polar
  space, generalized polygon, partial geometry, linear space, block design, or another incidence
  structure;
- the carriers and incidence relation: points and lines/blocks, finite types or finite sets,
  equality/isomorphism conventions, incidence axioms, nondegeneracy, order, dimension, field or
  division-ring coordinatization, and every source parameter;
- the graph construction: incidence/Levi bipartite graph, point/collinearity graph, line graph,
  polarity graph, flag graph, Cayley graph, or another construction, including whether it is
  simple, directed, colored, looped, or permits parallel edges;
- the direction of the relationship: construct a graph from a geometry, reconstruct a geometry
  from a graph, prove an equivalence, or characterize only one image class;
- the exact conclusion: degree and vertex counts, regularity, bipartiteness, strong or distance
  regularity, intersection array, spectrum, girth/diameter, clique/coclique or chromatic bound,
  automorphisms, expansion, extremal property, existence, uniqueness, or classification;
- ordered binders, hypotheses, conclusion, quantifier scope, universes, typeclasses, foundation and
  computation policies, and all empty, small-order, degenerate, disconnected, or non-Desarguesian
  cases.

These choices yield inequivalent theorems. This list is a resolution ledger, not a candidate target.

## Candidate families not credited

- The incidence graph of a finite projective plane has source-specific bipartite, regularity,
  cardinality, diameter, or girth parameters.
- A point/collinearity graph from a partial geometry, polar space, or generalized quadrangle has
  source-specific strong- or distance-regular parameters.
- A graph satisfying selected parameter and local-incidence axioms reconstructs a finite geometry.
- Finite-geometry constructions give extremal, coloring, spectral, or expansion examples.

No family is canonical at intake. In particular, the existence in pinned mathlib of a projective-
plane cardinality theorem does not authorize replacing the catalog's geometry/graph relationship.

## Neighbor-target boundaries

- `THM-M-0894` owns the catalog's distance-regular-graph theory target.
- `THM-M-0895` owns strongly regular graph parameter constraints.
- `THM-M-0897` owns combinatorial-design existence as a separate broad target.
- `THM-M-0903` owns the Bose-Shrikhande-Parker theorem recorded as a refutation of Euler's
  conjecture.

Those targets do not supply statement or proof credit here. This intake does not decide whether
the broad catalog wording was intended as an umbrella, a duplicate, or a specific omitted theorem.

## Degenerate and boundary cases

The selected source must decide empty point or line carriers, empty incidence, orders zero or one,
the smallest projective/affine planes, repeated blocks or parallel lines, loops and isolated graph
vertices, disconnected or bipartite conventions, finite versus locally finite structures,
Desarguesian versus non-Desarguesian planes, degenerate polarities, coincident points/lines, and
whether graph isomorphism corresponds to incidence isomorphism. No case is excluded at intake.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib exposes abstract incidence configurations,
`Configuration.ProjectivePlane`, its order and cardinality formulas, and `SimpleGraph`. The checked
probe authenticates representative interfaces only. The bounded intake search found no exact named
incidence/Levi/collinearity/point/polarity graph construction connecting a projective plane to graph
theory in pinned mathlib or repository-local Lean sources. This is substrate evidence, not an exact
statement, exhaustive anchor audit, or proof.
