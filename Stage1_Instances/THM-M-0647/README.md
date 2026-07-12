# THM-M-0647 rev-5.6 intake

This directory is the `planned` intake for the Lowenheim-Skolem-Tarski theorem. The repository's
literal claim is that an infinite model has elementarily equivalent models of different
cardinalities. The dossier interprets that phrase provisionally through the standard all-cardinals
form, while leaving the exact historical source, cardinal bounds, and Lean universe lifts open for
the dependent statement phase.

Pinned mathlib contains a very close formal candidate,
`FirstOrder.Language.exists_elementarilyEquivalent_card_eq`. `IntakeProbe.lean` checks only that
this declaration is present and exposes its type in the pinned environment. Candidate proximity is
not exact statement identity and earns no accepted proof state. The provisional root vector is
`[H1, M3, R3]`; audit and theorem completion are both false.

The scope map separates this target from the adjacent downward/upward formulations, and the source
crosswalk records every interpretation still requiring primary-source review. Exact commands and
results for this bounded intake are in `validation.md`.
