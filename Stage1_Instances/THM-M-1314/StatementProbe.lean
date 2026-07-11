import Mathlib.Analysis.SpecialFunctions.Trigonometric.Basic

/-!
This file checks only the real-valued expression commonly occurring in one
normalization of a Penrose inequality. The repository source does not select
that normalization or an exact geometric theorem, so this is not the
canonical target and earns no statement or proof credit.
-/

namespace Stage1.THM_M_1314.StatementProbe

noncomputable section

def candidateMassScale (area : ℝ) : ℝ :=
  Real.sqrt (area / (16 * Real.pi))

theorem candidateMassScale_nonneg (area : ℝ) :
    0 ≤ candidateMassScale area :=
  Real.sqrt_nonneg _

end

end Stage1.THM_M_1314.StatementProbe
