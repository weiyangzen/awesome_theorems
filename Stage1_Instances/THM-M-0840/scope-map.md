# Scope map

## Preserved theorem family

The intake preserves the finite-simple-graph strong perfect graph theorem identified by the
catalog and the inspected primary article: a graph is perfect if and only if it is Berge, where
perfectness quantifies over every induced subgraph and the Berge condition excludes induced odd
cycles of length at least five and their complements.

This is a source-backed scope description, not the frozen canonical proposition. The statement
phase must still select and independently approve an exact encoding before it may create an
elaborated expression fingerprint or inspect proof closure.

## Decisions required at statement freeze

An exact source-reviewed statement must decide all of the following:

1. The finite vertex representation: a `Fintype` simple graph, an explicitly finite vertex set, or
   a graph with a `Finite` instance, together with universe and decidability requirements.
2. The definition of perfectness, including whether every vertex subset, every induced embedding,
   or every induced subgraph object is quantified over and how the empty induced graph is handled.
3. How the source's natural-valued chromatic number is related to mathlib's `ENat`-valued
   `SimpleGraph.chromaticNumber`, and whether finiteness is used to eliminate `top`.
4. How maximum clique size is represented and coerced when compared with chromatic number.
5. The representation of a hole as an induced chordless cycle, including cycle length and parity,
   rather than an arbitrary cycle or a non-induced subgraph.
6. The representation of an antihole: a hole in the complement, or the complement of an induced
   hole, together with a checked equivalence between those encodings.
7. Whether the root is stated as `Perfect G <-> Berge G`, as forbidden odd holes and antiholes
   directly, or through an exact checked transport between the two.
8. The exact ordered binders, typeclasses, side conditions, foundation/TCB/computation profiles,
   minimal imports, and all mutation tests required by rev-5.6.

These choices alter the proposition, elaboration environment, or proof boundary. Intake does not
silently settle them from mathematical memory.

## Degenerate and boundary cases

Source review and statement mutation must explicitly address the empty graph, a singleton graph,
graphs on two to four vertices, complete and edgeless graphs, bipartite graphs, an odd cycle of
length exactly five, even holes, complements of cycles, self-complementary cases, empty induced
vertex subsets, and whether length-three cycles are excluded by the word "hole." It must also
verify that every induced subgraph in the perfectness definition remains finite and that no
decidability premise becomes an unintended mathematical hypothesis.

## Excluded substitutions

- The weak perfect graph theorem, `THM-M-0839`, only says that complements preserve perfectness.
- Only the easy direction, that every perfect graph is Berge, is not the biconditional theorem.
- Excluding odd cycles as ordinary subgraphs is stronger than excluding odd holes and changes the
  theorem; chordlessness and inducedness cannot be dropped.
- Excluding only odd holes, or only odd antiholes, is incomplete.
- Perfect matching, perfect groups, perfect fields, strongly regular graphs, or graph perfection
  algorithms are unrelated despite overlapping words.
- A result for a special graph class, a finite enumeration, or a stored witness of perfectness is
  not the universal theorem.
- A theorem title, source URL, `#check`, or the untrusted catalog label `已验证` supplies no H or M
  credit.

## Neighbor boundaries

`THM-M-0839` owns the weak perfect graph theorem (perfect iff complement perfect). `THM-M-0833`
owns the four-color theorem and `THM-M-0834` the five-color theorem. Coloring and clique APIs can be
shared substrate only after exact dependency freezes; no neighboring theorem grants proof status
to this target.

## Formal boundary

No canonical Lean expression is frozen at intake. At pinned mathlib revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95`, the discovery probe checks induced graphs,
complements, cycle predicates, chromatic number, clique number, and their basic inequality. A
bounded source search found no exact perfect-graph/Berge/SPGT declaration. This is scoped discovery
evidence, not an exhaustive anchor audit or a proof of global absence.
