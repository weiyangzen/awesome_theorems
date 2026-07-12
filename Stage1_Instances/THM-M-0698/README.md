# THM-M-0698 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for first-order compactness. It freezes
the human claim as the semantic compactness theorem: a first-order theory has a nonempty model if
and only if each of its finite subtheories has a nonempty model.

The repository's target row gives only the theorem name. A separate model-theory inventory row
states the displayed equivalence, but the repository does not establish that the two rows share one
source record or provide a primary edition, theorem/page, assumptions, or errata. The crosswalk
therefore treats that row as corroborating repository metadata, not `H0` evidence.

Pinned mathlib contains the exact candidate API and theorem in
`Mathlib.ModelTheory.Satisfiability`. `IntakeProbe.lean` checks their types, but this intake does not
claim the later statement or anchor-audit gates: no normalized expression fingerprint, checked
source identity, proof provenance audit, or accepted proof state is recorded here. The provisional
root vector is `[H1, M3, R4]`; audit and theorem completion are both false.

The obligation-tree phase additionally freezes 16 semantic obligations and
seven separate typed graphs. Its checked local composition isolates the
finite-to-satisfiable direction as the remaining root cut; it does not promote
the matching pinned mathlib body before the ordered proof phase. See
`obligation-tree.md` and `obligation-tree-validation.md`.
