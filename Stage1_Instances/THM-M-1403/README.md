# THM-M-1403 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for topological entropy. The repository
record gives the title, the names Adler/Konheim/McAndrew, the year 1965, and only the gloss
"complexity of a dynamical system." It supplies neither a proposition nor a pinpoint source
passage. The inventory label `verified` is untrusted under rev-5.6.

Topological entropy is an invariant and a theory with several non-interchangeable definitions and
theorems, not by itself one theorem statement. A later source decision could select an AKM
finite-open-cover definition or result, an equivalence with a Bowen-Dinaburg formulation,
invariance under conjugacy, monotonicity under factors, or another property. Choosing any one now
would substitute a convenient theorem for the repository target.

The pinned mathlib contains a substantive Bowen-Dinaburg uniform-space API. `IntakeProbe.lean`
checks six declarations from that API, including the entropy definition, the invariant-subset
liminf/limsup equality, the cover/net comparison theorem, and semiconjugacy/restriction results.
Those checks establish only that candidate encoding ingredients elaborate. They do not identify
the AKM source claim, freeze a canonical target, or provide proof credit.

The provisional root vector is `[H5, M3, R4]`; `H5` records that the current catalog wording is not
a stable proposition, not that a reviewed topological-entropy theorem is false. `M3` records only
the checked pinned definitions and theorem interfaces; none is credited as the canonical root.
Lifecycle remains `planned` and all downstream tasks are open. No exact Lean expression, accepted
proof state, audit completion, or theorem completion is claimed. Exact commands and results are
recorded in `validation.md` and `intake-receipt.json`.
