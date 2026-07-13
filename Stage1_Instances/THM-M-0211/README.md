# THM-M-0211 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label `帕斯卡定理`
(Pascal's theorem). The catalog attributes it to Blaise Pascal in 1640 and supplies only the gloss
`圆锥曲线内接六边形的共线性质`, or "the collinearity property of a hexagon inscribed in a
conic." Its `已验证` label is untrusted metadata under rev-5.6, not source or kernel evidence.

The title and gloss identify the classical Pascal-theorem family, but they do not determine one
exact proposition. They omit the projective-plane model and base field, the conic definition and
smoothness or degeneracy policy, the order and distinctness of the six points, the convention for
opposite-side intersections, and every coincident or repeated-point boundary case. They also do not
say whether the converse is included. Selecting any of these choices at intake would add or
substitute mathematics.

Two versioned modern source leads were inspected. Caminata and Schaffler state the forward theorem
for six points in a projective plane on a conic and distinguish a broader convention that also
includes the converse and degenerate conics. Wiese states a real-projective forward theorem that
permits repeated points via tangents when paired lines remain distinct. The difference is material,
so neither is silently adopted as the catalog's exact root or accepted as `H0`.

Pinned mathlib provides genuine adjacent substrate: projectivization, projective subspaces, a
homogeneous cross product and incidence relation, quadratic forms, and affine collinearity. The
API-only `IntakeProbe.lean` authenticates those interfaces. A bounded exact-topic search located no
Pascal-theorem declaration; the generic interfaces are not a conic model or a proof.

The provisional vector is `[H1, M4, R4]`: a complete published theorem family and proof leads are
known, but exact source identity, assumptions, degeneracies, corrections, and independent mapping
remain open; no usable exact formal artifact is credited; and no source-faithful reconstruction can
attach before the root is frozen. `instance.json` is the structured scope authority and
`task-dag.json` keeps all six downstream phases open. No canonical proposition, H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
