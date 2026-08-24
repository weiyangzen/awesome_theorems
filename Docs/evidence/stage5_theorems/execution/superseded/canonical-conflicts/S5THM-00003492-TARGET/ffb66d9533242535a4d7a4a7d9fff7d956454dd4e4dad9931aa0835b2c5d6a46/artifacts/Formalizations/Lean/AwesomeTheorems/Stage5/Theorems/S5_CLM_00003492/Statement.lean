import Mathlib

namespace Arxiv.«1609.08688»

def lt₂ {α : Type*} [LT α] (a b : Fin 3 → α) : Prop :=
  ∃ i j : Fin 3, i ≠ j ∧ a i < b i ∧ a j < b j

def IsIncreasing₂ {α : Type*} [LT α] (s : List (Fin 3 → α)) : Prop := s.Pairwise lt₂

theorem not_lt₂ {α : Type*} [LinearOrder α] {a b : Fin 3 → α} :
    ¬lt₂ a b ↔ ∀ i j, i ≠ j → a i < b i → b j ≤ a j := by simp [lt₂]

theorem not_lt₂_of_exists {α : Type*} [LinearOrder α] {a b : Fin 3 → α}
    (i j : Fin 3) (hij : i ≠ j) (hi : b i ≤ a i) (hj : b j ≤ a j) :
    ¬lt₂ a b := by
  refine not_lt₂.2 fun k l hkl h => ?_
  have hki : k ≠ i := fun hk => not_lt.2 hi (hk ▸ h)
  have hkj : k ≠ j := fun hk => not_lt.2 hj (hk ▸ h)
  have hlast : l = i ∨ l = j := by omega
  rcases hlast with rfl | rfl
  · exact hi
  · exact hj

theorem not_lt₂_self {α : Type*} [LinearOrder α] (a : Fin 3 → α) : ¬lt₂ a a := by
  simp [lt₂]

theorem isIncreasing₂_nil {α : Type*} [LT α] : IsIncreasing₂ (α := α) [] := by
  simp [IsIncreasing₂]

theorem isIncreasing₂_const_length {α : Type*} [LinearOrder α] {val : α}
    {s : List (Fin 3 → α)} (h : IsIncreasing₂ s)
    (h_const : ∀ a ∈ s, ∀ j, a j = val) : s.length < 2 := by
  by_contra!
  have h₀ : s[0] = fun _ => val := funext fun i => by simp [h_const s[0] (by simp)]
  have h₁ : s[1] = fun _ => val := funext fun i => by simp [h_const s[1] (by simp)]
  have hp := List.pairwise_iff_getElem.1 h 0 1 (by linarith) (by linarith) zero_lt_one
  rcases hp with ⟨i, j, hij, hi, hj⟩
  have hi0 : s[0] i = val := h_const s[0] (by simp) i
  have hi1 : s[1] i = val := h_const s[1] (by simp) i
  have hval : val < val := by
    calc
      val = s[0] i := hi0.symm
      _ < s[1] i := hi
      _ = val := hi1
  exact (lt_irrefl val hval)

noncomputable def maximalLength (n : ℕ) : ℕ :=
  sSup { List.length s | (s : List (Fin 3 → ℕ))
    (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
    (_ : IsIncreasing₂ s) }

theorem maximalLength_zero : maximalLength 0 = 0 := by
  have h (x : ℕ) (s : List (Fin 3 → ℕ)) :
      IsIncreasing₂ s ∧ (∀ a, a ∉ s) ∧ s.length = x ↔ s = [] ∧ x = 0 := by
    constructor
    · rintro ⟨_, hs, rfl⟩
      simp only [List.length_eq_zero_iff, and_self]
      refine List.eq_nil_of_subset_nil (fun ai hai => ?_)
      exact (hs ai hai).elim
    · rintro ⟨rfl, rfl⟩
      exact ⟨isIncreasing₂_nil, by simp⟩
  simp [maximalLength, fun x => exists_congr (h x)]

theorem maximalLength_one : maximalLength 1 = 1 := by
  classical
  have h (x : ℕ) (s : List (Fin 3 → ℕ)) :
      IsIncreasing₂ s ∧ (∀ a ∈ s, ∀ i, a i = 1) ∧ s.length = x ↔
        s = [fun _ => 1] ∧ x = 1 ∨ s = [] ∧ x = 0 := by
    constructor
    · rintro ⟨hs, hv, hx⟩
      have hlen : x < 2 := by simpa [hx] using isIncreasing₂_const_length hs hv
      rcases x with _ | _ | x
      · right; simp [List.length_eq_zero_iff.1 hx]
      · left
        obtain ⟨a, rfl⟩ := List.length_eq_one_iff.1 hx
        refine ⟨?_, rfl⟩
        congr 1
        funext i
        exact hv a (by simp) i
      · omega
    · intro hcase
      rcases hcase with hcase | hcase <;> rcases hcase with ⟨rfl, rfl⟩ <;> simp [IsIncreasing₂]
  simp [maximalLength, fun x => exists_congr (h x)]
  rw [Nat.sSup_def ⟨1, by aesop⟩, Nat.find_eq_iff]
  refine ⟨by aesop, fun n hn => ?_⟩
  simp [Nat.lt_one_iff.1 hn]
  exact ⟨1, ⟨[fun _ => 1], by simp⟩, one_ne_zero⟩

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
  obtain ⟨i, _, j, _, hij, hfij⟩ :=
    Finset.exists_ne_map_eq_of_card_lt_of_maps_to ht_card hf
  exact ⟨i, j, hij, congrArg Prod.fst hfij, congrArg Prod.snd hfij⟩

theorem maximalLength_le (n : ℕ) : maximalLength n ≤ n ^ 2 := by
  by_cases hn : 2 ≤ n
  · rw [maximalLength]
    refine csSup_le ?_ ?_
    · exact ⟨0, ⟨[], by simp, isIncreasing₂_nil, rfl⟩⟩
    · intro _ hm
      rcases hm with ⟨s, hs_range, hs_inc, rfl⟩
      by_contra hle
      have hs_length : n ^ 2 < s.length := Nat.lt_of_not_ge hle
      obtain ⟨i, j, hij, h0, h1⟩ := exists_pair_of_mem_Icc hn hs_range hs_length
      have hp : s.Pairwise lt₂ := hs_inc
      rcases lt_or_gt_of_ne hij with hij | hji
      · exact (not_lt₂_of_exists 0 1 zero_ne_one h0.ge h1.ge)
          (List.pairwise_iff_get.1 hp i j hij)
      · exact (not_lt₂_of_exists 0 1 zero_ne_one h0.le h1.le)
          (List.pairwise_iff_get.1 hp j i hji)
  · cases n with
    | zero => simpa using maximalLength_zero
    | succ n =>
      cases n with
      | zero => simpa [maximalLength_one]
      | succ n => exact (hn (Nat.succ_le_succ (Nat.succ_le_succ (Nat.zero_le _)))).elim

end Arxiv.«1609.08688»
