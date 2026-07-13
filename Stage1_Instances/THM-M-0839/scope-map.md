# Scope map

## Preserved catalog scope

The repository fixes target `THM-M-0839`, title `完美图定理`, attribution to Laszlo Lovasz, year
1972, and the claim `图的完美性与其补图的完美性等价`: the perfectness of a graph is equivalent to
the perfectness of its complement. The attribution, date, and neighboring strong-theorem entry
identify the weak perfect graph theorem family.

The intake preserves the equivalence and same-vertex complement boundary. It does not turn common
textbook conventions into accepted source clauses. In particular, "perfect" normally quantifies
over every induced subgraph, not just the ambient graph, but the repository record does not define
the term.

## Proposition-changing decisions

Before statement elaboration, an accepted source decision must freeze:

- one immutable primary edition, exact theorem/page, incorporated definitions, proof boundary,
  corrections or errata, and independent source review;
- finite simple undirected loopless graphs versus another graph model, the vertex type and universe,
  finiteness data, and all decidability assumptions;
- whether perfectness quantifies over every vertex subset, every induced subgraph up to embedding,
  or every graph isomorphic to an induced subgraph;
- the chromatic-number codomain and finite-value proof, the clique-number convention, coercions
  between `Nat` and `ENat`, and equality orientation;
- complement on the identical carrier, including its relation to induce, subtype carriers, and
  complement involution;
- whether the root is written as `Perfect G <-> Perfect Gᶜ`, one implication plus complement
  involution, or a source-approved equivalent statement with checked transports;
- ordered binders, typeclass hypotheses, classical-choice policy, and every excluded or admitted
  boundary case.

These choices alter the Lean proposition and cannot be selected merely because they are standard.

## Boundary cases

The statement phase must decide the empty and singleton vertex types, empty and complete graphs,
empty induced subsets, zero clique and chromatic numbers, graphs with isolated or universal
vertices, disconnected graphs, complement on subtype carriers, and whether finite cardinality is a
typeclass premise or encoded explicitly. No case is excluded at intake.

## Explicit exclusions

- The strong perfect graph theorem characterizing perfect graphs by odd holes and antiholes, owned
  separately by `THM-M-0840`.
- Equality of chromatic and clique numbers only for the ambient graph, without all induced
  subgraphs.
- Perfect matching, chordal, comparability, bipartite, weighted-perfect, directed, multigraph,
  infinite-graph, or hypergraph theorems substituted for the root.
- The replication lemma, stable-set inequalities, normal-hypergraph duality, or complement
  involution presented as the root rather than as possible proof ingredients.
- A predicate or hypothesis that stores the desired equivalence or assumes both perfectness facts.
- The catalog's `已验证` field, an API probe, or a bounded absence search used as proof evidence.

## Formal boundary

No canonical Lean expression is frozen. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, `IntakeProbe.lean` checks `SimpleGraph.compl_adj`,
`SimpleGraph.induce`, `SimpleGraph.chromaticNumber`, `SimpleGraph.cliqueNum`,
`SimpleGraph.cliqueNum_le_chromaticNumber`, and `SimpleGraph.cliqueNum_compl`. The definitions use
different codomains (`ENat` for chromatic number and `Nat` for clique number), making coercion and
finiteness choices substantive. A bounded exact-topic search found no graph-perfectness predicate
or weak perfect graph theorem. This is feasibility reconnaissance, not the downstream exhaustive
anchor audit and not proof evidence.
