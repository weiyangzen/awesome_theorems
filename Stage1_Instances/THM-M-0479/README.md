# THM-M-0479 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0479`, the catalog entry
named `狄利克雷定理` (Dirichlet's theorem). The repository gives only the gloss
`等差数列中存在无穷多素数` (there are infinitely many primes in arithmetic progressions),
attributes it to Peter Dirichlet in 1837, and labels it `已验证`. Under rev-5.6 that label is
untrusted metadata, not a source audit or a machine-proof claim.

The standard mathematical family says that every reduced residue class modulo a positive integer
contains infinitely many primes. The catalog does not state the universal modulus and residue
quantifiers, coprimality condition, sign and carrier conventions, or meaning of infinitude. It also
supplies no primary edition, theorem/page locator, definition chain, proof boundary, correction or
errata review, or independent source review. The canonical human statement and canonical Lean
expression therefore remain null at intake rather than silently importing a modern formulation.

Pinned mathlib contains a direct theorem family in `Mathlib.NumberTheory.LSeries.PrimesInAP`.
`Nat.infinite_setOf_prime_and_eq_mod` is the closest set-infinitude candidate, with natural and
integer congruence variants nearby. `IntakeProbe.lean` elaborates their exact types and reports the
axioms of the two set-infinitude forms. This authenticates a strong formal candidate surface and
supports provisional `M3`, but it does not select a source-identical root, freeze an expression
fingerprint, audit terminal proof bodies, or grant proof credit.

The provisional root vector is `[H1, M3, R4]`: the published theorem family is recognizable but no
exact human source is accepted; direct pinned formal interfaces exist but no canonical target is
frozen; and no source-faithful readable proof reconstruction is attached to an exact root. All six
downstream phases remain open. No H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
