# THM-M-0478 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the catalog entry named the law of
quadratic reciprocity. The repository supplies only the gloss "reciprocity property of the Legendre
symbol," attributes the result to Carl Friedrich Gauss in 1796, and labels it verified. Under
rev-5.6 that label is untrusted inventory metadata, not an exact statement, source audit, or proof
receipt.

The gloss identifies a standard theorem family but omits the prime and oddness assumptions, the
Legendre-symbol convention, the sign formula, whether the primes must be distinct, and whether the
root is the product form, signed equality, congruence-mod-4 case split, a residue predicate, or a
Jacobi-symbol extension. Intake does not silently choose among those proposition-changing variants.

Gauss's *Disquisitiones Arithmeticae*, Article 131, was inspected in a digitized primary-language
edition and an historical German translation. It states the fundamental reciprocity theorem in
quadratic-residue/nonresidue language. These are strong source-family leads, but the catalog cites
neither edition, Article 131 is not literally modern Legendre-symbol notation, and no accepted
translation, definition-chain, errata audit, or independent source review exists. They therefore
support `H1`, not `H0`.

Pinned mathlib contains several exact quadratic-reciprocity declarations in
`Mathlib.NumberTheory.LegendreSymbol.QuadraticReciprocity`. `IntakeProbe.lean` authenticates the
Legendre-symbol definition and six candidate theorem interfaces. This is real pinned API evidence,
but no canonical source-to-Lean target has been selected and the later anchor/provenance/trust audit
has not run. The candidates receive only `M3` discovery credit, never `M0-W`.

The provisional vector is `[H1, M3, R4]`. `instance.json` freezes the received scope, ambiguity,
source and formal leads, exclusions, profiles, and open downstream work. `task-dag.json` keeps all
six later phases open. No canonical proposition, statement fingerprint, H0, M0, R0, accepted proof
state, audit completion, theorem completion, accepted receipt, or master acceptance is claimed.
