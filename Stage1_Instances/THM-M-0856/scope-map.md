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

## Frozen Lean-facing decisions

The worker statement proposal freezes the intake-selected conventional claim using the following
Lean-facing decisions. Independent approval of the primary edition, exact result, incorporated
definitions, and corrections remains open on the `H` axis and may invalidate this proposal:

1. The formal domain is an arbitrary universe-polymorphic `SimpleGraph V` under `[Finite V]`, with
   no `Fintype`, decidable equality, adjacency decidability, connectedness, nonemptiness, or graph-
   order premise.
2. A perfect matching is represented as `M : G.Subgraph` satisfying `M.IsPerfectMatching`, hence a
   matching that is spanning in mathlib's pinned definition.
3. Deletion is induced deletion from the top subgraph by every `U : Set V`; odd components are
   counted by `.oddComponents.ncard`.
4. The root uses the direct inequality `oddComponents.ncard ≤ U.ncard`. Checked `Iff` transports
   cover its inline expansion and a local no-strict-violator spelling.
5. Empty and odd-order carriers, isolated vertices, disconnected graphs, and empty/full deletions
   stay in scope. Four mutations test finiteness, graph domain, graph-binder scope, and the empty-
   carrier boundary.
6. The proof-bearing `Mathlib.Combinatorics.SimpleGraph.Tutte` module is excluded from statement
   imports; candidate proof and trust inspection remain anchor-audit work.

## Degenerate and boundary cases

No finite vertex carrier is excluded. The graph on the empty vertex carrier satisfies the criterion
and has the empty perfect matching under the pinned representation. An edgeless graph on a nonempty
carrier is still in scope, but both sides of the equivalence are false. A graph of odd total order
fails the condition already at `U = ∅`, while even total order alone is not sufficient. Isolated
vertices, empty or full deletion sets, disconnected graphs, and singleton components remain visible
to the exact statement and its mutation tests rather than being silently removed.

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
The statement proposal now supplies the local target, expression serialization, checked alternate
transports, and mutations without importing that proof. Terminal-body provenance, transitive trust,
wrapper, and candidate acceptance remain ordered anchor-audit work, so the vector stays `M3`.
