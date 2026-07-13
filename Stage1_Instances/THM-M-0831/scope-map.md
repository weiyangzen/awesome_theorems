# Scope map

## Preserved topic boundary

The intake preserves the catalog's Karger randomized global-minimum-cut algorithm family. The
inspected 1993 paper makes several distinct mathematical claims in this family. The catalog does
not select among them, so none is frozen as the canonical proposition at intake:

1. **Single-trial fixed-cut probability.** For a connected undirected multigraph on `n` vertices,
   one run of the contraction algorithm returns a particular global minimum cut with probability
   at least `1 / binom(n, 2)`.
2. **Amplification.** Independent repetitions find a minimum cut, or every minimum cut, with a
   source-specified high-probability guarantee. This needs an explicit trial count, failure
   parameter, independence model, and output-selection rule.
3. **Weighted implementation.** Integer weights may be represented by parallel edges, while later
   paper sections describe efficient sampling for weighted graphs. This changes the input and
   algorithm model.
4. **Runtime or RNC results.** Sequential time, space, PRAM time, processor, and strongly
   polynomial bounds require executable semantics and a cost model beyond the probability lemma.

## Decisions required at statement freeze

1. Select and independently approve a pinpoint source proposition: Theorem 2.1, Corollary 2.1, a
   weighted extension, an implementation-correctness statement, a complexity statement, or an
   explicit conjunction with separately modeled obligations.
2. Fix the graph representation: finite connected undirected loopless multigraph; weighted graph;
   allowance for zero-weight edges; and whether the ambient vertex and edge types contain unused
   elements.
3. Define a cut, nontrivial bipartition, crossing-edge multiplicity or total weight, global
   minimum-cut value, equality of cuts up to complement, and the meaning of one "particular" cut.
4. Define contraction exactly: uniform selection among current edge instances, endpoint quotient,
   parallel-edge preservation, deletion of newly created loops, transition state, and termination
   at two nonempty supervertices.
5. Fix the probability semantics: finite trajectory PMF or measure, conditional choices after each
   contraction, treatment of impossible/empty states, event that the output equals a selected cut,
   and the codomain and coercions used for `1 / binom(n, 2)`.
6. Fix all ordered binders and hypotheses, including finiteness, connectivity, minimum-cut
   existence, `n >= 2` or a stronger lower bound, nonempty edge choices, and any decidable equality
   instances needed by an executable model.
7. For repetition, fix the number of trials, independence construction, tie handling, best-cut
   selection, exact failure probability, and the formal meaning of "with high probability."
8. For runtime claims, freeze the computation and machine model, primitive operations, input-size
   encoding, asymptotic relation, randomness cost, processor model, and space accounting.

## Boundary and degenerate cases

The statement phase must decide disconnected graphs; empty, singleton, and two-vertex graphs;
graphs with no edges; loops in the input; parallel edges; banana graphs; multiple distinct minimum
cuts; cuts equal up to complement; zero minimum-cut value; contraction states with no selectable
edge; repeated contractions; and whether `n = 2` returns the initial cut with probability one. For
weighted variants it must also decide zero, negative, nonintegral, and encoded multiplicities. The
formula `1 / binom(n, 2)` requires explicit handling where the denominator is zero.

## Explicit exclusions

- A deterministic min-cut theorem, max-flow/min-cut duality, Stoer-Wagner, or another algorithm may
  not substitute for Karger's randomized contraction result.
- An `s-t` minimum cut is not the source's unrestricted global minimum cut.
- A result for simple graphs alone silently loses the parallel edges created by contraction unless
  a checked transport preserves the source model.
- Directed graphs, hypergraphs, vertex cuts, multiway cuts, approximate cuts, and network
  reliability are neighboring results, not the unidentified root.
- Merely showing that avoiding a fixed cut implies it survives does not establish the survival
  probability or the algorithm's complete output theorem.
- A random permutation, minimum-spanning-tree interpretation, or weighted sampler can be used only
  with a checked equivalence to the selected contraction semantics.
- A finite simulation, benchmark, pseudocode transcription, URL, theorem name, or the catalog's
  `已验证` label supplies no human-source or kernel-proof credit.

## Neighbor and formal boundaries

`THM-M-0830` owns Push-Relabel and `THM-M-0832` owns Stoer-Wagner. Max-flow, deterministic global
min-cut, and adjacent graph-algorithm artifacts remain separate targets and grant no status here.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`, `Graph` models an
undirected multigraph with explicit vertex and edge sets and an incidence predicate; it permits
parallel edges and loops. `PMF.uniformOfFinset` and `PMF.ofMultiset` support finite random choice.
A bounded topic search found no graph-contraction or minimum-cut algorithm API. No canonical Lean
expression, checked transport, obligation registry, discovery protocol, proof state, or completion
claim is frozen at intake.
