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

The obligation-tree phase freezes registry version 1 in `obligation-registry.json`: 28 canonical
IDs, of which 25 are required mathematical obligations and three are informational provenance/trust
overlays. `typed-graphs.json` keeps proof, refinement, provenance, evidence, trust, documentation,
and workflow edges separate. The architecture expands the statement/foundation, powerset
normalization, strict-order branches, singleton construction, diagonal engine, imported boundary,
and exact-root composition layers. All nodes remain open; the checked anchor is not admitted as
proof evidence by this phase.

The proof phase subsequently kernel-checked an exact local wrapper, and the validation phase
replayed it alongside a separately written exact-root reconstruction. Both report only `propext`,
`Classical.choice`, and `Quot.sound`; pinned mathlib source and environment hashes also pass the
narrow validator. This remains nonrelease worker evidence: proof master acceptance, graph
reconciliation, cold/offline hermetic replay, a distinct independent runner, full transitive trust,
H0, R0, `AUDIT-Z`, and `THEOREM-Z` are open.
