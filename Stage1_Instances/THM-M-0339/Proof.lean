import Statement

open scoped BigOperators

namespace Stage1.THM_M_0339.Proof

/-!
# Partial proof execution for MSS Corollary 1.5

The elementary branches below reduce the remaining conditional engine to the genuinely hard
regime: positive dimension and family size, `1 < r`, `0 < delta < 1`, and `r < m`.
`HardRegimeEngine` is an explicit premise, not an implementation of the MSS argument.
-/

theorem one_part
    (d m : ℕ) (δ : ℝ) (_hδ : 0 ≤ δ)
    (u : Fin m → EuclideanSpace ℂ (Fin d))
    (hsum : (∑ i, InnerProductSpace.rankOne ℂ (u i) (u i)) =
      ContinuousLinearMap.id ℂ (EuclideanSpace ℂ (Fin d)))
    (_hu : ∀ i, ‖u i‖ ^ 2 ≤ δ) :
    ∃ color : Fin m → Fin 1,
      ∀ j : Fin 1,
        ‖∑ i with color i = j, InnerProductSpace.rankOne ℂ (u i) (u i)‖ ≤
          (1 / Real.sqrt (1 : ℝ) + Real.sqrt δ) ^ 2 := by
  refine ⟨fun _ => 0, ?_⟩
  intro j
  have hj : j = 0 := Subsingleton.elim _ _
  subst j
  have hfiber :
      (∑ i with (0 : Fin 1) = 0,
          InnerProductSpace.rankOne ℂ (u i) (u i)) =
        ∑ i, InnerProductSpace.rankOne ℂ (u i) (u i) := by
    apply Finset.sum_subset (by simp)
    simp
  rw [hfiber, hsum]
  calc
    ‖ContinuousLinearMap.id ℂ (EuclideanSpace ℂ (Fin d))‖ ≤ 1 :=
      ContinuousLinearMap.norm_id_le
    _ ≤ (1 / Real.sqrt (1 : ℝ) + Real.sqrt δ) ^ 2 := by
      rw [Real.sqrt_one, div_one]
      nlinarith [Real.sqrt_nonneg δ]

theorem zero_dimension
    (m r : ℕ) (δ : ℝ) (hr : 0 < r) (_hδ : 0 ≤ δ)
    (u : Fin m → EuclideanSpace ℂ (Fin 0))
    (_hsum : (∑ i, InnerProductSpace.rankOne ℂ (u i) (u i)) =
      ContinuousLinearMap.id ℂ (EuclideanSpace ℂ (Fin 0)))
    (_hu : ∀ i, ‖u i‖ ^ 2 ≤ δ) :
    ∃ color : Fin m → Fin r,
      ∀ j : Fin r,
        ‖∑ i with color i = j, InnerProductSpace.rankOne ℂ (u i) (u i)‖ ≤
          (1 / Real.sqrt r + Real.sqrt δ) ^ 2 := by
  let zeroPart : Fin r := ⟨0, hr⟩
  refine ⟨fun _ => zeroPart, ?_⟩
  intro j
  have hzero :
      (∑ i with zeroPart = j, InnerProductSpace.rankOne ℂ (u i) (u i)) = 0 := by
    apply Subsingleton.elim
  rw [hzero, norm_zero]
  exact sq_nonneg _

theorem empty_family
    (d r : ℕ) (δ : ℝ) (_hr : 0 < r) (_hδ : 0 ≤ δ)
    (u : Fin 0 → EuclideanSpace ℂ (Fin d))
    (hsum : (∑ i, InnerProductSpace.rankOne ℂ (u i) (u i)) =
      ContinuousLinearMap.id ℂ (EuclideanSpace ℂ (Fin d)))
    (_hu : ∀ i, ‖u i‖ ^ 2 ≤ δ) :
    ∃ color : Fin 0 → Fin r,
      ∀ j : Fin r,
        ‖∑ i with color i = j, InnerProductSpace.rankOne ℂ (u i) (u i)‖ ≤
          (1 / Real.sqrt r + Real.sqrt δ) ^ 2 := by
  have _hid : ContinuousLinearMap.id ℂ (EuclideanSpace ℂ (Fin d)) = 0 := by
    simpa using hsum.symm
  refine ⟨Fin.elim0, ?_⟩
  intro j
  simp only [Finset.univ_eq_empty, Finset.filter_empty, Finset.sum_empty, norm_zero]
  exact sq_nonneg _

