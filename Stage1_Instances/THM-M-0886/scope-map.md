# Scope map

## Preserved theorem family

The catalog phrase is preserved as the existence theorem for finite `(c,d)`-biregular bipartite
Ramanujan graphs. The closest exact source result is published MSS Theorem 5.6:

- natural degrees `c,d >= 3`;
- a finite undirected bipartite graph with every vertex on one side of the bipartition having
  degree `c` and every vertex on the other having degree `d`;
- trivial adjacency eigenvalues `+sqrt(c*d)` and `-sqrt(c*d)`;
- every nontrivial eigenvalue bounded in absolute value by
  `sqrt(c - 1) + sqrt(d - 1)`; and
- an infinite, size-growing sequence for each fixed pair `(c,d)`.

These bullets are a source-family crosswalk, not an accepted canonical statement. The statement
phase must freeze them against one admitted edition and independently review the translation.

## Decisions required at statement freeze

1. Fix the binder order and whether the root says `forall c d >= 3, exists sequence` or uses an
   equivalent family indexed by `Nat`.
2. Encode finite ordinary graphs, the vertex carrier and its finiteness, the two bipartition sides,
   coverage and disjointness, and the side-specific degree conditions.
3. Decide whether the paper's graph convention means loopless simple graphs in Lean or whether a
   multigraph model is required. No loops or parallel edges may be introduced silently.
4. Define the real adjacency matrix, eigenvalues with algebraic multiplicity, and exactly which
   occurrences of `+sqrt(c*d)` and `-sqrt(c*d)` are removed as trivial.
5. Freeze the Ramanujan inequality and the coercions/subtractions inside its square roots.
6. Make `infinite sequence` nonvacuous. The proof repeatedly takes 2-lifts and doubles vertex
   count; a constant or merely repeated sequence cannot satisfy the intended conclusion.
7. Decide whether connectedness is assumed, derived, or absent in the selected edition and
   definition. Do not import a conventional connectedness clause without source evidence.
8. Record every boundary case and checked relationship to alternate encodings before inspecting
   any proof candidate.

## Boundary and degenerate cases

The source definitions discuss `c,d >= 2`, while Theorem 5.6 assumes `c,d >= 3`. The cases
`c < 3`, `d < 3`, `c = d`, an empty bipartition side, a zero-vertex graph, unequal side cardinality,
disconnected graphs, repeated graphs in a sequence, duplicated trivial eigenvalues, loops,
parallel edges, and eigenvalues exactly on the spectral bound all require explicit treatment.

The inequality is non-strict. The regular specialization `c = d` is allowed by the biregular
theorem, but it must not be used to replace the two-parameter claim.

## Neighbor and substitution exclusions

- `THM-M-0339` is the distinct MSS/Kadison-Singer record. Its finite-frame partition theorem and
  evidence cannot supply this graph theorem.
- Published Theorem 5.5 proves the regular bipartite special case. It is not a replacement for
  Theorem 5.6 with independent `c` and `d`.
- *Interlacing Families IV* proves graphs of every degree and every size by unions of perfect
  matchings and explicitly permits multiple edges. It is a different theorem and graph model.
- The earlier MSS 2-lift theorem for one graph, the real-rooted/interlacing polynomial lemma, and
  the matching-polynomial bound are proof components, not the existence root.
- A single complete bipartite graph, a constant sequence, an arbitrarily large one-off graph, or a
  sequence merely assumed as structure data does not prove the infinite size-growing family.
- A graph whose nontrivial spectrum satisfies a weaker asymptotic or epsilon bound is not
  Ramanujan at the exact source constant.
- Numerical eigensolver output, random sampling, and a finite list of examples provide no theorem
  credit without a kernel-checked certificate for the exact quantified claim.
- The repository's `verified` label and this intake probe provide no source-fidelity or proof
  evidence.

## Formal boundary

Pinned mathlib exposes finite simple graphs, a newer multigraph structure, bipartite predicates,
finite degrees, real adjacency matrices, Hermitian spectral enumeration, and permutation matrices.
The intake probe authenticates only those interfaces. It does not define side-specific
biregularity, trivial spectral multiplicities, Ramanujan bounds, graph 2-lifts, or a size-growing
sequence. No canonical Lean target, expression fingerprint, checked transport, mutation suite, or
proof body is claimed.
