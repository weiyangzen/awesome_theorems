import FormalConjectures.Arxiv.«1609.08688».sIncreasingrTuples

#check type_of% Arxiv.«1609.08688».maximalLength_le

namespace AwesomeTheorems.Stage5.S5_CLM_00003492

/-- Membership in the provider's binder-style set is exactly the explicit
witness presentation used by the readability crosswalk. -/
theorem audit_source_set_membership_iff (n x : ℕ) :
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

/-- Bidirectional surface normalization, independently available to this
provider-native audit file. -/
theorem audit_statement_transport (n : ℕ) :
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
    exact audit_source_set_membership_iff n x
  rw [hset]

/-- Forward half of the explicit bidirectional surface transport. -/
theorem source_to_target_theorem (n : ℕ) :
    (sSup { List.length s | (s : List (Fin 3 → ℕ))
      (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
      (_ : s.Pairwise (fun a b =>
        ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j)) } ≤ n ^ 2) →
    (sSup { x : ℕ | ∃ s : List (Fin 3 → ℕ),
      (∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n) ∧
      s.Pairwise (fun a b =>
        ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j) ∧
      s.length = x } ≤ n ^ 2) :=
  (audit_statement_transport n).mp

/-- Reverse half of the explicit bidirectional surface transport. -/
theorem target_to_source_theorem (n : ℕ) :
    (sSup { x : ℕ | ∃ s : List (Fin 3 → ℕ),
      (∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n) ∧
      s.Pairwise (fun a b =>
        ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j) ∧
      s.length = x } ≤ n ^ 2) →
    (sSup { List.length s | (s : List (Fin 3 → ℕ))
      (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
      (_ : s.Pairwise (fun a b =>
        ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j)) } ≤ n ^ 2) :=
  (audit_statement_transport n).mpr

/-- More than `n²` positions in the coordinate box contain a collision in the
first two coordinates. -/
lemma audit_exists_pair_of_mem_Icc
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

/-- A collision in coordinates zero and one rules out strict growth in two
different coordinates. -/
lemma audit_not_pairwise_step_of_first_two_ge
    {a b : Fin 3 → ℕ} (h0 : b 0 ≤ a 0) (h1 : b 1 ≤ a 1) :
    ¬ ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j := by
  rintro ⟨i, j, hij, hi, hj⟩
  have hi0 : i ≠ 0 := by
    intro h
    subst i
    exact (not_lt_of_ge h0) hi
  have hi1 : i ≠ 1 := by
    intro h
    subst i
    exact (not_lt_of_ge h1) hi
  have hj01 : j = 0 ∨ j = 1 := by omega
  rcases hj01 with rfl | rfl
  · exact (not_lt_of_ge h0) hj
  · exact (not_lt_of_ge h1) hj

/-- Terminal claim-owned machine root. This repeats the independent proof in
the audit compilation unit and does not reference the provider proof body. -/
theorem maximalLength_le_audit (n : ℕ) :
    sSup { List.length s | (s : List (Fin 3 → ℕ))
      (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
      (_ : s.Pairwise (fun a b =>
        ∃ (i j : Fin 3), i ≠ j ∧ a i < b i ∧ a j < b j)) } ≤ n ^ 2 :=
  by
    refine csSup_le ?_ ?_
    · exact ⟨0, ⟨[], by simp, by simp, rfl⟩⟩
    · intro _ hm
      rcases hm with ⟨s, hsRange, hsIncreasing, rfl⟩
      by_contra hle
      have hsLength : n ^ 2 < s.length := Nat.lt_of_not_ge hle
      obtain ⟨i, j, hij, h0, h1⟩ :=
        audit_exists_pair_of_mem_Icc hsRange hsLength
      rcases lt_or_gt_of_ne hij with hij | hji
      · exact (audit_not_pairwise_step_of_first_two_ge h0.ge h1.ge)
          (List.pairwise_iff_get.1 hsIncreasing i j hij)
      · exact (audit_not_pairwise_step_of_first_two_ge h0.le h1.le)
          (List.pairwise_iff_get.1 hsIncreasing j i hji)

example : type_of% Arxiv.«1609.08688».maximalLength_le :=
  AwesomeTheorems.Stage5.S5_CLM_00003492.maximalLength_le_audit

#check type_of% AwesomeTheorems.Stage5.S5_CLM_00003492.maximalLength_le_audit
#print axioms AwesomeTheorems.Stage5.S5_CLM_00003492.maximalLength_le_audit

end AwesomeTheorems.Stage5.S5_CLM_00003492
