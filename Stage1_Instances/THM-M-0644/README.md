# THM-M-0644 rev-5.6 intake

This directory is the `planned` intake dossier for the first-order compactness theorem. The
repository statement is specific enough to freeze the human claim: a first-order theory has a
model if and only if each finite subtheory has a model. Here "model" means a nonempty structure
satisfying the theory; "finite subset" means a finite set of sentences contained in that theory.

The pinned mathlib snapshot contains an exact-looking formal candidate,
`FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable`. `IntakeProbe.lean` checks its
name, type, and the two definitions used by the repository wording. This is discovery evidence for
the next phase, not an accepted statement fingerprint or proof receipt. The primary historical
source, its exact theorem/page, assumptions, and errata also remain to be audited.

The lifecycle remains `planned` at `[H1, M4, R4]`. There is no accepted proof state, audit
completion, or theorem completion. The scope map, source crosswalk, and open task DAG record the
precise downstream boundary; `validation.md` records this intake's self-tests.

The statement phase now freezes and self-tests `Stage1.THM_M_0644.CompactnessTarget` in
`Statement.lean`, including direct expansion, a finite-`Set` transport, and four structural
mutations. `statement.json`, `statement-receipt.json`, and `statement-validation.md` record the
provisional `[_]` evidence. Master acceptance and every later phase remain open; this adds no proof
or theorem-completion claim.

The anchor audit identifies the exact pinned mathlib declaration at revision
`8a178386ffc0f5fef0b77738bb5449d50efeea95` and checks an exact-type wrapper in
`AnchorAudit.lean`. `anchor-audit.json` records its terminal body, license, source hash, axiom
profile, and bounded external searches. This is provisional anchor evidence only: the obligation
tree, accepted proof credit, full trust/provenance closure, validation, and theorem completion
remain open.

The obligation-tree phase freezes 16 canonical obligations and seven separate typed graphs. It
expands the easy restriction direction and the hard ultraproduct direction through finite-model
selection, the tail ultrafilter, filter product, eventual sentence realization, the ultraproduct
bridge, and final model packaging. `ObligationTree.lean` checks only their conditional composition
into the exact root. The denominator is frozen, but the root remains `M3`; later proof, provenance,
source, validation, and master-acceptance gates remain open.
