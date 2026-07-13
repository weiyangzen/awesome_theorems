# Scope map

## Preserved theorem scope

The intake preserves the standard finite-graph 1-factor criterion indicated jointly by the catalog
name, attribution, year, and perfect-matching gloss. The intended claim has both directions:

- if a finite graph has a perfect matching, deleting any vertex set `U` leaves at most `|U|` odd
  connected components; and
- if that inequality holds for every `U`, the graph has a perfect matching.

The leading Lean representation uses an arbitrary universe-polymorphic vertex type `V`, a loopless
undirected `SimpleGraph V`, and `[Finite V]`. A matching is a subgraph of `G`; perfect means both
matching and spanning. The deletion condition quantifies every `U : Set V` and counts the odd
connected components of the graph remaining after deleting `U`.

## Decisions required at statement freeze

The statement phase must independently approve the primary source edition and exact result, then
freeze the following proposition-changing details:

1. Whether the canonical human wording uses finite simple graphs and 1-factors exactly, and how the
   source treats loops, parallel edges, isolated vertices, and graph order.
2. Whether the Lean carrier uses `[Finite V]` or `[Fintype V]`, and whether any decidable equality or
   adjacency instances are explicit rather than implementation details.
3. Whether a perfect matching is a spanning matching subgraph, an edge set, an involution, or
   another representation, together with checked transports for credited alternates.
4. Whether deletion is induced deletion of all vertices in `U`, and whether odd components are
   counted by finite cardinality of their vertex supports.
5. The exact inequality form: at most `|U|` odd components, equivalently the absence of a strict
   `IsTutteViolator` inequality, for every `U`.
6. Ordered binders, universes, classical principles, source definitions, proof boundary,
   corrections, and all four required statement mutations.

## Degenerate and boundary cases

No finite vertex carrier is excluded provisionally. The empty graph satisfies the criterion and has
the empty perfect matching under the pinned representation. A graph of odd total order fails the
condition already at `U = ∅`, while an even total order alone is not sufficient. Isolated vertices,
empty or full deletion sets, disconnected graphs, and singleton components must remain visible to
the exact statement and its mutation tests rather than being silently removed.

## Explicit exclusions

- Hall's marriage theorem for bipartite graphs is not the general Tutte 1-factor theorem.
- Petersen's theorem for cubic bridgeless graphs is separately owned by `THM-M-0857`.
- Tutte's 3-connected wheel-decomposition theorem is separately owned by `THM-M-0864`.
- Infinite or locally finite matching criteria, `f`-factor theorems, maximum-matching formulae, and
  Tutte-Berge variants cannot replace this finite perfect-matching equivalence.
- One direction, an even-cardinality corollary, or a special graph class cannot replace the `Iff`.
- A structure or hypothesis that assumes a perfect matching or the odd-component inequality is an
  interface, not a proof.
- The catalog's `已验证` label, theorem name, source URL, and intake probe supply no accepted
  source-fidelity or machine-proof credit.

## Formal discovery boundary

Pinned mathlib's `SimpleGraph.tutte` is a direct candidate whose displayed type matches this scope.
Its proof-bearing source is present at an immutable dependency revision, but intake has not run the
ordered exact-statement gate, expression serialization, checked alternate transports, mutations,
or terminal proof-body and transitive trust audit. Those omissions keep the candidate at `M3` and
the canonical formal target unset during intake.
