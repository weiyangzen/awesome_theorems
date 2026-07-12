# THM-M-0219 rev-5.6 intake

This directory is the fail-closed `planned` intake dossier for the repository label
`庞加莱半平面模型` (Poincare half-plane model). The catalog attributes the entry to Henri
Poincare, dates it to 1882, and supplies only the gloss `双曲几何的另一种模型` ("another model
of hyperbolic geometry"). Its `已验证` label is untrusted metadata under rev-5.6 and supplies no
human-source or Lean proof credit.

The label names a mathematical model, but the gloss is not one truth-valued proposition. It does
not say whether the intended root is construction of the upper-half-plane carrier and metric, the
metric-space laws, conformality, completeness, constant curvature `-1`, a classification of
geodesics, satisfaction of a chosen axiom system for hyperbolic geometry, invariance under real
fractional-linear transformations, or an explicit isometry with the separately cataloged disk
model. Choosing one of these would add proposition-changing mathematics.

Pinned mathlib does provide genuine adjacent substrate: `UpperHalfPlane`, the Poincare distance
formula `UpperHalfPlane.dist_eq`, a `MetricSpace` and `ProperSpace`, the fractional-linear action,
and an `IsIsometricSMul SL(2, R) UpperHalfPlane` instance. These checked interfaces make a later
formalization plausible, but they are not matched to an exact source-selected root and receive no
statement or proof credit in this intake.

The provisional root vector is `[H5, M4, R4]`. `H5` classifies the received catalog model/gloss as
not yet a stable proposition; it does not refute or declare open any standard theorem about the
Poincare half-plane. The structured scope authority is `instance.json`; the scope map preserves
the proposition-changing choices and neighboring-model boundary; the crosswalk records source
provenance and the pinned Lean substrate; and the open DAG records all downstream phases. No
canonical Lean expression, H0, M0, R0, accepted execution state, audit completion, theorem
completion, or master acceptance is claimed.
