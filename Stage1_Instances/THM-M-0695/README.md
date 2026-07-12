# THM-M-0695 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
"Curry-Howard correspondence". The source inventory supplies only the gloss "correspondence
between proofs and programs" (and, in a duplicate computer-science record, "propositions as
types, proofs as programs"). It does not select a source calculus or state a theorem.

The Curry-Howard correspondence is a family of syntax-sensitive correspondences, not one
unparameterized proposition. A formal theorem must at least select a logic, a typed term calculus,
translations in both directions, equality or reduction relations, and the property being claimed
(for example derivation/typing equivalence, substitution compatibility, or reduction
correspondence). Choosing any such theorem from the slogan alone would substitute invented
mathematics for the repository target.

The intake therefore freezes that ambiguity and its exclusions rather than a canonical Lean
target. The root remains `[H3, M4, R4]`. A pinned Lean probe confirms only that Lean's kernel exposes
the proposition/type and proof/term primitives needed to encode small candidate fragments. It is
not the Curry-Howard metatheorem and receives no proof credit. Exact commands and results are in
`validation.md`.
