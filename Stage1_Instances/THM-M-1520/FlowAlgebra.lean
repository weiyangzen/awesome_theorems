import Statement

/-!
# THM-M-1520 flow algebra

This module implements the algebraic inverse-time part of `M1520-N-FLOW`. It does not supply
spatial differentiability, the variational equation, or the Jacobian argument needed by the root.
-/

namespace Stage1.THM_M_1520

/-- Each time map of a two-sided flow is bijective, with inverse the negative-time map. -/
theorem timeMap_bijective
    {n : Nat} {Phi : Real -> PhaseSpace n -> PhaseSpace n}
    (hzero : forall z, Phi 0 z = z)
    (hflow : forall s t z, Phi (s + t) z = Phi s (Phi t z))
    (t : Real) : Function.Bijective (Phi t) := by
  have hleft : Function.LeftInverse (Phi (-t)) (Phi t) := by
    intro z
    rw [← hflow (-t) t z, neg_add_cancel, hzero]
  have hright : Function.RightInverse (Phi (-t)) (Phi t) := by
    intro z
    rw [← hflow t (-t) z, add_neg_cancel, hzero]
  exact ⟨hleft.injective, hright.surjective⟩

#print sorries timeMap_bijective
#print axioms timeMap_bijective

end Stage1.THM_M_1520
