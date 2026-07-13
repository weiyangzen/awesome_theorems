# THM-M-0884 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0884`, the catalog item
`Ramanujan graphs`. The repository attributes the topic to many mathematicians in the twentieth
century and supplies only the gloss `optimal spectral expander graphs`. Its `verified` label is
untrusted inventory metadata under rev-5.6.

The gloss names a graph class and an optimality slogan, not one binder-complete proposition. It does
not decide whether the root is the definition of a Ramanujan graph, an assertion that such graphs
are optimal expanders, an Alon-Boppana asymptotic lower bound, an existence theorem, or a
construction theorem. Those alternatives have different binders, hypotheses, and conclusions.

An immutable exact-topic source lead is Alexander Lubotzky, *Ramanujan Graphs*,
`arXiv:1711.06558v1`. It describes a finite connected `k`-regular graph for `k >= 3` as Ramanujan
when every adjacency eigenvalue `lambda` satisfies either `|lambda| = k` or
`|lambda| <= 2 * sqrt (k - 1)`, and explains through Alon-Boppana why this is optimal for infinite
families. That source clarifies the standard vocabulary but still presents a definition plus
several surrounding results. The catalog does not select one of them as its canonical claim.

`instance.json` therefore leaves the canonical mathematical and Lean targets null and records the
provisional vector `[H5, M4, R4]`. `H5` classifies the received topic/gloss as not yet one stable
proposition; it does not refute Ramanujan-graph theory. The discovery-only Lean probe checks nearby
finite-simple-graph, regularity, adjacency-matrix, Hermitian-spectrum, and square-root interfaces.
It supplies no Ramanujan definition, theorem, or proof credit.

All six downstream tasks remain open. No H0, M0, R0, accepted execution state, audit completion,
theorem completion, or master acceptance is claimed.
