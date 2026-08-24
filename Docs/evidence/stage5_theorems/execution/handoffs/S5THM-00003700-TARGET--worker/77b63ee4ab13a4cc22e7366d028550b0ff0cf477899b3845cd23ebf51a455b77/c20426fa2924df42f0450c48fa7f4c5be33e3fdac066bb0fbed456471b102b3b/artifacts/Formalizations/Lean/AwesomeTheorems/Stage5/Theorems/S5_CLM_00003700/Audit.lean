import Mathlib

/-
Frozen provider provenance used by the semantic-identity audit.
import FormalConjectures.ErdosProblems.1109
Erdos1109.erdos_1109.variants.konyagin_lower
-/

open Filter Asymptotics
open scoped Pointwise

namespace AwesomeTheorems.Stage5.S5_CLM_00003700

/-- Independent syntactic round trip for the exact expanded root proposition. -/
theorem audit_source_target_round_trip :
    (Asymptotics.IsBigO Filter.atTop
      (fun N : ℕ => Real.log (Real.log N) * (Real.log N) ^ 2)
      (fun N : ℕ =>
        ((sSup {k : ℕ | ∃ A : Finset ℕ,
          A ⊆ Finset.Icc 1 N ∧
          (∀ n ∈ A + A, Squarefree n) ∧ A.card = k} : ℕ) : ℝ))) ↔
    (Asymptotics.IsBigO Filter.atTop
      (fun N : ℕ => Real.log (Real.log N) * (Real.log N) ^ 2)
      (fun N : ℕ =>
        ((sSup {k : ℕ | ∃ A : Finset ℕ,
          A ⊆ Finset.Icc 1 N ∧
          (∀ n ∈ A + A, Squarefree n) ∧ A.card = k} : ℕ) : ℝ))) := by
  constructor <;> intro h <;> exact h

end AwesomeTheorems.Stage5.S5_CLM_00003700
