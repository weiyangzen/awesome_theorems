import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.NumberTheory.Real.Irrational

/-!
# Exact statement for THM-M-0398

This module freezes only the canonical Thue-Siegel-Roth target. It does not
provide or assume a proof of that target.
-/

namespace Stage1Instances.THMM0398

/-- The normalized denominator of a rational, viewed as a positive real. -/
def denominator (r : ℚ) : ℝ :=
  r.den

/-- A rational approximation that beats exponent `2 + ε`. -/
def IsExceptional (α ε : ℝ) (r : ℚ) : Prop :=
  |α - (r : ℝ)| < 1 / denominator r ^ ((2 : ℝ) + ε)

/--
The exact rational-approximation form of the Thue-Siegel-Roth theorem:
for an irrational algebraic real and every positive `ε`, only finitely many
rationals beat denominator exponent `2 + ε`.
-/
def ThueSiegelRoth : Prop :=
  ∀ α : ℝ,
    IsAlgebraic ℚ α →
    Irrational α →
    ∀ ε : ℝ,
      0 < ε →
      {r : ℚ | IsExceptional α ε r}.Finite

/-- Checked expansion of the canonical target, fixing binder order and scope. -/
theorem thueSiegelRoth_iff :
    ThueSiegelRoth ↔
      ∀ α : ℝ,
        IsAlgebraic ℚ α →
        Irrational α →
        ∀ ε : ℝ,
          0 < ε →
          {r : ℚ |
            |α - (r : ℝ)| < 1 / (r.den : ℝ) ^ ((2 : ℝ) + ε)}.Finite := by
  rfl

/-- The normalized rational denominator is strictly positive. -/
theorem denominator_pos (r : ℚ) : 0 < denominator r := by
  unfold denominator
  exact_mod_cast r.pos

end Stage1Instances.THMM0398
