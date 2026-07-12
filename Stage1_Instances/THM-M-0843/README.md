# THM-M-0843 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Szemerédi's regularity lemma.
The repository source gives only the title, Endre Szemerédi, the year 1975, and the gloss "regular
partition of a dense graph." That identifies the finite dense-graph regularity-lemma family, but it
does not state the uniformity convention, equitable-partition requirement, parameter order, or
whether the size bound is existential or explicit.

Pinned mathlib contains a directly relevant theorem,
`szemeredi_regularity`, in
`Mathlib.Combinatorics.SimpleGraph.Regularity.Lemma`. A narrow Lean probe checks its exact
displayed type and the definitions that give meaning to its partition predicates. The candidate is
the effective equitable version documented by Dillies and Mehta: for positive `epsilon` and a
lower bound `l` no larger than the finite vertex count, it returns an `epsilon`-uniform
equipartition into between `l` and an explicit `bound epsilon l` parts.

This is discovery evidence, not a statement, anchor-audit, or proof receipt. The repository gloss
does not yet authorize that exact effective/equitable variant, and the terminal proof body and trust
closure have not been audited. The provisional root remains `[H1, M3, R4]`; accepted proof state,
audit completion, and theorem completion are all false. Commands and their precise boundary are in
`validation.md`.
