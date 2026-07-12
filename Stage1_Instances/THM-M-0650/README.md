# THM-M-0650 rev-5.6 intake

This directory is the `planned` intake dossier for the Tarski-Vaught test. The repository gloss,
"a criterion for elementary substructures", is scoped as the standard witness criterion: a
substructure is elementary when every existential formula with parameters in the substructure
that has a witness in the ambient structure also has a witness in the substructure.

Pinned mathlib contains exact-looking substructure and embedding candidates,
`FirstOrder.Language.Substructure.isElementary_of_exists` and
`FirstOrder.Language.Embedding.isElementary_of_exists`. `IntakeProbe.lean` checks their names and
types in the pinned environment. `Statement.lean` now freezes the intake-selected implication on an
unbundled substructure, checks its direct pinned mathlib shape, and covers the required structural
mutations plus the nullary-parameter boundary. This statement evidence is self-tested but remains
provisional until master acceptance; it is not a source-fidelity, anchor-audit, or proof receipt.

The historical source is not established by the repository's unsupported `1957` date or its
untrusted `已验证` label. Pinpoint primary-source theorem/page, historical directionality,
assumptions, and errata remain open. The lifecycle is therefore `planned` at `[H1, M3, R3]`, with no
accepted proof state, audit completion, or theorem completion.

The obligation-tree phase freezes 19 unique semantic obligations and seven separate typed graphs.
It expands the short substructure wrapper through subtype normalization and the embedding theorem's
formula recursion, including the nontrivial universal/negated-witness branch. `ObligationTree.lean`
checks the exact conditional specialization from the embedding package to the canonical root. The
pinned embedding body remains deliberately uncredited until the downstream proof and provenance
gates.
