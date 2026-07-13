import Mathlib.Analysis.Complex.Harmonic.Poisson
import Mathlib.Analysis.InnerProductSpace.Harmonic.Constructions
import Mathlib.MeasureTheory.Integral.IntervalIntegral.IntegrationByParts
import Mathlib.Topology.ContinuousMap.Compact
import Mathlib.Analysis.Calculus.ParametricIntervalIntegral
import Mathlib.Analysis.Complex.Tietze
import Mathlib.Topology.TietzeExtension

/-!
# Unit-disk Poisson extension lemmas for THM-M-1148

This file proves the analytic core of the Poisson construction on the unit
disk. It is intentionally local to this theorem dossier.

The declarations `poissonIntegral`, `herglotzIntegral`,
`poissonIntegral_eq_re_herglotzIntegral`,
`herglotzIntegral_differentiableOn`,
`harmonicOnNhd_re_of_differentiableOn`, `harmonicOnNhd_congr_eqOn`, and
`poissonIntegral_harmonic`, plus the analytic development from
`mobiusTransform` through `poissonIntegral_tendsto_boundary`, are adapted and
modified from source regions 38-194, 196-768, and 770-789 of the ATLAS project file
`Atlas/ComplexVariables/code/Lecture16.lean`, commit
`34ffed396f376454c1a9b297f3fd74c5c801fb50`.

Copyright (c) Meta Platforms, Inc. and affiliates. All rights reserved.

Original source:
https://github.com/facebookresearch/atlas-lean/blob/34ffed396f376454c1a9b297f3fd74c5c801fb50/Atlas/ComplexVariables/code/Lecture16.lean

License and disclaimer:
https://github.com/facebookresearch/atlas-lean/blob/34ffed396f376454c1a9b297f3fd74c5c801fb50/LICENSE

The full immutable upstream license text is vendored as `ATLAS-LICENSE` in
this target directory.

Upstream distributes the adapted material for academic and research use only
under CC BY-NC 4.0 with the ATLAS no-training rider. Commercial use and use
to train, fine-tune, distill, evaluate, or otherwise develop ML models are
prohibited. Modifications include target-local namespacing, renamed ASCII
identifiers, qualification and adjustment for the pinned mathlib API,
formatting, and additional target-local extension lemmas. Repository license
compatibility, including whether this automation use conflicts with the
no-training rider, has not been reviewed and remains a downstream release
blocker.
-/

noncomputable section

classical

open Complex InnerProductSpace Laplacian Metric Real Set Topology Filter MeasureTheory

namespace Stage1Instances.THM_M_1148.PoissonUnitDisk

def poissonIntegral (U : ℂ → ℝ) (a : ℂ) : ℝ :=
  circleAverage (poissonKernel 0 a • U) 0 1

def herglotzIntegral (U : ℂ → ℝ) (a : ℂ) : ℂ :=
  (2 * (Real.pi : ℝ))⁻¹ • ∫ theta in (0 : ℝ)..2 * Real.pi,
    herglotzRieszKernel 0 a (circleMap 0 1 theta) •
      (U (circleMap 0 1 theta) : ℂ)

theorem poissonIntegral_eq_re_herglotzIntegral
    (U : ℂ → ℝ) (hU : CircleIntegrable U 0 1) (a : ℂ)
    (ha : a ∈ ball (0 : ℂ) 1) :
    poissonIntegral U a = (herglotzIntegral U a).re := by
  simp only [poissonIntegral, herglotzIntegral, circleAverage]
  rw [Complex.smul_re]
  congr 1
  have hInt : IntervalIntegrable
      (fun theta => herglotzRieszKernel 0 a (circleMap 0 1 theta) •
      (U (circleMap 0 1 theta) : ℂ)) volume 0 (2 * Real.pi) := by
    apply IntervalIntegrable.continuousOn_smul
    · exact ⟨hU.1.ofReal, hU.2.ofReal⟩
    · simp only [herglotzRieszKernel_fun_def, sub_zero]
      apply ContinuousOn.div
      · exact ((continuous_circleMap 0 1).add continuous_const).continuousOn
      · exact ((continuous_circleMap 0 1).sub continuous_const).continuousOn
      · intro theta _
        simp only [sub_ne_zero]
        intro h
        rw [mem_ball, dist_zero_right] at ha
        have hmem := circleMap_mem_sphere 0 one_pos.le theta
        rw [mem_sphere, dist_zero_right] at hmem
        linarith [hmem ▸ h ▸ ha]
  rw [show (∫ theta in (0 : ℝ)..2 * Real.pi,
      herglotzRieszKernel 0 a (circleMap 0 1 theta) •
        (U (circleMap 0 1 theta) : ℂ)).re =
      reCLM (∫ theta in (0 : ℝ)..2 * Real.pi,
        herglotzRieszKernel 0 a (circleMap 0 1 theta) •
          (U (circleMap 0 1 theta) : ℂ)) from by simp [reCLM_apply]]
  rw [← ContinuousLinearMap.intervalIntegral_comp_comm reCLM hInt]
  congr 1
  ext theta
  simp only [reCLM_apply]
  change poissonKernel 0 a (circleMap 0 1 theta) * U (circleMap 0 1 theta) = _
  change _ = (herglotzRieszKernel 0 a (circleMap 0 1 theta) *
    ↑(U (circleMap 0 1 theta))).re
  rw [Complex.mul_re, Complex.ofReal_re, Complex.ofReal_im, mul_zero, sub_zero]
  have h := congr_fun (poissonKernel_eq_re_herglotzRieszKernel
    (c := 0) (w := a)) (circleMap 0 1 theta)
  simp only [Function.comp_apply] at h
  rw [h]

