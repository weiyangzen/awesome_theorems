import Statement

/-!
# THM-M-0312 differential validation

This module imports neither `Proof` nor `ObligationTree`. It reconstructs the exact frozen root
directly through the two pinned mathlib packages used by the public Banach-Steinhaus theorem.
-/

namespace Stage1Instances.THM_M_0312.Validation

universe uE uF uK uK2 uI

variable {E : Type uE} {F : Type uF} {K : Type uK} {K2 : Type uK2}
  [SeminormedAddCommGroup E] [SeminormedAddCommGroup F]
  [NontriviallyNormedField K] [NontriviallyNormedField K2]
  [NormedSpace K E] [NormedSpace K2 F]
  {sigma12 : K →+* K2} [RingHomIsometric sigma12]
  {I : Type uI} [CompleteSpace E]

/-- Same-worker reconstruction of the exact target without importing proof-phase code. -/
theorem uniformBoundedness_direct {g : I → E →SL[sigma12] F} :
    UniformBoundednessTarget g := by
  intro h
  rw [show (∃ C, ∀ i, ‖g i‖ ≤ C) ↔ _ from (NormedSpace.equicontinuous_TFAE g).out 5 2]
  refine (norm_withSeminorms K2 F).banach_steinhaus (fun _ x ↦ ?_)
  simpa [bddAbove_def, Set.forall_mem_range] using h x

#check uniformBoundedness_direct
#print axioms uniformBoundedness_direct

end Stage1Instances.THM_M_0312.Validation
