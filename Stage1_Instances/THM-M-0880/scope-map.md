# THM-M-0880 scope map

## Received scope

The repository fixes only the title `稀疏割`, the collective attribution `众多数学家`, the period
`20世纪`, and the gloss `图划分的稀疏性`. It gives no bibliography, definition, formula, ordered
binders, hypotheses, conclusion, constants, boundary cases, proof, or formal artifact. Stage0
repeats this wording and explicitly leaves the formal system, exact definitions and premises,
proof route, dependencies, equivalent forms, axioms, machine state, and artifact links open. The
`已验证` label is untrusted metadata.

The conventional English topic translation "sparse cut" is adequate for catalog navigation, but
not for statement identity. Depending on the source, "sparsity" can normalize a cut capacity by
side cardinalities, side volumes, a product, a minimum, or separated demand; can require a balanced
cut; and can denote an objective value, an optimizer, an existence theorem, or an approximation
guarantee.

## Candidate mathematical families

An eventual source-approved target could concern one of the following, but none is asserted or
credited at intake:

- the definition and elementary properties of an edge boundary or cut capacity;
- existence of a nontrivial cut attaining minimum sparsity in a finite graph;
- uniform sparsest cut, with an edge-capacity numerator and cardinality-based denominator;
- nonuniform sparsest cut, with capacity separated divided by demand separated;
- conductance or edge expansion, normalized by volume or the smaller side;
- a balanced-separator theorem with a stated balance parameter;
- exact optimization, an approximation algorithm and ratio, an integrality-gap result, or a
  flow/metric/spectral comparison theorem.

These have different domains, constants, quantifier orders, degenerate cases, algorithms, and
proof obligations. A textbook convention cannot choose among them.

## Proposition-changing decisions

Before the statement phase can freeze a canonical claim, an accepted source and reviewer must fix:

1. The graph model: finite simple graph, multigraph, directed graph, weighted graph, or a complete
   demand graph; and whether loops, parallel edges, and disconnected graphs are allowed.
2. The cut representation: one subset, an ordered bipartition, an unordered bipartition, or a
   partition with more than two parts; and whether both sides must be nonempty.
3. Edge capacities and pair demands, including coefficient type, nonnegativity, symmetry,
   finiteness, support, and whether an unweighted graph means unit capacity or edge count.
4. The numerator: crossing edge count, total crossing capacity, directed outgoing capacity, or
   another boundary measure.
5. The denominator/normalization: `|S| * |V \ S|`, `min |S| |V \ S|`, volume, separated demand,
   a balance constraint without division, or another convention.
6. The handling of zero denominators, zero demand, zero capacity, empty/full sides, isolated
   vertices, and empty or singleton vertex types.
7. Whether the root asks for a value, a minimizing cut, existence of an optimizer, an inequality,
   a reduction, an equivalence, or an algorithm.
8. If algorithmic, the input encoding, rational/real arithmetic, output and certificate, exact or
   approximate objective, approximation ratio, deterministic/randomized guarantee, success
   probability, and time/space complexity model.
9. All balance thresholds, constants, strict versus non-strict inequalities, asymptotic
   quantifiers, ordered binders, and source corrections.

These decisions alter truth conditions. They are a resolution checklist, not a canonical claim.

## Boundary and degenerate cases

The statement phase must explicitly resolve empty and full cuts, singleton graphs, disconnected
graphs, isolated vertices, edgeless and complete graphs, all-zero capacities or demands, demand
supported only within a side, zero denominators, infinite ratios, ties between minimizers, and
cuts whose two sides are exactly at a balance threshold. For weighted statements it must distinguish
natural, rational, nonnegative-real, and real weights and state whether negative weights are legal.

Without nontrivial-side or positive-demand conditions, common ratio definitions may be undefined,
convention-dependent, or vacuous. Without a balance condition, a "sparse partition" may select a
singleton side even when the intended problem is balanced separator. These are statement gates,
not details to infer later.

## Explicit exclusions

- `THM-M-0877` network flow, `THM-M-0878` minimum-cost flow, `THM-M-0879` multicommodity flow,
  `THM-M-0814` maximum-flow/minimum-cut, `THM-M-0831` Karger, `THM-M-0832` Stoer-Wagner,
  `THM-M-0881` expander graphs, `THM-M-0887` spectral graph theory, and `THM-M-0888` Cheeger
  inequality are separate Stage1 roots. They may become dependencies only through a selected exact
  statement and typed bridges.
- The `THM-C-0077` Arora-Rao-Vazirani record in `Docs/researches/cs_theorems.md` separately names an
  `O(sqrt(log n))` approximation result. It identifies one possible theorem family but is not this
  source record and cannot supply this root's statement or status.
- A minimum-cardinality cut, maximum cut, conductance, edge-connectivity, expansion, or balanced
  separator result cannot substitute for sparsest cut without source-selected definitions and
  checked transports.
- A structure or hypothesis that assumes the requested sparse cut, optimum, ratio, or approximation
  guarantee cannot be counted as constructing or proving it.
- A numerical cut search, benchmark, solver result, or finite graph example cannot replace a
  quantified theorem.
- The catalog's `已验证` label, a title match, a `#check`, or an adjacent API supplies no H or M
  credit.

## Formal boundary

No canonical Lean expression is frozen. Pinned mathlib supplies finite simple graphs, edge sets and
edge finsets, induced subgraphs, degree data, edge-deletion connectivity, and edge density between
two vertex finsets. `SimpleGraph.edgeDensity` divides an ordered interedge count by `|S| * |T|`;
this is adjacent substrate, not a selected sparsest-cut objective. Mathlib also has a graph-coloring
partition structure, which means a partition into independent sets rather than a two-way cut.
A bounded exact-topic search found no sparse-cut, conductance, Cheeger-constant, or edge-expansion
declaration matching the catalog. These are intake discovery facts only, not the downstream
immutable anchor audit or a global absence claim.
