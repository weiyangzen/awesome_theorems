import Statement
import Mathlib.Analysis.SpecialFunctions.Pow.Asymptotics

/-!
# THM-M-1006 frozen-target counterexample certificate

The exact frozen target asks for the two discrete Burkholder--Davis--Gundy comparisons for every
positive exponent.  For unrestricted discrete martingales this is false below exponent one.  The
finite martingales used in the accompanying blocker report depend on elementary two-point,
mean-zero transitions.  This module kernel-checks their algebra and the asymptotic obstruction at
the concrete exponent `p = 1 / 2`.

This is deliberately not advertised as a full formal refutation of `StatementShape`: the finite
probability spaces, filtrations, martingale laws, and moment evaluations are specified and checked
mathematically in `counterexample-analysis.md`, but have not all been encoded here.  No
positive proof credit follows from this certificate.
-/

namespace Stage1Instances.THM_M_1006.Counterexample

/-- The exponent used by both counterexample families lies in the omitted range `(0, 1)`. -/
theorem half_mem_openUnitInterval : (0 : Real) < 1 / 2 ∧ (1 / 2 : Real) < 1 := by
  norm_num

/-- In the upper-direction family, an active node moves by `+1` with probability `1-q` and by
`-(1-q)/q` with probability `q`.  Its conditional increment has mean zero. -/
theorem upper_transition_centered (q : Real) (hq : q ≠ 0) :
    (1 - q) * 1 + q * (-(1 - q) / q) = 0 := by
  field_simp
  ring

/-- In the lower-direction family, an active state `x` usually changes sign and rarely escapes to
`((2-q)/q) x`.  The conditional expectation of the new state is the old state. -/
theorem lower_transition_preserves_mean (q x : Real) (hq : q ≠ 0) :
    (1 - q) * (-x) + q * (((2 - q) / q) * x) = x := by
  field_simp
  ring

/-- With `q_N = 2^{-N}`, the rare compensating upper-family jump has size `2^N - 1`. -/
theorem upper_rare_jump_size (N : Nat) :
    ((1 - (2 : Real) ^ (-(N : Int))) / (2 : Real) ^ (-(N : Int))) = 2 ^ N - 1 := by
  rw [zpow_neg]
  field_simp
  norm_num

/-- With the same rarity, the lower-family escape multiplier is `2^(N+1) - 1`. -/
theorem lower_escape_multiplier (N : Nat) :
    ((2 - (2 : Real) ^ (-(N : Int))) / (2 : Real) ^ (-(N : Int))) = 2 ^ (N + 1) - 1 := by
  rw [zpow_neg, pow_succ]
  field_simp
  norm_num

/-- On a no-escape path of length `N`, the lower-family quadratic variation is one initial unit
jump followed by `N-1` sign changes of squared size four. -/
theorem lower_survival_quadratic_variation (N : Nat) (hN : 1 <= N) :
    (1 : Nat) + 4 * (N - 1) = 4 * N - 3 := by
  omega

/-- A polynomial factor is dominated by exponential decay.  After the base-two change of variables,
this is the asymptotic fact used by both counterexample error bounds at `p = 1 / 2`. -/
theorem upper_error_tends_to_zero :
    Filter.Tendsto (fun x : Real => x * Real.exp (-(1 / 2) * x))
      Filter.atTop (nhds 0) := by
  simpa only [one_div, Real.rpow_one] using
    tendsto_rpow_mul_exp_neg_mul_atTop_nhds_zero 1 (1 / 2) (by norm_num)

/-- The survival contribution in the lower-family square-function moment has a factor `N^(1/4)`,
which is unbounded. -/
theorem quarter_power_unbounded :
    Filter.Tendsto (fun x : Real => x ^ (1 / 4 : Real)) Filter.atTop Filter.atTop := by
  exact tendsto_rpow_atTop (by norm_num)

#print axioms half_mem_openUnitInterval
#print axioms upper_transition_centered
#print axioms lower_transition_preserves_mean
#print axioms upper_rare_jump_size
#print axioms lower_escape_multiplier
#print axioms lower_survival_quadratic_variation
#print axioms upper_error_tends_to_zero
#print axioms quarter_power_unbounded

end Stage1Instances.THM_M_1006.Counterexample
