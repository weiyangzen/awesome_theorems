import Mathlib.Tactic

/-!
# THM-M-0152 proof execution

This module contains a proof body for the frozen normal-orientation branch. It
does not declare the still-open Theorema Egregium root.
-/

namespace Stage1Instances.THM_M_0152.Proof

/-- Reversing the unit normal negates all three second-fundamental-form
coefficients but leaves the Gaussian-curvature quotient unchanged. This closes
the algebraic content of frozen obligation `M0152-B-ORIENTATION`.
-/
theorem gaussianQuotient_neg_normal (L M N D : ℝ) :
    ((-L) * (-N) - (-M) ^ 2) / D = (L * N - M ^ 2) / D := by
  ring

#print axioms gaussianQuotient_neg_normal

end Stage1Instances.THM_M_0152.Proof
