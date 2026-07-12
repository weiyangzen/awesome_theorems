# THM-M-0673 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Los's theorem (the fundamental
theorem of ultraproducts). The repository gloss, "elementary equivalence of ultraproducts", is
frozen as the standard sentence form: a first-order sentence holds in the ultraproduct of a family
of nonempty structures modulo an ultrafilter exactly when the set of indices where it holds belongs
to that ultrafilter.

Pinned mathlib contains the exact-shaped declaration
`FirstOrder.Language.Ultraproduct.sentence_realize`. `Statement.lean` now freezes the canonical
polymorphic target, checks a definitional transport to the declaration's direct type shape, and
elaborates four structural mutations plus the principal-ultrafilter boundary. `statement.json` and
`statement-validation.md` record its expression and environment fingerprints. This is provisional
statement-node evidence pending master acceptance; it does not credit the upstream proof body.

The lifecycle remains `planned` at `[H1, M3, R4]`. The source edition and pinpoint mapping,
statement master acceptance, obligation tree, trust/provenance closure, readable reconstruction,
and release checks remain open. No accepted proof state, audit completion, or theorem completion is
claimed.
