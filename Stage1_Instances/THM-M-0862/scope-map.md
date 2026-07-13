# Scope map

## Received claim

`Docs/researches/math_theorems.md:6320-6325` records `Menger定理`, Karl Menger, 1927, and the
gloss `顶点连通度与不相交路径` ("vertex connectivity and disjoint paths"). It supplies no graph
model, quantifiers, formula, definition, hypotheses, source locator, proof boundary, or formal
declaration. The Stage0 projection at `Docs/Stage0_Blueprint.md:23522-23547` repeats the gloss and
explicitly leaves precise definitions, premises, equivalent forms, axioms, machine status, and
artifact links open.

The phrase is a relation between two topics, not an exact proposition. Intake preserves that
boundary rather than completing the statement from memory.

## Candidate theorem family

An exact, independently reviewed source must select among materially different roots:

1. **Finite set-to-set vertex form.** The minimum size of an `A`-`B` vertex separator equals the
   maximum size of a family of pairwise vertex-disjoint `A`-`B` paths.
2. **Finite point-to-point vertex form.** For distinct nonadjacent vertices `a,b`, the minimum
   number of other vertices separating them equals the maximum number of internally
   vertex-disjoint `a`-`b` paths.
3. **Global vertex-connectivity form.** A graph is `k`-connected exactly when every two vertices
   have `k` internally vertex-disjoint paths between them.
4. **Connectivity-number equality.** Vertex connectivity is expressed as a minimum cut or a
   minimum, over pairs, of a maximum path-packing number. Complete graphs and adjacent endpoints
   require conventions that are not visible in the gloss.
5. **Directed, infinite, or topological forms.** These change the carrier, finiteness assumptions,
   cardinal arithmetic, separator notion, and often the conclusion.

Diestel, *Graph Theory*, sixth edition (2025), Section 3.3, distinguishes the first three. Theorem
3.3.1 is the finite set-to-set theorem, Corollary 3.3.5(i) is the nonadjacent point form, and
Theorem 3.3.6(i) is the global form. The notes attribute the core theorem to Menger (1927) but the
global form to Whitney (1932). The catalog's wording and attribution therefore do not select one of
these statements.

## Decisions required at statement freeze

- finite simple undirected graph, multigraph, digraph, infinite graph, or another model;
- local equality, global `k`-connectivity equivalence, or connectivity-number equality;
- terminal sets, a vertex and a set, or two distinct vertices;
- vertex-disjoint or internally vertex-disjoint paths and the family representation;
- separator definition, including whether endpoints may be removed and how adjacency is handled;
- natural-number, finite-cardinality, or infinite-cardinal counting;
- whether `k` is arbitrary, positive, bounded by graph order, or encoded through connectivity;
- conclusion orientation, universes, decidability/finiteness instances, and ordered binders; and
- every degenerate case listed below.

## Boundary cases to resolve

- empty, singleton, finite, and infinite vertex types;
- `k = 0`, `k = 1`, and `k` at or above the number of vertices;
- equal, adjacent, and distinct nonadjacent endpoints;
- empty, overlapping, or equal terminal sets;
- disconnected, empty, complete, and single-vertex graphs;
- zero-length paths, empty path families, isolated vertices, loops, and parallel edges;
- separators containing terminal vertices versus separators required to avoid them; and
- empty or infinite extrema and their number/cardinality representation.

No boundary case is excluded before one exact proposition is selected.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the inspected surface
provides:

- `SimpleGraph.Path` and `SimpleGraph.Walk.IsPath`;
- `SimpleGraph.Reachable` and `SimpleGraph.Reachable.exists_isPath`;
- `SimpleGraph.induce` for restriction to a vertex subtype;
- `SimpleGraph.IsEdgeReachable` and `SimpleGraph.IsEdgeConnected`; and
- `SimpleGraph.Walk.IsPath.disjoint_support_of_append`, a support fact for one appended path.

These APIs can support a future encoding. They do not define the required vertex connectivity,
path-family packing, or vertex-separator extrema, and they state no Menger characterization. A
bounded search of pinned `SimpleGraph` sources and local Lean modules found no direct candidate.
This supports `M4`, not M3 or M0.

## Overlap and neighbor boundary

`THM-M-0813` is separately scheduled with the same attribution and year but the gloss `图中不相交
路径的最大数目` ("the maximum number of disjoint paths in a graph"). Repository generation keeps
the records separate because their titles and glosses differ. No accepted alias, deduplication,
corrected-source, or canonical-root ownership decision exists. This intake neither edits that
target nor imports its evidence.

Whitney's connectivity theorem, Konig's theorem, and max-flow/min-cut may be corollaries or proof
routes after the root is frozen. They are not statement-identity substitutes.

## Explicit exclusions

- silently choosing the global characterization solely because the gloss says connectivity;
- silently choosing the local set or point theorem solely because Menger and 1927 are named;
- replacing vertex-disjointness with edge-disjointness;
- max-flow/min-cut, Konig, Whitney, or generic connectivity infrastructure alone;
- a fixed `k`, fixed endpoints, or a special complete, bipartite, planar, or directed case;
- a structure field, hypothesis, oracle, or unchecked certificate storing the desired result;
- `THM-M-0813` evidence without an accepted identity and ownership decision; and
- the catalog's untrusted `已验证` label, a citation, search result, or API probe treated as proof.

No canonical expression, statement fingerprint, alternate transport, obligation registry,
discovery protocol, proof state, or completion claim is frozen at intake.
