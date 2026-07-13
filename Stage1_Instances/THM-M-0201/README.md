# THM-M-0201 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`托勒密定理` (Ptolemy's theorem). The catalog supplies only the gloss
`圆内接四边形对角线乘积等于对边乘积之和`: in a cyclic quadrilateral, the product of
the diagonals equals the sum of the products of the two pairs of opposite sides. It attributes the
item to Claudius Ptolemy around 150 CE and labels it `已验证`. The label is untrusted metadata, not
source or kernel evidence.

The gloss identifies a classical theorem family but does not define cyclic order, convexity,
distinctness, degeneracy, the ambient Euclidean plane, or the encoding of a circle and segment
length. These choices matter: four points on a common sphere without an order do not determine
which pair is diagonal, and in higher dimension `Cospherical` is not literally a planar-circle
condition.

Pinned mathlib contains the exact-topic module `Mathlib.Geometry.Euclidean.Sphere.Ptolemy` and the
declaration `EuclideanGeometry.mul_dist_add_mul_dist_eq_mul_dist_of_cospherical`. Its conclusion is
the expected distance identity, while its hypotheses use a fifth point where both diagonals form
an angle of pi, thereby placing that point strictly inside both diagonal segments and constraining
their order. `IntakeProbe.lean` authenticates that interface and separately identifies Ptolemy's
inequality as a non-substitute.
This is direct statement/interface discovery, not an exact source transport, accepted anchor
audit, proof installation, or proof-body credit.

The provisional intake vector is `[H1, M3, R4]`: the classical human theorem is recognizable but
has no admitted source-exact crosswalk; a direct pinned formal interface exists but no canonical
root is frozen or credited; and no reviewed readable proof reconstruction exists. All six dependent
phases remain open in `task-dag.json`. Exact validation commands and boundaries appear in
`validation.md`. No H0, M0, R0, accepted receipt, audit completion, theorem completion, or master
acceptance is claimed.
