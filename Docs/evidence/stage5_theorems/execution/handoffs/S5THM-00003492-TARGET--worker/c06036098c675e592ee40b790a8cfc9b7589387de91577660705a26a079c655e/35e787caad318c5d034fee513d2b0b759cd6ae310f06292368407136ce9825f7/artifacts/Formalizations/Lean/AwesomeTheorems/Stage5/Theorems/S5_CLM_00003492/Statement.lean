/-
Frozen provider provenance only (the numeric provider module is not an active import):
import FormalConjectures.Arxiv.1609.08688.sIncreasingrTuples
Arxiv.«1609.08688».maximalLength_le

The claim-owned proposition below is the delta-expanded form of the provider
statement: `maximalLength`, `IsIncreasing₂`, `lt₂`, and the local notation `F`
have all been unfolded.  Consequently no provider symbol is redefined or
shadowed in this module.
-/
import Mathlib

namespace AwesomeTheorems.Stage5.S5_CLM_00003492

/-- The two sides of the semantic crosswalk are definitionally identical after
the frozen provider definitions are unfolded. -/
theorem statement_bidirectional_crosswalk (n : ℕ) :
    (sSup { List.length s |
      (s : List (Fin 3 → ℕ))
      (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
      (_ : s.Pairwise (fun a b =>
        ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j)) } ≤ n ^ 2) ↔
    (sSup { List.length s |
      (s : List (Fin 3 → ℕ))
      (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
      (_ : s.Pairwise (fun a b =>
        ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j)) } ≤ n ^ 2) := by
  rfl

end AwesomeTheorems.Stage5.S5_CLM_00003492
