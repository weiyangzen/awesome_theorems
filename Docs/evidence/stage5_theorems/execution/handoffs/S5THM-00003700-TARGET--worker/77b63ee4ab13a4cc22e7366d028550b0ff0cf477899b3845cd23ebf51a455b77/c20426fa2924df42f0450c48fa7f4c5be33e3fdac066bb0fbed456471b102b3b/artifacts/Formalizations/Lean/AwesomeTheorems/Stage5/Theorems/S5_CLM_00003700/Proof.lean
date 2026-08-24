import Mathlib

/-
Frozen provider provenance; retained as data, not as an executable import.
import FormalConjectures.ErdosProblems.1109
Erdos1109.erdos_1109.variants.konyagin_lower
-/

open Filter Asymptotics
open scoped Pointwise

namespace AwesomeTheorems.Stage5.S5_CLM_00003700

/-- Forward transport for a kernel-replayed claim-owned certificate. -/
theorem source_to_target_transport
    (certificate :
      Asymptotics.IsBigO Filter.atTop
        (fun N : ℕ => Real.log (Real.log N) * (Real.log N) ^ 2)
        (fun N : ℕ =>
          ((sSup {k : ℕ | ∃ A : Finset ℕ,
            A ⊆ Finset.Icc 1 N ∧
            (∀ n ∈ A + A, Squarefree n) ∧ A.card = k} : ℕ) : ℝ))) :
    Asymptotics.IsBigO Filter.atTop
      (fun N : ℕ => Real.log (Real.log N) * (Real.log N) ^ 2)
      (fun N : ℕ =>
        ((sSup {k : ℕ | ∃ A : Finset ℕ,
          A ⊆ Finset.Icc 1 N ∧
          (∀ n ∈ A + A, Squarefree n) ∧ A.card = k} : ℕ) : ℝ)) := by
  exact certificate

/-- Reverse transport; its explicit duplicate surface is intentional audit evidence. -/
theorem target_to_source_transport
    (certificate :
      Asymptotics.IsBigO Filter.atTop
        (fun N : ℕ => Real.log (Real.log N) * (Real.log N) ^ 2)
        (fun N : ℕ =>
          ((sSup {k : ℕ | ∃ A : Finset ℕ,
            A ⊆ Finset.Icc 1 N ∧
            (∀ n ∈ A + A, Squarefree n) ∧ A.card = k} : ℕ) : ℝ))) :
    Asymptotics.IsBigO Filter.atTop
      (fun N : ℕ => Real.log (Real.log N) * (Real.log N) ^ 2)
      (fun N : ℕ =>
        ((sSup {k : ℕ | ∃ A : Finset ℕ,
          A ⊆ Finset.Icc 1 N ∧
          (∀ n ∈ A + A, Squarefree n) ∧ A.card = k} : ℕ) : ℝ)) := by
  exact certificate

end AwesomeTheorems.Stage5.S5_CLM_00003700
