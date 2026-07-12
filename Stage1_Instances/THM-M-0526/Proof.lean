import «Stage1_Instances».«THM-M-0526».ObligationTree

/-!
# THM-M-0526: proof-phase implementation

This module closes `SVK-MAP-FUNCTORIALITY` and its parent `SVK-SQUARE` by
reducing both inclusion composites to the same map on path representatives.
The geometric existence and generation branches remain open; consequently
this file deliberately does not declare a proof of `SeifertVanKampenTarget`.
-/

namespace Stage1Instances.THM_M_0526

open Set

universe u

noncomputable section

variable {X : Type u} [TopologicalSpace X]

/-- The inclusion square commutes. After exposing a fundamental-group element
as a homotopy class, both composites map its representative to the same path
in the ambient space. -/
theorem square_commutativity_proof (U V : Set X) (x0 : X)
    (hxU : x0 ∈ U) (hxV : x0 ∈ V) :
    SquareCommutativity U V x0 hxU hxV := by
  change (FundamentalGroup.map (ambientInclusion U) _).comp
      (FundamentalGroup.map (subspaceInclusion inter_subset_left) _) =
    (FundamentalGroup.map (ambientInclusion V) _).comp
      (FundamentalGroup.map (subspaceInclusion inter_subset_right) _)
  ext p
  rcases p with ⟨p⟩
  rfl

/-- Cover-parametric package consumed by `compose_root`. None of the cover or
connectedness hypotheses is needed for functoriality of the inclusion maps. -/
theorem square_package :
    ∀ (X : Type u) [TopologicalSpace X]
      (U V : Set X) (x0 : X), IsOpen U → IsOpen V → U ∪ V = univ →
      (hxU : x0 ∈ U) → (hxV : x0 ∈ V) →
      IsPathConnected U → IsPathConnected V → IsPathConnected (U ∩ V) →
      SquareCommutativity U V x0 hxU hxV := by
  intro X _ U V x0 _ _ _ hxU hxV _ _ _
  exact square_commutativity_proof U V x0 hxU hxV

end

end Stage1Instances.THM_M_0526

#check Stage1Instances.THM_M_0526.square_commutativity_proof
#check Stage1Instances.THM_M_0526.square_package
#print axioms Stage1Instances.THM_M_0526.square_commutativity_proof
#print axioms Stage1Instances.THM_M_0526.square_package
