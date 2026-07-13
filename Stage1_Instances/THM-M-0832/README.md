# THM-M-0832 rev-5.6 dossier

This directory is the fail-closed `planned` intake dossier for the Stoer-Wagner algorithm. The
catalog supplies only the phrase "deterministic algorithm for the global minimum cut," attributes
it to Stoer and Wagner in 1994, and labels it verified. That identifies an algorithm family, but it
does not freeze a truth-valued correctness or complexity proposition.

The expanded paper by Mechthild Stoer and Frank Wagner, *A Simple Min-Cut Algorithm*, was inspected
at a recorded SHA-256. It states that the input is an ordinary undirected graph with nonnegative real
edge weights, defines a minimum cut as a nontrivial vertex partition of least crossing-edge weight,
and gives the contraction algorithm based on maximum-adjacency-search phases. Theorem 2.1 and Lemma
3.1 provide the correctness route. The paper also states the running time, but the catalog does not
say whether complexity is part of this target. The paper's preliminary version appeared at ESA 1994,
which explains the catalog year; the inspected expanded version appeared in JACM in 1997.

The source still leaves statement decisions for this repository: algorithm semantics and tie
breaking, the exact output contract, whether only correctness or also termination and complexity are
in the root, graph representation, parallel-edge contraction, and the treatment of graphs with zero
or one vertex. Pinned mathlib supplies adjacent finite simple-graph and edge-connectivity interfaces,
but no weighted global-min-cut or Stoer-Wagner declaration was located by the bounded intake search.

Accordingly the canonical mathematical and Lean statements remain null. The provisional vector is
`[H1, M4, R4]`: a pinpoint primary proof route is known, but the exact source proposition and all
assumptions are not yet admitted and reviewed; no usable exact Lean artifact exists; and no readable
proof reconstruction has been accepted. All downstream tasks remain open. No proof, accepted
execution state, audit completion, theorem completion, or master acceptance is claimed.
