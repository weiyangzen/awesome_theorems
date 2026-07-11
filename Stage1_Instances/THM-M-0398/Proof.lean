import ObligationTree

/-!
# THM-M-0398 proof execution

This module implements the constant-monotonicity and constant-one composition
parts of the frozen architecture. It does not supply Roth's substantive
auxiliary-polynomial finiteness engine.
-/

namespace Stage1Instances.THMM0398

/-- Finiteness at a larger positive constant implies finiteness at every
smaller positive constant. This is the elementary constant-normalization
part of the terminal finiteness interface. -/
theorem finite_exceptional_mono_constant
    {α ε C C' : ℝ} (hC : C' ≤ C)
    (hfinite : {r : ℚ |
      |α - (r : ℝ)| < C / denominator r ^ ((2 : ℝ) + ε)}.Finite) :
    {r : ℚ |
      |α - (r : ℝ)| < C' / denominator r ^ ((2 : ℝ) + ε)}.Finite := by
  apply hfinite.subset
  intro r hr
  exact hr.trans_le (div_le_div_of_nonneg_right hC
    (Real.rpow_pos_of_pos (denominator_pos r) _).le)

/-- Proof-phase recheck of the exact terminal-to-root composition. The
uniform Roth estimate remains an explicit premise. -/
theorem thueSiegelRoth_of_uniform_constant_estimate
    (h : FiniteExceptionalWithConstant) : ThueSiegelRoth := by
  exact root_of_finiteExceptionalWithConstant h

#print axioms finite_exceptional_mono_constant
#print axioms thueSiegelRoth_of_uniform_constant_estimate

end Stage1Instances.THMM0398
