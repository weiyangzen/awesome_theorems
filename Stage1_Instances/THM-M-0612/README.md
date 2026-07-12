# THM-M-0612 rev-5.6 intake

This directory is the `planned` dossier for Gromov's symplectic nonsqueezing theorem. It freezes the
human claim as the sharp obstruction to symplectically embedding a standard ball into a thinner
standard cylinder. The statement worker has now proposed and kernel-elaborated the exact
local-domain target in `Statement.lean`; master acceptance and the exact primary-source anchor are
still open.

The legacy Lean module is discovery input only. In particular, its global ambient self-map is not
automatically equivalent to the classical local embedding of a ball, and its proposition is not
proved. The provisional root vector is `[H2, M3, R4]`: this records statement/interface evidence,
not proof closure. No audit completion or theorem completion is claimed.

The fresh anchor audit records pinned mathlib infrastructure and an external Lean 4 declaration of
the named theorem, but the external theorem and its dependencies contain `sorry`; it is not proof
evidence or an integration target. The scope map, source crosswalk, and open task DAG define the
downstream work. Phase checks and their exact results are recorded in `validation.md`.
