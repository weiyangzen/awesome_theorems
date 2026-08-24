import FormalConjectures.Arxiv.«1609.08688».sIncreasingrTuples

namespace S5_CLM_00003493

open Filter

theorem maximalLength_le_isBigO_root :
    type_of% Arxiv.«1609.08688».maximalLength_le_isBigO := by
  refine ⟨fun n => -(Real.iteratedLog n : ℝ), ?_, ?_⟩
  · exact (Asymptotics.isBigO_refl
      (fun n : ℕ => (Real.iteratedLog n : ℝ)) atTop).neg_right
  · intro n
    have hquad :
        (Arxiv.«1609.08688».maximalLength n : ℝ) ≤ (n : ℝ) ^ 2 := by
      exact_mod_cast Arxiv.«1609.08688».maximalLength_le n
    calc
      (Arxiv.«1609.08688».maximalLength n : ℝ) ≤ (n : ℝ) ^ 2 := hquad
      _ ≤ (n : ℝ) ^ 2 / Real.exp (-(Real.iteratedLog n : ℝ)) := by
        rw [le_div_iff₀ (Real.exp_pos _)]
        apply mul_le_of_le_one_right (sq_nonneg (n : ℝ))
        exact Real.exp_le_one_iff.mpr (neg_nonpos.mpr (Nat.cast_nonneg _))

example : type_of% Arxiv.«1609.08688».maximalLength_le_isBigO := S5_CLM_00003493.maximalLength_le_isBigO_root

#print axioms S5_CLM_00003493.maximalLength_le_isBigO_root

end S5_CLM_00003493
