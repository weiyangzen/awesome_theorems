# THM-M-0414 rev-5.6 intake

This directory is the `planned` dossier for the unique factorization of ideals in a Dedekind
domain. The canonical statement covers every nonzero integral ideal: a proper nonzero ideal
factors uniquely, up to order, as a finite product of nonzero prime ideals, while the unit ideal
has the empty factorization.

The intake itself gives the existing Lean file and mathlib declarations no proof credit. The
statement phase has now selected and self-tested the combined finite-product and
unique-factorization-monoid target in `Statement.lean`; `statement.json` records its expression and
environment fingerprints. This provisional statement evidence still requires master acceptance
and gives no proof-body or theorem-completion credit.

The provisional root vector remains `[H2, M3, R3]`. No exact source edition, accepted proof state,
audit completion, or theorem completion is claimed. Downstream work remains open in
`task-dag.json`; intake validation is in `validation.md` and statement validation is in
`statement-validation.md`.
