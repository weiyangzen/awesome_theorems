# THM-M-1251 rev-5.6 intake

This directory is the `planned` intake for tempered distributions. It freezes the human claim as
the identification of tempered distributions with continuous linear functionals on Schwartz
space, while leaving the scalar field, base space, and topology on the dual to the exact-source
statement phase.

The statement node now freezes and elaborates the complex pointwise-dual interpretation over
finite-dimensional real normed spaces in `Statement.lean`. This follows the topology explicitly
documented by the pinned mathlib API and does not assert an unstated strong-dual equivalence.
The obligation registry freezes 11 semantic nodes and seven separate typed graphs. The exact root
has an `M0-W` definitional anchor, but this is not proof-phase or release acceptance;
`[H2, M0-W, R4]` remains an audit classification.

The scope map, crosswalk, and open task DAG record downstream decisions. Intake evidence is in
`validation.md`; statement-gate evidence is in `statement-validation.md` and `statement.json`.
The frozen architecture and scoped validation are in `obligation-tree.md`,
`obligation-registry.json`, `typed-graphs.json`, and `obligation-tree-validation.md`.