set_option maxHeartbeats 1600000 in
theorem herglotzIntegral_differentiableOn
    (U : ℂ → ℝ) (hU : CircleIntegrable U 0 1) :
    DifferentiableOn ℂ (herglotzIntegral U) (ball 0 1) := by
  intro a0 ha0
  rw [mem_ball_zero_iff] at ha0
  have r0_lt : max ‖a0‖ (1 / 2 : ℝ) < 1 := max_lt ha0 (by norm_num)
  have eps0_pos : (1 - max ‖a0‖ (1 / 2 : ℝ)) / 2 > 0 := by linarith
  have hU_int : IntervalIntegrable (fun theta => U (circleMap 0 1 theta))
      volume 0 (2 * Real.pi) := (circleIntegrable_def U 0 1).mp hU
  have huIoc : uIoc (0 : ℝ) (2 * Real.pi) = Ioc 0 (2 * Real.pi) :=
    uIoc_of_le (by linarith [Real.pi_pos])
  have hU_meas : AEStronglyMeasurable (fun theta =>
      (U (circleMap 0 1 theta) : ℂ)) (volume.restrict (uIoc 0 (2 * Real.pi))) := by
    rw [huIoc]
    exact Complex.continuous_ofReal.comp_aestronglyMeasurable
      hU_int.aestronglyMeasurable
  suffices DifferentiableAt ℂ (herglotzIntegral U) a0 from
    this.differentiableWithinAt
  unfold herglotzIntegral
  simp_rw [herglotzRieszKernel_def, sub_zero, smul_eq_mul, Complex.real_smul]
  apply DifferentiableAt.const_mul
  set eps0 := (1 - max ‖a0‖ (1 / 2 : ℝ)) / 2
  have hx_norm : ∀ x ∈ ball a0 eps0, ‖x‖ < 1 - eps0 := by
    intro x hx
    rw [mem_ball, Complex.dist_eq] at hx
    have h1 : ‖x‖ ≤ ‖a0‖ + ‖x - a0‖ := norm_le_insert' x a0
    have h2 : ‖a0‖ ≤ max ‖a0‖ (1 / 2 : ℝ) := le_max_left _ _
    have h3 : max ‖a0‖ (1 / 2 : ℝ) + eps0 = 1 - eps0 := by
      simp [eps0]
      ring
    linarith
  have hzx_bound : ∀ x ∈ ball a0 eps0, ∀ theta : ℝ,
      ‖circleMap 0 1 theta - x‖ ≥ eps0 := by
    intro x hx theta
    have hxn := hx_norm x hx
    have hz : ‖circleMap 0 1 theta‖ = 1 := by
      rw [norm_circleMap_zero]
      simp
    have : eps0 < 1 - ‖x‖ := by linarith
    linarith [norm_sub_norm_le (circleMap 0 1 theta) x]
  have hzx_ne : ∀ x ∈ ball a0 eps0, ∀ theta : ℝ,
      circleMap 0 1 theta - x ≠ 0 := by
    intro x hx theta h
    have hbound := hzx_bound x hx theta
    simp [h] at hbound
    linarith
  have key := (intervalIntegral.hasDerivAt_integral_of_dominated_loc_of_deriv_le
    (μ := volume) (a := 0) (b := 2 * Real.pi) (x₀ := a0)
    (F := fun y theta => (circleMap 0 1 theta + y) /
      (circleMap 0 1 theta - y) * ↑(U (circleMap 0 1 theta)))
    (F' := fun y theta => 2 * circleMap 0 1 theta /
      (circleMap 0 1 theta - y) ^ 2 * ↑(U (circleMap 0 1 theta)))
    (bound := fun theta => 2 / eps0 ^ 2 * ‖(U (circleMap 0 1 theta) : ℂ)‖)
    (s := ball a0 eps0)
    ?hs ?hF_meas ?hF_int ?hF'_meas ?h_bound ?bound_int ?h_diff).2.differentiableAt
  · exact key
  case hs => exact ball_mem_nhds a0 eps0_pos
  case hF_meas =>
    apply eventually_of_mem (ball_mem_nhds a0 eps0_pos)
    intro x hx
    have hcont : Continuous (fun theta => (circleMap 0 1 theta + x) /
        (circleMap 0 1 theta - x)) := by
      apply Continuous.div (by fun_prop) (by fun_prop)
      intro theta
      exact hzx_ne x hx theta
    exact hcont.aestronglyMeasurable.mul hU_meas
  case hF_int =>
    have hcont : ContinuousOn (fun theta => (circleMap 0 1 theta + a0) /
        (circleMap 0 1 theta - a0)) (uIcc 0 (2 * Real.pi)) := by
      apply ContinuousOn.div (by fun_prop) (by fun_prop)
      intro theta _
      exact hzx_ne a0 (mem_ball_self eps0_pos) theta
    exact IntervalIntegrable.continuousOn_mul
      ⟨hU_int.1.ofReal, hU_int.2.ofReal⟩ hcont
  case hF'_meas =>
    have hcont : Continuous (fun theta => 2 * circleMap 0 1 theta /
        (circleMap 0 1 theta - a0) ^ 2) := by
      apply Continuous.div (by fun_prop) (by fun_prop)
      intro theta
      exact pow_ne_zero 2 (hzx_ne a0 (mem_ball_self eps0_pos) theta)
    exact hcont.aestronglyMeasurable.mul hU_meas
  case h_bound =>
    filter_upwards with theta htheta x hx
    simp only [norm_mul]
    apply mul_le_mul_of_nonneg_right _ (norm_nonneg _)
    have hzx := hzx_bound x hx theta
    have heps : (0 : ℝ) < eps0 := eps0_pos
    have hz : ‖circleMap 0 1 theta‖ = 1 := by
      rw [norm_circleMap_zero]
      simp
    rw [norm_div, norm_mul, Complex.norm_ofNat, norm_pow, hz, mul_one]
    apply div_le_div_of_nonneg_left (by norm_num : (0 : ℝ) ≤ 2) (by positivity)
    exact pow_le_pow_left₀ (by linarith) hzx 2
  case bound_int =>
    apply IntervalIntegrable.const_mul
    simp_rw [Complex.norm_real]
    exact ⟨hU_int.1.norm, hU_int.2.norm⟩
  case h_diff =>
    filter_upwards with theta htheta x hx
    have hne := hzx_ne x hx theta
    have h1 : HasDerivAt (fun a => circleMap 0 1 theta + a) 1 x :=
      (hasDerivAt_id x).const_add _
    have h2 : HasDerivAt (fun a => circleMap 0 1 theta - a) (-1) x := by
      have h := (hasDerivAt_const x (circleMap 0 1 theta)).sub (hasDerivAt_id x)
      simp at h
      exact h
    have hdiv := h1.div h2 hne
    have hderiv : HasDerivAt
        (fun a => (circleMap 0 1 theta + a) / (circleMap 0 1 theta - a))
        (2 * circleMap 0 1 theta / (circleMap 0 1 theta - x) ^ 2) x := by
      refine hdiv.congr_deriv ?_
      field_simp
      ring
    exact hderiv.mul_const _

theorem harmonicOnNhd_re_of_differentiableOn
    {f : ℂ → ℂ} {s : Set ℂ} (hs : IsOpen s)
    (hf : DifferentiableOn ℂ f s) :
    HarmonicOnNhd (fun z => (f z).re) s := by
  intro z hz
  exact AnalyticAt.harmonicAt_re ((hf.analyticOnNhd hs) z hz)

lemma harmonicOnNhd_congr_eqOn {f g : ℂ → ℝ} {s : Set ℂ}
    (hs : IsOpen s) (hf : HarmonicOnNhd f s) (heq : EqOn f g s) :
    HarmonicOnNhd g s := by
  intro x hx
  have hfx := hf x hx
  have hev : f =ᶠ[nhds x] g :=
    eventuallyEq_iff_exists_mem.mpr ⟨s, hs.mem_nhds hx, heq⟩
  exact ⟨hfx.1.congr_of_eventuallyEq hev.symm,
    (laplacian_congr_nhds hev).symm.trans hfx.2⟩

theorem poissonIntegral_harmonic
    (U : ℂ → ℝ) (hU : CircleIntegrable U 0 1) :
    HarmonicOnNhd (poissonIntegral U) (ball 0 1) := by
  have hDiff := herglotzIntegral_differentiableOn U hU
  have hHarm := harmonicOnNhd_re_of_differentiableOn isOpen_ball hDiff
  exact harmonicOnNhd_congr_eqOn isOpen_ball hHarm
    (fun a ha => (poissonIntegral_eq_re_herglotzIntegral U hU a ha).symm)

noncomputable def unitDiskExtension (U : ℂ → ℝ) : ℂ → ℝ := by
  classical
  exact
  fun z => if _h : z ∈ ball (0 : ℂ) 1 then poissonIntegral U z else U z

theorem unitDiskExtension_harmonic
    (U : ℂ → ℝ) (hU : CircleIntegrable U 0 1) :
    HarmonicOnNhd (unitDiskExtension U) (ball 0 1) := by
  apply harmonicOnNhd_congr_eqOn isOpen_ball (poissonIntegral_harmonic U hU)
  intro z hz
  simp [unitDiskExtension, hz]

theorem unitDiskExtension_eqOn_sphere (U : ℂ → ℝ) :
    EqOn (unitDiskExtension U) U (sphere 0 1) := by
  intro z hz
  simp only [unitDiskExtension]
  rw [dif_neg]
  exact fun hball => sphere_disjoint_ball.le_bot ⟨hz, hball⟩

theorem unitDiskExtension_continuousOn
    (U : ℂ → ℝ) (hU : Continuous U)
    (hboundary : ∀ z0 ∈ sphere (0 : ℂ) 1,
      Tendsto (poissonIntegral U) (nhdsWithin z0 (ball 0 1)) (nhds (U z0))) :
    ContinuousOn (unitDiskExtension U) (closedBall 0 1) := by
  rw [← ball_union_sphere]
  intro z hz
  rcases hz with hz | hz
  · have hlocal : unitDiskExtension U =ᶠ[nhds z] poissonIntegral U := by
      filter_upwards [isOpen_ball.mem_nhds hz] with x hx
      simp [unitDiskExtension, hx]
    exact (poissonIntegral_harmonic U
      (hU.continuousOn.circleIntegrable' (c := 0) (R := 1)) z hz).1.continuousAt
      |>.congr_of_eventuallyEq hlocal
      |>.continuousWithinAt
  · rw [ContinuousWithinAt, nhdsWithin_union]
    apply Tendsto.sup
    · have hboundary' : Tendsto (poissonIntegral U)
          (nhdsWithin z (ball 0 1)) (nhds (unitDiskExtension U z)) := by
        rw [unitDiskExtension_eqOn_sphere U hz]
        exact hboundary z hz
      apply hboundary'.congr'
      filter_upwards [self_mem_nhdsWithin] with x hx
      simp [unitDiskExtension, hx]
    · have hU' : Tendsto U (nhdsWithin z (sphere 0 1))
          (nhds (unitDiskExtension U z)) := by
        rw [unitDiskExtension_eqOn_sphere U hz]
        exact hU.continuousAt.tendsto.mono_left nhdsWithin_le_nhds
      apply hU'.congr'
      filter_upwards [self_mem_nhdsWithin] with x hx
      exact (unitDiskExtension_eqOn_sphere U hx).symm

theorem unitKernelMass {a : ℂ} (ha : a ∈ ball (0 : ℂ) 1) :
    circleAverage (poissonKernel 0 a) 0 1 = 1 := by
  have h := (harmonicOnNhd_const (E := ℂ) (s := closedBall (0 : ℂ) 1)
    (1 : ℝ)).circleAverage_poissonKernel_smul ha
  calc
    circleAverage (poissonKernel 0 a) 0 1 =
        circleAverage (poissonKernel 0 a • fun _ => (1 : ℝ)) 0 1 := by
      apply circleAverage_congr_sphere
      intro z hz
      change poissonKernel 0 a z = poissonKernel 0 a z * 1
      rw [mul_one]
    _ = 1 := h

theorem unitPoissonKernel_nonneg {a z : ℂ} (ha : a ∈ ball (0 : ℂ) 1)
    (hz : z ∈ sphere (0 : ℂ) 1) :
    0 ≤ poissonKernel 0 a z := by
  rw [poissonKernel_def]
  have hznorm : ‖z‖ = 1 := by
    simpa [mem_sphere, dist_zero_right] using hz
  have hanorm : ‖a‖ < 1 := by
    simpa [mem_ball, dist_zero_right] using ha
  rw [sub_zero, sub_zero, hznorm, one_pow]
  apply div_nonneg
  · apply sub_nonneg.mpr
    simpa using pow_le_pow_left₀ (norm_nonneg a) hanorm.le 2
  · exact sq_nonneg _

theorem boundaryData_uniformContinuousOn {U : ℂ → ℝ}
    (hU : ContinuousOn U (sphere (0 : ℂ) 1)) :
    UniformContinuousOn U (sphere 0 1) :=
  (isCompact_sphere (0 : ℂ) 1).uniformContinuousOn_of_continuous hU

theorem continuous_extension_of_sphere {g : ℂ → ℝ}
    (hg : ContinuousOn g (sphere (0 : ℂ) 1)) :
    ∃ U : ℂ → ℝ, Continuous U ∧ EqOn U g (sphere 0 1) := by
  let boundary : C(sphere (0 : ℂ) 1, ℝ) :=
    ⟨fun z => g z, continuousOn_iff_continuous_restrict.mp hg⟩
  obtain ⟨extension, hextension⟩ :=
    boundary.exists_restrict_eq (isClosed_sphere : IsClosed (sphere (0 : ℂ) 1))
  refine ⟨(extension : ℂ → ℝ), extension.continuous, ?_⟩
  intro z hz
  let zh : (sphere (0 : ℂ) 1 : Set ℂ) := ⟨z, hz⟩
  have heq : extension zh = boundary zh := by
    exact DFunLike.congr_fun hextension zh
  simpa [boundary] using heq

noncomputable def mobiusTransform (a z : ℂ) : ℂ :=
  (z + a) / (starRingEnd ℂ a * z + 1)

lemma continuous_poissonKernel_circleMap (a : ℂ) (ha : a ∈ ball (0 : ℂ) 1) :
    Continuous (fun t => poissonKernel 0 a (circleMap 0 1 t)) := by
  unfold poissonKernel; simp only [sub_zero]
  apply Continuous.div
  · exact (continuous_norm.pow 2 |>.comp (continuous_circleMap 0 1)).sub continuous_const
  · exact continuous_norm.pow 2 |>.comp ((continuous_circleMap 0 1).sub continuous_const)
  · intro t; simp only [ne_eq]
    rw [pow_eq_zero_iff (by norm_num : 2 ≠ 0), norm_eq_zero, sub_eq_zero]
    intro heq
    have h1 : ‖circleMap 0 1 t‖ = 1 := by
      have := circleMap_mem_sphere 0 one_pos.le t
      rw [Metric.mem_sphere, dist_zero_right] at this; exact this
    have h2 : ‖a‖ < 1 := by rw [mem_ball, dist_zero_right] at ha; exact ha
    rw [heq] at h1; linarith

noncomputable def invMobiusAngle (a : ℂ) (_ha : a ∈ ball (0 : ℂ) 1) : ℝ → ℝ :=
  fun θ => Complex.arg ((1 - a) / (1 - starRingEnd ℂ a)) +
    ∫ t in (0 : ℝ)..θ, poissonKernel 0 a (circleMap 0 1 t)

lemma mobiusTransform_circleMap_invMobiusAngle_zero (a : ℂ) (ha : a ∈ ball (0 : ℂ) 1) :
    mobiusTransform a (circleMap 0 1 (invMobiusAngle a ha 0)) = 1 := by

  simp only [invMobiusAngle, intervalIntegral.integral_same, add_zero]


  set u := (1 - a) / (1 - starRingEnd ℂ a) with hu_def

  have hconj_sub : (1 : ℂ) - starRingEnd ℂ a = starRingEnd ℂ (1 - a) := by
    simp [map_sub]
  have ha_norm : ‖a‖ < 1 := by rwa [mem_ball, dist_zero_right] at ha
  have h1_sub_a_ne : (1 : ℂ) - a ≠ 0 := by
    intro h
    have ha1 : a = 1 := by rwa [sub_eq_zero, eq_comm] at h
    rw [ha1] at ha_norm; simp at ha_norm

  have h1_sub_conj_ne : (1 : ℂ) - starRingEnd ℂ a ≠ 0 := by
    rw [hconj_sub]
    intro h
    apply h1_sub_a_ne
    have : ‖starRingEnd ℂ (1 - a)‖ = 0 := by rw [h, norm_zero]
    rwa [Complex.norm_conj, norm_eq_zero] at this

  have hu_norm : ‖u‖ = 1 := by
    rw [hu_def, norm_div, hconj_sub, Complex.norm_conj, div_self]
    exact norm_ne_zero_iff.mpr h1_sub_a_ne
  have hu_ne : u ≠ 0 := norm_ne_zero_iff.mp (by rw [hu_norm]; exact one_ne_zero)

  have hcircle : circleMap 0 1 (arg u) = u := by
    rw [circleMap_zero, show (1 : ℝ) = ‖u‖ from hu_norm.symm]
    exact norm_mul_exp_arg_mul_I u

  rw [hcircle]


  rw [mobiusTransform, div_eq_one_iff_eq]
  ·
    rw [hu_def]
    have : (1 : ℂ) - starRingEnd ℂ a ≠ 0 := h1_sub_conj_ne
    field_simp
    ring
  ·
    rw [hu_def]
    rw [show starRingEnd ℂ a * ((1 - a) / (1 - starRingEnd ℂ a)) + 1 =
        (starRingEnd ℂ a * (1 - a) + (1 - starRingEnd ℂ a)) / (1 - starRingEnd ℂ a) by
      field_simp]
    apply div_ne_zero
    ·

      have hkey : starRingEnd ℂ a * (1 - a) + (1 - starRingEnd ℂ a) = 1 - starRingEnd ℂ a * a := by
        ring
      rw [hkey]
      intro h
      have h1 : starRingEnd ℂ a * a = 1 := by rwa [sub_eq_zero, eq_comm] at h

      have : ‖starRingEnd ℂ a * a‖ = 1 := by rw [h1]; simp
      rw [norm_mul, Complex.norm_conj] at this

      have hmul : ‖a‖ * ‖a‖ = 1 := this
      have : ‖a‖ * ‖a‖ < 1 :=
        mul_lt_one_of_nonneg_of_lt_one_left (norm_nonneg a) ha_norm ha_norm.le
      linarith
    · exact h1_sub_conj_ne

lemma eq_zero_of_hasDerivAt_mul {y : ℝ → ℂ} {c : ℝ → ℂ}
    (hc_cont : Continuous c)
    (hy_deriv : ∀ θ, HasDerivAt y (c θ * y θ) θ)
    (hy0 : y 0 = 0) (θ : ℝ) : y θ = 0 := by
  set G : ℝ → ℂ := fun θ => ∫ t in (0:ℝ)..θ, c t with hG_def
  set E : ℝ → ℂ := fun θ => Complex.exp (-G θ) with hE_def
  set u : ℝ → ℂ := fun θ => y θ * E θ with hu_def
  have hG_deriv : ∀ θ, HasDerivAt G (c θ) θ := fun θ =>
    intervalIntegral.integral_hasDerivAt_right
      (hc_cont.intervalIntegrable _ _)
      (hc_cont.stronglyMeasurableAtFilter _ _)
      hc_cont.continuousAt
  have hE_deriv : ∀ θ, HasDerivAt E (-c θ * E θ) θ := by
    intro θ
    have h1 := Complex.hasDerivAt_exp (-G θ)
    have h2 : HasDerivAt (fun t => -G t) (-c θ) θ := (hG_deriv θ).neg
    convert (h1.comp θ h2) using 1; ring
  have hu_deriv : ∀ θ, HasDerivAt u 0 θ := by
    intro θ
    convert (hy_deriv θ).mul (hE_deriv θ) using 1
    simp [hE_def]; ring
  have hu_diff : Differentiable ℝ u := fun x => (hu_deriv x).differentiableAt
  have hu_deriv_eq : ∀ x, deriv u x = 0 := fun x => (hu_deriv x).deriv
  have hu_const : u θ = u 0 := is_const_of_deriv_eq_zero hu_diff hu_deriv_eq θ 0
  have hu0 : u 0 = 0 := by simp [hu_def, hy0]
  have huθ : u θ = 0 := by rw [hu_const, hu0]
  have hE_ne : E θ ≠ 0 := by simp [hE_def]
  exact (mul_eq_zero.mp huθ).resolve_right hE_ne

lemma deriv_inv_mobius_eq_poisson_mul' (a z : ℂ) (hz : ‖z‖ = 1)
    (hd : 1 - starRingEnd ℂ a * z ≠ 0) (hza : z - a ≠ 0) :
    ((1 - starRingEnd ℂ a * a) / (1 - starRingEnd ℂ a * z) ^ 2) * (z * Complex.I) =
    ↑(poissonKernel 0 a z) * ((z - a) / (1 - starRingEnd ℂ a * z) * Complex.I) := by
  have hz_ne : z ≠ 0 := by intro h; rw [h, norm_zero] at hz; linarith
  have hz_conj : z * starRingEnd ℂ z = 1 := by
    rw [mul_comm, ← Complex.normSq_eq_conj_mul_self]
    simp [Complex.normSq_eq_norm_sq, hz]
  have h_nsq : (↑(‖z - a‖ ^ 2) : ℂ) * z = (z - a) * (1 - starRingEnd ℂ a * z) := by
    have : (↑(‖z - a‖ ^ 2) : ℂ) = (z - a) * starRingEnd ℂ (z - a) := by
      rw [show (↑(‖z - a‖ ^ 2) : ℂ) = ↑(Complex.normSq (z - a)) from by
        simp [Complex.normSq_eq_norm_sq]]
      rw [Complex.normSq_eq_conj_mul_self]; ring
    rw [this, map_sub]
    have hcz : starRingEnd ℂ z * z = 1 := by rw [← hz_conj]; ring
    suffices (starRingEnd ℂ z - starRingEnd ℂ a) * z = 1 - starRingEnd ℂ a * z by
      rw [mul_assoc, this]
    linear_combination hcz
  have hP : poissonKernel 0 a z = (1 - ‖a‖ ^ 2) / ‖z - a‖ ^ 2 := by
    unfold poissonKernel; simp [hz]
  have h_nsq_div : (↑(‖z - a‖ ^ 2) : ℂ) = (z - a) * (1 - starRingEnd ℂ a * z) / z := by
    rw [eq_div_iff hz_ne]; exact h_nsq
  have h1a : Complex.ofReal (1 - ‖a‖ ^ 2) = 1 - starRingEnd ℂ a * a := by
    have : Complex.ofReal (‖a‖ ^ 2) = starRingEnd ℂ a * a := by
      rw [← Complex.normSq_eq_conj_mul_self]; simp [Complex.normSq_eq_norm_sq]
    simp only [Complex.ofReal_sub, Complex.ofReal_one, this]
  rw [hP, Complex.ofReal_div, h1a, h_nsq_div]
  field_simp

lemma one_sub_conj_mul_circleMap_ne_zero (a : ℂ) (ha : a ∈ ball (0 : ℂ) 1) (θ : ℝ) :
    1 - starRingEnd ℂ a * circleMap 0 1 θ ≠ 0 := by
  intro h
  have ha_norm : ‖a‖ < 1 := by rwa [Metric.mem_ball, dist_zero_right] at ha
  have hz_norm : ‖circleMap 0 1 θ‖ = 1 := by
    have := circleMap_mem_sphere 0 one_pos.le θ
    rwa [Metric.mem_sphere, dist_zero_right] at this
  have h1 : starRingEnd ℂ a * circleMap 0 1 θ = 1 := by
    have := sub_eq_zero.mp h; exact this.symm
  have hle : ‖starRingEnd ℂ a * circleMap 0 1 θ‖ < 1 := by
    rw [norm_mul, Complex.norm_conj]
    exact mul_lt_one_of_nonneg_of_lt_one_left (norm_nonneg _) ha_norm (le_of_eq hz_norm)
  rw [h1] at hle; simp at hle

theorem invMobiusAngle_mobiusTransform_core (a : ℂ) (ha : a ∈ ball (0 : ℂ) 1) (θ : ℝ) :
    mobiusTransform a (circleMap 0 1 (invMobiusAngle a ha θ)) = circleMap 0 1 θ := by


  have ha' : ‖a‖ < 1 := by rw [mem_ball, dist_zero_right] at ha; exact ha
  set c := starRingEnd ℂ a with hc_def

  let φ : ℝ → ℂ := fun t => circleMap 0 1 (invMobiusAngle a ha t)
  let w : ℝ → ℂ := fun t => (circleMap 0 1 t - a) / (1 - c * circleMap 0 1 t)
  let P : ℝ → ℝ := fun t => poissonKernel 0 a (circleMap 0 1 t)

  have hz_norm : ∀ t, ‖circleMap 0 1 t‖ = 1 := fun t => by
    have := circleMap_mem_sphere 0 one_pos.le t
    rw [Metric.mem_sphere, dist_zero_right] at this; exact this

  have hd : ∀ t, (1 : ℂ) - c * circleMap 0 1 t ≠ 0 :=
    fun t => one_sub_conj_mul_circleMap_ne_zero a ha t

  have hca : (1 : ℂ) - c * a ≠ 0 := by
    intro h
    have h1 : c * a = 1 := by rwa [sub_eq_zero, eq_comm] at h
    have : ‖c * a‖ = 1 := by rw [h1]; simp
    rw [norm_mul, Complex.norm_conj] at this
    have : ‖a‖ * ‖a‖ = 1 := this
    have : ‖a‖ * ‖a‖ < 1 := mul_lt_one_of_nonneg_of_lt_one_left (norm_nonneg a) ha' ha'.le
    linarith

  have hza : ∀ t, circleMap 0 1 t - a ≠ 0 := fun t => by
    intro h
    have heq : a = circleMap 0 1 t := by rwa [sub_eq_zero, eq_comm] at h
    rw [heq, hz_norm] at ha'; linarith


  have hφ_deriv : ∀ t, HasDerivAt φ (↑(P t) * (φ t * Complex.I)) t := fun t => by

    have hcont := continuous_poissonKernel_circleMap a ha
    have h_int : HasDerivAt (fun θ₀ => ∫ s in (0 : ℝ)..θ₀,
        poissonKernel 0 a (circleMap 0 1 s))
      (poissonKernel 0 a (circleMap 0 1 t)) t := by
      apply intervalIntegral.integral_hasDerivAt_right
      · exact hcont.intervalIntegrable _ _
      · exact hcont.stronglyMeasurableAtFilter _ _
      · exact hcont.continuousAt
    have h_const : HasDerivAt (fun _ : ℝ => Complex.arg ((1 - a) / (1 - starRingEnd ℂ a))) 0 t :=
      hasDerivAt_const t _
    have hψ : HasDerivAt (invMobiusAngle a ha) (P t) t := by
      have h3 := h_const.add h_int; simp only [zero_add] at h3; exact h3

    have hcm := hasDerivAt_circleMap 0 1 (invMobiusAngle a ha t)
    simp at hcm
    convert (hcm.scomp t hψ) using 1


  have hw_deriv : ∀ t, HasDerivAt w (↑(P t) * (w t * Complex.I)) t := fun t => by
    set z := circleMap 0 1 t with hz_def

    have hcm : HasDerivAt (circleMap 0 1) (z * Complex.I) t := by
      have := hasDerivAt_circleMap 0 1 t; simp at this; exact this

    have hT : HasDerivAt (fun z => (z - a) / (1 - c * z)) ((1 - c * a) / (1 - c * z) ^ 2) z := by
      have h1 : HasDerivAt (fun z => z - a) 1 z := by
        convert (hasDerivAt_id z).sub (hasDerivAt_const z a) using 1; ring
      have h2 : HasDerivAt (fun z => 1 - c * z) (-c) z := by
        convert (hasDerivAt_const z (1 : ℂ)).sub ((hasDerivAt_const z c).mul (hasDerivAt_id z))
          using 1; simp [mul_comm]
      convert h1.div h2 (hd t) using 1; field_simp; ring

    have hchain := hT.comp t hcm

    have halg := deriv_inv_mobius_eq_poisson_mul' a z (hz_norm t) (hd t) (hza t)
    convert hchain using 1
    exact halg.symm


  have hP_cont : Continuous (fun t => ↑(P t) * Complex.I) := by
    exact (continuous_ofReal.comp (continuous_poissonKernel_circleMap a ha)).mul continuous_const

  have hh_deriv : ∀ t, HasDerivAt (fun t => φ t - w t)
      ((↑(P t) * Complex.I) * (φ t - w t)) t := fun t => by
    have := (hφ_deriv t).sub (hw_deriv t)
    convert this using 1; ring

  have h0 : φ 0 - w 0 = 0 := by
    rw [sub_eq_zero]


    have hS := mobiusTransform_circleMap_invMobiusAngle_zero a ha


    rw [mobiusTransform] at hS

    have hden0 : c * φ 0 + 1 ≠ 0 := by
      intro h
      have : (φ 0 + a) / (c * φ 0 + 1) = 1 := hS
      rw [h, div_zero] at this; exact one_ne_zero this.symm
    have hnum : φ 0 + a = c * φ 0 + 1 := by
      rwa [div_eq_one_iff_eq hden0] at hS

    have hφ_eq : φ 0 * (1 - c) = 1 - a := by linear_combination hnum

    show φ 0 = w 0
    have hcm0 : circleMap 0 1 (0 : ℝ) = 1 := by simp [circleMap_zero]
    change φ 0 = (circleMap 0 1 0 - a) / (1 - c * circleMap 0 1 0)
    rw [hcm0, mul_one]

    have h1c : (1 : ℂ) - c ≠ 0 := by
      intro h
      have hc1 : c = 1 := by rwa [sub_eq_zero, eq_comm] at h
      have : ‖c‖ = 1 := by rw [hc1]; simp
      rw [RCLike.norm_conj] at this
      linarith
    rw [eq_div_iff h1c]
    exact hφ_eq


  have huniq : ∀ t, φ t - w t = 0 :=
    eq_zero_of_hasDerivAt_mul hP_cont hh_deriv h0

  have hφw : φ θ = w θ := sub_eq_zero.mp (huniq θ)

  rw [show circleMap 0 1 (invMobiusAngle a ha θ) = φ θ from rfl, hφw]


  show mobiusTransform a ((circleMap 0 1 θ - a) / (1 - c * circleMap 0 1 θ)) = circleMap 0 1 θ
  rw [mobiusTransform]

  have hD_ne : c * ((circleMap 0 1 θ - a) / (1 - c * circleMap 0 1 θ)) + 1 ≠ 0 := by
    have h1 : c * ((circleMap 0 1 θ - a) / (1 - c * circleMap 0 1 θ)) + 1 =
        (1 - c * a) / (1 - c * circleMap 0 1 θ) := by
      rw [show c * ((circleMap 0 1 θ - a) / (1 - c * circleMap 0 1 θ)) =
        (circleMap 0 1 θ - a) * c / (1 - c * circleMap 0 1 θ) from by ring_nf]
      rw [div_add_one (hd θ)]; congr 1; ring
    rw [h1]; exact div_ne_zero hca (hd θ)
  rw [div_eq_iff hD_ne, eq_comm]
  have key : ((circleMap 0 1 θ - a) / (1 - c * circleMap 0 1 θ) + a) *
      (1 - c * circleMap 0 1 θ) =
      circleMap 0 1 θ * (c * ((circleMap 0 1 θ - a) / (1 - c * circleMap 0 1 θ)) + 1) *
      (1 - c * circleMap 0 1 θ) := by
    rw [add_mul, div_mul_cancel₀ _ (hd θ), mul_assoc, add_mul]
    rw [show c * ((circleMap 0 1 θ - a) / (1 - c * circleMap 0 1 θ)) *
        (1 - c * circleMap 0 1 θ) =
        c * ((circleMap 0 1 θ - a) / (1 - c * circleMap 0 1 θ) *
        (1 - c * circleMap 0 1 θ)) from by ring]
    rw [div_mul_cancel₀ _ (hd θ)]; ring
  exact mul_right_cancel₀ (hd θ) key.symm

theorem invMobiusAngle_mobiusTransform (a : ℂ) (ha : a ∈ ball (0 : ℂ) 1) (θ : ℝ) :
    mobiusTransform a (circleMap 0 1 (invMobiusAngle a ha θ)) = circleMap 0 1 θ :=
  invMobiusAngle_mobiusTransform_core a ha θ

theorem hasDerivAt_invMobiusAngle (a : ℂ) (ha : a ∈ ball (0 : ℂ) 1) (θ : ℝ) :
    HasDerivAt (invMobiusAngle a ha) (poissonKernel 0 a (circleMap 0 1 θ)) θ := by
  have hcont := continuous_poissonKernel_circleMap a ha
  have h1 : HasDerivAt (fun θ₀ => ∫ t in (0 : ℝ)..θ₀,
      poissonKernel 0 a (circleMap 0 1 t))
    (poissonKernel 0 a (circleMap 0 1 θ)) θ := by
    apply intervalIntegral.integral_hasDerivAt_right
    · exact hcont.intervalIntegrable _ _
    · exact hcont.stronglyMeasurableAtFilter _ _
    · exact hcont.continuousAt
  have h2 : HasDerivAt (fun _ : ℝ => Complex.arg ((1 - a) / (1 - starRingEnd ℂ a))) 0 θ :=
    hasDerivAt_const θ _
  have h3 := h2.add h1
  simp only [zero_add] at h3
  exact h3

theorem invMobiusAngle_add_two_pi (a : ℂ) (ha : a ∈ ball (0 : ℂ) 1) (θ : ℝ) :
    invMobiusAngle a ha (θ + 2 * π) = invMobiusAngle a ha θ + 2 * π := by
  simp only [invMobiusAngle]
  have hcont := continuous_poissonKernel_circleMap a ha
  suffices h : ∫ t in (0 : ℝ)..(θ + 2 * π), poissonKernel 0 a (circleMap 0 1 t) =
      (∫ t in (0 : ℝ)..θ, poissonKernel 0 a (circleMap 0 1 t)) + 2 * π by linarith
  have hint : ∀ (x y : ℝ), IntervalIntegrable
      (fun t => poissonKernel 0 a (circleMap 0 1 t)) volume x y :=
    hcont.intervalIntegrable
  have hsplit := intervalIntegral.integral_add_adjacent_intervals
    (hint 0 θ) (hint θ (θ + 2 * π))
  have hperiod : Function.Periodic (fun t => poissonKernel 0 a (circleMap 0 1 t)) (2 * π) := by
    intro t; show poissonKernel 0 a (circleMap 0 1 (t + 2 * π)) =
      poissonKernel 0 a (circleMap 0 1 t)
    rw [periodic_circleMap 0 1 t]
  have hshift := hperiod.intervalIntegral_add_eq 0 θ
  simp only [zero_add] at hshift
  have h_int_eq : ∫ t in (0 : ℝ)..(2 * π), poissonKernel 0 a (circleMap 0 1 t) = 2 * π := by
    have h4 : Real.circleAverage (poissonKernel 0 a • fun _ => (1 : ℝ)) 0 1 = 1 := by
      apply InnerProductSpace.HarmonicOnNhd.circleAverage_poissonKernel_smul
      · exact fun z _ => harmonicAt_const 1
      · exact ha
    rw [Real.circleAverage_def] at h4
    have key : ∀ t, (poissonKernel 0 a • fun _ => (1 : ℝ)) (circleMap 0 1 t) =
        poissonKernel 0 a (circleMap 0 1 t) := by
      intro t; simp [smul_eq_mul]
    simp_rw [key] at h4
    rw [smul_eq_mul] at h4
    have hpi : (0 : ℝ) < 2 * π := by positivity
    nlinarith [mul_inv_cancel₀ (ne_of_gt hpi)]
  linarith

lemma norm_circleMap_zero_one (θ : ℝ) : ‖circleMap 0 1 θ‖ = 1 := by
  have h := circleMap_mem_sphere 0 one_pos.le θ
  rw [Metric.mem_sphere, dist_zero_right] at h; exact h

lemma poissonKernel_nonneg_circleMap (a : ℂ) (ha : a ∈ ball (0 : ℂ) 1) (θ : ℝ) :
    0 ≤ poissonKernel 0 a (circleMap 0 1 θ) := by
  simp only [poissonKernel_def, sub_zero]
  apply div_nonneg
  · rw [norm_circleMap_zero_one, one_pow, sub_nonneg, sq_le_one_iff_abs_le_one, abs_norm]
    rw [mem_ball, dist_zero_right] at ha; exact ha.le
  · positivity

theorem poissonIntegral_eq_circleAverage_mobiusTransform
    (U : ℂ → ℝ) (hU : CircleIntegrable U 0 1) (a : ℂ) (ha : a ∈ ball (0 : ℂ) 1) :
    poissonIntegral U a = Real.circleAverage (U ∘ mobiusTransform a) 0 1 := by
  simp only [poissonIntegral, Real.circleAverage]
  congr 1
  set ψ := invMobiusAngle a ha
  set φ' : ℝ → ℝ := fun θ => poissonKernel 0 a (circleMap 0 1 θ)
  set g : ℝ → ℝ := fun t => U (mobiusTransform a (circleMap 0 1 t))

  have h_eq : ∀ θ, (poissonKernel 0 a • U) (circleMap 0 1 θ) = φ' θ • (g ∘ ψ) θ := by
    intro θ
    simp only [smul_eq_mul, Function.comp_apply]
    show poissonKernel 0 a (circleMap 0 1 θ) * U (circleMap 0 1 θ) =
      poissonKernel 0 a (circleMap 0 1 θ) * U (mobiusTransform a (circleMap 0 1 (ψ θ)))
    rw [invMobiusAngle_mobiusTransform]
  simp_rw [h_eq]

  have hcov : ∫ θ in (0 : ℝ)..2 * π, φ' θ • (g ∘ ψ) θ =
      ∫ u in ψ 0..ψ (2 * π), g u := by
    apply intervalIntegral.integral_deriv_smul_comp_of_deriv_nonneg
    · exact (continuous_iff_continuousAt.mpr
        (fun x => (hasDerivAt_invMobiusAngle a ha x).continuousAt)).continuousOn
    · intro x _; exact hasDerivAt_invMobiusAngle a ha x
    · intro x _; exact poissonKernel_nonneg_circleMap a ha x
  rw [hcov]

  have hψ_shift : ψ (2 * π) = ψ 0 + 2 * π := by
    have := invMobiusAngle_add_two_pi a ha 0; simp only [zero_add] at this; exact this
  rw [hψ_shift]

  have hg_periodic : Function.Periodic g (2 * π) := by
    intro t
    show U (mobiusTransform a (circleMap 0 1 (t + 2 * π))) =
      U (mobiusTransform a (circleMap 0 1 t))
    rw [periodic_circleMap 0 1 t]
  rw [hg_periodic.intervalIntegral_add_eq (ψ 0) 0, zero_add]
  simp only [g, Function.comp_apply]

theorem mobiusTransform_tendsto_on_circle
    (z₀ : ℂ) (hz₀ : z₀ ∈ sphere (0 : ℂ) 1) :
    ∀ᵐ θ ∂MeasureTheory.volume, θ ∈ Set.uIoc (0 : ℝ) (2 * π) →
      Filter.Tendsto (fun a => mobiusTransform a (circleMap 0 1 θ))
        (nhdsWithin z₀ (ball 0 1)) (nhds z₀) := by
  have hnorm : ‖z₀‖ = 1 := mem_sphere_zero_iff_norm.mp hz₀
  have hz₀_ne : z₀ ≠ 0 := by
    intro h; simp [h] at hnorm

  have hstar_mul : star z₀ * z₀ = 1 := by
    have hinv : (starRingEnd ℂ z₀) = z₀⁻¹ := (RCLike.inv_eq_conj hnorm).symm
    rw [starRingEnd_apply] at hinv
    rw [hinv]
    exact inv_mul_cancel₀ hz₀_ne

  have hbad : (circleMap 0 1 ⁻¹' {-z₀}).Countable :=
    (Set.countable_singleton _).preimage_circleMap 0 one_ne_zero
  filter_upwards [hbad.ae_notMem volume] with θ hθne _hθ_mem
  simp only [Set.mem_preimage, Set.mem_singleton_iff] at hθne
  set z := circleMap 0 1 θ

  have hzz₀_ne : z + z₀ ≠ 0 := by
    intro h; exact hθne (by linear_combination h)

  have hdenom_ne : starRingEnd ℂ z₀ * z + 1 ≠ 0 := by
    rw [starRingEnd_apply, show star z₀ * z + 1 = star z₀ * (z + z₀) from by
      rw [mul_add, hstar_mul]]
    exact mul_ne_zero (by rwa [ne_eq, star_eq_zero]) hzz₀_ne

  have hval : mobiusTransform z₀ z = z₀ := by
    simp only [mobiusTransform, starRingEnd_apply]
    rw [show star z₀ * z + 1 = star z₀ * (z + z₀) from by rw [mul_add, hstar_mul]]
    rw [div_mul_eq_div_div_swap, div_self hzz₀_ne, one_div]
    have h_inv : z₀⁻¹ = star z₀ := by
      rw [RCLike.inv_eq_conj hnorm, starRingEnd_apply]
    rw [← h_inv, inv_inv]

  have hcont : ContinuousAt (fun a => mobiusTransform a z) z₀ := by
    show ContinuousAt (fun a => (z + a) / (starRingEnd ℂ a * z + 1)) z₀
    apply ContinuousAt.div
    · exact continuousAt_const.add continuousAt_id
    · have : ContinuousAt (fun a => star a * z + 1) z₀ :=
        (continuous_star.continuousAt.mul continuousAt_const).add continuousAt_const
      simp only [← starRingEnd_apply] at this
      exact this
    · exact hdenom_ne
  rw [show nhds z₀ = nhds (mobiusTransform z₀ z) from congr_arg nhds hval.symm]
  exact hcont.tendsto.mono_left nhdsWithin_le_nhds

theorem circleAverage_mobiusTransform_aestronglyMeasurable
    (U : ℂ → ℝ) (hU : CircleIntegrable U 0 1)
    (z₀ : ℂ) (_hz₀ : z₀ ∈ sphere (0 : ℂ) 1) :
    ∀ᶠ a in nhdsWithin z₀ (ball 0 1),
      AEStronglyMeasurable (fun θ => U (mobiusTransform a (circleMap 0 1 θ)))
        (MeasureTheory.volume.restrict (Set.uIoc (0 : ℝ) (2 * π))) := by
  apply Filter.Eventually.mono (eventually_of_mem self_mem_nhdsWithin (fun a ha => ha))
  intro a ha
  set ψ := invMobiusAngle a ha
  set g : ℝ → ℝ := fun t => U (mobiusTransform a (circleMap 0 1 t))

  have hg_periodic : Function.Periodic g (2 * π) := by
    intro t; show U (mobiusTransform a (circleMap 0 1 (t + 2 * π))) =
      U (mobiusTransform a (circleMap 0 1 t)); rw [periodic_circleMap 0 1 t]

  have hgψ : ∀ θ, (g ∘ ψ) θ = U (circleMap 0 1 θ) := by
    intro θ; simp only [Function.comp_apply, g]; rw [invMobiusAngle_mobiusTransform]

  have hψ_cont : ContinuousOn ψ (Set.uIcc 0 (2 * π)) :=
    (continuous_iff_continuousAt.mpr
      (fun x => (hasDerivAt_invMobiusAngle a ha x).continuousAt)).continuousOn

  have hprod : IntervalIntegrable
      (fun θ => poissonKernel 0 a (circleMap 0 1 θ) • (g ∘ ψ) θ) volume 0 (2 * π) := by
    simp_rw [smul_eq_mul, hgψ]
    have hP_cont : ContinuousOn (fun θ => poissonKernel 0 a (circleMap 0 1 θ))
        (Set.uIcc 0 (2 * π)) := by
      apply ContinuousOn.mono (Continuous.continuousOn _) (Set.subset_univ _)
      simp only [poissonKernel_def, sub_zero]
      apply Continuous.div
      · exact ((continuous_norm.comp (continuous_circleMap 0 1)).pow 2).sub continuous_const
      · exact (continuous_norm.comp ((continuous_circleMap 0 1).sub continuous_const)).pow 2
      · intro θ
        apply pow_ne_zero 2; rw [norm_ne_zero_iff]
        intro heq
        have ha' := sub_eq_zero.mp heq
        have hn := norm_circleMap_zero_one θ
        rw [ha'] at hn
        rw [mem_ball, dist_zero_right] at ha; linarith
    exact hU.continuousOn_mul hP_cont

  have hg_ii_shifted : IntervalIntegrable g volume (ψ 0) (ψ (2 * π)) := by
    rw [← intervalIntegral.integrable_deriv_smul_comp_iff_of_deriv_nonneg hψ_cont
      (fun x _ => hasDerivAt_invMobiusAngle a ha x)
      (fun x _ => poissonKernel_nonneg_circleMap a ha x)]
    exact hprod

  have hψ_shift : ψ (2 * π) = ψ 0 + 2 * π := by
    have := invMobiusAngle_add_two_pi a ha 0; simp only [zero_add] at this; exact this
  rw [hψ_shift] at hg_ii_shifted

  have hg_ii : IntervalIntegrable g volume 0 (2 * π) := by
    have := (@Function.Periodic.intervalIntegrable_iff _ _ g (2 * π) (ψ 0) 0
      hg_periodic).mp hg_ii_shifted
    simpa using this

  rw [show Set.uIoc (0 : ℝ) (2 * π) = Set.Ioc 0 (2 * π) from Set.uIoc_of_le (by positivity)]
  exact hg_ii.aestronglyMeasurable

theorem circleAverage_mobiusTransform_bound
    (U : ℂ → ℝ) (hU : CircleIntegrable U 0 1)
    (hUbd : ∃ M : ℝ, ∀ z, ‖U z‖ ≤ M)
    (z₀ : ℂ) (hz₀ : z₀ ∈ sphere (0 : ℂ) 1) :
    ∃ bound : ℝ → ℝ,
      IntervalIntegrable bound MeasureTheory.volume (0 : ℝ) (2 * π) ∧
      ∀ᶠ a in nhdsWithin z₀ (ball 0 1),
        ∀ᵐ θ ∂MeasureTheory.volume, θ ∈ Set.uIoc (0 : ℝ) (2 * π) →
          ‖U (mobiusTransform a (circleMap 0 1 θ))‖ ≤ bound θ := by
  obtain ⟨M, hM⟩ := hUbd
  exact ⟨fun _ => M, intervalIntegrable_const,
    Filter.Eventually.of_forall (fun _ => Filter.Eventually.of_forall (fun _ _ => hM _))⟩

theorem circleAverage_mobiusTransform_tendsto
    (U : ℂ → ℝ) (hU : CircleIntegrable U 0 1)
    (hUbd : ∃ M : ℝ, ∀ z, ‖U z‖ ≤ M)
    (z₀ : ℂ) (hz₀ : z₀ ∈ sphere (0 : ℂ) 1) (hcont : ContinuousAt U z₀) :
    Filter.Tendsto (fun a => Real.circleAverage (U ∘ mobiusTransform a) 0 1)
      (nhdsWithin z₀ (ball 0 1)) (nhds (U z₀)) := by

  simp only [Real.circleAverage_def, Function.comp_def]


  have h_ptwise := mobiusTransform_tendsto_on_circle z₀ hz₀
  obtain ⟨bound, h_bound_int, h_bound⟩ := circleAverage_mobiusTransform_bound U hU hUbd z₀ hz₀
  have h_meas := circleAverage_mobiusTransform_aestronglyMeasurable U hU z₀ hz₀

  have h_lim : ∀ᵐ θ ∂MeasureTheory.volume, θ ∈ Set.uIoc (0 : ℝ) (2 * π) →
      Filter.Tendsto (fun a => U (mobiusTransform a (circleMap 0 1 θ)))
        (nhdsWithin z₀ (ball 0 1)) (nhds (U z₀)) := by
    filter_upwards [h_ptwise] with θ hθ hθ_mem
    exact hcont.tendsto.comp (hθ hθ_mem)

  have h_integral_tendsto := intervalIntegral.tendsto_integral_filter_of_dominated_convergence
    bound h_meas h_bound h_bound_int h_lim


  have h_const_integral : ∫ θ in (0 : ℝ)..2 * π, U z₀ = 2 * π * U z₀ := by
    rw [intervalIntegral.integral_const, sub_zero, smul_eq_mul]

  rw [h_const_integral] at h_integral_tendsto
  have h_smul_tendsto : Filter.Tendsto
    (fun a => (2 * (π : ℝ))⁻¹ • ∫ θ in (0 : ℝ)..2 * π, U (mobiusTransform a (circleMap 0 1 θ)))
    (nhdsWithin z₀ (ball 0 1)) (nhds ((2 * π)⁻¹ • (2 * π * U z₀))) :=
    h_integral_tendsto.const_smul _
  rwa [show (2 * (π : ℝ))⁻¹ • (2 * π * U z₀) = U z₀ from by
    rw [smul_eq_mul, inv_mul_cancel_left₀ (by positivity)]] at h_smul_tendsto

theorem poissonIntegral_tendsto_boundary
    (U : ℂ → ℝ) (hU : CircleIntegrable U 0 1)
    (hUbd : ∃ M : ℝ, ∀ z, ‖U z‖ ≤ M)
    (z₀ : ℂ) (hz₀ : z₀ ∈ sphere (0 : ℂ) 1) (hcont : ContinuousAt U z₀) :
    Filter.Tendsto (poissonIntegral U) (nhdsWithin z₀ (ball 0 1)) (nhds (U z₀)) := by


  apply (circleAverage_mobiusTransform_tendsto U hU hUbd z₀ hz₀ hcont).congr'
  filter_upwards [self_mem_nhdsWithin] with a ha
  exact (poissonIntegral_eq_circleAverage_mobiusTransform U hU a ha).symm

lemma bounded_continuous_extension_of_sphere {g : ℂ → ℝ}
    (hg : ContinuousOn g (sphere (0 : ℂ) 1)) :
    ∃ U : ℂ → ℝ, Continuous U ∧ (∃ M : ℝ, ∀ z, ‖U z‖ ≤ M) ∧
      EqOn U g (sphere 0 1) := by
  let boundaryC : C(sphere (0 : ℂ) 1, ℝ) :=
    ⟨fun z => g z, continuousOn_iff_continuous_restrict.mp hg⟩
  let boundary : BoundedContinuousFunction (sphere (0 : ℂ) 1) ℝ :=
    ContinuousMap.equivBoundedOfCompact _ _ boundaryC
  obtain ⟨extension, _hextNorm, hext⟩ :=
    BoundedContinuousFunction.exists_norm_eq_restrict_eq (𝕜 := ℝ)
      (isClosed_sphere : IsClosed (sphere (0 : ℂ) 1)) boundary
  refine ⟨(extension : ℂ → ℝ), extension.continuous, ⟨‖extension‖, ?_⟩, ?_⟩
  · intro z
    exact extension.norm_coe_le_norm z
  · intro z hz
    let zh : sphere (0 : ℂ) 1 := ⟨z, hz⟩
    have heq : extension zh = boundary zh := by
      exact DFunLike.congr_fun hext zh
    simpa [boundary, boundaryC] using heq

theorem unitDiskConstruction {g : ℂ → ℝ}
    (hg : ContinuousOn g (sphere (0 : ℂ) 1)) :
    ∃ u : ℂ → ℝ,
      HarmonicOnNhd u (ball 0 1) ∧
        ContinuousOn u (closedBall 0 1) ∧ EqOn u g (sphere 0 1) := by
  obtain ⟨U, hUc, hUbd, hUg⟩ := bounded_continuous_extension_of_sphere hg
  have hUint : CircleIntegrable U 0 1 :=
    hUc.continuousOn.circleIntegrable' (c := 0) (R := 1)
  have hboundary : ∀ z0 ∈ sphere (0 : ℂ) 1,
      Tendsto (poissonIntegral U) (nhdsWithin z0 (ball 0 1)) (nhds (U z0)) := by
    intro z0 hz0
    exact poissonIntegral_tendsto_boundary U hUint hUbd z0 hz0 hUc.continuousAt
  refine ⟨unitDiskExtension U, unitDiskExtension_harmonic U hUint,
    unitDiskExtension_continuousOn U hUc hboundary, ?_⟩
  exact (unitDiskExtension_eqOn_sphere U).trans hUg

lemma normalize_mem_ball {c x : ℂ} {R : ℝ} (hR : 0 < R) :
    (x - c) / R ∈ ball (0 : ℂ) 1 ↔ x ∈ ball c R := by
  rw [mem_ball, dist_zero_right, norm_div, norm_real, Real.norm_eq_abs, abs_of_pos hR,
    mem_ball, dist_eq_norm, div_lt_one hR]

lemma normalize_mem_closedBall {c x : ℂ} {R : ℝ} (hR : 0 < R) :
    (x - c) / R ∈ closedBall (0 : ℂ) 1 ↔ x ∈ closedBall c R := by
  rw [mem_closedBall, dist_zero_right, norm_div, norm_real, Real.norm_eq_abs, abs_of_pos hR,
    mem_closedBall, dist_eq_norm, div_le_one hR]

lemma normalize_mem_sphere {c x : ℂ} {R : ℝ} (hR : 0 < R) :
    (x - c) / R ∈ sphere (0 : ℂ) 1 ↔ x ∈ sphere c R := by
  rw [mem_sphere, dist_zero_right, norm_div, norm_real, Real.norm_eq_abs, abs_of_pos hR,
    mem_sphere, dist_eq_norm]
  constructor <;> intro h
  · calc
      ‖x - c‖ = (‖x - c‖ / R) * R := by field_simp
      _ = R := by rw [h, one_mul]
  · rw [h, div_self hR.ne']

lemma denormalize_mem_sphere {c z : ℂ} {R : ℝ} (hR : 0 < R) :
    R * z + c ∈ sphere c R ↔ z ∈ sphere (0 : ℂ) 1 := by
  rw [← normalize_mem_sphere hR]
  constructor <;> intro hz
  · simpa [hR.ne'] using hz
  · simpa [hR.ne'] using hz

lemma normalized_boundary_continuousOn {c : ℂ} {R : ℝ} (hR : 0 < R)
    {g : ℂ → ℝ} (hg : ContinuousOn g (sphere c R)) :
    ContinuousOn (fun z => g (R * z + c)) (sphere (0 : ℂ) 1) := by
  apply hg.comp (by fun_prop)
  intro z hz
  exact (denormalize_mem_sphere hR).2 hz

lemma harmonicAt_comp_affine_of_realpart
    {v : ℂ → ℝ} {F : ℂ → ℂ} {x c : ℂ} {R : ℝ}
    (_hR : R ≠ 0)
    (hF : AnalyticAt ℂ F ((x - c) / R))
    (hEq : ∀ᶠ y in nhds ((x - c) / R), (F y).re = v y) :
    HarmonicAt (fun w => v ((w - c) / R)) x := by
  let aff : ℂ → ℂ := fun w => (w - c) / R
  have hAff : AnalyticAt ℂ aff x := by fun_prop
  have hF' : AnalyticAt ℂ F (aff x) := by simpa [aff] using hF
  have hcomp : AnalyticAt ℂ (F ∘ aff) x := hF'.comp hAff
  have hh : HarmonicAt (fun w => (F (aff w)).re) x := hcomp.harmonicAt_re
  apply (harmonicAt_congr_nhds (f₁ := fun w => (F (aff w)).re)
    (f₂ := fun w => v (aff w)) ?_).mp hh
  filter_upwards [show ∀ᶠ w in nhds x, aff w ∈ {y | (F y).re = v y} from
    (show Tendsto aff (nhds x) (nhds ((x - c) / R)) by
      simpa [aff] using (show ContinuousAt aff x by fun_prop)) hEq] with w hw
  exact hw

lemma harmonicOnNhd_affine_pullback
    {v : ℂ → ℝ} {c : ℂ} {R : ℝ} (hR : 0 < R)
    (hv : HarmonicOnNhd v (ball 0 1)) :
    HarmonicOnNhd (fun w => v ((w - c) / R)) (ball c R) := by
  intro x hx
  have hx' : (x - c) / R ∈ ball (0 : ℂ) 1 := (normalize_mem_ball hR).2 hx
  obtain ⟨F, hF, hEq⟩ := hv.exists_analyticOnNhd_ball_re_eq
  apply harmonicAt_comp_affine_of_realpart hR.ne'
  · exact hF ((x - c) / R) hx'
  · exact eventually_of_mem (isOpen_ball.mem_nhds hx') hEq

lemma continuousOn_affine_pullback {v : ℂ → ℝ} {c : ℂ} {R : ℝ} (hR : 0 < R)
    (hv : ContinuousOn v (closedBall (0 : ℂ) 1)) :
    ContinuousOn (fun w => v ((w - c) / R)) (closedBall c R) := by
  apply hv.comp (by fun_prop)
  intro x hx
  exact (normalize_mem_closedBall hR).2 hx

lemma eqOn_affine_pullback {v g : ℂ → ℝ} {c : ℂ} {R : ℝ} (hR : 0 < R)
    (hv : EqOn v (fun z => g (R * z + c)) (sphere (0 : ℂ) 1)) :
    EqOn (fun w => v ((w - c) / R)) g (sphere c R) := by
  intro x hx
  have hx' : (x - c) / R ∈ sphere (0 : ℂ) 1 := (normalize_mem_sphere hR).2 hx
  change v ((x - c) / R) = g x
  rw [hv hx']
  change g ((R : ℂ) * ((x - c) / (R : ℂ)) + c) = g x
  have hcast : (R : ℂ) ≠ 0 := by exact_mod_cast hR.ne'
  congr 1
  field_simp
  abel

theorem generalDiskConstruction (c : ℂ) (R : ℝ) (hR : 0 < R)
    (g : ℂ → ℝ) (hg : ContinuousOn g (sphere c R)) :
    ∃ u : ℂ → ℝ,
      HarmonicOnNhd u (ball c R) ∧
        ContinuousOn u (closedBall c R) ∧ EqOn u g (sphere c R) := by
  obtain ⟨v, hvH, hvC, hvG⟩ :=
    unitDiskConstruction (normalized_boundary_continuousOn hR hg)
  refine ⟨fun w => v ((w - c) / R), ?_, ?_, ?_⟩
  · exact harmonicOnNhd_affine_pullback hR hvH
  · exact continuousOn_affine_pullback hR hvC
  · exact eqOn_affine_pullback hR hvG

#print axioms poissonIntegral_eq_re_herglotzIntegral
#print axioms herglotzIntegral_differentiableOn
#print axioms poissonIntegral_harmonic
#print axioms unitDiskExtension_harmonic
#print axioms unitDiskExtension_eqOn_sphere
#print axioms unitDiskExtension_continuousOn
#print axioms unitKernelMass
#print axioms unitPoissonKernel_nonneg
#print axioms boundaryData_uniformContinuousOn
#print axioms continuous_extension_of_sphere
#print axioms invMobiusAngle_mobiusTransform_core
#print axioms poissonIntegral_eq_circleAverage_mobiusTransform
#print axioms mobiusTransform_tendsto_on_circle
#print axioms circleAverage_mobiusTransform_tendsto
#print axioms poissonIntegral_tendsto_boundary
#print axioms bounded_continuous_extension_of_sphere
#print axioms unitDiskConstruction
#print axioms harmonicOnNhd_affine_pullback
#print axioms continuousOn_affine_pullback
#print axioms eqOn_affine_pullback
#print axioms generalDiskConstruction

end Stage1Instances.THM_M_1148.PoissonUnitDisk
