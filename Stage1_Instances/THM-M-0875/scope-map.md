# THM-M-0875 scope map

## Received scope

The repository owns one topic record: the Weisfeiler-Lehman algorithm, glossed only as a heuristic
algorithm for graph isomorphism. Intake preserves that boundary and the catalog's 1968 attribution
without treating the `已验证` label as source or proof evidence. The standard spelling
Weisfeiler-Leman and the exact historical source relationship require review.

## Candidate roots not selected or credited

- define and prove isomorphism invariance of one-dimensional vertex color refinement;
- prove that unequal stable color data soundly witnesses nonisomorphism;
- prove refinement stabilizes, perhaps within a source-selected vertex-count bound;
- prove a runtime bound under a fixed data representation, implementation, and cost model;
- define the ordered-pair/coherent-closure procedure in the original paper and prove one of its
  stated invariants or termination properties;
- define `k`-dimensional tuple refinement and prove invariance, monotonicity, or a fixed-dimension
  complexity bound;
- prove completeness on a precisely named graph class; or
- formalize a source-selected limitation or counterexample to generic completeness.

The catalog selects none of these. In particular, no generic graph-isomorphism decision theorem is
admitted: the 2018 historical preface states that the original conjectures asserting such a result
were incorrect.

## Proposition-changing choices for statement freeze

1. Fix the algorithm variant: original ordered-arc/coherent-closure procedure, 1-WL vertex color
   refinement, `k`-WL tuple refinement, individualization-refinement, or another named variant.
2. Fix graph data: finite simple, directed, colored, labeled, looped, or multigraph; common or
   distinct vertex types; and any decidable equality, adjacency, or finiteness instances.
3. Fix initial colors and their equality/encoding; whether degrees, loops, edge colors, labels, or
   tuple equality patterns initialize the process.
4. Fix the update: neighbor-color sets or multisets, in/out-neighbor separation, tuple replacement
   coordinates, canonical renaming, simultaneous refinement of two graphs, and round indexing.
5. Fix termination and output: first stable partition, a bounded round, a stable color histogram,
   a coherent configuration, canonical labeling, an isomorphism rejection predicate, or another
   object.
6. Fix the theorem: well-definedness, invariance, soundness, stabilization, complexity,
   class-specific completeness, or a limitation/counterexample. State the ordered binders,
   hypotheses, conclusion, constants, and relationship to the source.
7. Fix computation and trust: mathematical function versus executable algorithm; exact versus
   hashed colors; collision assumptions; data structures; cost model; generated code, native
   evaluation, certificates, and any oracle or experiment boundary.

## Degenerate cases to resolve

- empty and singleton graphs, empty vertex or tuple types, and graphs of unequal cardinality;
- zero refinement rounds and dimension zero or one;
- constant, non-surjective, or differently encoded initial colors;
- isolated vertices, complete or edgeless graphs, loops, parallel edges, and directed asymmetry;
- already stable or fully discrete initial partitions and ties under canonical renaming;
- comparing graphs on one disjoint union versus separate runs and aligning color names;
- arithmetic overflow, hash collisions, malformed encodings, and zero-size cost bounds; and
- false completeness boundaries, including nonisomorphic graphs indistinguishable by the selected
  fixed-dimensional refinement.

No case is excluded at intake because no proposition is selected.

## Neighbor and substitution boundaries

- `THM-M-0873` separately owns the generic graph-isomorphism/quasipolynomial catalog record.
- `THM-M-0874` separately owns the Babai algorithm record.
- `THM-M-0876` separately owns the unresolved graph-isomorphism complexity-position record.
- `THM-M-1567` is a separate duplicate-domain graph-isomorphism catalog record.

None may donate a source statement, algorithm, complexity result, or proof body. Generic finite
graph or isomorphism APIs, a refinement datatype, an example computation, or a hypothesis that
stores the desired result is likewise not a proof of this target.

## Lean and review boundary

Pinned mathlib can express finite simple graphs, graph isomorphisms, neighborhoods, finite neighbor
sets, and degrees. It does not thereby select or implement the received algorithm. The statement
phase must first obtain an independently reviewed immutable source proposition and freeze the exact
Lean expression, minimal imports, environment fingerprint, checked transports, and required
mutations. The anchor audit, obligation registry, typed graphs, proof, validation, and release work
remain downstream.
