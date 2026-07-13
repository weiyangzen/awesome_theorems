# Scope map

## Received claim

`Docs/researches/math_theorems.md:5977-5982` records the title `门格尔定理`, Karl Menger, 1927,
and the gloss `图中不相交路径的最大数目` ("the maximum number of disjoint paths in a graph").
It gives no equality, comparator, terminal objects, graph model, definitions, assumptions, formula,
proof boundary, bibliography, or formal declaration. The Stage0 projection at
`Docs/Stage0_Blueprint.md:22199-22224` repeats the gloss and explicitly leaves precise definitions,
premises, equivalent forms, axioms, machine status, and artifact links open.

The phrase is not yet a proposition: it names one side of an extremal equality without saying what
the maximum equals. Intake preserves this literal boundary instead of silently completing it from
memory.

## Candidate theorem family

The statement phase must select, from an independently reviewed exact source, among materially
different roots such as:

1. **Set-to-set vertex form.** The minimum size of an `A`-`B` vertex separator equals the maximum
   size of a family of pairwise vertex-disjoint `A`-`B` paths.
2. **Point-to-point vertex form.** For distinct nonadjacent vertices `a,b`, the minimum number of
   other vertices separating them equals the maximum number of internally vertex-disjoint
   `a`-`b` paths.
3. **Edge form.** The minimum size of an edge separator equals the maximum number of pairwise
   edge-disjoint paths.
4. **Global connectivity form.** `k`-vertex-connectivity or `k`-edge-connectivity is characterized
   by the corresponding number of independent or edge-disjoint paths between every two vertices.
5. **Directed, infinite, or topological forms.** These change the graph carrier, direction,
   finiteness assumptions, cardinal arithmetic, and often the separator or path-family conclusion.

Diestel, *Graph Theory*, sixth edition (2025), Section 3.3, distinguishes exactly the first four:
Theorem 3.3.1 is the finite set-to-set vertex theorem; Corollary 3.3.5 gives the point and edge
forms; Theorem 3.3.6 gives the global forms. Their mathematical relationships do not authorize the
intake to merge them into one unspecified root.

## Decisions required at statement freeze

- finite simple undirected graph, multigraph, digraph, infinite graph, or another graph model;
- vertex-disjoint, internally vertex-disjoint, or edge-disjoint paths;
- terminal sets `A,B`, a vertex and a set, or distinct vertices `a,b`;
- whether terminal sets may overlap and whether zero-length paths count;
- the separator definition, whether terminal vertices may be removed, and how adjacency is handled;
- minimum/maximum as natural numbers, finite cardinalities, extended cardinalities, or existence of
  `k` witnesses without explicitly forming extrema;
- the exact family representation and pairwise-disjointness predicate;
- local equality versus global connectivity equivalence and every finiteness hypothesis; and
- ordered binders, universes, decidability/typeclass assumptions, conclusion orientation, and all
  degenerate cases.

## Boundary cases to resolve

- empty, singleton, and infinite vertex types;
- empty, overlapping, equal, or non-disjoint terminal sets;
- equal endpoints and adjacent distinct endpoints;
- disconnected graphs and graphs with no eligible path;
- `k = 0` and `k = 1`, empty path families, and trivial paths;
- complete and empty graphs, isolated vertices, loops or parallel edges if the model permits them;
- separators containing terminal vertices versus separators required to avoid them; and
- maxima/minima when the relevant collection is empty or infinite.

No boundary case is excluded before one exact proposition is selected.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, the directly inspected
simple-graph surface provides:

- `SimpleGraph.Path` and `SimpleGraph.Walk.IsPath`;
- `SimpleGraph.Reachable` and `SimpleGraph.Reachable.exists_isPath`;
- `SimpleGraph.induce` for restriction to a vertex subtype;
- `SimpleGraph.IsEdgeReachable` and `SimpleGraph.IsEdgeConnected`; and
- `SimpleGraph.Walk.IsPath.disjoint_support_of_append`, a local support fact for one appended path.

These definitions and lemmas can support a later encoding. They neither define the required
path-family packing and vertex-separator extrema nor state a Menger equality. A bounded search of
the pinned `SimpleGraph` sources and local Lean modules found no direct terminal declaration. This
justifies `M4`, not M3 or M0.

## Duplicate and neighbor boundary

`THM-M-0862` is separately scheduled with the same attribution and year but the gloss
`顶点连通度与不相交路径` ("vertex connectivity and disjoint paths"). It may intend a local or
global vertex form of the same theorem family. No accepted alias, deduplication, corrected-source,
or canonical-root ownership decision exists. This intake neither edits that target nor transfers
its prospective evidence.

Nearby catalog targets such as Konig's theorem and max-flow/min-cut can furnish reductions or proof
routes only after the root is frozen. They are not substitute statements.

## Explicit exclusions

- choosing a familiar point-to-point theorem solely because it is convenient to encode;
- replacing vertex-disjointness by edge-disjointness, or conversely;
- max-flow/min-cut, Hall, Konig, Whitney, or generic connectivity alone;
- a special `k`, a complete/bipartite/planar graph restriction, or a fixed pair of vertices;
- a structure field, hypothesis, oracle, or unchecked certificate storing the desired paths or cut;
- `THM-M-0862` evidence without an accepted identity and ownership decision; and
- the catalog's untrusted `已验证` label, a citation, search result, or API probe treated as proof.

No canonical expression, statement fingerprint, checked alternate encoding, obligation registry,
discovery protocol, proof state, or completion claim is frozen at intake.
