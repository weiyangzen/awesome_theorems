# THM-M-0034 rev-5.6 intake

`THM-M-0034` is the Quillen-Suslin theorem catalog item. The repository calls it the proof of
Serre's conjecture, attributes it to Daniel Quillen and Andrei Suslin in 1976, and labels it
verified. That label is untrusted metadata, not human-source or kernel evidence.

## Planned scope

The adjacent catalog entry describes Serre's conjecture as saying that projective modules over a
polynomial ring are free. This identifies the Quillen-Suslin theorem family but does not fix a
truth-valued proposition: the coefficient ring, number and encoding of variables, finite-generation
premise, left/right module convention, zero-variable case, or meaning of free are absent. The
familiar field-coefficient, finitely generated projective-module statement is therefore recorded
only as a candidate for source ratification. It is not silently installed as the canonical claim.

The target is the theorem, not the historical fact that Quillen and Suslin published proofs.
`THM-M-0033` separately owns the catalog's Serre-conjecture record; statement or proof credit does
not transfer between the two entries.

## Formal boundary

Pinned mathlib exposes `Module.Projective`, `Module.Free`, `Module.Finite`, polynomial and
multivariable-polynomial rings, and the theorem that free modules are projective. A bounded search
found no Quillen-Suslin declaration or converse from finite projectivity to freeness over a
polynomial ring. `IntakeProbe.lean` authenticates only these adjacent APIs. It states no target and
supplies no proof credit.

The planned vector is `[H1, M3, R4]`: the classical theorem family and primary publication leads
are identifiable, but no pinpoint source packet has been admitted; only definitions and interfaces,
not a target-level formal artifact, have been located; and no readable proof reconstruction exists. All six
downstream tasks remain open. No accepted execution state, audit completion, theorem completion, or
master acceptance is claimed.
