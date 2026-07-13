# THM-M-0215 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the hyperbolic law of cosines. The
repository gives only the gloss `双曲三角形边与角的关系` ("a relation between the sides and angles
of a hyperbolic triangle"), attributes the result to multiple mathematicians in the nineteenth
century, and labels it verified. Under rev-5.6 that label is untrusted inventory metadata, not an
exact source statement or proof evidence.

The title identifies a familiar theorem family, but the gloss does not choose the side or angle
law, a curvature normalization, a model of the hyperbolic plane, definitions of side length and
interior angle, a vertex-label convention, or a policy for degenerate and ideal triangles. These
choices change the proposition. Intake therefore records the standard side-law formula only as a
source-search lead and does not silently promote it to the canonical target.

Immanuel Asmus's immutable arXiv paper *Duality between Hyperbolic and de Sitter Geometry*,
arXiv:0810.5303v2, was inspected as a modern source lead. Theorem 5.1 gives all three side-law
equations for non-degenerate hyperbolic and antipodal-hyperbolic triangles in a normalized
hyperboloid model, including
`cosh(a) = cosh(b) * cosh(c) - cos(alpha) * sinh(b) * sinh(c)`. This disambiguates a strong
candidate, but the catalog does not cite the paper, the historical/source identity is unresolved,
and an independent source review is absent. It supports provisional `H1`, not `H0`.

Pinned mathlib provides real hyperbolic trigonometry and the Poincare metric on
`UpperHalfPlane`, including `UpperHalfPlane.cosh_dist`, but a bounded search found no hyperbolic
triangle or hyperbolic cosine-law declaration. `IntakeProbe.lean` authenticates only those adjacent
interfaces. They are ingredients, not a substitute theorem.

The provisional vector is `[H1, M4, R4]`. `instance.json` is the structured scope authority and
`task-dag.json` keeps all six downstream phases open. No canonical statement, H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
