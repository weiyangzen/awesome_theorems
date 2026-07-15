/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Cocycle.Basic
import ErgodicTheory.Cocycle.Norm
import ErgodicTheory.Ergodic.Kingman.Core
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse

/-!
# The Furstenberg–Kesten theorem (extremal Lyapunov exponents)

Applying Kingman's subadditive ergodic theorem to `gₙ = log‖A⁽ⁿ⁾‖` (a subadditive cocycle
by submultiplicativity of the operator norm) yields the **top Lyapunov exponent**
`λ₁ = lim (1/n) log‖A⁽ⁿ⁾(x)‖`; applying it to the inverse cocycle `gₙ = log‖(A⁽ⁿ⁾)⁻¹‖`
yields the (negative of the) **bottom exponent** `λ_k`. These are the extremal cases of
the Oseledets spectrum.

The proofs build the two subadditive cocycles, verify the three hypotheses of
`tendsto_kingman_ergodic` (subadditivity, integrability of each level, bounded-below
normalized means), and read off the a.e.-constant limit. The cocycle entries are required
to be invertible (`det ≠ 0`) and both `log⁺‖A‖` and `log⁺‖A⁻¹‖` are required to be
integrable; the second integrability hypothesis is what keeps the bounded-below proviso
(hence the limit) finite in `ℝ` for the *top* exponent.

## Main results

* `ErgodicTheory.furstenbergKesten_norm`: for an ergodic measure-preserving `T` and an
  everywhere-invertible measurable generator `A` with integrable `log⁺‖A‖` and
  `log⁺‖A⁻¹‖`, the normalized log norms `(1/n) log‖A⁽ⁿ⁾(x)‖` converge `μ`-a.e. to a
  constant (the top Lyapunov exponent).
* `ErgodicTheory.furstenbergKesten_norm_inv`: the analogous a.e. limit for the inverse cocycle
  `(1/n) log‖(A⁽ⁿ⁾(x))⁻¹‖` (the negative of the bottom Lyapunov exponent).
* `ErgodicTheory.isSubadditiveCocycle_logNorm` and `ErgodicTheory.isSubadditiveCocycle_logNorm_inv`:
  subadditivity of the two log-norm cocycles.
* `ErgodicTheory.logNorm_cocycle_le_birkhoffSum` and
  `ErgodicTheory.neg_birkhoffSum_le_logNorm_cocycle`: Birkhoff-sum sandwich bounds, driving
  both the integrability and the bounded-below hypotheses.

## References

* H. Furstenberg and H. Kesten, *Products of random matrices*,
  Ann. Math. Statist. **31** (1960), 457–469.
-/

open MeasureTheory Filter Topology
open scoped Matrix.Norms.L2Operator

namespace ErgodicTheory

variable {X : Type*} {T : X → X} {d : ℕ}

/-! ### Positivity of the iterate norms (needs invertibility and `NeZero d`) -/

/-- `det (cocycle A T n x) ≠ 0` when the generator is everywhere invertible. -/
theorem det_cocycle_ne_zero {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) (n : ℕ) (x : X) :
    (cocycle A T n x).det ≠ 0 := by
  induction n generalizing x with
  | zero => simp
  | succ n ih => rw [cocycle_succ, Matrix.det_mul]; exact mul_ne_zero (ih (T x)) (hA x)

/-- The norm of every cocycle iterate is strictly positive (needs `NeZero d`). -/
theorem norm_cocycle_pos {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) [NeZero d] (n : ℕ) (x : X) :
    0 < ‖cocycle A T n x‖ := by
  rw [norm_pos_iff]; intro h
  apply det_cocycle_ne_zero hA n x
  rw [h, Matrix.det_zero]; exact ⟨⟨0, Nat.pos_of_ne_zero (NeZero.ne d)⟩⟩

