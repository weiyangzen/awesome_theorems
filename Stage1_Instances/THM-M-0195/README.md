# THM-M-0195 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the Euler line theorem. The
repository catalog gives only the attribution Leonhard Euler, the year 1767, and the gloss
`三角形垂心、重心、外心共线` (the orthocenter, centroid, and circumcenter of a triangle are
collinear). It cites no mathematical source and fixes no definitions, ambient space,
nondegeneracy convention, binder order, boundary cases, or proof. The catalog label `已验证` is
untrusted metadata and supplies no human-source or machine-proof credit.

The University of the Pacific Euler Archive identifies a matching primary historical source:
Euler's *Solutio facilis problematum quorundam geometricorum difficillimorum*, Enestrom E325,
written in 1763 and published in 1767 in *Novi Commentarii academiae scientiarum
Petropolitanae* 11, pages 103-123. Its institutional record and primary scan were inspected as
source-family evidence. The scan studies the relevant triangle centers and gives stronger distance
relations, but the complete Latin definition, assumption, statement, proof, translation, and
correction crosswalk has not been independently reviewed. It therefore supports `H1`, not `H0`.

Pinned mathlib contains a strong exact-topic interface in
`Mathlib.Geometry.Euclidean.MongePoint`. Its `Affine.Triangle` is a three-point affinely
independent simplex, and it defines the centroid, circumcenter, and orthocenter. The theorem
`Affine.Triangle.orthocenter_eq_smul_vsub_vadd_circumcenter` gives the stronger affine position
formula `H = 3 • (G - O) + O`, from which collinearity is plausibly derivable. The discovery-only
`IntakeProbe.lean` authenticates these pinned definitions and interfaces. It does not select a
canonical source statement, declare the target, or prove it.

The intake therefore leaves the canonical mathematical statement and Lean target null. Statement
work must admit and independently review an immutable source, decide whether the catalog means
only set collinearity or also the Euler-line order and ratio, map classical triangle centers to the
Lean definitions, and resolve dimension and degenerate cases before crediting the mathlib anchor.

The provisional vector is `[H1, M3, R4]`: a classical published theorem family is recognizable but
the exact primary-source statement and assumption map are not audited; usable pinned formal
interfaces exist but no source-identical target, transport, or proof receipt is frozen; and no
source-faithful proof reconstruction exists. All six dependent phases remain open. No H0, M0, R0,
accepted state, audit completion, theorem completion, accepted receipt, or master acceptance is
claimed.
