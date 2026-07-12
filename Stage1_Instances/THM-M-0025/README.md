# THM-M-0025 rev-5.6 dossier

`THM-M-0025` is the Hilbert basis theorem catalog item. The repository states that a polynomial
ring over a Noetherian ring is Noetherian, attributes the result to David Hilbert in 1890, and
labels it verified. The label is untrusted metadata, not source or machine evidence.

## Planned scope

The dossier selects the conventional commutative, one-indeterminate claim for later source review:
for every commutative ring `R`, if `R` is Noetherian, then `R[X]` is Noetherian. No nontriviality,
domain, field, or characteristic premise is added. The zero ring therefore remains in scope under
the intended Lean convention. Noncommutative one-sided variants, infinitely many variables, finite
type algebras, and Hilbert's Nullstellensatz are distinct statements and cannot silently replace
this target.

The catalog gives no primary citation or definition of Noetherian. Hilbert's 1890 paper is recorded
only as a bibliographic lead. Stacks Project Lemma 10.31.1 is an authoritative modern secondary
cross-check, not the historical source packet needed for `H0`.

## Formal boundary

The statement phase freezes the claim as
`Stage1Instances.THM_M_0025.HilbertBasisTheoremTarget`. It elaborates with only
`Mathlib.Algebra.Polynomial.Basic` and `Mathlib.RingTheory.Noetherian.Defs`; the proof-bearing
polynomial ring-theory module is not imported. A checked iff expands Noetherianity to finite
generation of every ideal, four structural mutations are distinguished, and a subsingleton-ring
boundary confirms that the root does not silently add `Nontrivial`. `BoundaryProbe.lean` also
checks `PUnit` as a concrete commutative Noetherian zero-ring coefficient instance.

At pinned mathlib revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`,
`Mathlib.RingTheory.Polynomial.Basic` contains the exact candidate
`Polynomial.isNoetherianRing`.

## Anchor-audit result

`AnchorAudit.lean` now checks a literal copy of the frozen target through that declaration. The
pinned body proves finite generation by a well-founded minimum of leading-coefficient ideals and
strong induction on polynomial degree. Lean reports the terminal and wrapper sorry-free and gives
the axiom set `propext`, `Classical.choice`, and `Quot.sound`. `anchor-audit.json` binds the mathlib
revision, tree, source blob and hashes, body lineage, dependencies, license, bounded discovery
ledger, exact statement comparison, and supplemental source hygiene.

The bounded public search also classifies an immutable Lean power-series result as a carrier
mismatch, not a substitute. GitHub code search and grep.app were inaccessible, so discovery
saturation is not claimed.

The planned vector is `[H1, M3, R3]`: a stable conventional statement and source lead exist; an
exact pinned mathlib route is a self-tested `M0-W / E2` candidate but the accepted root remains
`M3` until downstream proof, provenance/trust, composition, validation, and master-acceptance
gates; and this dossier maps scope without reconstructing the proof. No accepted execution state,
`E1`, audit completion, theorem completion, or master acceptance is claimed.
