import Mathlib

/-
Frozen provider provenance; the numeric module path is deliberately not a
canonical Lake import.  The claim-owned proposition below is elaborated using
Mathlib alone.
import FormalConjectures.ErdosProblems.1109
Erdos1109.erdos_1109.variants.konyagin_lower
-/

open Filter Asymptotics
open scoped Pointwise

namespace AwesomeTheorems.Stage5.S5_CLM_00003700

/--
The claim-owned spelling of the frozen Konyagin lower-bound proposition.
The source function `Erdos1109.f` is expanded from its pinned definition so
that no local alias can capture or reinterpret the provider symbol.
-/
theorem statement_bidirectional_identity :
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
  rfl

end AwesomeTheorems.Stage5.S5_CLM_00003700
