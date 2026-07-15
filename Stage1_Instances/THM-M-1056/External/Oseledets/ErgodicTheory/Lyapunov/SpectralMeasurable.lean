/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.ForwardV

/-!
# Measurability of spectral sublevel projectors

For a measurable family of self-adjoint real matrices, the orthogonal projection onto the
eigenspace for eigenvalues `≤ t` is measurable in the parameter. Since this projector is the
continuous functional calculus of the *discontinuous* indicator `Set.indicator (Set.Iic t) 1`,
measurability is obtained by approximating the indicator from above by continuous downward ramps
`gApprox t m`, whose CFCs are measurable, and passing to the entrywise pointwise limit. The main
results are `measurable_spectralProjector` and its specialization `measurable_slowProjector` to
the sanitized Oseledets limit `lambdaHat`.
-/

open MeasureTheory Filter Topology Matrix
open scoped Matrix

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ} [NeZero d]

/-- A continuous approximation to `indicator (Iic t) 1`: a downward ramp from `1` (at `s = t`)
to `0` (at `s = t + 1/(m+1)`), clamped to `[0,1]`. -/
noncomputable def gApprox (t : ℝ) (m : ℕ) : ℝ → ℝ :=
  fun s => max 0 (min 1 ((t + 1 / (m + 1) - s) * (m + 1)))

theorem continuous_gApprox (t : ℝ) (m : ℕ) : Continuous (gApprox t m) := by
  unfold gApprox
  fun_prop

/-- For `s ≤ t`, the ramp is exactly `1`, agreeing with the indicator. -/
theorem gApprox_of_le (t : ℝ) (m : ℕ) {s : ℝ} (hs : s ≤ t) : gApprox t m s = 1 := by
  unfold gApprox
  have hm : (0 : ℝ) < (m : ℝ) + 1 := by positivity
  have h1 : (1 : ℝ) ≤ (t + 1 / (m + 1) - s) * (m + 1) := by
    have : (1 : ℝ) / (m + 1) ≤ t + 1 / (m + 1) - s := by linarith
    calc (1 : ℝ) = (1 / (m + 1)) * (m + 1) := by field_simp
      _ ≤ (t + 1 / (m + 1) - s) * (m + 1) := by
          apply mul_le_mul_of_nonneg_right this hm.le
  rw [min_eq_left h1, max_eq_right (by norm_num)]

/-- For `s > t`, eventually (once `1/(m+1) < s - t`) the ramp is `0`, agreeing with the
indicator. -/
theorem gApprox_eventually_zero (t : ℝ) {s : ℝ} (hs : t < s) :
    ∀ᶠ m in atTop, gApprox t m s = 0 := by
  -- need 1/(m+1) ≤ s - t, i.e. m+1 ≥ 1/(s-t)
  obtain ⟨N, hN⟩ := exists_nat_gt (1 / (s - t))
  filter_upwards [eventually_ge_atTop N] with m hm
  unfold gApprox
  have hmN : (N : ℝ) ≤ (m : ℝ) := by exact_mod_cast hm
  have hst : (0 : ℝ) < s - t := by linarith
  have hle : (1 : ℝ) / (s - t) ≤ (m : ℝ) := le_trans hN.le hmN
  have h1 : (1 : ℝ) / (m + 1) ≤ s - t := by
    rw [div_le_iff₀ (by positivity)]
    have : (1 : ℝ) ≤ (s - t) * m := by
      rw [div_le_iff₀ hst] at hle; linarith
    nlinarith
  have hneg : (t + 1 / (m + 1) - s) * (m + 1) ≤ 0 := by
    have : t + 1 / (m + 1) - s ≤ 0 := by linarith
    apply mul_nonpos_of_nonpos_of_nonneg this (by positivity)
  rw [min_eq_right (le_trans hneg (by norm_num)), max_eq_left hneg]

/-- At every point, `gApprox t m s` is eventually equal to `indicator (Iic t) 1 s`. -/
theorem gApprox_eventually_eq_indicator (t : ℝ) (s : ℝ) :
    ∀ᶠ m in atTop, gApprox t m s = Set.indicator (Set.Iic t) (1 : ℝ → ℝ) s := by
  by_cases hs : s ≤ t
  · filter_upwards with m
    rw [gApprox_of_le t m hs, Set.indicator_of_mem (by simpa using hs), Pi.one_apply]
  · rw [not_le] at hs
    filter_upwards [gApprox_eventually_zero t hs] with m hm
    rw [hm, Set.indicator_of_notMem (by simp; linarith)]

