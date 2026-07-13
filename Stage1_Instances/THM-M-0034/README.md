# THM-M-0034 rev-5.6 intake

`THM-M-0034` is the Quillen-Suslin theorem catalog item. The repository calls it the proof of
Serre's conjecture, attributes it to Daniel Quillen and Andrei Suslin in 1976, and labels it
verified. That label is untrusted metadata, not human-source or kernel evidence.

## Statement scope

The adjacent catalog entry describes Serre's conjecture as saying that projective modules over a
polynomial ring are free. This identifies the Quillen-Suslin theorem family but does not fix a
truth-valued proposition: the coefficient ring, number and encoding of variables, finite-generation
premise, left/right module convention, zero-variable case, or meaning of free are absent. The
statement phase selects the field specialization of Suslin's Theorem 3* on page 1066, aligned with
the field question and affirmative answer on page 1063. The canonical proposal uses a field, a
positive finite number of variables, and a finitely generated projective module, and concludes that
the module is free. The positive-variable boundary follows the source notation `X1,...,Xn`; a
zero-variable extension is not silently added.

The target is the theorem, not the historical fact that Quillen and Suslin published proofs.
`THM-M-0033` separately owns the catalog's Serre-conjecture record; statement or proof credit does
not transfer between the two entries.

## Formal boundary

Pinned mathlib exposes `Module.Projective`, `Module.Free`, `Module.Finite`, polynomial and
multivariable-polynomial rings, and the theorem that free modules are projective. A bounded search
found no Quillen-Suslin declaration or converse from finite projectivity to freeness over a
polynomial ring. `Statement.lean` now defines and fingerprints the target without providing an
inhabitant. Three narrow direct imports are individually required, and four statement mutations
cover removed finite generation, a broader domain, changed binder scope, and the zero-variable
boundary. None of this supplies proof credit.

The planned vector remains `[H1, M3, R4]`. The exact Lean expression is self-tested, but the Russian
source lacks independent translation, errata review, Quillen reconciliation, and master acceptance.
No located external candidate or proof body receives closure credit, and no readable proof reconstruction exists. All
downstream proof and release work remains open. No accepted execution state, audit completion,
theorem completion, or master acceptance is claimed.

## Obligation architecture

The obligation-tree phase freezes 41 canonical obligations and seven separate typed graph families
in `obligation-registry.json` and `typed-graphs.json`. The visible route of the selected immutable
external source is expanded through finite-variable induction, monic localization, Quillen
patching, fibre freeness, and an independent-universe `ULift` transport. This is architecture, not
external proof credit. `ObligationTree.lean` checks only that the all-natural-number external field
statement conditionally implies the positive-variable root.

The first machine cut is `M0034-X-EXTERNAL-BODY`. The source remains outside the dependency closure,
has no usable license artifact, and has not received a local kernel/axiom replay or complete
transitive provenance audit. The exact root therefore remains `[H1, M3, R4]` with no accepted closed
obligation. See `obligation-tree.md` and `obligation-tree-validation.md` for the frozen ledger and
the exact self-test boundary.
