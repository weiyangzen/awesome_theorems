import Mathlib.Tactic

/-!
# THM-M-0152 independent validation probe

This module independently reconstructs the exact algebraic obligation closed
by `Proof.lean`. It intentionally does not declare the open Theorema Egregium
root.
-/

namespace Stage1Instances.THM_M_0152.Validation

/-- Independent check of frozen obligation `M0152-B-ORIENTATION`. This proof
expands squares and normalizes multiplication rather than invoking `ring`. -/
theorem independentGaussianQuotientNegNormal (L M N D : ℝ) :
    ((-L) * (-N) - (-M) ^ 2) / D = (L * N - M ^ 2) / D := by
  simp only [neg_mul_neg, neg_sq]

#check independentGaussianQuotientNegNormal
#print axioms independentGaussianQuotientNegNormal

end Stage1Instances.THM_M_0152.Validation
