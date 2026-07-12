import Mathlib.Topology.Algebra.Module.LocallyConvex
import Mathlib.Dynamics.FixedPoints.Basic

-- Intake-only shape probe: this declaration assumes the conclusion and earns no proof credit.
example {E : Type*} [AddCommGroup E] [Module ℝ E] [TopologicalSpace E]
    [IsTopologicalAddGroup E] [ContinuousSMul ℝ E] [LocallyConvexSpace ℝ E]
    (K : Set E) (f : E → E) (_hKne : K.Nonempty) (_hKcompact : IsCompact K)
    (_hKconvex : Convex ℝ K) (_hfcontinuous : Continuous f) (_hfK : Set.MapsTo f K K)
    (hresult : ∃ x ∈ K, Function.IsFixedPt f x) : ∃ x ∈ K, Function.IsFixedPt f x :=
  hresult
