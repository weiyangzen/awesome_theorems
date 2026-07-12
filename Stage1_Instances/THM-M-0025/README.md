# THM-M-0025 rev-5.6 intake

`THM-M-0025` is the Hilbert basis theorem catalog item. The repository states that a polynomial
ring over a Noetherian ring is Noetherian, attributes the result to David Hilbert in 1890, and
labels it verified. The label is untrusted metadata, not source or machine evidence.

## Planned scope

This intake selects the conventional commutative, one-indeterminate claim for later source review:
for every commutative ring `R`, if `R` is Noetherian, then `R[X]` is Noetherian. No nontriviality,
domain, field, or characteristic premise is added. The zero ring therefore remains in scope under
the intended Lean convention. Noncommutative one-sided variants, infinitely many variables, finite
type algebras, and Hilbert's Nullstellensatz are distinct statements and cannot silently replace
this target.

The catalog gives no primary citation or definition of Noetherian. Hilbert's 1890 paper is recorded
only as a bibliographic lead. Stacks Project Lemma 10.31.1 is an authoritative modern secondary
cross-check, not the historical source packet needed for `H0`.

## Formal boundary

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.RingTheory.Polynomial.Basic` contains the exact candidate
`Polynomial.isNoetherianRing`. `IntakeProbe.lean` authenticates its type and adjacent definitions
with the pinned toolchain. Intake does not freeze an elaborated canonical declaration, perform the
terminal proof-body/provenance audit, credit closure, or establish `M0`.

The planned vector is `[H1, M3, R3]`: a stable conventional statement and source lead exist; an
exact formal interface is located but not accepted through the statement and anchor-audit gates;
and this dossier maps scope without reconstructing the proof. All six downstream tasks remain
open. No accepted execution state, audit completion, theorem completion, or master acceptance is
claimed.
