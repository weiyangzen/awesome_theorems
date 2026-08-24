import Mathlib

/-!
Statement transport for `S5-CLM-00003493`.

The frozen logical module is recorded verbatim for the semantic audit:
import FormalConjectures.Arxiv.1609.08688.sIncreasingrTuples
Pinned declaration: Arxiv.«1609.08688».maximalLength_le_isBigO

The provider's `Real.iteratedLog` is unfolded below to its pinned body.  Thus
the proposition is definitionally the frozen source proposition while the
proof does not consume the provider theorem, whose body contains `sorryAx`.
-/

namespace AwesomeTheorems.Stage5.Theorems.S5_CLM_00003493

open Filter Asymptotics

/-- Source-to-target transport after unfolding the pinned iterated-log definition. -/
theorem maximalLength_le_isBigO_statement
    (h : ∃ Ω : ℕ → ℝ,
      (fun (n : ℕ) =>
        ((sInf {k : ℕ | Real.log^[k] (n : ℝ) ≤ 1} : ℕ) : ℝ)) =O[atTop] Ω ∧
        ∀ n,
          ((sSup {List.length s | (s : List (Fin 3 → ℕ))
            (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
            (_ : s.Pairwise fun a b =>
              ∃ i j : Fin 3, i ≠ j ∧ a i < b i ∧ a j < b j)} : ℕ) : ℝ) ≤
            n ^ 2 / Real.exp (Ω n)) :
    ∃ Ω : ℕ → ℝ,
      (fun (n : ℕ) =>
        ((sInf {k : ℕ | Real.log^[k] (n : ℝ) ≤ 1} : ℕ) : ℝ)) =O[atTop] Ω ∧
        ∀ n,
          ((sSup {List.length s | (s : List (Fin 3 → ℕ))
            (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
            (_ : s.Pairwise fun a b =>
              ∃ i j : Fin 3, i ≠ j ∧ a i < b i ∧ a j < b j)} : ℕ) : ℝ) ≤
            n ^ 2 / Real.exp (Ω n) := by
  exact h

/-- Target-to-source transport is the reverse identity at the unfolded type. -/
theorem maximalLength_le_isBigO_statement_to_source
    (h : ∃ Ω : ℕ → ℝ,
      (fun (n : ℕ) =>
        ((sInf {k : ℕ | Real.log^[k] (n : ℝ) ≤ 1} : ℕ) : ℝ)) =O[atTop] Ω ∧
        ∀ n,
          ((sSup {List.length s | (s : List (Fin 3 → ℕ))
            (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
            (_ : s.Pairwise fun a b =>
              ∃ i j : Fin 3, i ≠ j ∧ a i < b i ∧ a j < b j)} : ℕ) : ℝ) ≤
            n ^ 2 / Real.exp (Ω n)) :
    ∃ Ω : ℕ → ℝ,
      (fun (n : ℕ) =>
        ((sInf {k : ℕ | Real.log^[k] (n : ℝ) ≤ 1} : ℕ) : ℝ)) =O[atTop] Ω ∧
        ∀ n,
          ((sSup {List.length s | (s : List (Fin 3 → ℕ))
            (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
            (_ : s.Pairwise fun a b =>
              ∃ i j : Fin 3, i ≠ j ∧ a i < b i ∧ a j < b j)} : ℕ) : ℝ) ≤
            n ^ 2 / Real.exp (Ω n) := by
  exact h

end AwesomeTheorems.Stage5.Theorems.S5_CLM_00003493