/-- Uniform convergence on the finite spectrum: on a finite set, the eventual pointwise equality of
`gApprox t m` with the indicator upgrades to uniform convergence. -/
theorem tendstoUniformlyOn_gApprox (t : ℝ) {S : Set ℝ} (hS : S.Finite) :
    TendstoUniformlyOn (gApprox t) (Set.indicator (Set.Iic t) (1 : ℝ → ℝ)) atTop S := by
  rw [Metric.tendstoUniformlyOn_iff]
  intro ε hε
  -- For each s ∈ S, eventually gApprox t m s = indicator s; take the finite intersection.
  have hev : ∀ s ∈ S, ∀ᶠ m in atTop,
      dist (Set.indicator (Set.Iic t) (1 : ℝ → ℝ) s) (gApprox t m s) < ε := by
    intro s _
    filter_upwards [gApprox_eventually_eq_indicator t s] with m hm
    rw [hm, dist_self]; exact hε
  exact (hS.eventually_all.2 hev).mono fun m hm s hs => hm s hs

omit [NeZero d] in
/-- **Spectral CFC convergence.** For a self-adjoint matrix `M`, the continuous CFCs of the
ramp `gApprox t m` converge (in the matrix topology) to the CFC of the discontinuous indicator. -/
theorem tendsto_cfc_gApprox (t : ℝ) (M : Matrix (Fin d) (Fin d) ℝ) :
    Tendsto (fun m => cfc (gApprox t m) M) atTop
      (𝓝 (cfc (Set.indicator (Set.Iic t) (1 : ℝ → ℝ)) M)) := by
  apply tendsto_cfc_fun
  · exact tendstoUniformlyOn_gApprox t M.finite_real_spectrum
  · filter_upwards with m
    exact (continuous_gApprox t m).continuousOn

omit [NeZero d] in
/-- For a measurable family `M : X → matrix` of self-adjoint real matrices, the spectral sublevel
projector `x ↦ cfc (Set.indicator (Set.Iic t) 1) (M x)` — the orthogonal projection onto the `≤ t`
eigenspace — is measurable. The indicator is *discontinuous*, so this is obtained as the entrywise
pointwise limit of the measurable continuous-CFC ramps `cfc (gApprox t m) (M x)`. -/
theorem measurable_spectralProjector
    (t : ℝ) (M : X → Matrix (Fin d) (Fin d) ℝ)
    (hM : Measurable M) (hMsa : ∀ x, IsSelfAdjoint (M x)) :
    Measurable (fun x => cfc (Set.indicator (Set.Iic t) (1 : ℝ → ℝ)) (M x)) := by
  -- entrywise: it suffices to prove each (i,j) entry is measurable
  refine measurable_pi_iff.2 fun i => measurable_pi_iff.2 fun j => ?_
  -- each ramp's entry is measurable (continuous CFC of a measurable self-adjoint family)
  have hentry : ∀ m, Measurable (fun x => (cfc (gApprox t m) (M x)) i j) := by
    intro m
    have hcfc : Measurable (fun x => cfc (gApprox t m) (M x)) :=
      measurable_cfc_continuous (gApprox t m) (continuous_gApprox t m) M hM hMsa
    exact ((measurable_pi_apply j).comp (measurable_pi_apply i)).comp hcfc
  -- pointwise (entrywise) convergence to the indicator CFC
  refine measurable_of_tendsto_metrizable hentry ?_
  rw [tendsto_pi_nhds]; intro x
  exact ((continuous_matrix_entry i j).tendsto _).comp (tendsto_cfc_gApprox t (M x))

/-- Measurability of the slow (sublevel) spectral projector family
`x ↦ slowProjector A T t x = cfc (indicator (Iic t) 1) (lambdaHat A T x)`, obtained by composing
the spectral-projector measurability with the measurability and everywhere self-adjointness of the
sanitized Oseledets limit `lambdaHat`. -/
theorem measurable_slowProjector
    (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (t : ℝ)
    (hAmeas : Measurable A) (hTmeas : Measurable T) :
    Measurable (fun x => ErgodicTheory.slowProjector A T t x) :=
  measurable_spectralProjector t (lambdaHat A T)
    (measurable_lambdaHat hAmeas hTmeas)
    (fun x => lambdaHat_isSelfAdjoint A T x)

end ErgodicTheory
