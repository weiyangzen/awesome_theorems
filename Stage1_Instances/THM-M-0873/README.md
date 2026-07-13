# THM-M-0873 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0873`, the repository topic
`图的同构问题` (graph isomorphism problem). The catalog supplies only the gloss `图同构的复杂性`,
a collective attribution, a twentieth-century date, and the untrusted status
`准多项式时间解决` (solved in quasipolynomial time).

The status points toward the published quasipolynomial upper-bound theorem family, but it is not a
theorem statement. Babai's arXiv version 2, his January 2017 correction note, and Harald Helfgott's
detailed post-fix Bourbaki exposition were inspected. Helfgott's Theorem 1.1 and Corollary 1.2 state
the String Isomorphism and Graph Isomorphism quasipolynomial results and report that Helfgott found
a nontrivial timing error which Babai repaired. An author update and fix note corroborate the
withdrawal and restoration timeline. These are strong source leads, but no Stage1 independent
source review has admitted an exact root, assumptions, correction bundle, or proof-node mapping.

The source family also leaves proposition-changing formal choices: finite-graph and input
encodings, malformed inputs, deterministic machine and cost semantics, the exact asymptotic bound,
quantifier order, and small-input conventions. The catalog separately assigns `THM-M-0874` to the
Babai algorithm and duplicates the generic graph-isomorphism record as `THM-M-1567`; their proof
credit cannot be transferred or counted twice.

`instance.json` therefore freezes `[H1, M4, R4]` with a null canonical statement. H1 records an
inspected published theorem family while exact source admission and statement mapping remain open.
`IntakeProbe.lean` elaborates only adjacent pinned APIs. All six downstream tasks remain open in
`task-dag.json`.

No canonical Lean target, H0, M0, R0, accepted proof state, audit completion, theorem completion,
or master acceptance is claimed.
