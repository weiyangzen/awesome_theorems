# THM-M-0673 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Los's theorem (the fundamental
theorem of ultraproducts). The repository gloss, "elementary equivalence of ultraproducts", is
frozen as the standard sentence form: a first-order sentence holds in the ultraproduct of a family
of nonempty structures modulo an ultrafilter exactly when the set of indices where it holds belongs
to that ultrafilter.

Pinned mathlib contains the exact-shaped declaration
`FirstOrder.Language.Ultraproduct.sentence_realize`. `IntakeProbe.lean` checks that this declaration
is present and exposes its type, but intake does not yet credit it as an exact canonical statement or
proof body. The statement phase must freeze the expression, source mapping, imports, mutations, and
environment fingerprint before the anchor can advance machine debt.

The lifecycle is `planned` at `[H1, M3, R4]`. The source edition and pinpoint mapping, exact Lean
statement gate, obligation tree, trust/provenance closure, readable reconstruction, and release
checks remain open. No accepted proof state, audit completion, or theorem completion is claimed.
