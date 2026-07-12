# THM-M-0062 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0062`, the Sylow theorems.
The repository gloss says that the target covers existence, conjugacy, and counting of `p`-subgroups
in finite groups. Intake preserves that three-part package and interprets the counted and conjugate
objects as maximal `p`-subgroups, but it does not yet freeze a single binder-complete source or Lean
proposition.

The original 1872 paper was inspected at Theorems I-II, printed pages 586-587. It states the
maximal-prime-power existence result, conjugacy of all subgroups of that order, and a congruence
formula for their number in the language of finite substitution groups. Translating that historical
scope to arbitrary finite groups, reconciling its notation with the modern three-theorem package,
and independently reviewing every assumption and conclusion remain source-gate work. The
repository's `已验证` field is untrusted metadata and supplies no H or M credit.

Pinned mathlib contains an unusually close formal candidate in `Mathlib.GroupTheory.Sylow`.
`IntakeProbe.lean` checks the existence, conjugacy, and counting APIs and kernel-checks representative
calls under a finite group and prime. This is real intake feasibility evidence only. No combined
canonical expression, expression fingerprint, mutation suite, terminal-body audit, or accepted
wrapper is created in this phase.

The provisional root vector is `[H1, M3, R4]`: the historical and formal source families are
identified, but the exact source-to-modern statement mapping is not accepted; only formal
definitions and candidates are credited; and no reviewed readable proof reconstruction exists.
`instance.json` is the structured scope authority, while `task-dag.json` leaves all six downstream
phases open. No H0, M0, R0, accepted proof state, audit completion, theorem completion, or master
acceptance is claimed.
