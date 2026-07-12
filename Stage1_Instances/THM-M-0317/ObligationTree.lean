import Statement

/-!
Conditional composition interfaces for the frozen Tychonoff fixed-point route.
The two package hypotheses remain explicit; this file does not prove them.
-/

universe u

namespace AwesomeTheorems.THM_M_0317

/-- A point fixed modulo every neighbourhood of zero. -/
def HasArbitrarilySmallDisplacement {E : Type u} [AddCommGroup E]
    [TopologicalSpace E] (K : Set E) (f : E -> E) : Prop :=
  forall V : Set E, V ∈ nhds (0 : E) -> ∃ x, x ∈ K ∧ f x - x ∈ V

/-- The finite-dimensional approximation half of the architecture. -/
def ApproximationPackage : Prop :=
  forall {E : Type u} [AddCommGroup E] [Module Real E]
    [TopologicalSpace E] [IsTopologicalAddGroup E] [ContinuousSMul Real E]
    [T2Space E] [LocallyConvexSpace Real E] (K : Set E) (f : E -> E),
      K.Nonempty -> IsCompact K -> Convex Real K -> Continuous f ->
        Set.MapsTo f K K -> HasArbitrarilySmallDisplacement K f

/-- The compactness/separation limit half of the architecture. -/
def CompactnessLimitPackage : Prop :=
  forall {E : Type u} [AddCommGroup E] [Module Real E]
    [TopologicalSpace E] [IsTopologicalAddGroup E] [ContinuousSMul Real E]
    [T2Space E] [LocallyConvexSpace Real E] (K : Set E) (f : E -> E),
      K.Nonempty -> IsCompact K -> Convex Real K -> Continuous f ->
        Set.MapsTo f K K -> HasArbitrarilySmallDisplacement K f ->
          ∃ x, x ∈ K ∧ Function.IsFixedPt f x

/-- Checked conditional composition of the two open packages into the exact target. -/
theorem root_of_approximation_and_limit
    (approximation : ApproximationPackage.{u})
    (limit : CompactnessLimitPackage.{u}) :
    forall {E : Type u} [AddCommGroup E] [Module Real E]
      [TopologicalSpace E] [IsTopologicalAddGroup E] [ContinuousSMul Real E]
      [T2Space E] [LocallyConvexSpace Real E] (K : Set E) (f : E -> E),
        TychonoffFixedPointTarget K f := by
  intro E _ _ _ _ _ _ _ K f hK hc hconv hf hmaps
  exact limit K f hK hc hconv hf hmaps
    (approximation K f hK hc hconv hf hmaps)

#print axioms root_of_approximation_and_limit

end AwesomeTheorems.THM_M_0317
