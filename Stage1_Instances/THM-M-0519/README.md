# THM-M-0519 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Breuil-Conrad-Diamond-Taylor
modularity theorem. The repository gloss "all elliptic curves are modular" is made precise by the
primary paper's Theorem A: every elliptic curve over `Q` is modular, with modularity defined there
by six equivalent analytic, Galois-representation, and modular-parametrization conditions.

The intake freezes that human claim and its scope, but deliberately does not invent a Lean
predicate for modularity. Pinned mathlib supplies Weierstrass curves and a nonsingularity
typeclass, but the bounded search found no modular-form/Galois-representation interface expressing
the paper's definition. `IntakeProbe.lean` checks only those available encoding ingredients.

The planned root is `[H1, M4, R4]`: the primary statement is identified, while the complete
source-to-proof-node audit, exact Lean target, proof architecture, and reviews remain downstream.
No proof, audit completion, or theorem completion is claimed.
