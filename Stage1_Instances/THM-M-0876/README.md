# THM-M-0876 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0876`, the repository topic
`图同构的复杂性` (complexity of graph isomorphism). The catalog supplies only the gloss
`图同构在NP与P之间的位置`, literally "the position of graph isomorphism between NP and P," a
collective attribution, a twentieth-century date, and the untrusted status `部分解决`.

The gloss is not a truth-valued proposition. It does not say whether the target is membership of
graph isomorphism in NP, membership in P, NP-intermediacy under an explicit condition, Babai's
quasipolynomial upper bound, or a reviewed conjunction of closed and open branches. It also omits
the graph and input encodings, machine and cost models, reductions, quantifier order, and boundary
cases. In particular, "between" cannot be formalized as membership in `NP \ P`: nonmembership in P
is not supplied by the catalog.

Babai's arXiv paper *Graph Isomorphism in Quasipolynomial Time*, version 2, was inspected as a
author-authored primary-source preprint lead for a partial branch. Its Corollary 1.1.2 states a quasipolynomial algorithmic upper
bound, but the repository already represents the generic result and Babai algorithm in
neighboring targets `THM-M-0873` and `THM-M-0874`. The paper does not identify the intended root of
this target, so no branch or source status is credited here.

`instance.json` freezes the provisional vector `[H5, M4, R4]`. `H5` classifies the received wording
as not yet one stable proposition; it does not claim that graph isomorphism is refuted or
independent. `IntakeProbe.lean` elaborates only adjacent pinned graph-isomorphism, language, and
computable-reduction APIs. All six downstream tasks remain open in `task-dag.json`.

No canonical mathematical or Lean statement, H0, M0, R0, accepted proof state, audit completion,
theorem completion, or master acceptance is claimed.
