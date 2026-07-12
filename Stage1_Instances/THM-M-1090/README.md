# THM-M-1090 rev-5.6 intake

This directory is the `planned` rev-5.6 instance for the repository record named "Markov
process" (`马氏过程`) and glossed only as "the Markov property" (`马尔可夫性质`). That wording names
a class of stochastic processes and its defining conditional-independence property; it does not
identify one theorem asserting that a specified process is Markov. The intake therefore preserves
the conventional property family and records the missing choices instead of silently selecting a
finite-state chain, an SDE, or a strong-Markov theorem.

The provisional root vector is `[H3, M4, R4]`. `H3` reflects that only a historical/topic-level
source record is present, not a source theorem with an audited proof and premise crosswalk. The
metadata label `已验证` is untrusted and gives no proof credit. No exact Lean expression, kernel
closure, audit completion, or theorem completion is claimed.

The dossier consists of `intake.json`, `scope-map.md`, `source-statement-crosswalk.md`, the open
`task-dag.json`, and the exact intake validation record in `validation.md`. `IntakeProbe.lean`
checks only that relevant pinned mathlib substrate is available; it is not a formalization of the
unidentified root theorem.

## Intake verdict

Lifecycle is `planned`. The first downstream failed gate is exact source-statement identity: the
record does not supply a process construction or hypothesis from which the Markov property is to be
proved, nor does it choose a precise Markov predicate. Those decisions belong to the dependent
statement phase and must come from an authoritative source rather than this intake.
