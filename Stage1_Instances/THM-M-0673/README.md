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

`AnchorAudit.lean` now checks an exact wrapper at the immutable mathlib pin. The terminal theorem,
formula bridge, bounded-formula route, and wrapper are sorry-free and report only `propext`,
`Classical.choice`, and `Quot.sound`; a machine traversal found no bodyless nonaxiom or unsafe
declaration in their 5,075-declaration closure. The bounded public audit also classifies
Foundation's equality-free raw-product theorem as a statement/integration mismatch rather than a
substitute root.

The lifecycle remains `planned` at the accepted `[H1, M3, R4]` vector. The exact mathlib route is a
provisional `M0-W` candidate pending dependency-ordered master acceptance and downstream gates. The
obligation registry now freezes 28 semantic obligations and seven typed graph families before any
proof-phase credit. `ObligationTree.lean` checks the sentence/formula adapters only conditionally,
with the bounded-formula induction left as an explicit premise. This is provisional obligation-tree
evidence pending dependency-ordered master acceptance, not installation of the candidate.

The source edition and pinpoint mapping, proof-phase integration and remaining composition
certificates, release-grade trust/provenance closure, independently reviewed readable
reconstruction, and release checks remain open. No accepted proof state, audit completion, or
theorem completion is claimed.
