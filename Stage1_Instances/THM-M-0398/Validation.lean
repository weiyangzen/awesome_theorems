import ObligationTree

/-!
# Independent validation probes for THM-M-0398

These probes independently reimplement the two proof bodies that the proof
phase actually supplies. They deliberately retain the uniform Roth estimate
as a premise and therefore do not close the canonical theorem.
-/

namespace Stage1Instances.THMM0398.Validation

open Stage1Instances.THMM0398

theorem independent_finite_exceptional_mono_constant
    {α ε C C' : ℝ} (hC : C' ≤ C)
    (hfinite : {r : ℚ |
      |α - (r : ℝ)| < C / denominator r ^ ((2 : ℝ) + ε)}.Finite) :
    {r : ℚ |
      |α - (r : ℝ)| < C' / denominator r ^ ((2 : ℝ) + ε)}.Finite := by
  refine hfinite.subset ?_
  rintro r hr
  change |α - (r : ℝ)| < C / denominator r ^ ((2 : ℝ) + ε)
  change |α - (r : ℝ)| < C' / denominator r ^ ((2 : ℝ) + ε) at hr
  exact lt_of_lt_of_le hr (div_le_div_of_nonneg_right hC
    (Real.rpow_pos_of_pos (denominator_pos r) _).le)

theorem independent_root_composition
    (h : FiniteExceptionalWithConstant) : ThueSiegelRoth := by
  intro α hα hirr ε hε
  simpa [IsExceptional] using h α hα hirr ε 1 hε zero_lt_one

#print axioms independent_finite_exceptional_mono_constant
#print axioms independent_root_composition

end Stage1Instances.THMM0398.Validation
