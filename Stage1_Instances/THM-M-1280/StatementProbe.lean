import Mathlib.Geometry.Manifold.Riemannian.Basic

/-!
This file checks only the pinned manifold substrate relevant to the Yamabe statement.
It is not a formal statement or proof of the Yamabe theorem.
-/

#check Bundle.RiemannianMetric
#check Bundle.ContMDiffRiemannianMetric
#check IsManifold
#check CompactSpace
#check ConnectedSpace
#check Module.finrank

universe u

/-- The available positive smooth conformal-factor boundary, without a curvature API. -/
abbrev PositiveSmoothFactor (M : Type u) [TopologicalSpace M] : Type u :=
  {u : C(M, ℝ) // ∀ x, 0 < u x}
