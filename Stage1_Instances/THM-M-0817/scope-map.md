# Scope map

## Preserved theorem family

The repository fixes the eponym, Frank Ramsey attribution, year 1930, and a graph-language gloss:
"arbitrarily large graphs contain large complete subgraphs or independent sets." The intended root
must remain within Ramsey's homogeneous-substructure family. Intake does not silently choose among
these materially different statements:

1. **Finite symmetric graph form.** For every requested size `r`, some finite threshold `N` forces
   every sufficiently large finite simple graph to contain an `r`-clique or an `r`-independent set.
2. **Finite asymmetric graph form.** For requested sizes `r` and `s`, some threshold forces an
   `r`-clique or an `s`-independent set.
3. **Finite edge-coloring form.** For numbers of colors and requested homogeneous vertices, a large
   enough complete graph has a monochromatic complete subgraph. The graph form is a two-color
   encoding, not definitionally the same statement.
4. **Ramsey-number form.** Define or characterize the least threshold `R(r,s)`, which adds leastness
   and existence obligations beyond a threshold-existence theorem.
5. **Infinite form.** Every coloring of pairs from an infinite carrier has an infinite homogeneous
   set. This is not interchangeable with the finite theorem without a checked, source-approved
   bridge.
6. **Hypergraph or higher-arity form.** Colorings of `k`-subsets rather than graph edges. Nothing in
   the catalog selects this broader generalization.

## Decisions required at statement freeze

1. Select a lawful immutable primary edition and pinpoint result, then independently review its
   identity with the catalog target, incorporated definitions, proof boundary, and corrections.
2. Fix finite versus infinite scope and the quantifier order. In particular, distinguish "for each
   requested homogeneous size there exists a graph threshold" from the false reading that every
   individually large graph contains arbitrarily large homogeneous sets.
3. Fix symmetric versus asymmetric parameters, the number of colors, pair-coloring versus graph
   complement encoding, and threshold existence versus least Ramsey number.
4. Fix the graph carrier and finiteness model: `Fin N`, arbitrary finite types, finite sets inside a
   larger type, or cardinal lower bounds; specify simple/undirected/loopless assumptions.
5. Fix whether the conclusion uses a set, finset, induced subgraph, graph copy, or embedding, and
   whether size means exactly or at least the requested cardinality.
6. Resolve ordered-binder dependencies, monotonicity in the vertex threshold, and transports among
   complete-subgraph, independent-set, and monochromatic-edge formulations.
7. Resolve boundary cases for zero or one colors, zero/one/two requested vertices, empty or
   singleton carriers, thresholds below requested size, and any nonempty assumptions.
8. Freeze foundation, TCB, computation, freshness, minimal imports, expression fingerprint,
   checked alternate encodings, and all four statement mutations only after exact target selection.

## Explicit exclusions

- The specific numerical identities `R(3,3) = 6`, `R(4,4) = 18`, or any isolated Ramsey-number
  computation substituted for the general theorem.
- Van der Waerden, Hales-Jewett, Hindman, Erdos-Szekeres, Erdos-Ko-Rado, or other neighboring
  Ramsey-theory results substituted for the graph theorem.
- An infinite, hypergraph, multicolor, symmetric, asymmetric, or least-number theorem substituted
  for another variant without an approved source decision and checked relationship.
- A weakened bound, fixed small parameter, convenient finite carrier, assumed clique/independent
  witness, or structure that stores the desired conclusion as input.
- Pinned clique/independent-set definitions or complement lemmas presented as a Ramsey theorem.
- The catalog label `已验证`, a bibliographic URL, a successful `#check`, or prose certainty treated
  as human-proof, kernel-closure, or theorem-completion evidence.

No canonical expression, statement fingerprint, checked alternate encoding, obligation registry,
discovery protocol, proof state, or completion claim is frozen at intake.
