# THM-M-0268 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Lebesgue dominated convergence
theorem. The repository catalog gives Henri Lebesgue, the year 1902, and only the gloss
`积分与极限交换的条件` (conditions for exchanging an integral and a limit). It supplies no
citation, formula, domains, quantifiers, assumptions, or selected theorem variant. Its `已验证`
label is untrusted metadata and supplies no human-source or Lean proof credit.

The title identifies the classical dominated-convergence family, but it does not decide between a
real-, complex-, or normed-space-valued Bochner integral and a nonnegative extended-real Lebesgue
integral. It also does not decide whether convergence, measurability, and domination are everywhere
or almost everywhere, whether the index is a sequence or a general filter, or how the integrable
dominating function is encoded. Lebesgue's 1902 *Intégrale, Longueur, Aire* is a matching primary
bibliographic lead, but no exact proposition or proof passage from it has been admitted.

Pinned mathlib contains direct exact-topic declarations, including
`MeasureTheory.tendsto_integral_of_dominated_convergence` and nonnegative `lintegral` variants.
`IntakeProbe.lean` authenticates those interfaces and representative axiom reports. This supports
discovery status `M3`, not source identity, a frozen statement, a terminal-body audit, or proof
credit.

The provisional vector is `[H1, M3, R4]`: a classical published theorem family and primary-source
lead are known but the exact source mapping remains open; strong pinned interfaces exist but no
canonical target has been selected; and no source-faithful proof reconstruction exists.
`instance.json` is the structured scope authority. The scope map and source-statement crosswalk
freeze the unresolved choices, and `task-dag.json` leaves all six dependent phases open. No exact
statement, H0, M0, R0, accepted proof state, audit completion, theorem completion, or master
acceptance is claimed.
