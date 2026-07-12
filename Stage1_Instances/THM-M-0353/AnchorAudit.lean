import Mathlib.RingTheory.Polynomial.Hermite.Gaussian

/-!
# THM-M-0353: pinned mathlib anchor audit

These wrappers check the nearest declarations in the pinned mathlib revision.
They characterize the probabilists' Hermite polynomials and their relation to
Gaussian derivatives. Neither declaration proves `L2` membership,
orthonormality, density, or the existence of the target `HilbertBasis`.
-/

namespace Stage1Instances.THM_M_0353.AnchorAudit

open Polynomial

#check @Polynomial.hermite_monic
#check @Polynomial.deriv_gaussian_eq_hermite_mul_gaussian

/-- Mathlib's `hermite` really uses the monic probabilists' convention selected
by the frozen statement. This is a normalization anchor, not a basis theorem. -/
theorem probabilistsConvention (n : Nat) : (Polynomial.hermite n).Monic := by
  exact Polynomial.hermite_monic n

/-- The pinned Gaussian-derivative identity is useful analytic infrastructure,
but contains no integration or completeness conclusion. -/
theorem gaussianDerivativeAnchor (n : Nat) (x : Real) :
    deriv^[n] (fun y => Real.exp (-(y ^ 2 / 2))) x =
      (-1 : Real) ^ n * Polynomial.aeval x (Polynomial.hermite n) *
        Real.exp (-(x ^ 2 / 2)) := by
  exact Polynomial.deriv_gaussian_eq_hermite_mul_gaussian n x

end Stage1Instances.THM_M_0353.AnchorAudit

#print axioms Stage1Instances.THM_M_0353.AnchorAudit.probabilistsConvention
#print axioms Stage1Instances.THM_M_0353.AnchorAudit.gaussianDerivativeAnchor
