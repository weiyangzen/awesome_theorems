# THM-M-0771 rev-5.6 intake

This directory is the fail-closed `planned` dossier for the well-ordering theorem. The repository
claim is "every set can be well-ordered." The statement phase freezes this as every `alpha : Type u`
admitting a relation `r` with `IsWellOrder alpha r`; it also checks the equivalence with existence
of a `LinearOrder alpha` satisfying `WellFoundedLT alpha`.

`Statement.lean` uses only `Mathlib.Order.RelClasses`, so it does not import the cardinal
construction or `exists_wellOrder`. The exact target, both encoding transports, mutations, and
empty/singleton boundaries elaborate. This is statement identity evidence, not proof credit: the
The pinned anchor audit identifies the construction but does not credit it as a proof. The
obligation-tree phase freezes nine stable semantic units and seven separate typed graphs.
`ObligationTree.lean` checks only conditional composition from a pointwise relation witness to the
exact root, deliberately leaving the construction witness open for the proof phase.

The root remains `[H1, M3, R4]`. A primary 1904 source is located, but its exact passage,
translation, assumptions, errata, and independent review remain open. Exact commands and results
are recorded in `validation.md`; architecture commands and results are in
`obligation-tree-validation.md`. Proof, validation, and release remain open.