/-- The norm of every inverse cocycle iterate is strictly positive (needs `NeZero d`). -/
theorem norm_inv_cocycle_pos {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) [NeZero d] (n : ℕ) (x : X) :
    0 < ‖(cocycle A T n x)⁻¹‖ := by
  rw [norm_pos_iff]; intro h
  have hdet : (cocycle A T n x)⁻¹.det ≠ 0 := by
    rw [Matrix.det_nonsing_inv, Ring.inverse_eq_inv']
    exact inv_ne_zero (det_cocycle_ne_zero hA n x)
  apply hdet
  rw [h, Matrix.det_zero]; exact ⟨⟨0, Nat.pos_of_ne_zero (NeZero.ne d)⟩⟩

/-- `‖(1 : Matrix (Fin d) (Fin d) ℝ)‖ = 1` for the L2 operator norm when `d ≠ 0`. -/
theorem norm_one_matrix [NeZero d] :
    ‖(1 : Matrix (Fin d) (Fin d) ℝ)‖ = 1 := by
  haveI : Nontrivial (EuclideanSpace ℝ (Fin d)) := by
    have : Nonempty (Fin d) := ⟨⟨0, Nat.pos_of_ne_zero (NeZero.ne d)⟩⟩
    infer_instance
  rw [← Matrix.l2_opNorm_toEuclideanCLM, map_one]
  exact ContinuousLinearMap.norm_id

/-! ### Measurability of the (inverse) log-norm cocycle -/

section Measurability

variable [MeasurableSpace X]

/-- `x ↦ log‖A⁽ⁿ⁾(x)‖` is measurable. -/
theorem measurable_logNorm_cocycle {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : Measurable A) (hT : Measurable T) (n : ℕ) :
    Measurable (fun x => Real.log ‖cocycle A T n x‖) :=
  Real.measurable_log.comp (measurable_l2_opNorm.comp (measurable_cocycle hA hT n))

/-- `x ↦ log‖(A⁽ⁿ⁾(x))⁻¹‖` is measurable. -/
theorem measurable_logNorm_inv_cocycle {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : Measurable A) (hT : Measurable T) (n : ℕ) :
    Measurable (fun x => Real.log ‖(cocycle A T n x)⁻¹‖) :=
  Real.measurable_log.comp
    (measurable_l2_opNorm.comp (measurable_inv_matrix.comp (measurable_cocycle hA hT n)))

end Measurability

/-! ### Subadditivity of the two log-norm cocycles -/

/-- **The top subadditive cocycle.** `gₙ = log‖A⁽ⁿ⁾‖` is subadditive over `T`. -/
theorem isSubadditiveCocycle_logNorm {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) [NeZero d] :
    IsSubadditiveCocycle T (fun n x => Real.log ‖cocycle A T n x‖) := by
  refine ⟨fun m n x ↦ ?_⟩
  change Real.log ‖cocycle A T (m + n) x‖ ≤ _
  rw [Nat.add_comm m n, cocycle_add]
  have hpos1 : 0 < ‖cocycle A T n (T^[m] x)‖ := norm_cocycle_pos hA n _
  have hpos2 : 0 < ‖cocycle A T m x‖ := norm_cocycle_pos hA m _
  have hposp : 0 < ‖cocycle A T n (T^[m] x) * cocycle A T m x‖ := by
    rw [← cocycle_add, Nat.add_comm n m]; exact norm_cocycle_pos hA _ _
  calc Real.log ‖cocycle A T n (T^[m] x) * cocycle A T m x‖
      ≤ Real.log (‖cocycle A T n (T^[m] x)‖ * ‖cocycle A T m x‖) :=
        Real.log_le_log hposp (Matrix.l2_opNorm_mul _ _)
    _ = Real.log ‖cocycle A T n (T^[m] x)‖ + Real.log ‖cocycle A T m x‖ :=
        Real.log_mul (ne_of_gt hpos1) (ne_of_gt hpos2)
    _ = Real.log ‖cocycle A T m x‖ + Real.log ‖cocycle A T n (T^[m] x)‖ := by ring

/-- **The bottom subadditive cocycle.** `gₙ = log‖(A⁽ⁿ⁾)⁻¹‖` is subadditive over `T`. -/
theorem isSubadditiveCocycle_logNorm_inv {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) [NeZero d] :
    IsSubadditiveCocycle T (fun n x => Real.log ‖(cocycle A T n x)⁻¹‖) := by
  refine ⟨fun m n x ↦ ?_⟩
  change Real.log ‖(cocycle A T (m + n) x)⁻¹‖ ≤ _
  rw [Nat.add_comm m n, cocycle_add, Matrix.mul_inv_rev]
  have hpos1 : 0 < ‖(cocycle A T m x)⁻¹‖ := norm_inv_cocycle_pos hA m _
  have hpos2 : 0 < ‖(cocycle A T n (T^[m] x))⁻¹‖ := norm_inv_cocycle_pos hA n _
  have hposp : 0 < ‖(cocycle A T m x)⁻¹ * (cocycle A T n (T^[m] x))⁻¹‖ := by
    rw [← Matrix.mul_inv_rev, ← cocycle_add, Nat.add_comm n m]
    exact norm_inv_cocycle_pos hA _ _
  calc Real.log ‖(cocycle A T m x)⁻¹ * (cocycle A T n (T^[m] x))⁻¹‖
      ≤ Real.log (‖(cocycle A T m x)⁻¹‖ * ‖(cocycle A T n (T^[m] x))⁻¹‖) :=
        Real.log_le_log hposp (Matrix.l2_opNorm_mul _ _)
    _ = Real.log ‖(cocycle A T m x)⁻¹‖ + Real.log ‖(cocycle A T n (T^[m] x))⁻¹‖ :=
        Real.log_mul (ne_of_gt hpos1) (ne_of_gt hpos2)

/-! ### Birkhoff-sum sandwich bounds (drive integrability and bounded-below) -/

/-- Upper Fekete bound: `log‖A⁽ⁿ⁾(x)‖ ≤ birkhoffSum T (log⁺‖A‖) n x`. -/
theorem logNorm_cocycle_le_birkhoffSum {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) [NeZero d] (n : ℕ) (x : X) :
    Real.log ‖cocycle A T n x‖ ≤ birkhoffSum T (fun y => Real.posLog ‖A y‖) n x := by
  induction n generalizing x with
  | zero => simp
  | succ n ih =>
    rw [cocycle_succ, birkhoffSum_succ']
    have hposc : 0 < ‖cocycle A T n (T x)‖ := norm_cocycle_pos hA n _
    have hposa : 0 < ‖A x‖ := by
      rw [norm_pos_iff]; intro h
      exact hA x (by rw [h, Matrix.det_zero]; exact ⟨⟨0, Nat.pos_of_ne_zero (NeZero.ne d)⟩⟩)
    calc Real.log ‖cocycle A T n (T x) * A x‖
        ≤ Real.log (‖cocycle A T n (T x)‖ * ‖A x‖) :=
          Real.log_le_log (by rw [← cocycle_succ]; exact norm_cocycle_pos hA _ _)
            (Matrix.l2_opNorm_mul _ _)
      _ = Real.log ‖A x‖ + Real.log ‖cocycle A T n (T x)‖ := by
          rw [Real.log_mul (ne_of_gt hposc) (ne_of_gt hposa)]; ring
      _ ≤ Real.posLog ‖A x‖ + birkhoffSum T (fun y => Real.posLog ‖A y‖) n (T x) := by
          gcongr
          · rw [Real.posLog_def]; exact le_max_right _ _
          · exact ih (T x)

/-- Upper Fekete bound for the inverse cocycle:
`log‖(A⁽ⁿ⁾(x))⁻¹‖ ≤ birkhoffSum T (log⁺‖A⁻¹‖) n x`. -/
theorem logNorm_inv_cocycle_le_birkhoffSum {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) [NeZero d] (n : ℕ) (x : X) :
    Real.log ‖(cocycle A T n x)⁻¹‖ ≤
      birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) n x := by
  induction n generalizing x with
  | zero => simp
  | succ n ih =>
    rw [cocycle_succ, Matrix.mul_inv_rev, birkhoffSum_succ']
    have hposc : 0 < ‖(cocycle A T n (T x))⁻¹‖ := norm_inv_cocycle_pos hA n _
    have hposa : 0 < ‖(A x)⁻¹‖ := by
      rw [norm_pos_iff]; intro h
      have hdet : (A x)⁻¹.det ≠ 0 := by
        rw [Matrix.det_nonsing_inv, Ring.inverse_eq_inv']; exact inv_ne_zero (hA x)
      exact hdet (by rw [h, Matrix.det_zero]; exact ⟨⟨0, Nat.pos_of_ne_zero (NeZero.ne d)⟩⟩)
    have hposp : 0 < ‖(A x)⁻¹ * (cocycle A T n (T x))⁻¹‖ := by
      rw [← Matrix.mul_inv_rev, ← cocycle_succ]; exact norm_inv_cocycle_pos hA _ _
    calc Real.log ‖(A x)⁻¹ * (cocycle A T n (T x))⁻¹‖
        ≤ Real.log (‖(A x)⁻¹‖ * ‖(cocycle A T n (T x))⁻¹‖) :=
          Real.log_le_log hposp (Matrix.l2_opNorm_mul _ _)
      _ ≤ Real.posLog ‖(A x)⁻¹‖ +
            birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) n (T x) := by
          rw [Real.log_mul (ne_of_gt hposa) (ne_of_gt hposc)]
          have h1 : Real.log ‖(A x)⁻¹‖ ≤ Real.posLog ‖(A x)⁻¹‖ := by
            rw [Real.posLog_def]; exact le_max_right _ _
          have h2 := ih (T x)
          linarith

/-- Lower bound on the (forward) log-norm via the inverse Birkhoff sum:
`- birkhoffSum T (log⁺‖A⁻¹‖) n x ≤ log‖A⁽ⁿ⁾(x)‖`. -/
theorem neg_birkhoffSum_le_logNorm_cocycle {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) [NeZero d] (n : ℕ) (x : X) :
    - birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) n x ≤ Real.log ‖cocycle A T n x‖ := by
  have hposc : 0 < ‖cocycle A T n x‖ := norm_cocycle_pos hA n _
  have hposi : 0 < ‖(cocycle A T n x)⁻¹‖ := norm_inv_cocycle_pos hA n _
  have hmulinv : cocycle A T n x * (cocycle A T n x)⁻¹ = 1 :=
    Matrix.mul_nonsing_inv _ (Ne.isUnit (det_cocycle_ne_zero hA n x))
  have h1 : (1 : ℝ) ≤ ‖cocycle A T n x‖ * ‖(cocycle A T n x)⁻¹‖ := by
    have := Matrix.l2_opNorm_mul (cocycle A T n x) (cocycle A T n x)⁻¹
    rw [hmulinv, norm_one_matrix] at this; exact this
  have hlog : 0 ≤ Real.log ‖cocycle A T n x‖ + Real.log ‖(cocycle A T n x)⁻¹‖ := by
    rw [← Real.log_mul (ne_of_gt hposc) (ne_of_gt hposi)]; exact Real.log_nonneg h1
  have hub := logNorm_inv_cocycle_le_birkhoffSum (T := T) hA n x
  linarith

/-! ### Integrability of each level, and the Birkhoff integral identity -/

section Integrability

variable [MeasurableSpace X] {μ : Measure X}

/-- The integral of a Birkhoff sum equals `n` times the integral, for measure-preserving
`T` (each composition with `T^[k]` is integral-preserving). -/
theorem integral_birkhoffSum (hT : MeasurePreserving T μ μ) {f : X → ℝ}
    (hf : Integrable f μ) (n : ℕ) :
    ∫ x, birkhoffSum T f n x ∂μ = n • ∫ x, f x ∂μ := by
  simp only [birkhoffSum]
  rw [integral_finset_sum]
  · have hk : ∀ k ∈ Finset.range n, ∫ x, f (T^[k] x) ∂μ = ∫ x, f x ∂μ := by
      intro k _
      have hmp := hT.iterate k
      have haesm : AEStronglyMeasurable f (Measure.map (T^[k]) μ) := by
        rw [hmp.map_eq]; exact hf.aestronglyMeasurable
      have hmap := integral_map (μ := μ) (φ := T^[k]) hmp.aemeasurable (f := f) haesm
      rw [hmp.map_eq] at hmap; exact hmap.symm
    rw [Finset.sum_congr rfl hk, Finset.sum_const, Finset.card_range]
  · intro k _
    exact (hT.iterate k).integrable_comp_of_integrable hf

/-- Integrability of each top level `gₙ = log‖A⁽ⁿ⁾‖`, by domination by the (integrable)
sum of the two Birkhoff sums `birkhoffSum (log⁺‖A‖) n + birkhoffSum (log⁺‖A⁻¹‖) n`. -/
theorem integrable_logNorm_cocycle (hT : MeasurePreserving T μ μ) [IsFiniteMeasure μ]
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) [NeZero d]
    (hAmeas : Measurable A) (hTmeas : Measurable T)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (n : ℕ) : Integrable (fun x => Real.log ‖cocycle A T n x‖) μ := by
  have hBp_int : Integrable
      (fun x => birkhoffSum T (fun y => Real.posLog ‖A y‖) n x) μ :=
    integrable_birkhoffSum hT hint n
  have hBm_int : Integrable
      (fun x => birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) n x) μ :=
    integrable_birkhoffSum hT hint' n
  refine Integrable.mono' (hBp_int.add hBm_int)
    (measurable_logNorm_cocycle hAmeas hTmeas n).aestronglyMeasurable
    (Filter.Eventually.of_forall fun x => ?_)
  have hub : Real.log ‖cocycle A T n x‖ ≤
      birkhoffSum T (fun y => Real.posLog ‖A y‖) n x :=
    logNorm_cocycle_le_birkhoffSum hA n x
  have hlb : - birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) n x ≤
      Real.log ‖cocycle A T n x‖ := neg_birkhoffSum_le_logNorm_cocycle hA n x
  have hBp_nonneg : 0 ≤ birkhoffSum T (fun y => Real.posLog ‖A y‖) n x :=
    Finset.sum_nonneg fun k _ => Real.posLog_nonneg
  have hBm_nonneg : 0 ≤ birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) n x :=
    Finset.sum_nonneg fun k _ => Real.posLog_nonneg
  rw [Real.norm_eq_abs, abs_le]
  exact ⟨by simp only [Pi.add_apply]; linarith, by simp only [Pi.add_apply]; linarith⟩

