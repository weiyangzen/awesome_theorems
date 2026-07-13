import «Stage1_Instances».«THM-M-1518».ObligationTree
import Mathlib.Analysis.Calculus.ParametricIntervalIntegral
import Mathlib.Analysis.Calculus.ContDiff.Deriv
import Mathlib.Analysis.Calculus.ContDiff.Operations

/-!
# THM-M-1518: first variation formula

This module closes the differentiation-under-the-integral package in the
frozen obligation tree. The weak-to-pointwise package is implemented in its
own module.
-/

noncomputable section
open Set MeasureTheory
open scoped Interval
namespace Stage1Instances.THM_M_1518

/-- Differentiate the action along an admissible variation. -/
theorem firstVariation_formula (n : Nat) (L : ℝ × (Configuration n × Configuration n) → ℝ)
    (B : BoundaryData n) (q : Path n) (hL : ContDiff ℝ 2 L) (hq : ContDiff ℝ 2 q)
    (η : Path n) (hη : AdmissibleVariation B η) :
    FirstVariation L B q η =
      ∫ t in B.initialTime..B.finalTime,
        PositionDerivative L t (q t) (deriv q t) (η t) +
          VelocityDerivative L t (q t) (deriv q t) (deriv η t) := by
  rcases hη with ⟨hη, _, _⟩
  let F : ℝ → ℝ → ℝ := fun ε t => L (t, VariedPath q η ε t, deriv (VariedPath q η ε) t)
  let F' : ℝ → ℝ → ℝ := fun ε t =>
    PositionDerivative L t (VariedPath q η ε t) (deriv (VariedPath q η ε) t) (η t) +
      VelocityDerivative L t (VariedPath q η ε t) (deriv (VariedPath q η ε) t) (deriv η t)
  have hderiv_varied (ε t : ℝ) : deriv (VariedPath q η ε) t = deriv q t + ε • deriv η t := by
    have hq' := hq.differentiable (by norm_num : (2 : WithTop ℕ∞) ≠ 0) t
    have hη' := hη.differentiable one_ne_zero t
    unfold VariedPath
    change deriv (q + fun t => ε • η t) t = _
    rw [show deriv (q + fun t => ε • η t) t =
        deriv q t + deriv (fun t => ε • η t) t by
      exact deriv_add hq' ((differentiableAt_const (c := ε)).smul hη')]
    congr 1
    exact deriv_const_smul_field ε η
  have hF_cont : Continuous fun p : ℝ × ℝ => F p.1 p.2 := by
    rw [show (fun p : ℝ × ℝ => F p.1 p.2) = fun p =>
        L (p.2, q p.2 + p.1 • η p.2, deriv q p.2 + p.1 • deriv η p.2) by
      funext p
      simp [F, VariedPath, hderiv_varied]
    ]
    apply hL.continuous.comp
    exact continuous_snd.prodMk (((hq.continuous.comp continuous_snd).add
        (continuous_fst.smul (hη.continuous.comp continuous_snd))).prodMk
      ((hq.continuous_deriv one_le_two).comp continuous_snd |>.add
        (continuous_fst.smul ((hη.continuous_deriv (le_refl 1)).comp continuous_snd))))
  have hF'_cont : Continuous fun p : ℝ × ℝ => F' p.1 p.2 := by
    unfold F' PositionDerivative VelocityDerivative
    simp_rw [hderiv_varied]
    dsimp only [VariedPath]
    have hq0 : ContDiff ℝ 0 q := hq.of_le (by norm_num)
    have hη0 : ContDiff ℝ 0 η := hη.of_le (by norm_num)
    have hqd : ContDiff ℝ 0 (deriv q) := (by simpa using hq.deriv' : ContDiff ℝ 1 (deriv q)).of_le (by norm_num)
    have hηd : ContDiff ℝ 0 (deriv η) := by
      simpa only [show (0 : WithTop ℕ∞) + 1 = 1 by norm_num] using
        (ContDiff.deriv' (n := 0) hη)
    have hLD : ContDiff ℝ 1 (fderiv ℝ L) := hL.fderiv_right (by norm_num)
    let X : ℝ × ℝ → Configuration n := fun p => q p.2 + p.1 • η p.2
    let V : ℝ × ℝ → Configuration n := fun p => deriv q p.2 + p.1 • deriv η p.2
    have hX : ContDiff ℝ 0 X := (hq0.comp contDiff_snd).add
      ((show ContDiff ℝ 0 (fun p : ℝ × ℝ => p.1) from contDiff_fst).smul
        (hη0.comp contDiff_snd))
    have hV : ContDiff ℝ 0 V := (hqd.comp contDiff_snd).add
      ((show ContDiff ℝ 0 (fun p : ℝ × ℝ => p.1) from contDiff_fst).smul
        (hηd.comp contDiff_snd))
    have hD : ContDiff ℝ 0 (fun p : ℝ × ℝ => fderiv ℝ L (p.2, X p, V p)) :=
      (hLD.of_le (by norm_num)).comp (contDiff_snd.prodMk (hX.prodMk hV))
    have hpos : ContDiff ℝ 0 (fun p : ℝ × ℝ =>
        (fderiv ℝ L (p.2, X p, V p)) (0, η p.2, 0)) :=
      hD.clm_apply (contDiff_const.prodMk ((hη0.comp contDiff_snd).prodMk contDiff_const))
    have hvel : ContDiff ℝ 0 (fun p : ℝ × ℝ =>
        (fderiv ℝ L (p.2, X p, V p)) (0, 0, deriv η p.2)) :=
      hD.clm_apply (contDiff_const.prodMk (contDiff_const.prodMk (hηd.comp contDiff_snd)))
    have hpartial (p : ℝ × ℝ) :
        (fderiv ℝ (fun y => L (p.2, y, V p)) (X p)) (η p.2) =
          (fderiv ℝ L (p.2, X p, V p)) (0, η p.2, 0) := by
      have h := (hL.differentiable (by norm_num) _).hasFDerivAt.comp
        (X p) ((hasFDerivAt_const (x := X p) p.2).prodMk
          (hasFDerivAt_id (x := X p) |>.prodMk (hasFDerivAt_const (x := X p) (V p))))
      have hd := h.fderiv
      change fderiv ℝ (fun y => L (p.2, y, V p)) (X p) = _ at hd
      rw [hd]
      simp
    have hpartial' (p : ℝ × ℝ) :
        (fderiv ℝ (fun w => L (p.2, X p, w)) (V p)) (deriv η p.2) =
          (fderiv ℝ L (p.2, X p, V p)) (0, 0, deriv η p.2) := by
      have h := (hL.differentiable (by norm_num) _).hasFDerivAt.comp
        (V p) ((hasFDerivAt_const (x := V p) p.2).prodMk
          ((hasFDerivAt_const (x := V p) (X p)).prodMk (hasFDerivAt_id (x := V p))))
      have hd := h.fderiv
      change fderiv ℝ (fun w => L (p.2, X p, w)) (V p) = _ at hd
      rw [hd]
      simp
    apply Continuous.add
    · simpa only [X, V, hpartial] using hpos.continuous
    · simpa only [X, V, hpartial'] using hvel.continuous
  obtain ⟨C, hC⟩ := (isCompact_Icc.prod (isCompact_uIcc (a := B.initialTime)
      (b := B.finalTime))).exists_bound_of_continuousOn
    hF'_cont.norm.continuousOn
  have hbound : ∀ᵐ t ∂volume, t ∈ Ι B.initialTime B.finalTime →
      ∀ ε ∈ Icc (-1) 1, ‖F' ε t‖ ≤ C :=
    Filter.Eventually.of_forall (fun t ht ε hε => by
      simpa using hC (ε, t) ⟨hε, uIoc_subset_uIcc ht⟩)
  have hdiff : ∀ᵐ t ∂volume, t ∈ Ι B.initialTime B.finalTime →
      ∀ ε ∈ Icc (-1) 1, HasDerivAt (fun ε => F ε t) (F' ε t) ε :=
    Filter.Eventually.of_forall (fun t _ ε _ => by
    unfold F F'
    rw [hderiv_varied]
    dsimp only [VariedPath]
    have hpath : HasDerivAt (fun ε : ℝ => q t + ε • η t) (η t) ε := by
      simpa using (hasDerivAt_id ε).smul_const (η t) |>.const_add (q t)
    have hvel : HasDerivAt (fun ε : ℝ => deriv q t + ε • deriv η t) (deriv η t) ε := by
      simpa using (hasDerivAt_id ε).smul_const (deriv η t) |>.const_add (deriv q t)
    have hinput : HasDerivAt
        (fun ε : ℝ => (t, q t + ε • η t, deriv q t + ε • deriv η t))
        (0, η t, deriv η t) ε :=
      (hasDerivAt_const ε t).prodMk (hpath.prodMk hvel)
    have hmain := (hL.differentiable (by norm_num : (2 : WithTop ℕ∞) ≠ 0) _).hasFDerivAt.comp_hasDerivAt ε hinput
    unfold PositionDerivative VelocityDerivative
    have hpartial : (fderiv ℝ L (t, q t + ε • η t, deriv q t + ε • deriv η t)) (0, η t, deriv η t) =
          (fderiv ℝ (fun y => L (t, y, deriv q t + ε • deriv η t))
            (q t + ε • η t)) (η t) +
          (fderiv ℝ (fun w => L (t, q t + ε • η t, w))
          (deriv q t + ε • deriv η t)) (deriv η t) := by
      have hpos := (hL.differentiable (by norm_num) _).hasFDerivAt.comp
          (q t + ε • η t)
          ((hasFDerivAt_const (x := q t + ε • η t) t).prodMk
            (hasFDerivAt_id (x := q t + ε • η t) |>.prodMk
              (hasFDerivAt_const (x := q t + ε • η t) (deriv q t + ε • deriv η t))))
      have hvelp := (hL.differentiable (by norm_num) _).hasFDerivAt.comp
          (deriv q t + ε • deriv η t)
          ((hasFDerivAt_const (x := deriv q t + ε • deriv η t) t).prodMk
            ((hasFDerivAt_const (x := deriv q t + ε • deriv η t) (q t + ε • η t)).prodMk
              (hasFDerivAt_id (x := deriv q t + ε • deriv η t))))
      have hdpos := hpos.fderiv
      have hdvel := hvelp.fderiv
      change fderiv ℝ (fun y => L (t, y, deriv q t + ε • deriv η t))
        (q t + ε • η t) = _ at hdpos
      change fderiv ℝ (fun w => L (t, q t + ε • η t, w))
        (deriv q t + ε • deriv η t) = _ at hdvel
      rw [hdpos, hdvel]
      simp only [ContinuousLinearMap.comp_apply, ContinuousLinearMap.prod_apply,
        ContinuousLinearMap.zero_apply, ContinuousLinearMap.id_apply]
      change _ = (fderiv ℝ L (t, q t + ε • η t, deriv q t + ε • deriv η t))
          (0, η t, 0) +
        (fderiv ℝ L (t, q t + ε • η t, deriv q t + ε • deriv η t))
          (0, 0, deriv η t)
      rw [← map_add]
      congr
      all_goals simp
    refine (hmain.congr_deriv hpartial).congr_of_eventuallyEq ?_
    exact Filter.Eventually.of_forall (fun ε => by
      change L (t, q t + ε • η t, deriv (VariedPath q η ε) t) = _
      rw [hderiv_varied]
      rfl))
  have key := intervalIntegral.hasDerivAt_integral_of_dominated_loc_of_deriv_le
    (a := B.initialTime) (b := B.finalTime) (μ := volume)
    (F := F) (F' := F') (bound := fun _ => C) (x₀ := 0) (s := Icc (-1) 1)
    (Icc_mem_nhds (by norm_num : (-1 : ℝ) < 0) (by norm_num : (0 : ℝ) < 1))
    (Filter.Eventually.of_forall fun ε =>
      (hF_cont.comp (continuous_const.prodMk continuous_id)).aestronglyMeasurable.restrict)
    ((hF_cont.comp (continuous_const.prodMk continuous_id)).intervalIntegrable _ _)
    ((hF'_cont.comp (continuous_const.prodMk continuous_id)).aestronglyMeasurable.restrict)
    hbound
    (intervalIntegrable_const (c := C))
    hdiff
  unfold FirstVariation Action
  have hkey := key.2.deriv
  simpa [F, F', VariedPath, hderiv_varied] using hkey

/-- Inhabitant of the frozen differentiation package. -/
theorem firstVariationFormula : ObligationTree.FirstVariationFormula := by
  intro n L B q hL hq η hη
  exact firstVariation_formula n L B q hL hq η hη

#check firstVariationFormula
#print axioms firstVariationFormula

end Stage1Instances.THM_M_1518
