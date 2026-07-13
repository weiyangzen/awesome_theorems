# THM-M-0199 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`梅涅劳斯定理` (Menelaus's theorem). The catalog attributes it to Menelaus of Alexandria around
100 CE and supplies only the gloss `共线点的比例关系` ("the ratio relation of collinear points")
plus an untrusted `已验证` label. It gives no citation, formula, definitions, assumptions, proof,
reviewer, or formal artifact.

The title identifies the classical Menelaus theorem family, but the gloss does not determine one
proposition. A conventional form concerns three points on the extended side lines of a
nondegenerate triangle and characterizes their collinearity by a product of directed ratios. The
source does not choose the point/side correspondence, signed or unsigned convention, product sign
and order, implication or equivalence, affine domain, denominators, points at infinity, or
degenerate cases. Intake records that familiar reading only as a search target and does not silently
turn it into the canonical claim.

An inspected modern source lead, McConnell's *A Six-Point Ceva-Menelaus Theorem*, states a directed
ratio form of the classical theorem as an iff. It is not cited by the catalog or independently
accepted, so it is discovery evidence rather than `H0`. Pinned mathlib contains affine triangles,
line interpolation, collinearity, and an exact-topic Ceva module, but bounded searches found no
Menelaus declaration. `IntakeProbe.lean` authenticates this substrate and explicitly treats Ceva as
a neighboring theorem, not a substitute.

The provisional vector is `[H1, M4, R4]`: the classical theorem and a complete modern statement
lead are identifiable, exact source fidelity remains unreviewed, no usable exact Lean root is
credited, and no source-faithful proof reconstruction exists. `instance.json` freezes this intake
boundary and `task-dag.json` leaves all six dependent phases open. No canonical proposition,
statement fingerprint, H0, M0, R0, accepted execution state, audit completion, theorem completion,
or master acceptance is claimed.