/-- Integrability of each bottom level `gₙ = log‖(A⁽ⁿ⁾)⁻¹‖`. The inverse cocycle is the
forward cocycle of the generator `A⁻¹` reflected; we dominate directly by the two
Birkhoff sums (the upper bound is `birkhoffSum (log⁺‖A⁻¹‖) n`, the lower bound comes from
`‖(A⁽ⁿ⁾)⁻¹‖ · ‖A⁽ⁿ⁾‖ ≥ 1`). -/
theorem integrable_logNorm_inv_cocycle (hT : MeasurePreserving T μ μ) [IsFiniteMeasure μ]
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) [NeZero d]
    (hAmeas : Measurable A) (hTmeas : Measurable T)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (n : ℕ) : Integrable (fun x => Real.log ‖(cocycle A T n x)⁻¹‖) μ := by
  have hBp_int : Integrable
      (fun x => birkhoffSum T (fun y => Real.posLog ‖A y‖) n x) μ :=
    integrable_birkhoffSum hT hint n
  have hBm_int : Integrable
      (fun x => birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) n x) μ :=
    integrable_birkhoffSum hT hint' n
  refine Integrable.mono' (hBp_int.add hBm_int)
    (measurable_logNorm_inv_cocycle hAmeas hTmeas n).aestronglyMeasurable
    (Filter.Eventually.of_forall fun x => ?_)
  have hub : Real.log ‖(cocycle A T n x)⁻¹‖ ≤
      birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) n x :=
    logNorm_inv_cocycle_le_birkhoffSum hA n x
  have hposc : 0 < ‖cocycle A T n x‖ := norm_cocycle_pos hA n _
  have hposi : 0 < ‖(cocycle A T n x)⁻¹‖ := norm_inv_cocycle_pos hA n _
  have hmulinv : cocycle A T n x * (cocycle A T n x)⁻¹ = 1 :=
    Matrix.mul_nonsing_inv _ (Ne.isUnit (det_cocycle_ne_zero hA n x))
  have h1 : (1 : ℝ) ≤ ‖cocycle A T n x‖ * ‖(cocycle A T n x)⁻¹‖ := by
    have := Matrix.l2_opNorm_mul (cocycle A T n x) (cocycle A T n x)⁻¹
    rw [hmulinv, norm_one_matrix] at this; exact this
  have hlog : 0 ≤ Real.log ‖cocycle A T n x‖ + Real.log ‖(cocycle A T n x)⁻¹‖ := by
    rw [← Real.log_mul (ne_of_gt hposc) (ne_of_gt hposi)]; exact Real.log_nonneg h1
  have hubf : Real.log ‖cocycle A T n x‖ ≤
      birkhoffSum T (fun y => Real.posLog ‖A y‖) n x :=
    logNorm_cocycle_le_birkhoffSum hA n x
  have hBp_nonneg : 0 ≤ birkhoffSum T (fun y => Real.posLog ‖A y‖) n x :=
    Finset.sum_nonneg fun k _ => Real.posLog_nonneg
  have hBm_nonneg : 0 ≤ birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) n x :=
    Finset.sum_nonneg fun k _ => Real.posLog_nonneg
  rw [Real.norm_eq_abs, abs_le]
  exact ⟨by simp only [Pi.add_apply]; linarith, by simp only [Pi.add_apply]; linarith⟩

