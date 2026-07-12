import Mathlib.Analysis.Convex.KreinMilman
import Mathlib.Topology.Algebra.ContinuousAffineMap

open Set

#check IsCompact
#check Convex
#check LocallyConvexSpace
#check ContinuousAffineMap

namespace Stage1Instances.THM_M_0321.IntakeProbe

variable {E : Type*} [AddCommGroup E] [Module ℝ E] [TopologicalSpace E]
  [IsTopologicalAddGroup E] [ContinuousSMul ℝ E] [LocallyConvexSpace ℝ E]

/-- A type-level probe for the intended input vocabulary; this is not the theorem target. -/
def InputVocabulary (K : Set E) : Prop :=
  K.Nonempty ∧ IsCompact K ∧ Convex ℝ K

/-- A type-level probe for one possible ambient-map encoding; no existence is asserted. -/
def CommonFixedPointShape {ι : Type*} (K : Set E) (f : ι → E →ᴬ[ℝ] E) : Prop :=
  (∀ i, MapsTo (f i) K K) ∧ ∃ x ∈ K, ∀ i : ι, f i x = x

end Stage1Instances.THM_M_0321.IntakeProbe
