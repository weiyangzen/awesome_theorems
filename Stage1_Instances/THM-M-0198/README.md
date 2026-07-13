# THM-M-0198 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for `THM-M-0198`, the catalog item
`西姆松线定理` (Simson line theorem). The repository supplies only the attribution Robert Simson,
the year 1756, the gloss `三角形外接圆上一点在三边的投影共线` (the projections of a point on a
triangle's circumcircle onto its three sides are collinear), and an untrusted `已验证` label. It
supplies no bibliography, definitions, ordered binders, hypotheses, proof, or formal declaration.

The gloss identifies the forward classical theorem family but not one exact proposition. In
particular, it does not fix a Euclidean plane model, the nondegeneracy of the triangle, whether
"sides" means the three supporting lines or the closed segments, whether the circle point may be a
vertex, or the encodings of projection and collinearity. Intake records these proposition-changing
choices without silently resolving them. It also excludes the converse and stronger equivalence,
neither of which appears in the received wording.

Pinned mathlib supplies an affine-independent `Affine.Triangle`, its `circumsphere`, orthogonal
projection onto the affine span of each opposite face, and a general `Collinear` predicate.
`IntakeProbe.lean` authenticates only those interfaces. A bounded exact-topic search found no
Simson, Wallace-Simson, or pedal-line declaration in pinned mathlib or repository-local Lean.

The provisional vector is `[H1, M3, R4]`: the named classical theorem family is historically
established but has no accepted source-statement crosswalk; usable statement-level geometry
interfaces exist but no exact Simson root or proof body is selected; and no reviewed readable proof
reconstruction exists. All six downstream phases remain open. No H0, M0, R0, accepted execution
state, audit completion, theorem completion, or master acceptance is claimed.
