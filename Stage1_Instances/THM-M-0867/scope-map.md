# THM-M-0867 scope map

## Received claim

The repository supplies the name `Robertson-Seymour图子式定理` and the gloss
`图子式良拟序定理`. Intake preserves the recognizable finite-graph/minor/WQO family but does not
choose one exact proposition from that wording.

## Candidate family

A conventional sequence form is:

```text
For every sequence G : Nat -> finite graphs, there are i < j such that G i is
isomorphic to a minor of G j.
```

This is explanatory scope, not the canonical statement. The statement phase must source-select and
fix all of the following:

1. finite undirected graphs, finite directed graphs, simple graphs, multigraphs, or another model;
2. a sigma type of finite vertex types, a canonical `Fin n` representation, or isomorphism classes;
3. whether loops and parallel edges are allowed during contraction and how they are simplified;
4. the exact minor relation: deletion plus edge contraction, branch-set models, or a checked
   equivalent encoding, including its argument orientation;
5. an infinite-set, infinite-sequence, or WQO formulation and the checked implications between
   them, including the role of repetitions and isomorphism;
6. ordered binders, universes, finiteness witnesses, decidable equality/adjacency, and all
   typeclass assumptions;
7. empty and singleton graphs, edgeless graphs, isolated vertices, loops, parallel edges, empty
   input families, and constant or repeating sequences.

## Primary-source boundary

The inspected Robertson-Seymour paper states in its abstract that every infinite set of finite
graphs contains one member isomorphic to a minor of another. The introduction explicitly says all
graphs in the paper are finite. Theorem 10.5 states a countable-sequence result for directed graphs
and says it immediately implies the standard undirected form. These passages identify the family,
but intake does not silently equate them with a particular Lean `WellQuasiOrdered` expression.

Before H0, reviewers must preserve the admitted edition, identify the authoritative theorem and
all incorporated definitions, map every premise and conclusion, establish set/sequence/WQO and
directed/undirected transports, inspect corrections and errata, and independently approve the
crosswalk.

## Pinned Lean boundary

At mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`:

- `WellQuasiOrdered` supplies the generic sequence predicate;
- `SimpleGraph`, `SimpleGraph.Iso`, and `SimpleGraph.induce` supply adjacent graph structure;
- `SimpleGraph.deleteEdges` supplies edge deletion;
- `SimpleGraph.map` is a generic pushforward operation, not by itself a graph-minor definition or
  a proof that contraction has the required semantics.

The bounded pinned/repo-local search located no named Robertson-Seymour theorem, graph-minor WQO
closure, or simple-graph minor/contraction API. This is a bounded discovery result, not a complete
anchor audit or an external nonexistence claim.

## Explicit exclusions

- Replacing the root with the generic fact that a finite carrier is WQO.
- Using induced-subgraph containment, graph embedding, graph homomorphism, edge deletion alone, or
  matroid minors as the graph-minor relation.
- Defining a structure with the desired theorem as a field and projecting it.
- Assuming the WQO conclusion as a hypothesis or typeclass instance.
- Proving only bounded-order graphs, trees, planar graphs, excluded-minor classes, or another
  special family.
- Treating a theorem name, the catalog's `已验证` label, a `#check`, or a source URL as proof credit.

## Neighbor boundary

`THM-M-0868` is separately named `图子式定理`, dated 1983-2004, and glossed as the proof of
Wagner's conjecture. The literature overlaps, but no source, statement, task, or proof credit may
be transferred between the targets without a later explicit reconciliation. Wagner's planar-graph
theorem (`THM-M-0866`), Kuratowski's theorem (`THM-M-0865`), treewidth (`THM-M-0870`), and
Courcelle's theorem (`THM-M-0871`) also remain distinct targets.
