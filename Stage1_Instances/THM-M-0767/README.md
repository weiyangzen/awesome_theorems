# THM-M-0767 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Cantor's theorem. The repository
claim is that every set has strictly smaller cardinality than its power set. The intake preserves
that full cardinal comparison, including finite and empty cases; it does not replace it with only
the diagonal non-surjectivity lemma or an infinite-set special case.

The exact primary-source edition, source wording, assumptions, and errata have not been inspected.
The Lean statement phase must also select between a type-level formulation and a formulation for a
set `s : Set alpha`, then compile a checked transport between them. Pinned mathlib contains relevant
Cantor and cardinal-power APIs, but the intake probe is discovery evidence only and supplies no
machine-proof credit before statement identity and the anchor audit are complete.

The provisional root vector is `[H1, M4, R4]`. No exact Lean expression, expression fingerprint,
formal-anchor acceptance, proof state, audit completion, or theorem completion is claimed. Exact
commands and results for this intake are recorded in `validation.md`.
