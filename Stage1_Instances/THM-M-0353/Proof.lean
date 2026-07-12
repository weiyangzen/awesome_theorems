import Statement
import Mathlib.Analysis.SpecialFunctions.Gaussian.GaussianIntegral

/-!
# THM-M-0353 proof execution

This module contains proved leaves of the frozen obligation tree.  It deliberately
does not expose the canonical root until both analytic packages are closed.
-/

namespace Stage1Instances.THM_M_0353

open scoped ENNReal
open MeasureTheory

/-- The zeroth normalized Hermite function is square-integrable. -/
theorem hermiteFunction_zero_memLp :
    MemLp (hermiteFunction 0) (2 : ENNReal) leb := by
  have hzero : hermiteFunction 0 = fun x : Real =>
      (((Real.pi ^ (-(1 : Real) / 4)) * Real.exp (-(x ^ 2 / 2)) : Real) : Complex) := by
    funext x
    simp [hermiteFunction]
  rw [hzero, memLp_two_iff_integrable_sq_norm]
  · convert
    (integrable_exp_neg_mul_sq (by norm_num : (0 : Real) < 1)).const_mul
      ((Real.pi ^ (-(1 : Real) / 4)) ^ 2) using 1
    all_goals
      ext x
      rw [Complex.norm_real, Real.norm_eq_abs, abs_mul,
        abs_of_nonneg (Real.rpow_nonneg Real.pi_pos.le _),
        abs_of_pos (Real.exp_pos _), mul_pow, ← Real.exp_nat_mul]
      ring_nf
  · fun_prop

#print axioms hermiteFunction_zero_memLp

end Stage1Instances.THM_M_0353
