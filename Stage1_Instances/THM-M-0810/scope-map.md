# Scope map

## Received family

The repository fixes the graph-theory title `欧拉公式`, attribution to Leonhard Euler, year 1750,
and the gloss "relationship among the vertices, edges, and faces of a planar graph." This excludes
Euler's complex exponential identity and his number-theoretic theorem, but it does not yet select
one graph proposition.

The familiar connected plane-graph equation `V - E + F = 2` is a candidate interpretation only.
It is not the canonical statement until a reviewed source fixes every term and hypothesis. Intake
therefore preserves the following possible family members without crediting any one as the root:

- the connected finite plane-graph formula with the unbounded face included;
- the equivalent spherical cellular-embedding formula;
- a disconnected plane-graph generalization with a component correction;

Polyhedral and higher-genus surface identities are related generalizations, not candidates for the
catalog's explicit planar-graph root. They remain excluded unless a source audit proves that the
catalog intended a checked transport from one of them to the planar statement.

## Decisions required at statement freeze

1. Select an immutable proposition-level source and independently review its formula, incorporated
   definitions, assumptions, proof boundary, corrections, and errata.
2. Fix a plane graph with embedding data versus an abstract graph that merely admits an embedding.
   An abstract graph alone does not determine a face set.
3. Fix finite simple graphs, finite multigraphs, combinatorial maps, or another edge model, including
   the policy for loops, parallel edges, bridges, and isolated vertices.
4. Fix connectedness, the empty graph, the number of connected components, and the exact correction
   term for any disconnected form.
5. Define faces from the complement in the plane, a rotation system, darts/orbits, or a cellular
   embedding, and state whether the outer face is counted.
6. Fix plane versus sphere and cellularity. Higher-genus surfaces are excluded generalizations.
7. Freeze number types, ordered binders, universes, all hypotheses, the exact equality, and checked
   transports among source-approved encodings.
8. Mutation-test connectedness, embedding/cellularity, graph class, binder scope, and boundary cases
   before inspecting proof closure.

## Boundary cases

No case is excluded at intake. Statement work must decide the empty graph, a single isolated
vertex, forests and trees, bridges, graphs with several components, disconnected drawings with
nested components, loops and parallel edges, noncellular embeddings, and the treatment of the
unbounded face.

## Explicit exclusions

- Euler's identity `exp (i*pi) + 1 = 0`, Euler's exponential formula, Euler's totient theorem,
  Euler paths/circuits (`THM-M-0811`), Euler lines, Euler classes, and analytic Euler equations.
- A planar edge bound such as `E <= 3V - 6`, a coloring theorem, or Kuratowski's theorem used as a
  substitute for the vertex-edge-face identity.
- A polyhedral or higher-genus statement silently substituted for the source-selected plane-graph
  theorem, or conversely, without a checked source-approved transport.
- A structure or hypothesis that stores the desired equality, an assumed face-count oracle, or a
  definition engineered to make the conclusion tautological.
- A diagram, finite enumeration, numerical experiment, theorem-name match, or the catalog label
  `已验证` used as human-source or machine-proof evidence.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, finite simple graphs
have `SimpleGraph.edgeFinset` and connectivity has `SimpleGraph.Connected` and
`SimpleGraph.ConnectedComponent`. These are adjacent ingredients only. The bounded intake search
did not locate a graph-planarity predicate, embedded-plane-graph or face type, face cardinality, or
Euler-formula declaration in pinned `Mathlib.Combinatorics.SimpleGraph`. This is not an exhaustive
anchor audit or a claim about external projects.

No canonical Lean expression, minimal import, expression hash, environment fingerprint, checked
alternate encoding, discovery protocol, or obligation registry is frozen at intake.
