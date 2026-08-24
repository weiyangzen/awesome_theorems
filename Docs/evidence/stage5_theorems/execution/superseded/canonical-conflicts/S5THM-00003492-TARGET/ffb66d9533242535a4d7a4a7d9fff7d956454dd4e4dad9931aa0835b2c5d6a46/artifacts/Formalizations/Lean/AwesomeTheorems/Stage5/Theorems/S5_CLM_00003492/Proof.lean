import Mathlib

namespace Arxiv.«1609.08688»

def lt₂ {α : Type*} [LT α] (a b : Fin 3 → α) : Prop :=
  ∃ i j : Fin 3, i ≠ j ∧ a i < b i ∧ a j < b j

def IsIncreasing₂ {α : Type*} [LT α] (s : List (Fin 3 → α)) : Prop := s.Pairwise lt₂

noncomputable def maximalLength (n : ℕ) : ℕ :=
  sSup { List.length s | (s : List (Fin 3 → ℕ))
    (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n) (_ : IsIncreasing₂ s) }

theorem not_lt₂_of_exists {α : Type*} [LinearOrder α] {a b : Fin 3 → α}
    (i j : Fin 3) (hij : i ≠ j) (hi : b i ≤ a i) (hj : b j ≤ a j) : ¬lt₂ a b := by
  refine fun h => ?_
  rcases h with ⟨k, l, hkl, hk, hl⟩
  have hki : k ≠ i := fun he => (not_lt_of_ge hi) (he ▸ hk)
  have hkj : k ≠ j := fun he => (not_lt_of_ge hj) (he ▸ hk)
  have hli : l ≠ i := fun he => (not_lt_of_ge hi) (he ▸ hl)
  have hlj : l ≠ j := fun he => (not_lt_of_ge hj) (he ▸ hl)
  fin_cases k <;> fin_cases l <;> simp_all

theorem isIncreasing₂_nil {α : Type*} [LT α] : IsIncreasing₂ (α := α) [] := by simp [IsIncreasing₂]

theorem maximalLength_zero : maximalLength 0 = 0 := by
  simp [maximalLength]

theorem maximalLength_one : maximalLength 1 = 1 := by
  classical
  simp [maximalLength]

lemma exists_pair_of_mem_Icc {s : List (Fin 3 → ℕ)} {n : ℕ} (_hn : 2 ≤ n)
    (hs₁ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n) (hs₂ : s.length > n ^ 2) :
    ∃ i j : Fin s.length, i ≠ j ∧ s[i] 0 = s[j] 0 ∧ s[i] 1 = s[j] 1 := by
  classical
  let f : Fin s.length → ℕ × ℕ := fun k => (s[k] 0, s[k] 1)
  let t : Finset (ℕ × ℕ) := Finset.Icc 1 n ×ˢ Finset.Icc 1 n
  have ht_card : t.card < (Finset.univ : Finset (Fin s.length)).card := by
    simp only [t, Finset.card_univ, Fintype.card_fin, Finset.card_product,
      Nat.card_Icc, Nat.add_sub_cancel, ← sq]
    exact hs₂
  have hf : ∀ k ∈ (Finset.univ : Finset (Fin s.length)), f k ∈ t := by
    intro k _
    have hmem : s[k] ∈ s := List.getElem_mem k.isLt
    have h0 := hs₁ _ hmem ⟨0, rfl⟩
    have h1 := hs₁ _ hmem ⟨1, rfl⟩
    rw [Set.mem_Icc] at h0 h1
    simp only [t, f, Finset.mem_product, Finset.mem_Icc]
    exact ⟨h0, h1⟩
  obtain ⟨i, _, j, _, hij, hfij⟩ := Finset.exists_ne_map_eq_of_card_lt_of_maps_to ht_card hf
  exact ⟨i, j, hij, congrArg Prod.fst hfij, congrArg Prod.snd hfij⟩

theorem maximalLength_le_proof (n : ℕ) : maximalLength n ≤ n ^ 2 := by
  by_cases hn : 2 ≤ n
  · rw [maximalLength]
    refine csSup_le ?_ ?_
    · exact ⟨0, ⟨[], by simp, isIncreasing₂_nil, rfl⟩⟩
    · intro _ hm
      rcases hm with ⟨s, hs_range, hs_inc, rfl⟩
      by_contra hle
      have hs_length : n ^ 2 < s.length := Nat.lt_of_not_ge hle
      obtain ⟨i, j, hij, h0, h1⟩ := exists_pair_of_mem_Icc hn hs_range hs_length
      rcases lt_or_gt_of_ne hij with hij | hji
      · exact (not_lt₂_of_exists 0 1 zero_ne_one h0.ge h1.ge)
          (List.pairwise_iff_get.1 hs_inc i j hij)
      · exact (not_lt₂_of_exists 0 1 zero_ne_one h0.le h1.le)
          (List.pairwise_iff_get.1 hs_inc j i hji)
  · cases n with
    | zero => exact Nat.zero_le _
    | succ n =>
      cases n with
      | zero => exact le_of_eq maximalLength_one
      | succ n => exact (hn (by omega)).elim

end Arxiv.«1609.08688»
