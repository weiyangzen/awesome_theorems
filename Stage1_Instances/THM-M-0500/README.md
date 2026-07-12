# THM-M-0500 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository entry
`狄利克雷L函数`. The repository's actual claim is `等差数列素数定理` (Dirichlet's theorem on
primes in arithmetic progressions), not a generic assertion that Dirichlet L-functions exist.

The human scope is frozen as the infinitude of primes in every reduced residue class: for a
positive modulus and a residue class coprime to it, infinitely many primes lie in that class.
The statement phase now freezes the exact binder order and residue-class formulation in
`Statement.lean`: every `q : Nat` with `[NeZero q]`, every `a : ZMod q`, and `IsUnit a` lead to an
infinite set of natural primes reducing to `a`. The `q = 1` case is included, and a checked theorem
relates the canonical infinitude form to existence above every natural bound.

The statement imports only residue-class vocabulary and the generic order-theoretic infinitude
transport. It deliberately does not import mathlib's proof-bearing `PrimesInAP` module. Four
structural mutations are rejected, and exact hashes and commands are recorded in
`statement-validation.md` and `statement-receipt.json`.

The source inventory provides only a short secondary gloss, attribution, and date. It supplies no
edition, theorem/page, assumptions, proof passage, or errata record. The root therefore remains
`[H1, M3, R4]`; audit and theorem completion are both false. Intake commands remain in
`validation.md`; statement evidence is in `statement-validation.md`.
