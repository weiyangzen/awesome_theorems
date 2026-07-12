import Statement

/-!
# THM-M-0349 proof execution

This module contains the repo-local proof body currently available for the
Fourier-polynomial construction leaf.  It deliberately does not declare the
root theorem: pinned mathlib has no weak `(1, 1)` conjugate-function estimate
or interpolation theorem from which the strong `L^p` result could be derived.
-/

namespace Stage1Instances.THM_M_0349

open MeasureTheory

/-- Apply the conjugate-function multiplier to one Fourier mode. -/
noncomputable def conjugateMode (n : Int) (a : Complex) : Circle -> Complex :=
  fun x => (conjugateMultiplier n * a) * fourier n x

/-- The one-mode construction has exactly the intended Fourier coefficients. -/
theorem fourierCoeff_conjugateMode (n : Int) (a : Complex) :
    forall k : Int, fourierCoeff (conjugateMode n a) k =
      (conjugateMultiplier n * a) * (Pi.single n 1 : Int -> Complex) k := by
  intro k
  unfold conjugateMode
  rw [fourierCoeff.const_mul]
  rw [congrFun (fourierCoeff_fourier (T := (1 : Real)) n) k]

/-- The multiplier vanishes on the constant mode. -/
theorem conjugateMultiplier_zero : conjugateMultiplier 0 = 0 := by
  rfl

#print axioms fourierCoeff_conjugateMode
#print axioms conjugateMultiplier_zero

end Stage1Instances.THM_M_0349
