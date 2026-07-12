# THM-M-1251 rev-5.6 intake

This directory is the `planned` intake for tempered distributions. It freezes the human claim as
the identification of tempered distributions with continuous linear functionals on Schwartz
space, while leaving the scalar field, base space, and topology on the dual to the exact-source
statement phase.

The statement node now freezes and elaborates the complex pointwise-dual interpretation over
finite-dimensional real normed spaces in `Statement.lean`. This follows the topology explicitly
documented by the pinned mathlib API and does not assert an unstated strong-dual equivalence. The
provisional root vector remains `[H2, M4, R4]`: statement elaboration is not proof closure.

The scope map, crosswalk, and open task DAG record downstream decisions. Intake evidence is in
`validation.md`; statement-gate evidence is in `statement-validation.md` and `statement.json`.
