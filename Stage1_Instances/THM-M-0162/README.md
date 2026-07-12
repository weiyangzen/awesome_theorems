# THM-M-0162 rev-5.6 statement dossier

This directory is the `planned` intake for the Frenet-Serret formulas. It freezes the intended
human claim as the moving-frame derivative equations for a sufficiently differentiable,
unit-speed curve in Euclidean three-space at points of nonzero curvature. The sign convention is
fixed in `scope-map.md`: `B = T x N` and `tau = -<B', N>`.

The exact statement is now elaborated as
`Stage1Instances.THM_M_0162.FrenetSerretTarget` in `Statement.lean`, with its environment and
boundary choices frozen in `statement.json`. A modern source family is identified, but no exact
edition/page has been inspected. The provisional root vector remains `[H1, M4, R4]`: statement
elaboration is not proof closure.

The scope map, source-statement crosswalk, and open task DAG define downstream work. Intake checks
are in `validation.md`; exact statement checks are in `statement-validation.md`. No proof, audit,
or theorem-completion credit is claimed.
