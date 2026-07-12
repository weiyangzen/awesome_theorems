import Mathlib.Topology.Algebra.Module.LocallyConvex
import Mathlib.Dynamics.FixedPoints.Basic
import Mathlib.Topology.Order.IntermediateValue
import Mathlib.Topology.MetricSpace.Contracting

/-! Kernel probes for the immutable anchor audit. This file does not prove the target. -/

namespace AwesomeTheorems.THM_M_0317.AnchorAudit

#check LocallyConvexSpace
#check IsCompact
#check Convex
#check Function.IsFixedPt
#check exists_mem_Icc_isFixedPt_of_mapsTo
#check ContractingWith.exists_fixedPoint'

/-- The pinned interval theorem closes only the one-dimensional interval special case. -/
example {a b : Real} {f : Real -> Real} (hf : ContinuousOn f (Set.Icc a b))
    (hab : a <= b) (hmaps : Set.MapsTo f (Set.Icc a b) (Set.Icc a b)) :
    ∃ x ∈ Set.Icc a b, Function.IsFixedPt f x :=
  exists_mem_Icc_isFixedPt_of_mapsTo hf hab hmaps

/-- The exact root shape used to reject narrower fixed-point candidates. -/
def AuditedRootShape {E : Type*} [AddCommGroup E] [Module Real E]
    [TopologicalSpace E] [IsTopologicalAddGroup E] [ContinuousSMul Real E]
    [T2Space E] [LocallyConvexSpace Real E] (K : Set E) (f : E -> E) : Prop :=
  K.Nonempty -> IsCompact K -> Convex Real K -> Continuous f -> Set.MapsTo f K K ->
    ∃ x ∈ K, Function.IsFixedPt f x

#check AuditedRootShape

end AwesomeTheorems.THM_M_0317.AnchorAudit
