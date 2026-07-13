# Scope map

## Preserved catalog scope

The repository fixes only target `THM-M-0845`, the label `图同态计数` (graph homomorphism
counting), collective attribution to many mathematicians, the twentieth century, and the gloss
`子图同态的计数` (literally "counting of subgraph homomorphisms"). Intake preserves the finite
graph-theory and homomorphism-counting subject boundary without turning the noun phrase into a
theorem.

## Candidate families not credited

The inspected source lead demonstrates several inequivalent possibilities. None is selected at
intake:

1. The raw number `hom(F,G)` of adjacency-preserving maps from one finite graph to another.
2. The normalized density `t(F,G)`, interpreted as the probability that a uniformly random vertex
   map is a homomorphism.
3. Weighted homomorphism sums and partition functions, allowing vertex or edge weights and loops.
4. Identities for disjoint unions or products, and inequalities among homomorphism numbers.
5. Conversion identities among ordinary, injective, induced, and surjective counts.
6. A Lovasz-type theorem that a graph is characterized by its homomorphism profile.
7. Characterizations of graph parameters representable as homomorphism functions.
8. Graph-sequence convergence, graph limits, metric, or property-testing results expressed through
   homomorphism densities.
9. An algorithmic counting or computational-complexity theorem.

A definition or computable cardinality for one fixed pair is not itself a selected catalog theorem.
The survey is a topic-level source lead, not evidence that the catalog intended every result it
contains or any particular one.

## Proposition-changing decisions

Before statement elaboration, an approved source decision must freeze all of the following:

- an immutable primary or authoritative source, exact numbered result, edition/pages, incorporated
  definitions, proof boundary, corrections, and independent review;
- whether graphs are finite simple graphs, looped graphs, multigraphs, directed graphs, bipartite
  graphs, labelled graphs, weighted graphs, graphons, or another structure;
- the direction and order of the source and target graphs in every homomorphism type;
- whether maps preserve adjacency only or also reflect adjacency, and whether injectivity,
  surjectivity, inducedness, labels, or colors are required;
- whether "counting" denotes a natural cardinality, weighted sum, normalized density, asymptotic,
  identity, inequality, characterization, algorithm, or complexity claim;
- the coefficient and normalization domains, including treatment of zero vertex counts and zero
  weights;
- exact ordered binders, quantification over graphs or graph families, hypotheses, conclusion,
  strictness, equality or approximation mode, parameter dependence, and every boundary case; and
- whether a finite decidable encoding is required for computation or only mathematical finiteness
  is required for a noncomputable cardinality.

These choices change the proposition. They cannot be reconstructed from the title by selecting the
most familiar theorem.

## Explicit exclusions

- A definition of `SimpleGraph.Hom` or `Fintype.card (F →g G)` presented as the missing theorem.
- An embedding, induced-copy, coloring, triangle-counting, or subgraph-count theorem silently
  substituted for an ordinary graph-homomorphism result.
- A normalized density silently substituted for an unnormalized count, or conversely.
- Weighted or looped graphs silently substituted for finite simple graphs.
- A graph-limit, characterization, inequality, or complexity theorem chosen only because it uses
  homomorphism counts.
- A calculation for one convenient pair of graphs, exhaustive experiment, or generated table.
- A predicate, structure, hypothesis, axiom, or placeholder that assumes the desired count result.
- The catalog label `已验证` as human-source or Lean kernel evidence.

## Boundary cases

The statement phase must resolve empty source and target vertex types, edgeless and complete graphs,
loops and parallel edges if allowed, homomorphisms into an empty graph, the unique empty-domain map,
isolated vertices, equal source and target, disconnected graphs, zero normalization denominators,
zero or negative weights if weighted graphs are selected, labelled versus unlabelled counting,
automorphism multiplicities, and the relationship among ordinary, injective, induced, and
surjective maps.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean` checks
`SimpleGraph.Hom`, `SimpleGraph.Embedding`, `SimpleGraph.Iso`, homomorphism composition, the finite
instance for relation homomorphisms, and `Fintype.card`. It also synthesizes
`Fintype (F →g G)` under finite decidable graph assumptions. A bounded exact-topic source search
found no named general graph-homomorphism-count theorem. These are feasibility observations, not an
exhaustive anchor audit, a canonical statement, or proof evidence.
