# THM-M-0214 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`球面几何余弦定理` (spherical law of cosines). The catalog supplies only the gloss
`球面三角形边与角的关系` ("the relation between the sides and angles of a spherical triangle"),
the attribution "many mathematicians", and the date "ancient". It gives no source, formula,
definitions, hypotheses, conclusion, or formal artifact. Its `已验证` ("verified") field is
untrusted metadata under rev-5.6 and supplies no source or kernel credit.

The gloss identifies spherical trigonometry, but not one exact proposition. In standard notation,
both the side cosine rule and its dual angle rule match the wording. Even the side rule changes
shape depending on whether sides are central angles or arc lengths on a sphere of radius `R`.
Selecting one convention at intake would add proposition-changing mathematics absent from the
source record.

This intake therefore freezes the ambiguity while leaving the canonical mathematical and Lean
statements null. The provisional root vector is `[H5, M4, R4]`: `H5` classifies the received gloss
as not yet a stable proposition, not the classical cosine rules as false; `M4` records that no
source-identical usable formal artifact is admitted; and `R4` records that a source-faithful proof
reconstruction cannot attach to an unfrozen root.

Pinned mathlib provides ambient Euclidean spheres, vector and point angles, and the Euclidean law
of cosines. These are useful encoding ingredients, not an intrinsic spherical distance or a
spherical-triangle cosine theorem. `IntakeProbe.lean` checks those adjacent APIs only. All six
downstream phases remain open. No canonical statement, H0, M0, R0, accepted proof state, audit
completion, theorem completion, or master acceptance is claimed.