theorem enough_colors
    (d m r : ℕ) (δ : ℝ) (_hr : 0 < r) (hδ : 0 ≤ δ) (hmr : m ≤ r)
    (u : Fin m → EuclideanSpace ℂ (Fin d))
    (_hsum : (∑ i, InnerProductSpace.rankOne ℂ (u i) (u i)) =
      ContinuousLinearMap.id ℂ (EuclideanSpace ℂ (Fin d)))
    (hu : ∀ i, ‖u i‖ ^ 2 ≤ δ) :
    ∃ color : Fin m → Fin r,
      ∀ j : Fin r,
        ‖∑ i with color i = j, InnerProductSpace.rankOne ℂ (u i) (u i)‖ ≤
          (1 / Real.sqrt r + Real.sqrt δ) ^ 2 := by
  let color : Fin m → Fin r := Fin.castLE hmr
  refine ⟨color, ?_⟩
  intro j
  by_cases hj : j.val < m
  · let i : Fin m := ⟨j.val, hj⟩
    have hfiber :
        (∑ k with color k = j, InnerProductSpace.rankOne ℂ (u k) (u k)) =
          InnerProductSpace.rankOne ℂ (u i) (u i) := by
      have hi : color i = j := by
        apply Fin.ext
        rfl
      have hset : (Finset.univ.filter fun k : Fin m => color k = j) = {i} := by
        ext b
        simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_singleton]
        constructor
        · intro hb
          exact Fin.castLE_injective hmr (hb.trans hi.symm)
        · rintro rfl
          exact hi
      rw [hset, Finset.sum_singleton]
    rw [hfiber, InnerProductSpace.norm_rankOne]
    calc
      ‖u i‖ * ‖u i‖ = ‖u i‖ ^ 2 := by ring
      _ ≤ δ := hu i
      _ ≤ (1 / Real.sqrt r + Real.sqrt δ) ^ 2 := by
        have hsδ : (Real.sqrt δ) ^ 2 = δ := Real.sq_sqrt hδ
        have hsr : 0 ≤ 1 / Real.sqrt (r : ℝ) :=
          div_nonneg (by norm_num) (Real.sqrt_nonneg _)
        nlinarith [Real.sqrt_nonneg δ]
  · have hfilter : (Finset.univ.filter fun k : Fin m => color k = j) = ∅ := by
      apply Finset.filter_eq_empty_iff.mpr
      intro k hk
      simp only [color, Fin.castLE]
      exact fun h => hj (h ▸ k.isLt)
    simp only [hfilter, Finset.sum_empty, norm_zero]
    exact sq_nonneg _

theorem constant_color_large_bound
    (d m r : ℕ) (δ : ℝ) (hr : 0 < r) (_hδ : 0 ≤ δ)
    (hbound : 1 ≤ (1 / Real.sqrt r + Real.sqrt δ) ^ 2)
    (u : Fin m → EuclideanSpace ℂ (Fin d))
    (hsum : (∑ i, InnerProductSpace.rankOne ℂ (u i) (u i)) =
      ContinuousLinearMap.id ℂ (EuclideanSpace ℂ (Fin d)))
    (_hu : ∀ i, ‖u i‖ ^ 2 ≤ δ) :
    ∃ color : Fin m → Fin r,
      ∀ j : Fin r,
        ‖∑ i with color i = j, InnerProductSpace.rankOne ℂ (u i) (u i)‖ ≤
          (1 / Real.sqrt r + Real.sqrt δ) ^ 2 := by
  let zeroPart : Fin r := ⟨0, hr⟩
  refine ⟨fun _ => zeroPart, ?_⟩
  intro j
  by_cases hj : zeroPart = j
  · subst j
    have hfiber :
        (∑ i with zeroPart = zeroPart, InnerProductSpace.rankOne ℂ (u i) (u i)) =
          ∑ i, InnerProductSpace.rankOne ℂ (u i) (u i) := by
      apply Finset.sum_subset (by simp)
      simp
    rw [hfiber, hsum]
    exact ContinuousLinearMap.norm_id_le.trans hbound
  · have hfiber :
        (∑ i with zeroPart = j, InnerProductSpace.rankOne ℂ (u i) (u i)) = 0 := by
      simp [hj]
    rw [hfiber, norm_zero]
    exact zero_le_one.trans hbound

theorem delta_ge_one
    (d m r : ℕ) (δ : ℝ) (hr : 0 < r) (hδ : 1 ≤ δ)
    (u : Fin m → EuclideanSpace ℂ (Fin d))
    (hsum : (∑ i, InnerProductSpace.rankOne ℂ (u i) (u i)) =
      ContinuousLinearMap.id ℂ (EuclideanSpace ℂ (Fin d)))
    (hu : ∀ i, ‖u i‖ ^ 2 ≤ δ) :
    ∃ color : Fin m → Fin r,
      ∀ j : Fin r,
        ‖∑ i with color i = j, InnerProductSpace.rankOne ℂ (u i) (u i)‖ ≤
          (1 / Real.sqrt r + Real.sqrt δ) ^ 2 := by
  apply constant_color_large_bound d m r δ hr (by positivity) _ u hsum hu
  have hsqrt : 1 ≤ Real.sqrt δ := by
    nlinarith [Real.sq_sqrt (zero_le_one.trans hδ), Real.sqrt_nonneg δ]
  have hrreal : (0 : ℝ) < r := by exact_mod_cast hr
  have hsqrr : 0 < Real.sqrt r := Real.sqrt_pos.2 hrreal
  have hdiv : 0 ≤ 1 / Real.sqrt r := div_nonneg (by norm_num) hsqrr.le
  nlinarith

