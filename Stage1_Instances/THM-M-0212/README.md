# THM-M-0212 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`布里昂雄定理` (Brianchon's theorem). The catalog attributes it to Charles Julien Brianchon in
1806 and supplies only the gloss `圆锥曲线外切六边形的共点性质`, or "the concurrency property
of a hexagon circumscribed about a conic." Its `已验证` label is untrusted metadata under
rev-5.6, not source or kernel evidence.

The title and gloss identify the classical Brianchon-theorem family, but they do not determine one
exact proposition. They omit the projective-plane model and scalar field, the conic and tangency
definitions, the order and noncoincidence of the six tangent sides, how vertices are formed, the
three principal diagonals, the encoding of concurrency, and every degenerate boundary. They also
do not say whether a converse or a theorem obtained by projective duality is part of the target.
Selecting any of these choices at intake would add, narrow, or substitute mathematics.

Two modern source leads were inspected. Valles states a complex-projective theorem for a polygon
of tangent lines to a smooth conic as the `n = 3` case of a dual Mobius theorem and derives it by
polarity. The publisher abstract for Lampa-Baczynska and Wojcik describes the classical six-tangent
configuration and three concurrent diagonals. These are valuable discovery leads, but neither is
silently adopted as the catalog's exact root or accepted as `H0`.

Pinned mathlib provides adjacent substrate: projective points and subspaces, homogeneous cross
product and incidence, projective dependence, and quadratic forms. The API-only
`IntakeProbe.lean` authenticates those interfaces. It does not define a source-selected conic,
tangent-line or polarity model, a projective concurrency predicate, or Brianchon's theorem. A
bounded exact-topic search located no target declaration.

The provisional vector is `[H1, M4, R4]`: a published statement and polarity proof route are known,
but exact source identity, assumptions, degeneracies, correction status, and independent mapping
remain open; no usable exact formal artifact is credited; and no source-faithful reconstruction can
attach before the root is frozen. `instance.json` is the structured scope authority and
`task-dag.json` keeps all six downstream phases open. No canonical proposition, H0, M0, R0,
accepted execution state, audit completion, theorem completion, or master acceptance is claimed.
