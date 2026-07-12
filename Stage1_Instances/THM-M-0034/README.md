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
No formal candidate or proof body is credited, and no readable proof reconstruction exists. All
downstream proof and release work remains open. No accepted execution state, audit completion,
theorem completion, or master acceptance is claimed.
