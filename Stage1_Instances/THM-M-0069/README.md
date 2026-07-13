# THM-M-0069 intake dossier

This directory is the fail-closed `planned` intake dossier for `THM-M-0069`, the catalog item
`伯恩赛德定理` (Burnside's p-alpha q-beta theorem). The repository supplies only this claim:

> Groups of order p^a q^b are solvable.

The phrase "group of order `p^a q^b`" conventionally entails finiteness, but the catalog does not
separately bind that convention or say how finiteness is encoded or derived. It also does not say
that `p` and `q` are distinct primes, specify whether `a` and `b` may be zero, or define group order
and solvability. Those choices affect the formal proposition. The 1904 Burnside paper is a strong
primary-source lead, but only its bibliographic metadata was inspected during intake. Consequently
the dossier preserves the recognizable theorem family while leaving the canonical mathematical
statement and Lean target unset. Selecting the usual textbook form here would exceed the intake
phase.

Pinned mathlib provides `IsSolvable`, prime-power group and Sylow interfaces, Burnside's
normal p-complement theorem, and solvability of finite Z-groups. The narrow Lean probe authenticates
those interfaces. No direct theorem closing the p-alpha q-beta root was located by the bounded
repo-local search, and none of the adjacent results is credited as a substitute.

The authoritative scope record is [instance.json](instance.json). Proposition-changing decisions
and exclusions are in [scope-map.md](scope-map.md), the source and formal-candidate mapping is in
[source-statement-crosswalk.md](source-statement-crosswalk.md), and all downstream phases remain
open in [task-dag.json](task-dag.json).

Status boundary: provisional, self-tested planned intake only. No canonical target, source `H0`,
machine `M0`, readable `R0`, accepted state, audit completion, theorem completion, or master
acceptance is claimed.
