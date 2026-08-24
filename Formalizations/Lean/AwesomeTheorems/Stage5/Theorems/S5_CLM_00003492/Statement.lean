import FormalConjectures.Arxiv.«1609.08688».sIncreasingrTuples

#check Arxiv.«1609.08688».maximalLength_le

namespace AwesomeTheorems.Stage5.S5_CLM_00003492

/-- Membership in the provider's binder-style set, with `maximalLength`,
`IsIncreasing₂`, and `lt₂` unfolded, is exactly the explicit witness form. -/
theorem source_set_membership_iff (n x : ℕ) :
    x ∈ { List.length s | (s : List (Fin 3 → ℕ))
      (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
      (_ : s.Pairwise (fun a b =>
        ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j)) } ↔
      ∃ s : List (Fin 3 → ℕ),
        (∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n) ∧
        s.Pairwise (fun a b =>
          ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j) ∧
        s.length = x := by
  constructor
  · rintro ⟨s, hsRange, hsIncreasing, rfl⟩
    exact ⟨s, hsRange, hsIncreasing, rfl⟩
  · rintro ⟨s, hsRange, hsIncreasing, rfl⟩
    exact ⟨s, hsRange, hsIncreasing, rfl⟩

/-- Bidirectional surface normalization for the exact frozen proposition. -/
theorem maximalLength_le_statement (n : ℕ) :
    (sSup { List.length s | (s : List (Fin 3 → ℕ))
      (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
      (_ : s.Pairwise (fun a b =>
        ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j)) } ≤ n ^ 2) ↔
    (sSup { x : ℕ | ∃ s : List (Fin 3 → ℕ),
      (∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n) ∧
      s.Pairwise (fun a b =>
        ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j) ∧
      s.length = x } ≤ n ^ 2) := by
  have hset :
      { List.length s | (s : List (Fin 3 → ℕ))
        (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
        (_ : s.Pairwise (fun a b =>
          ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j)) } =
      { x : ℕ | ∃ s : List (Fin 3 → ℕ),
        (∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n) ∧
        s.Pairwise (fun a b =>
          ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j) ∧
        s.length = x } := by
    ext x
    exact source_set_membership_iff n x
  rw [hset]

end AwesomeTheorems.Stage5.S5_CLM_00003492