/-! ### The two Furstenberg–Kesten theorems -/

/-- **Furstenberg–Kesten, top exponent.** For an ergodic measure-preserving `T`, an
everywhere-invertible measurable cocycle generator with `log⁺‖A‖, log⁺‖A⁻¹‖ ∈ L¹`, the
normalized log operator norm of the cocycle converges `μ`-a.e. to a constant `λ₁` (the
top Lyapunov exponent).

Only *existence* of the `μ`-a.e.-constant limit is proved; the constant is not characterized —
neither the classical infimum formula `λ₁ = ⨅ n, (1/n) ∫ log‖A⁽ⁿ⁾‖` nor `L¹` convergence is
included. -/
theorem furstenbergKesten_norm
    [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∃ lam : ℝ, ∀ᵐ x ∂μ,
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖cocycle A T n x‖) atTop (𝓝 lam) := by
  rcases Nat.eq_zero_or_pos d with hd | hd
  · -- `d = 0`: the matrix algebra is trivial, every norm is `0`, limit is `0`.
    subst hd
    refine ⟨0, Filter.Eventually.of_forall fun x => ?_⟩
    have : (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖cocycle A T n x‖) = fun _ => 0 := by
      funext n; rw [Subsingleton.elim (cocycle A T n x) 0]; simp
    rw [this]; exact tendsto_const_nhds
  · haveI : NeZero d := ⟨hd.ne'⟩
    have hmp : MeasurePreserving T μ μ := hT.toMeasurePreserving
    have hTmeas : Measurable T := hmp.measurable
    -- bounded-below proviso: `(∫ g_{n+1})/(n+1) ≥ - ∫ log⁺‖A⁻¹‖`.
    refine (tendsto_kingman_ergodic hT (isSubadditiveCocycle_logNorm hA)
      (fun n => integrable_logNorm_cocycle hmp hA hAmeas hTmeas hint hint' n) ?_)
    refine ⟨- ∫ x, Real.posLog ‖(A x)⁻¹‖ ∂μ, ?_⟩
    rintro _ ⟨n, rfl⟩
    have hpos : (0 : ℝ) < (n : ℝ) + 1 := by positivity
    rw [le_div_iff₀ hpos]
    have hlb : ∀ x, - birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) (n + 1) x ≤
        Real.log ‖cocycle A T (n + 1) x‖ := fun x =>
      neg_birkhoffSum_le_logNorm_cocycle hA (n + 1) x
    have hmono : - ∫ x, birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) (n + 1) x ∂μ ≤
        ∫ x, Real.log ‖cocycle A T (n + 1) x‖ ∂μ := by
      rw [← integral_neg]
      exact integral_mono ((integrable_birkhoffSum hmp hint' (n + 1)).neg)
        (integrable_logNorm_cocycle hmp hA hAmeas hTmeas hint hint' (n + 1)) hlb
    rw [integral_birkhoffSum hmp hint' (n + 1), nsmul_eq_mul] at hmono
    push_cast at hmono ⊢
    nlinarith [hmono]

/-- **Furstenberg–Kesten, bottom exponent.** For the same GL cocycle — invertibility comes from
`hA : det ≠ 0` — with `log⁺‖A‖, log⁺‖A⁻¹‖ ∈ L¹`, the normalized log norm of the inverse cocycle
converges `μ`-a.e. to a constant; equivalently the bottom Lyapunov exponent
`λ_k = -lim (1/n) log‖A⁽ⁿ⁾(x)⁻¹‖` exists and is finite.

As with the top exponent, only *existence* of the `μ`-a.e.-constant limit is proved — the
constant is not characterized (no infimum formula, no `L¹` convergence). -/
theorem furstenbergKesten_norm_inv
    [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∃ lam : ℝ, ∀ᵐ x ∂μ,
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖(cocycle A T n x)⁻¹‖) atTop (𝓝 lam) := by
  rcases Nat.eq_zero_or_pos d with hd | hd
  · subst hd
    refine ⟨0, Filter.Eventually.of_forall fun x => ?_⟩
    have : (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖(cocycle A T n x)⁻¹‖) = fun _ => 0 := by
      funext n; rw [Subsingleton.elim (cocycle A T n x)⁻¹ 0]; simp
    rw [this]; exact tendsto_const_nhds
  · haveI : NeZero d := ⟨hd.ne'⟩
    have hmp : MeasurePreserving T μ μ := hT.toMeasurePreserving
    have hTmeas : Measurable T := hmp.measurable
    refine (tendsto_kingman_ergodic hT (isSubadditiveCocycle_logNorm_inv hA)
      (fun n => integrable_logNorm_inv_cocycle hmp hA hAmeas hTmeas hint hint' n) ?_)
    -- bounded-below proviso: `(∫ g_{n+1})/(n+1) ≥ - ∫ log⁺‖A‖`.
    refine ⟨- ∫ x, Real.posLog ‖A x‖ ∂μ, ?_⟩
    rintro _ ⟨n, rfl⟩
    have hpos : (0 : ℝ) < (n : ℝ) + 1 := by positivity
    rw [le_div_iff₀ hpos]
    -- lower bound: `- birkhoffSum (log⁺‖A‖) (n+1) ≤ log‖(A⁽ⁿ⁺¹⁾)⁻¹‖`.
    have hlb : ∀ x, - birkhoffSum T (fun y => Real.posLog ‖A y‖) (n + 1) x ≤
        Real.log ‖(cocycle A T (n + 1) x)⁻¹‖ := by
      intro x
      have hposc : 0 < ‖cocycle A T (n + 1) x‖ := norm_cocycle_pos hA (n + 1) _
      have hposi : 0 < ‖(cocycle A T (n + 1) x)⁻¹‖ := norm_inv_cocycle_pos hA (n + 1) _
      have hmulinv : cocycle A T (n + 1) x * (cocycle A T (n + 1) x)⁻¹ = 1 :=
        Matrix.mul_nonsing_inv _ (Ne.isUnit (det_cocycle_ne_zero hA (n + 1) x))
      have h1 : (1 : ℝ) ≤ ‖cocycle A T (n + 1) x‖ * ‖(cocycle A T (n + 1) x)⁻¹‖ := by
        have := Matrix.l2_opNorm_mul (cocycle A T (n + 1) x) (cocycle A T (n + 1) x)⁻¹
        rw [hmulinv, norm_one_matrix] at this; exact this
      have hlog : 0 ≤ Real.log ‖cocycle A T (n + 1) x‖ +
          Real.log ‖(cocycle A T (n + 1) x)⁻¹‖ := by
        rw [← Real.log_mul (ne_of_gt hposc) (ne_of_gt hposi)]; exact Real.log_nonneg h1
      have hubf := logNorm_cocycle_le_birkhoffSum (T := T) hA (n + 1) x
      linarith
    have hmono : - ∫ x, birkhoffSum T (fun y => Real.posLog ‖A y‖) (n + 1) x ∂μ ≤
        ∫ x, Real.log ‖(cocycle A T (n + 1) x)⁻¹‖ ∂μ := by
      rw [← integral_neg]
      exact integral_mono ((integrable_birkhoffSum hmp hint (n + 1)).neg)
        (integrable_logNorm_inv_cocycle hmp hA hAmeas hTmeas hint hint' (n + 1)) hlb
    rw [integral_birkhoffSum hmp hint (n + 1), nsmul_eq_mul] at hmono
    push_cast at hmono ⊢
    nlinarith [hmono]

end Integrability

end ErgodicTheory
