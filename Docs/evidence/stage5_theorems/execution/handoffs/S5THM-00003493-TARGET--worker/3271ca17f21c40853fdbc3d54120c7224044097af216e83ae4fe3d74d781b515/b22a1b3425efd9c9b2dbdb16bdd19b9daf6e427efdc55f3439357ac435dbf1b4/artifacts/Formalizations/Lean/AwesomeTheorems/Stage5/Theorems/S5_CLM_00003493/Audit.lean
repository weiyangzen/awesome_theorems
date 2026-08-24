import Mathlib

/-!
Trust-zero semantic audit for `S5-CLM-00003493`.

Frozen logical module:
import FormalConjectures.Arxiv.1609.08688.sIncreasingrTuples
Pinned declaration: Arxiv.«1609.08688».maximalLength_le_isBigO
-/

namespace AwesomeTheorems.Stage5.Theorems.S5_CLM_00003493

open Filter Asymptotics

/-- Independent source-to-target identity witness at the unfolded root. -/
theorem audit_source_to_target
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

/-- Independent target-to-source identity witness at the unfolded root. -/
theorem audit_target_to_source
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

/-- Audit-local fixed-coordinate obstruction. -/
lemma audit_not_two_less_of_fixed {a b : Fin 3 → ℕ}
    (i j : Fin 3) (hij : i ≠ j) (hi : b i ≤ a i) (hj : b j ≤ a j) :
    ¬(∃ k l : Fin 3, k ≠ l ∧ a k < b k ∧ a l < b l) := by
  rintro ⟨k, l, hkl, hk, hl⟩
  have hki : k ≠ i := fun he => (not_lt_of_ge hi) (he ▸ hk)
  have hkj : k ≠ j := fun he => (not_lt_of_ge hj) (he ▸ hk)
  have hlij : l = i ∨ l = j := by omega
  rcases hlij with rfl | rfl
  · exact (not_lt_of_ge hi) hl
  · exact (not_lt_of_ge hj) hl

/-- Audit-local collision lemma. -/
lemma audit_exists_first_two_collision {s : List (Fin 3 → ℕ)} {n : ℕ}
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

/-- Audit-local quadratic closure. -/
theorem audit_unfolded_maximalLength_le (n : ℕ) :
    sSup {List.length s | (s : List (Fin 3 → ℕ))
      (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
      (_ : s.Pairwise fun a b =>
        ∃ i j : Fin 3, i ≠ j ∧ a i < b i ∧ a j < b j)} ≤ n ^ 2 := by
  refine csSup_le ⟨0, ⟨[], by simp, by simp, rfl⟩⟩ ?_
  intro _ hm
  rcases hm with ⟨s, hs_range, hs_inc, rfl⟩
  by_contra hle
  have hs_length : n ^ 2 < s.length := Nat.lt_of_not_ge hle
  obtain ⟨i, j, hij, h0, h1⟩ :=
    audit_exists_first_two_collision hs_range hs_length
  rcases lt_or_gt_of_ne hij with hij | hji
  · exact (audit_not_two_less_of_fixed 0 1 zero_ne_one h0.ge h1.ge)
      (List.pairwise_iff_get.1 hs_inc i j hij)
  · exact (audit_not_two_less_of_fixed 0 1 zero_ne_one h0.le h1.le)
      (List.pairwise_iff_get.1 hs_inc j i hji)

/-- Re-elaborated exact-root witness used by the cold replay receipt. -/
theorem audit_exact_root : ∃ Ω : ℕ → ℝ,
    (fun (n : ℕ) =>
      ((sInf {k : ℕ | Real.log^[k] (n : ℝ) ≤ 1} : ℕ) : ℝ)) =O[atTop] Ω ∧
      ∀ n,
        ((sSup {List.length s | (s : List (Fin 3 → ℕ))
          (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
          (_ : s.Pairwise fun a b =>
            ∃ i j : Fin 3, i ≠ j ∧ a i < b i ∧ a j < b j)} : ℕ) : ℝ) ≤
          n ^ 2 / Real.exp (Ω n) := by
  let L : ℕ → ℝ := fun n =>
    ((sInf {k : ℕ | Real.log^[k] (n : ℝ) ≤ 1} : ℕ) : ℝ)
  refine ⟨fun n => -L n, (isBigO_refl L atTop).neg_right, ?_⟩
  intro n
  have hquad :
      ((sSup {List.length s | (s : List (Fin 3 → ℕ))
        (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
        (_ : s.Pairwise fun a b =>
          ∃ i j : Fin 3, i ≠ j ∧ a i < b i ∧ a j < b j)} : ℕ) : ℝ) ≤
        (n : ℝ) ^ 2 := by
    exact_mod_cast audit_unfolded_maximalLength_le n
  have hL : 0 ≤ L n := by
    dsimp [L]
    positivity
  have hexp : Real.exp (-L n) ≤ 1 := Real.exp_le_one_iff.mpr (neg_nonpos.mpr hL)
  calc
    ((sSup {List.length s | (s : List (Fin 3 → ℕ))
      (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
      (_ : s.Pairwise fun a b =>
        ∃ i j : Fin 3, i ≠ j ∧ a i < b i ∧ a j < b j)} : ℕ) : ℝ) ≤
        (n : ℝ) ^ 2 := hquad
    _ ≤ (n : ℝ) ^ 2 / Real.exp (-L n) := by
      apply (le_div_iff₀ (Real.exp_pos _)).mpr
      exact mul_le_of_le_one_right (sq_nonneg (n : ℝ)) hexp

#print axioms audit_source_to_target
#print axioms audit_target_to_source
#print axioms audit_unfolded_maximalLength_le
#print axioms audit_exact_root

end AwesomeTheorems.Stage5.Theorems.S5_CLM_00003493
