# THM-M-1111 rev-5.6 dossier

This directory is the `planned` intake for the Tao-Vu four moment theorem. It fixes the target to
the eigenvalue-statistics comparison theorem for two Wigner Hermitian ensembles with four-moment
off-diagonal matching and two-moment diagonal matching. It does not silently replace that result
with a generic moment lemma or with an unquantified universality slogan.

The statement node selects Theorem 15 of arXiv `0906.0510v10` and freezes its exact four-moment
branch in `Statement.lean`. The formal target preserves uniform Condition C0 constants, matching
orders four and two, five derivative orders, bulk indices, normalization through the semantic
eigenvalue-statistic operation, and the quantitative `n^(-c0)` conclusion. The analytic notions
are deliberately exposed as an unproved semantic interface rather than falsely attributed to
mathlib. No implementation of that interface and no proof completion is claimed.

The scope map and source crosswalk state the frozen boundaries; the open task DAG records all later
phases. Intake evidence remains in `validation.md`, and statement evidence is in
`statement-validation.md` and `statement.json`.