theorem zero_delta
    (d m r : ℕ) (hr : 0 < r)
    (u : Fin m → EuclideanSpace ℂ (Fin d))
    (_hsum : (∑ i, InnerProductSpace.rankOne ℂ (u i) (u i)) =
      ContinuousLinearMap.id ℂ (EuclideanSpace ℂ (Fin d)))
    (hu : ∀ i, ‖u i‖ ^ 2 ≤ (0 : ℝ)) :
    ∃ color : Fin m → Fin r,
      ∀ j : Fin r,
        ‖∑ i with color i = j, InnerProductSpace.rankOne ℂ (u i) (u i)‖ ≤
          (1 / Real.sqrt r + Real.sqrt (0 : ℝ)) ^ 2 := by
  have hzero : ∀ i, u i = 0 := by
    intro i
    have hsquare : ‖u i‖ ^ 2 = 0 := le_antisymm (hu i) (sq_nonneg _)
    exact norm_eq_zero.mp (sq_eq_zero_iff.mp hsquare)
  let zeroPart : Fin r := ⟨0, hr⟩
  refine ⟨fun _ => zeroPart, ?_⟩
  intro j
  have hfiber :
      (∑ i with zeroPart = j, InnerProductSpace.rankOne ℂ (u i) (u i)) = 0 := by
    apply Finset.sum_eq_zero
    intro i hi
    rw [hzero i]
    exact (InnerProductSpace.rankOne_eq_zero).2 (Or.inl rfl)
  rw [hfiber, norm_zero]
  exact sq_nonneg _

/-- The still-unproved MSS engine after every elementary parameter branch above is removed. -/
def HardRegimeEngine : Prop :=
  ∀ (d m r : ℕ) (δ : ℝ),
    0 < d →
    0 < m →
    1 < r →
    0 < δ →
    δ < 1 →
    r < m →
    ∀ u : Fin m → EuclideanSpace ℂ (Fin d),
      (∑ i, InnerProductSpace.rankOne ℂ (u i) (u i)) =
          ContinuousLinearMap.id ℂ (EuclideanSpace ℂ (Fin d)) →
      (∀ i, ‖u i‖ ^ 2 ≤ δ) →
      ∃ color : Fin m → Fin r,
        ∀ j : Fin r,
          ‖∑ i with color i = j, InnerProductSpace.rankOne ℂ (u i) (u i)‖ ≤
            (1 / Real.sqrt r + Real.sqrt δ) ^ 2

/-- Exact root composition from the genuinely hard residual engine. The premise remains open. -/
theorem mssPartitionStatement_of_hardRegimeEngine
    (engine : HardRegimeEngine) : Stage1.THM_M_0339.MSSPartitionStatement := by
  intro d m r δ hr hδ u hsum hu
  by_cases hd : d = 0
  · subst d
    exact zero_dimension m r δ hr hδ u hsum hu
  by_cases hm : m = 0
  · subst m
    exact empty_family d r δ hr hδ u hsum hu
  have hdpos : 0 < d := Nat.pos_of_ne_zero hd
  have hmpos : 0 < m := Nat.pos_of_ne_zero hm
  rcases (Nat.one_le_iff_ne_zero.mpr (Nat.ne_of_gt hr)).eq_or_lt with hr1 | hrmany
  · subst r
    simpa using one_part d m δ hδ u hsum hu
  by_cases hmr : m ≤ r
  · exact enough_colors d m r δ hr hδ hmr u hsum hu
  by_cases hδone : 1 ≤ δ
  · exact delta_ge_one d m r δ hr hδone u hsum hu
  by_cases hδzero : δ = 0
  · subst δ
    exact zero_delta d m r hr u hsum hu
  have hδpos : 0 < δ := lt_of_le_of_ne hδ (Ne.symm hδzero)
  have hδlt : δ < 1 := lt_of_not_ge hδone
  have hrm : r < m := lt_of_not_ge hmr
  exact engine d m r δ hdpos hmpos hrmany hδpos hδlt hrm u hsum hu

#print axioms one_part
#print axioms zero_dimension
#print axioms empty_family
#print axioms enough_colors
#print axioms constant_color_large_bound
#print axioms delta_ge_one
#print axioms zero_delta
#print axioms mssPartitionStatement_of_hardRegimeEngine

end Stage1.THM_M_0339.Proof
