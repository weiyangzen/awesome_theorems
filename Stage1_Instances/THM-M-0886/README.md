# THM-M-0886 rev-5.6 intake

`THM-M-0886` is the combinatorics/graph-theory catalog item named the
Marcus-Spielman-Srivastava theorem. The repository attributes it to Marcus, Spielman, and
Srivastava, dates it to 2015, and supplies only the gloss "existence of biregular Ramanujan
graphs" plus an untrusted `verified` label.

## Intake result

This dossier records a fail-closed `planned` instance. The exact matching primary result is
Theorem 5.6 of Marcus, Spielman, and Srivastava, *Interlacing families I: Bipartite Ramanujan
graphs of all degrees*, *Annals of Mathematics* 182 (2015), 307-325. It asserts an infinite
sequence of `(c,d)`-biregular bipartite Ramanujan graphs for every `c,d >= 3`. Section 2.3 defines
the two degrees, the trivial eigenvalues, and the spectral bound.

The catalog nevertheless omits proposition-changing details: the lower degree bounds, the
bipartition and finiteness conventions, the precise meaning of an infinite sequence, simplicity
versus multigraphs, the adjacency-spectrum multiplicity convention, and all ordered binders.
The primary theorem is therefore a strong candidate, not yet the canonical repository statement.
The statement phase must admit and independently review one immutable edition and freeze these
choices rather than silently filling them in.

## Formal boundary

`IntakeProbe.lean` elaborates adjacent pinned APIs for finite simple graphs, multigraphs,
bipartiteness, degrees, adjacency matrices, Hermitian eigenvalues, and permutation matrices. It is
an API probe only. No definition of biregularity or the Ramanujan property, no infinite graph
sequence, no exact Lean expression, and no proof is supplied.

The provisional vector is `[H1, M4, R4]`: the exact primary theorem family and numbered candidate
are identified, but the complete source admission and independent review are open; no usable exact
Lean artifact is credited; and no reviewed readable proof reconstruction exists. All six
downstream tasks remain open. No accepted execution state, audit completion, theorem completion,
or master acceptance is claimed.
