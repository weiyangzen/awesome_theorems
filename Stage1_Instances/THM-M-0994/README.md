# THM-M-0994 rev-5.6 intake

This directory is the `planned` intake for Hoeffding's inequality. It freezes the intended claim as
the one-sided concentration bound for a finite sum of independent, almost surely interval-bounded
real random variables, centered by its expectation.

The statement node now freezes and elaborates the exact arbitrary finite-family target in
`Statement.lean`; its fingerprint and scoped checks are recorded in `statement.json` and
`statement-validation.md`. The legacy Lean module remains discovery input only. Its initial-segment
and variance-proxy encoding receives no proof or transport credit before later nodes. The
provisional machine status remains M3; no audit or theorem completion is claimed.

The scope map, source crosswalk, and open task DAG define the downstream work. Intake validation and
its exact limits are recorded in `validation.md`.
