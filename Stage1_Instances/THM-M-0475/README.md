# THM-M-0475 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for Euler's totient theorem. The
repository supplies the formula `a^phi(n) congruent to 1 (mod n)`, the attribution Leonhard Euler,
and the year 1763. It does not supply the indispensable coprimality premise, the domains and
quantifier order, a source locator, or boundary conventions.

Taken as an unconditional claim about natural numbers, the displayed formula is false: for
`a = 2` and `n = 4`, `2^phi(4) = 4` is congruent to `0`, not `1`, modulo `4`. The conventional
natural-number completion is that `a` and `n` are coprime. Intake records that completion only as a
candidate family; it does not silently repair the catalog or freeze a canonical statement before an
accountable source review.

Pinned mathlib contains the direct candidate `Nat.ModEq.pow_totient`, including its `n = 0` and
`n = 1` behavior under `Nat.Coprime`. `IntakeProbe.lean` checks that candidate, its units form, the
two degenerate cases, and the concrete counterexample. This is discovery-only `M3` evidence: the
statement, anchor-audit, proof-body, provenance, and trust gates remain downstream.

`instance.json` is the structured scope authority. `scope-map.md` and
`source-statement-crosswalk.md` record every proposition-changing choice currently visible.
`task-dag.json` leaves all six dependent phases open. No H0, M0, R0, accepted proof state, audit
completion, theorem completion, or master acceptance is claimed.
