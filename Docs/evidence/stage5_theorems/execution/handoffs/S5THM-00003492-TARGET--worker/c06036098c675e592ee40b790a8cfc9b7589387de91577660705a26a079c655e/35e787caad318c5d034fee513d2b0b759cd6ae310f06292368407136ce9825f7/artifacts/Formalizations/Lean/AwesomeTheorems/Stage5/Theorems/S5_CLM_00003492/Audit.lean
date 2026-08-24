/-
Frozen provider provenance only (the numeric provider module is not an active import):
import FormalConjectures.Arxiv.1609.08688.sIncreasingrTuples
Arxiv.«1609.08688».maximalLength_le

The audit transports below deliberately expose both directions without an
alias, definition, notation, macro, coercion, instance, or provider proof body.
-/
import Mathlib

namespace AwesomeTheorems.Stage5.S5_CLM_00003492

/-- Delta-unfolded provider proposition transports to the claim-owned root. -/
theorem audit_source_to_target (n : ℕ)
    (h : sSup { List.length s |
      (s : List (Fin 3 → ℕ))
      (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
      (_ : s.Pairwise (fun a b =>
        ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j)) } ≤ n ^ 2) :
    sSup { List.length s |
      (s : List (Fin 3 → ℕ))
      (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
      (_ : s.Pairwise (fun a b =>
        ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j)) } ≤ n ^ 2 := by
  exact h

/-- The claim-owned root transports back to the delta-unfolded provider
proposition. -/
theorem audit_target_to_source (n : ℕ)
    (h : sSup { List.length s |
      (s : List (Fin 3 → ℕ))
      (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
      (_ : s.Pairwise (fun a b =>
        ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j)) } ≤ n ^ 2) :
    sSup { List.length s |
      (s : List (Fin 3 → ℕ))
      (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
      (_ : s.Pairwise (fun a b =>
        ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j)) } ≤ n ^ 2 := by
  exact h

end AwesomeTheorems.Stage5.S5_CLM_00003492
