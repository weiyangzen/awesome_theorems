# THM-M-0283 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Markov's inequality. The repository
catalogue gives Andrey Markov, the year 1889, and only the gloss "probability upper bound for a
nonnegative random variable." Its `已验证` label is untrusted metadata under rev-5.6 and supplies no
source, statement, or proof credit.

The gloss identifies the classical theorem family but not one proposition. It does not select a
probability measure or a general measure, the random-variable codomain, pointwise or almost-
everywhere nonnegativity, measurability or integrability, a positive finite threshold, a strict or
closed tail event, or product versus division form. Choosing the familiar formula now would add
proposition-changing mathematics that is absent from the repository source.

Pinned mathlib contains strong exact-topic candidates. Its Lebesgue-integral module explicitly
labels `mul_meas_ge_le_lintegral₀`, `mul_meas_ge_le_lintegral`, and
`meas_ge_le_lintegral_div` as Markov's inequality, and its Bochner-integral module provides the
real-valued `mul_meas_ge_le_integral_of_nonneg`. The intake probe authenticates these declarations
at the pinned revision. None is silently identified with the unfrozen catalogue root.

The provisional root vector is `[H1, M3, R4]`: the catalogue treats this standard theorem family as
proved, but provides no primary citation and leaves its exact source statement unaudited; usable
pinned formal candidates exist, but no source-faithful canonical target or checked transport is
frozen; and no source-faithful proof reconstruction exists. This is a conservative intake
classification, not accepted source evidence. All six downstream phases remain open in
`task-dag.json`.

No canonical mathematical or Lean proposition, H0, M0, R0, accepted execution state, audit
completion, theorem completion, or master acceptance is claimed.
