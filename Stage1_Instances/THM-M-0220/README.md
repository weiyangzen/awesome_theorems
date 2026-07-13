# THM-M-0220 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`双曲面积公式` (hyperbolic area formula). The catalog supplies only the gloss
`双曲三角形面积与角亏的关系`: the relationship between the area of a hyperbolic
triangle and its angle defect. It attributes the item only to "many mathematicians" in the
nineteenth century, cites no source, and labels it `已验证`. Under rev-5.6 that label is
untrusted metadata, not source or kernel evidence.

The gloss identifies a classical theorem family but not one exact proposition. In curvature
`-1`, a common finite-geodesic-triangle formula is `Area = pi - (alpha + beta + gamma)`; in
curvature `-k^2`, the corresponding normalization divides the defect by `k^2`. The catalog fixes
neither scale. It also does not select a hyperbolic-plane model, the triangle and area objects,
angle conventions, finite versus ideal vertices, orientation, or degenerate cases. Neither common
formula is frozen or credited here.

Pinned mathlib contains a genuine upper-half-plane metric and invariant measure plus Euclidean
angle APIs. `IntakeProbe.lean` checks those adjacent interfaces only. A bounded exact-topic search
located no hyperbolic-triangle area-defect or Gauss-Bonnet declaration in pinned mathlib or the
repo-local Lean tree. That is intake discovery, not an exhaustive anchor audit or global absence
claim.

The provisional root vector is `[H1, M4, R4]`: the classical proved family is recognizable but no
exact primary statement and premise crosswalk is accepted; no usable exact formal artifact is
located; and no source-faithful readable proof exists. `instance.json` is the structured scope
authority, the scope map and crosswalk freeze all proposition-changing choices, and `task-dag.json`
keeps all six downstream phases open. No canonical statement, H0, M0, R0, accepted proof state,
audit completion, theorem completion, or master acceptance is claimed.
