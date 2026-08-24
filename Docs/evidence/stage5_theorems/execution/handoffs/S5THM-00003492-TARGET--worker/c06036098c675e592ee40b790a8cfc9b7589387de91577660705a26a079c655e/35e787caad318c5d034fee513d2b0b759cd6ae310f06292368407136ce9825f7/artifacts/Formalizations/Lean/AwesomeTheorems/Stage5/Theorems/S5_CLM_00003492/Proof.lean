/-
Frozen provider provenance only (the numeric provider module is not an active import):
import FormalConjectures.Arxiv.1609.08688.sIncreasingrTuples
Arxiv.«1609.08688».maximalLength_le

This file proves the delta-expanded, claim-owned proposition using Mathlib
alone.  It neither imports the provider proof nor declares a local replacement
for any provider definition.
-/
import Mathlib

namespace AwesomeTheorems.Stage5.S5_CLM_00003492

/-- If a list is longer than the `n²` possible first-coordinate pairs, two
positions have equal coordinates zero and one. -/
lemma proof_exists_equal_first_two
    {s : List (Fin 3 → ℕ)} {n : ℕ}
    (hsRange : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
    (hsLength : s.length > n ^ 2) :
    ∃ (i j : Fin s.length),
      i ≠ j ∧ s[i] 0 = s[j] 0 ∧ s[i] 1 = s[j] 1 := by
  classical
  let f : Fin s.length → ℕ × ℕ := fun k => (s[k] 0, s[k] 1)
  let t : Finset (ℕ × ℕ) := Finset.Icc 1 n ×ˢ Finset.Icc 1 n
  have htCard : t.card < (Finset.univ : Finset (Fin s.length)).card := by
    simp only [t, Finset.card_univ, Fintype.card_fin, Finset.card_product,
      Nat.card_Icc, Nat.add_sub_cancel, ← sq]
    exact hsLength
  have hf : ∀ k ∈ (Finset.univ : Finset (Fin s.length)), f k ∈ t := by
    intro k _
    have hmem : s[k] ∈ s := List.getElem_mem k.isLt
    have h0 := hsRange _ hmem ⟨0, rfl⟩
    have h1 := hsRange _ hmem ⟨1, rfl⟩
    rw [Set.mem_Icc] at h0 h1
    simp only [t, f, Finset.mem_product, Finset.mem_Icc]
    exact ⟨h0, h1⟩
  obtain ⟨i, _, j, _, hij, hfij⟩ :=
    Finset.exists_ne_map_eq_of_card_lt_of_maps_to htCard hf
  exact ⟨i, j, hij, congrArg Prod.fst hfij, congrArg Prod.snd hfij⟩

/-- Equal first two coordinates rule out being strictly increasing in two of
the three coordinates. -/
lemma proof_not_two_increases_of_equal_first_two
    {a b : Fin 3 → ℕ} (h0 : a 0 = b 0) (h1 : a 1 = b 1) :
    ¬ ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j := by
  rintro ⟨i, j, hij, hi, hj⟩
  fin_cases i <;> fin_cases j <;> simp_all

/-- Claim-owned proof of the fully expanded form of
`Arxiv.«1609.08688».maximalLength_le`. -/
theorem proof_maximalLength_le (n : ℕ) :
    sSup { List.length s |
      (s : List (Fin 3 → ℕ))
      (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
      (_ : s.Pairwise (fun a b =>
        ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j)) } ≤ n ^ 2 := by
  refine csSup_le ?_ ?_
  · exact ⟨0, ⟨[], by simp, by simp, rfl⟩⟩
  · intro _ hm
    rcases hm with ⟨s, hsRange, hsIncreasing, rfl⟩
    by_contra hle
    have hsLength : n ^ 2 < s.length := Nat.lt_of_not_ge hle
    obtain ⟨i, j, hij, h0, h1⟩ :=
      proof_exists_equal_first_two hsRange hsLength
    rcases lt_or_gt_of_ne hij with hij | hji
    · exact (proof_not_two_increases_of_equal_first_two h0 h1)
        (List.pairwise_iff_get.1 hsIncreasing i j hij)
    · exact (proof_not_two_increases_of_equal_first_two h0.symm h1.symm)
        (List.pairwise_iff_get.1 hsIncreasing j i hji)

end AwesomeTheorems.Stage5.S5_CLM_00003492
