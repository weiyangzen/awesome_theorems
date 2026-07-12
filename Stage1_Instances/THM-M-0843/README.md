# THM-M-0843 rev-5.6 dossier

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

That was the intake boundary: its probe was discovery evidence rather than a statement or proof
receipt. The statement phase below now selects the inspected effective/equitable variant, while the
terminal proof body and trust closure remain unaudited. The provisional root remains
`[H1, M3, R4]`; accepted proof state, audit completion, and theorem completion are all false.
Intake commands remain recorded in `validation.md`.

## Statement result

The statement phase selects the effective Lean-facing formulation displayed in Section 3 of the
inspected ITP article. `Statement.lean` freezes the exact finite-graph binders, positive real
tolerance, graph-size premise, equitable full-vertex partition, explicit bound, and mathlib
ordered-off-diagonal uniformity predicate. It uses the two independently necessary definition
imports `Regularity.Bound` and `Regularity.Uniform`; the proof-bearing `Regularity.Lemma` module is
not imported.

`check_statement.py`, `statement.json`, `statement-validation.md`, and
`statement-receipt.json` bind the explicit expression fingerprint, environment, checked one-way
transport to an existential-bound form, and four required structural mutations. This is a
self-tested statement proposal pending master acceptance. It supplies no formal-anchor audit,
proof credit, debt-vector promotion, audit completion, or theorem completion.
