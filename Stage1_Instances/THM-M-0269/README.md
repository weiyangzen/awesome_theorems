# THM-M-0269 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Lebesgue monotone convergence
theorem. The repository catalog supplies Henri Lebesgue, the year 1902, and only the gloss
`单调函数列的积分极限` (the integral limit of a monotone sequence of functions). It gives no
formula, source, domain, codomain, measure, measurability convention, monotonicity convention, or
exact conclusion.

Axler's modern Theorem 3.11 is a close source candidate: an increasing sequence of nonnegative
extended-real measurable functions on an arbitrary measure space has integral limit equal to the
integral of its pointwise limit. Pinned mathlib contains direct versions using a pointwise supremum,
an almost-everywhere version, and a limit-form theorem. None is silently selected as the repository
root: the catalog does not choose among those formulations, and its Lebesgue/1902 attribution is not
yet reconciled with mathlib's description of the result as the Beppo Levi lemma.

The provisional vector is `[H1, M3, R4]`: a complete modern proof source is located but source
identity, history, assumptions, errata mapping, and independent review remain open; direct pinned
Lean interfaces elaborate but no canonical target or checked source transport is frozen; and no
source-faithful proof reconstruction exists for an exact root.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` preserve the proposition-changing choices. `task-dag.json` records
this intake as self-tested pending master acceptance and leaves all six downstream phases open;
`IntakeProbe.lean` checks candidate APIs only. The literal catalog wording is frozen as a
non-propositional human claim, but no exact mathematical or Lean statement, H0, M0, R0, accepted
proof state, audit completion, theorem completion, or master
acceptance is claimed.
