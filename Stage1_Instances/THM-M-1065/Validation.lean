import Statement

/-!
# THM-M-1065 differential validation probes

This module independently reconstructs the frozen statement expansion and the `n = 1` event
boundary. It imports neither `Proof` nor `ObligationTree`, and it deliberately provides no KMT
coupling, maximal-tail estimate, or proof of the canonical root.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal

namespace Stage1Instances.THM_M_1065.Validation

/-- A separate elaboration of the definitional transport used to freeze the exact target. -/
theorem independentlyReconstructedTargetExpansion :
    KMTStrongApproximationTarget <-> ExpandedSourceShape := by
  rfl

/-- A separate reconstruction of the positive-time boundary calculation. -/
theorem independentlyReconstructedDiscrepancyEventOne {Omega : Type*}
    (X Y : Nat -> Omega -> Real) (C x : Real) :
    DiscrepancyEvent X Y C x 1 =
      {omega | |X 0 omega - Y 0 omega| > C * Real.log 1 + x} := by
  ext omega
  constructor
  · rintro ⟨k, hk1, hk2, hk⟩
    have : k = 1 := by omega
    subst k
    simpa using hk
  · intro h
    exact ⟨1, by simp, by simpa using h⟩

#print sorries independentlyReconstructedTargetExpansion
#print axioms independentlyReconstructedTargetExpansion
#print sorries independentlyReconstructedDiscrepancyEventOne
#print axioms independentlyReconstructedDiscrepancyEventOne

end Stage1Instances.THM_M_1065.Validation
