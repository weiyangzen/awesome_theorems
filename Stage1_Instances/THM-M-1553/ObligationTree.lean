import «Statement»

/-!
# THM-M-1553 obligation-tree interface

This file checks the final composition shape only.  The logarithmic-derivative
bridge is an explicit premise; no proof of that bridge is claimed here.
-/

noncomputable section

namespace Stage1Instances.THM_M_1553

/-- The open analytic bridge after the Hirota sums and the KdV residual have
been expanded.  Keeping it separate prevents a certificate field from being
mistaken for a proof of the public theorem. -/
def LogDerivativeBridge (tau : Field) : Prop :=
  ContDiff ℝ 5 tau →
  (∀ z : ℝ × ℝ, 0 < tau z) →
  SatisfiesKdVBilinearEquation tau →
  ∀ z : ℝ × ℝ, kdvResidual (tauTransform tau) z = 0

/-- Checked child-to-root composition.  This theorem consumes, rather than
constructs, the central analytic bridge. -/
theorem hirotaKdVTarget_of_logDerivativeBridge
    (bridge : ∀ tau : Field, LogDerivativeBridge tau) : HirotaKdVTarget := by
  intro tau smooth positive bilinear z
  exact bridge tau smooth positive bilinear z

#check hirotaKdVTarget_of_logDerivativeBridge
#print axioms hirotaKdVTarget_of_logDerivativeBridge

end Stage1Instances.THM_M_1553
