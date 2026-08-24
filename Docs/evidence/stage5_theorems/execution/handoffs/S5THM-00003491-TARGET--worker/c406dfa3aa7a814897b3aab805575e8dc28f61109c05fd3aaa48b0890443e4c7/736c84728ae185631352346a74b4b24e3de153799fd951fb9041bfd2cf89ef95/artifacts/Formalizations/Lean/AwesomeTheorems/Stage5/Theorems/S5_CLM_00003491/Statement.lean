import Mathlib
import FormalConjectures.Arxiv.«1609.08688».sIncreasingrTuples

-- Keep the frozen provider declaration visible to the semantic audit without
-- using its sorry-backed proof as an oracle.
#check Arxiv.«1609.08688».maximalLength_ge_of_isSquare

-- Exact frozen module provenance: import FormalConjectures.Arxiv.1609.08688.sIncreasingrTuples

/-
Frozen provider provenance (a provenance string, not a canonical Lake import):
import FormalConjectures.Arxiv.1609.08688.sIncreasingrTuples
Arxiv.«1609.08688».maximalLength_ge_of_isSquare
revision 2270d31e8dd611521f979de6d86da364930b7669
-/

namespace AwesomeTheorems.Stage5.S5_CLM_00003491

private theorem block_lt
    {q a a' b b' : ℕ} (hb : b < q) (haa' : a < a') :
    a * q + b + 1 < a' * q + b' + 1 := by
  have h₁ : a * q + b + 1 ≤ (a + 1) * q := by
    rw [Nat.add_mul]
    omega
  have h₂ : (a + 1) * q ≤ a' * q :=
    Nat.mul_le_mul_right q (Nat.succ_le_of_lt haa')
  omega

private theorem block_le_square
    {q a b : ℕ} (ha : a < q) (hb : b < q) :
    a * q + b + 1 ≤ q ^ 2 := by
  have h₁ : a * q + b + 1 ≤ (a + 1) * q := by
    rw [Nat.add_mul]
    omega
  have h₂ : (a + 1) * q ≤ q * q :=
    Nat.mul_le_mul_right q (Nat.succ_le_of_lt ha)
  simpa [pow_two] using h₁.trans h₂

private theorem pairwise_append_of_cross
    {α : Type*} {R : α → α → Prop} {xs ys : List α}
    (hxs : xs.Pairwise R) (hys : ys.Pairwise R)
    (hcross : ∀ x ∈ xs, ∀ y ∈ ys, R x y) :
    (xs ++ ys).Pairwise R := by
  induction xs with
  | nil => simpa using hys
  | cons x xs ih =>
      simp only [List.pairwise_cons] at hxs ⊢
      constructor
      · intro z hz
        rcases List.mem_append.mp hz with hz | hz
        · exact hxs.1 z hz
        · exact hcross x (by simp) z hz
      · exact ih hxs.2 (fun z hz y hy => hcross z (by simp [hz]) y hy)

private theorem pairwise_range_flatMap
    {α : Type*} {R : α → α → Prop} (f : ℕ → List α) :
    ∀ q,
      (∀ i, i < q → (f i).Pairwise R) →
      (∀ i, i < q → ∀ j, j < q → i < j →
        ∀ x ∈ f i, ∀ y ∈ f j, R x y) →
      ((List.range q).flatMap f).Pairwise R := by
  intro q
  induction q with
  | zero => simp
  | succ q ih =>
      intro hwithin hcross
      rw [List.range_succ, List.flatMap_append]
      simp only [List.flatMap_singleton]
      apply pairwise_append_of_cross
      · exact ih
          (fun i hi => hwithin i (Nat.lt_trans hi (Nat.lt_succ_self q)))
          (fun i hi j hj hij => hcross i
            (Nat.lt_trans hi (Nat.lt_succ_self q)) j
            (Nat.lt_trans hj (Nat.lt_succ_self q)) hij)
      · exact hwithin q (Nat.lt_succ_self q)
      · intro x hx y hy
        rw [List.mem_flatMap] at hx
        obtain ⟨i, hi, hxi⟩ := hx
        have hiq : i < q := List.mem_range.mp hi
        exact hcross i (Nat.lt_trans hiq (Nat.lt_succ_self q)) q
          (Nat.lt_succ_self q) hiq x hxi y hy

private theorem exists_equal_first_two
    {s : List (Fin 3 → ℕ)} {n : ℕ} (_hn : 2 ≤ n)
    (hs₁ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
    (hs₂ : s.length > n ^ 2) :
    ∃ (i j : Fin s.length), i ≠ j ∧
      s[i] 0 = s[j] 0 ∧ s[i] 1 = s[j] 1 := by
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

private theorem length_lt_two_of_const
    {α : Type*} [LinearOrder α] {val : α} {s : List (Fin 3 → α)}
    (h : s.Pairwise fun a b =>
      ∃ i j : Fin 3, i ≠ j ∧ a i < b i ∧ a j < b j)
    (h_const : ∀ a ∈ s, ∀ j, a j = val) :
    s.length < 2 := by
  by_contra!
  have hp := List.pairwise_iff_getElem.1 h 0 1 (by omega) (by omega) zero_lt_one
  rcases hp with ⟨i, j, hij, hi, hj⟩
  have h0i : s[0] i = val := h_const s[0] (List.getElem_mem (by omega : 0 < s.length)) i
  have h1i : s[1] i = val := h_const s[1] (List.getElem_mem (by omega : 1 < s.length)) i
  rw [h0i, h1i] at hi
  exact (lt_irrefl val hi).elim

/--
Claim-owned expansion of the frozen provider proposition.  The provider's
`maximalLength`, `IsIncreasing₂`, and `lt₂` are delta-expanded in the type, so
no local alias or imported provider proof participates in this declaration.
-/
theorem statement {n : ℕ} (h : IsSquare n) :
    n.sqrt ^ 3 ≤
      sSup { List.length s |
        (s : List (Fin 3 → ℕ))
        (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
        (_ : s.Pairwise fun x y =>
          ∃ i j : Fin 3, i ≠ j ∧ x i < y i ∧ x j < y j) } := by
  let q := n.sqrt
  let R : (Fin 3 → ℕ) → (Fin 3 → ℕ) → Prop := fun x y =>
    ∃ i j : Fin 3, i ≠ j ∧ x i < y i ∧ x j < y j
  let lengths : Set ℕ :=
    { List.length s |
      (s : List (Fin 3 → ℕ))
      (_ : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n)
      (_ : s.Pairwise R) }
  let s : List (Fin 3 → ℕ) :=
    (List.range q).flatMap fun a =>
      (List.range q).flatMap fun b =>
        (List.range q).flatMap fun c =>
          [![a * q + b + 1, a * q + c + 1, b * q + c + 1]]
  have hq_square : q ^ 2 = n := by
    dsimp only [q]
    apply (Nat.exists_mul_self' n).mp
    rcases h with ⟨m, hm⟩
    exact ⟨m, by simpa [pow_two] using hm.symm⟩
  have hs_length : s.length = q ^ 3 := by
    simp [s, List.length_flatMap, pow_succ, Nat.mul_assoc]
  have hs_range : ∀ a ∈ s, Set.range a ⊆ Set.Icc 1 n := by
    intro x hx
    simp only [s, List.mem_flatMap, List.mem_range, List.mem_singleton] at hx
    obtain ⟨a, ha, b, hb, c, hc, rfl⟩ := hx
    intro z hz
    obtain ⟨i, rfl⟩ := hz
    rw [Set.mem_Icc]
    fin_cases i
    · exact ⟨Nat.succ_pos _, hq_square ▸ block_le_square ha hb⟩
    · exact ⟨Nat.succ_pos _, hq_square ▸ block_le_square ha hc⟩
    · exact ⟨Nat.succ_pos _, hq_square ▸ block_le_square hb hc⟩
  have hs_pairwise : s.Pairwise R := by
    dsimp only [s]
    apply pairwise_range_flatMap
    · intro a ha
      apply pairwise_range_flatMap
      · intro b hb
        apply pairwise_range_flatMap
        · intro c hc
          simp
        · intro c hc d hd hcd x hx y hy
          simp only [List.mem_singleton] at hx hy
          subst x
          subst y
          refine ⟨1, 2, by decide, ?_, ?_⟩ <;> simp
          all_goals omega
      · intro b hb d hd hbd x hx y hy
        simp only [List.mem_flatMap, List.mem_range, List.mem_singleton] at hx hy
        obtain ⟨c, hc, rfl⟩ := hx
        obtain ⟨e, he, rfl⟩ := hy
        refine ⟨0, 2, by decide, ?_, ?_⟩
        · simp
          omega
        · simpa using block_lt (q := q) (a := b) (a' := d)
            (b := c) (b' := e) hc hbd
    · intro a ha d hd had x hx y hy
      simp only [List.mem_flatMap, List.mem_range, List.mem_singleton] at hx hy
      obtain ⟨b, hb, c, hc, rfl⟩ := hx
      obtain ⟨e, he, f, hf, rfl⟩ := hy
      refine ⟨0, 1, by decide, ?_, ?_⟩
      · simpa using block_lt (q := q) (a := a) (a' := d)
          (b := b) (b' := e) hb had
      · simpa using block_lt (q := q) (a := a) (a' := d)
          (b := c) (b' := f) hc had
  have hbounded : BddAbove lengths := by
    refine ⟨n ^ 2, ?_⟩
    intro x hx
    obtain ⟨u, hu_range, hu_pairwise, rfl⟩ := hx
    by_cases hn : 2 ≤ n
    · by_contra hle
      have hu_length : n ^ 2 < u.length := Nat.lt_of_not_ge hle
      obtain ⟨i, j, hij, h0, h1⟩ :=
        exists_equal_first_two hn hu_range hu_length
      rcases lt_or_gt_of_ne hij with hij | hji
      · have hp := List.pairwise_iff_get.1 hu_pairwise i j hij
        rcases hp with ⟨k, l, hkl, hk, hl⟩
        fin_cases k <;> fin_cases l <;> simp_all
      · have hp := List.pairwise_iff_get.1 hu_pairwise j i hji
        rcases hp with ⟨k, l, hkl, hk, hl⟩
        fin_cases k <;> fin_cases l <;> simp_all
    · have hn_small : n = 0 ∨ n = 1 := by omega
      rcases hn_small with rfl | rfl
      · have hu_nil : u = [] := by
          apply List.eq_nil_of_subset_nil
          intro a ha
          have hbad := hu_range a ha ⟨0, rfl⟩
          simp at hbad
        simp [hu_nil]
      · have hu_const : ∀ a ∈ u, ∀ i, a i = 1 := by
          intro a ha i
          have hi := hu_range a ha ⟨i, rfl⟩
          simpa using hi
        have := length_lt_two_of_const hu_pairwise hu_const
        omega
  have hs_mem : q ^ 3 ∈ lengths :=
    ⟨s, hs_range, hs_pairwise, hs_length⟩
  change q ^ 3 ≤ sSup lengths
  exact le_csSup hbounded hs_mem

end AwesomeTheorems.Stage5.S5_CLM_00003491
