# THM-M-0767 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Cantor's theorem. The repository
claim is that every set has strictly smaller cardinality than its power set. The intake preserves
that full cardinal comparison, including finite and empty cases; it does not replace it with only
the diagonal non-surjectivity lemma or an infinite-set special case.

The statement phase selects the set-subtype target
`forall (alpha : Type u) (s : Set alpha), Cardinal.mk s < Cardinal.mk (Set.powerset s)`.
`Statement.lean` checks both directions of transport to the type-level formulation and checks the
normalized `2 ^ Cardinal.mk` forms. Empty and finite boundary fixtures elaborate without added
hypotheses. The exact primary-source edition, source wording, assumptions, and errata remain open.

The anchor audit identifies pinned mathlib's `Cardinal.cantor`, normalized by
`Cardinal.mk_powerset`, as an exact candidate for the canonical root. `AnchorAudit.lean` checks the
wrapper and reports the candidate's axioms; `anchor-audit.json` records immutable revisions, source
locations and hashes, terminal-body provenance, the supporting diagonal declarations, and the
bounded external search. The provisional vector is now `[H1, M3, R4]`: a usable interface exists,
but the obligation/provenance graph and all proof-acceptance gates remain downstream. Exact commands
and results are recorded in `validation.md`.
