import Mathlib.Analysis.InnerProductSpace.PiL2

open scoped BigOperators

namespace Stage1.THM_M_0339.Proof

/-!
# Executed proof leaves for THM-M-0339

These are genuine proofs of the frozen `r = 1`, `d = 0`, and `m = 0` boundary leaves. They do not
assume or expose a theorem-shaped package for the open MSS argument. The general `1 < r`, positive-
dimensional branch remains unproved.
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
  rw [hfiber]
  rw [hsum]
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
  have hid : ContinuousLinearMap.id ℂ (EuclideanSpace ℂ (Fin d)) = 0 := by
    simpa using hsum.symm
  refine ⟨Fin.elim0, ?_⟩
  intro j
  simp only [Finset.univ_eq_empty, Finset.filter_empty, Finset.sum_empty, norm_zero]
  exact sq_nonneg _

#print axioms one_part
#print axioms zero_dimension
#print axioms empty_family

end Stage1.THM_M_0339.Proof
