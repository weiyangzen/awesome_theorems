import Statement

/-!
# THM-M-1520 validation probes

These proofs independently reconstruct two boundary results from the frozen statement surface.
They deliberately do not import the proof or obligation-tree modules and do not assert the open
positive-dimensional Liouville root.
-/

open MeasureTheory

namespace Stage1.THM_M_1520.Validation

open Stage1.THM_M_1520

/-- Independent reconstruction of volume preservation at time zero. -/
theorem timeZero_measurePreserving_direct
    {n : Nat} {Phi : Real -> PhaseSpace n -> PhaseSpace n}
    (hzero : forall z, Phi 0 z = z) :
    MeasurePreserving (Phi 0) volume volume := by
  convert MeasurePreserving.id (volume : Measure (PhaseSpace n)) using 1
  exact funext hzero

/-- Independent reconstruction of the inverse-time bijection supplied by the flow laws. -/
theorem timeMap_bijective_direct
    {n : Nat} {Phi : Real -> PhaseSpace n -> PhaseSpace n}
    (hzero : forall z, Phi 0 z = z)
    (hflow : forall s t z, Phi (s + t) z = Phi s (Phi t z))
    (t : Real) : Function.Bijective (Phi t) := by
  refine Function.bijective_iff_has_inverse.mpr ⟨Phi (-t), ?_, ?_⟩
  · intro z
    rw [← hflow (-t) t z, neg_add_cancel, hzero]
  · intro z
    rw [← hflow t (-t) z, add_neg_cancel, hzero]

#check LiouvilleStatement
#print sorries timeZero_measurePreserving_direct
#print axioms timeZero_measurePreserving_direct
#print sorries timeMap_bijective_direct
#print axioms timeMap_bijective_direct

end Stage1.THM_M_1520.Validation
