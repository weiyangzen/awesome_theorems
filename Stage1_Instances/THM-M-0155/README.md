# THM-M-0155 rev-5.6 intake

This directory is the fail-closed `planned` intake for Green's theorem in the plane. It identifies
the intended circulation form: the integral of `P dx + Q dy` around the positively oriented
boundary of a regular planar region equals the area integral of `partial_x Q - partial_y P`.

That familiar sentence is not yet an exact theorem. Published formulations differ on admissible
regions, boundary multiplicity and orientation, regularity near the boundary, and whether the
integrals are Riemann, measure-theoretic, chain, or differential-form integrals. The scope map keeps
these choices open for primary-source inspection instead of silently combining variants.

The provisional root vector is `[H1, M4, R4]`. The repository's `已验证` metadata is untrusted, and
no canonical Lean expression, proof, audit completion, or theorem completion is claimed. The open
downstream nodes are in `task-dag.json`; exact intake checks and results are in `validation.md`.
