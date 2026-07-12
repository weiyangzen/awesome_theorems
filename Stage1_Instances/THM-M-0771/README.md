# THM-M-0771 rev-5.6 intake

This directory is the fail-closed `planned` dossier for the well-ordering theorem. The repository
claim is "every set can be well-ordered." The statement phase freezes this as every `alpha : Type u`
admitting a relation `r` with `IsWellOrder alpha r`; it also checks the equivalence with existence
of a `LinearOrder alpha` satisfying `WellFoundedLT alpha`.

`Statement.lean` uses only `Mathlib.Order.RelClasses`, so it does not import the cardinal
construction or `exists_wellOrder`. The exact target, both encoding transports, mutations, and
empty/singleton boundaries elaborate. This is statement identity evidence, not proof credit: the
anchor audit, terminal-body provenance, and all later phases remain open.

The root remains `[H1, M3, R4]`. A primary 1904 source is located, but its exact passage,
translation, assumptions, errata, and independent review remain open. Exact commands and results
are recorded in `validation.md`; all downstream tasks remain open in `task-dag.json`.
