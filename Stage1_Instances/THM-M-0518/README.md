# THM-M-0518 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Wiles's semistable
elliptic-curve modularity theorem. The repository gloss matches the sentence labeled Theorem 0.4
in Wiles's 1995 paper: every semistable elliptic curve over the rational numbers is modular.

That sentence fixes the human claim, but it is not yet an exact Lean proposition. Pinned mathlib
has Weierstrass elliptic curves, local good/multiplicative/additive reduction, and analytic modular
forms. The intake did not locate a ready global predicate saying that a rational elliptic curve is
semistable at every finite place, nor a conductor/newform or equivalent representation-theoretic
relation defining genuine modularity. An older Stage1 boundary file for `THM-M-0132` models these
missing relations with abstract `Prop` fields; rev-5.6 does not admit that as this target's statement
or proof.

The root therefore remains `[H1, M3, R4]`: a primary theorem locator exists, encoding ingredients
exist, and the source-definition audit, exact Lean target, proof architecture, and readable proof
remain open. Exact intake validation commands and results are recorded in `validation.md`.
