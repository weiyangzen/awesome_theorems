# Scope map

## Preserved topic boundary

The intake preserves the catalog's Bodlaender treewidth-algorithm family without silently
converting its approximation gloss into the famous exact fixed-parameter theorem. At least the
following materially different roots are plausible, and none is credited as the canonical target:

1. For each fixed natural `k`, decide in linear time whether a finite graph has treewidth at most
   `k`, returning a width-at-most-`k` tree decomposition in the positive branch.
2. Return a tree decomposition whose width is within a source-specified multiplicative or additive
   factor of optimum, with a source-specified running time.
3. Approximate only the numeric treewidth, without producing a decomposition certificate.
4. Prove correctness, termination, or a complexity bound for one executable implementation.

The 1996 Bodlaender article supports the first family, not the repository's literal approximation
wording. Choosing it is a proposition-changing source decision reserved for the statement phase
and independent review.

## Decisions required at statement freeze

1. Select an immutable source edition and exact theorem/page, reconcile the catalog wording with
   the 1996 article and its 1992/1993 precursors, audit corrections, and obtain independent scope
   approval.
2. Fix finite simple versus multi/directed graph input, vertex/edge encoding, graph size, and all
   decidability and finiteness assumptions.
3. Define a tree decomposition: the index tree, bags, vertex coverage, edge coverage, and connected
   or running-intersection condition.
4. Define decomposition width and graph treewidth, including the convention for empty graphs and
   the `max bag cardinality - 1` boundary.
5. Fix the quantifier order. The source family says `for every fixed k, there exists an algorithm`
   whose linear-time constant may depend on `k`; it does not automatically provide one uniform
   linear algorithm with a `k`-independent constant.
6. Fix the algorithm output: Boolean decision, positive certificate, negative certificate, exact
   width, approximate width, or decomposition; state soundness and completeness separately.
7. If approximation is retained, freeze the factor/additive error, success mode, and whether the
   guarantee concerns width, objective value, or a returned decomposition.
8. Fix executable semantics, input/output encodings, RAM or Turing-machine cost model, exact
   meaning of linear time, constants, arithmetic, and trusted computation boundary.

## Boundary cases to resolve

- empty, singleton, edgeless, complete, disconnected, and already-tree input graphs;
- `k = 0`, negative encodings, `k` at least the vertex count, and whether `k` is fixed or input;
- empty index trees or bag families, empty bags, repeated bags, and unused tree nodes;
- width of an empty decomposition and avoidance of natural-number underflow in `|bag| - 1`;
- multiple valid decompositions, positive witness selection, and negative-output semantics;
- loops, parallel edges, directed edges, labeled vertices, and graph isomorphism invariance;
- runtime measured in vertices, vertices plus edges, encoded bits, machine steps, or word-RAM
  operations; and
- exact mathematical execution versus finite-precision, heuristic, randomized, or oracle behavior.

## Substitution exclusions

- `THM-M-0870` treewidth definitions or structural properties alone;
- `THM-M-0871` Courcelle's theorem or any bounded-treewidth model-checking result;
- a generic graph-tree theorem, separator lemma, chordal completion, graph-minor theorem, or
  elimination ordering without the selected algorithmic conclusion;
- a decision theorem without the source-required decomposition output, or a decomposition theorem
  without the decision and runtime clauses;
- fixed-`k` linear time strengthened to uniform linear time, or an exact theorem weakened to an
  unspecified approximation;
- a structure or hypothesis that stores the desired algorithm correctness or runtime result;
- pseudocode, benchmark output, empirical runtime, a generated decomposition, or an unchecked
  certificate; and
- the catalog's `已验证` label, a citation, DOI, `#check`, or successful build used as proof credit.

No canonical statement, Lean target, expression fingerprint, checked alternate encoding,
discovery-protocol hash, obligation-registry hash, or accepted proof state is frozen at intake.
