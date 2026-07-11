import Statement

/-!
# Checked composition interface for THM-M-0398

This file checks only the passage from a uniform constant-factor Roth estimate
to the exact constant-one target. It does not provide the uniform estimate.
-/

namespace Stage1Instances.THMM0398

/-- A deliberately stronger interface used by the frozen proof architecture. -/
def FiniteExceptionalWithConstant : Prop :=
  ∀ α : ℝ,
    IsAlgebraic ℚ α →
    Irrational α →
    ∀ ε C : ℝ,
      0 < ε →
      0 < C →
      {r : ℚ |
        |α - (r : ℝ)| < C / denominator r ^ ((2 : ℝ) + ε)}.Finite

/-- Constant-one specialization, checked against the exact canonical root. -/
theorem root_of_finiteExceptionalWithConstant
    (h : FiniteExceptionalWithConstant) : ThueSiegelRoth := by
  intro α hα hirr ε hε
  simpa [IsExceptional] using h α hα hirr ε 1 hε zero_lt_one

#print axioms root_of_finiteExceptionalWithConstant

end Stage1Instances.THMM0398
