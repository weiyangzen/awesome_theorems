import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
This file checks only the pinned Riemannian-manifold substrate relevant to
`THM-M-0181`. It is not a statement of Hamilton's Ricci-flow theorem.
-/

#check Bundle.RiemannianMetric
#check Bundle.ContMDiffRiemannianMetric
#check IsManifold
#check CompactSpace

universe u

/-- A checked time-indexed metric-family boundary, without a Ricci tensor or flow equation. -/
abbrev TimeIndexedMetricFamily
    {M : Type u} (E : M → Type*)
    [(x : M) → TopologicalSpace (E x)]
    [(x : M) → AddCommGroup (E x)]
    [(x : M) → Module ℝ (E x)] :=
  ℝ → Bundle.RiemannianMetric E
