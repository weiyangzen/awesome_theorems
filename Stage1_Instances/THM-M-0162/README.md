# THM-M-0162 rev-5.6 intake

This directory is the `planned` intake for the Frenet-Serret formulas. It freezes the intended
human claim as the moving-frame derivative equations for a sufficiently differentiable,
unit-speed curve in Euclidean three-space at points of nonzero curvature. The sign convention is
fixed in `scope-map.md`: `B = T x N` and `tau = -<B', N>`.

The repository supplies only the phrase "the moving-frame equations for a space curve," the
historical names Frenet and Serret, and an untrusted `已验证` label. A modern source family is
identified, but no exact edition/page has been inspected and no canonical Lean expression has
been elaborated. The provisional root vector is `[H1, M4, R4]`.

The scope map, source-statement crosswalk, and open task DAG define the downstream work. Intake
checks and their exact results are recorded in `validation.md`. No statement, proof, audit, or
theorem-completion credit is claimed.
