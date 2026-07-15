/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.FiltrationFromSpectralUpper
import ErgodicTheory.Lyapunov.SpectrumResiduals

/-!
# The Oseledets filtration from the spectral-identification hypothesis

This file proves the Oseledets filtration theorem `ErgodicTheory.oseledets_filtration_of_upper'`, in
which the band-projector convergence hypothesis `hband` is replaced by the spectral-identification
hypothesis `hident`, and the lower-bound step `hlb` is accordingly obtained from
`specList_le_liminf_inv_mul_log_norm_cocycle_apply_of_slowflag` (fed `hident` and the slow-flag
datum `hslowflag` computed earlier in the proof) instead of
`specList_le_liminf_inv_mul_log_norm_cocycle_apply_of_bandProjector`.

## Main results

* `ErgodicTheory.oseledets_filtration_of_upper'`: the Oseledets filtration theorem, conditional
  on the a.e. spectral upper bound over the slow flag, the reverse slow-flag inclusion, the
  two spectrum inclusions, and the spectral-identification band-projector limit.
-/

open MeasureTheory Filter Topology Matrix
open scoped Matrix Matrix.Norms.L2Operator

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ} [NeZero d]

/-- **Oseledets filtration theorem, via the spectral-identification hypothesis.**

The Oseledets filtration theorem with the band-projector hypothesis `hband`
replaced by the spectral-identification hypothesis `hident`, consumed by
`specList_le_liminf_inv_mul_log_norm_cocycle_apply_of_slowflag`. -/
theorem oseledets_filtration_of_upper'
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X}
    (hT : Ergodic T μ) (hTmeas : Measurable T)
    {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    -- The spectral upper bound: vectors of the slow subspace grow at most at the cut rate.
    (hupper : ∀ᵐ x ∂μ, ∀ t : ℝ, ∀ v ∈ vslow A T (Real.exp t) x, v ≠ 0 →
      Filter.limsup (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) Filter.atTop ≤ t)
    -- The reverse slow-flag inclusion: slow growth implies membership in the slow subspace.
    (hslowrev : ∀ᵐ x ∂μ, ∀ t : ℝ, lambdaSublevel A T x t ≤ vslow A T (Real.exp t) x)
    -- Spectrum upper inclusion: every realized exponent is a deterministic one.
    (hub_spec : ∀ lam0 : ℕ → ℝ,
      (∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Tendsto
        (fun n : ℕ => (n : ℝ)⁻¹ *
          Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
        atTop (𝓝 (lam0 i))) →
      ∀ᵐ x ∂μ, lyapunovSpectrum A T x ⊆ distinctExp lam0 d)
    -- Spectrum lower inclusion: every deterministic exponent is attained.
    (hlb_spec : ∀ lam0 : ℕ → ℝ,
      (∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Tendsto
        (fun n : ℕ => (n : ℝ)⁻¹ *
          Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
        atTop (𝓝 (lam0 i))) →
      ∀ᵐ x ∂μ, distinctExp lam0 d ⊆ lyapunovSpectrum A T x)
    -- The spectral-identification band-projector convergence hypothesis.
    (hident : ∀ᵐ x ∂μ, ∀ c : ℝ, 0 < c →
      (∀ i : Fin d, Real.exp (lamSing A T x (i : ℕ)) ≠ c) →
      Filter.Tendsto (fun n : ℕ => bandProjector A T (Set.indicator (Set.Ioi c) 1) n x)
        Filter.atTop (𝓝 (cfc (Set.indicator (Set.Ioi c) (1 : ℝ → ℝ)) (lambdaHat A T x)))) :
    ∃ (k : ℕ) (lam : Fin k → ℝ)
      (V : Fin (k + 1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin d))),
      StrictAnti lam ∧
      (∀ i, MeasurableSubspace fun x => V i x) ∧
      ∀ᵐ x ∂μ,
        V 0 x = ⊤ ∧ V (Fin.last k) x = ⊥ ∧
        (∀ i : Fin k, V i.succ x < V i.castSucc x) ∧
        (∀ i : Fin (k + 1),
          Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap (V i x) =
            V i (T x)) ∧
        (∀ i : Fin k, ∀ v ∈ (V i.castSucc x : Set (EuclideanSpace ℝ (Fin d))),
            v ∉ V i.succ x →
            Tendsto
              (fun n : ℕ => (n : ℝ)⁻¹ *
                Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖)
              atTop (𝓝 (lam i))) := by
  classical
  -- The deterministic singular-value exponents.
  obtain ⟨lam0, _hmono, hlam0⟩ :=
    exists_lam_tendsto_singularValue hT hA hAmeas hint hint'
  -- `hspec` from the two spectrum inclusions.
  have hspec := specList_eq_expEnum_of_subsets_standing hT A hA hAmeas hint hint' lam0
    (hub_spec lam0 hlam0) (hlb_spec lam0 hlam0)
  -- `hslowflag` from `hupper` and the reverse inclusion.
  have hslowflag := vslow_eq_lambdaSublevel_of_upper hT hA hAmeas hint hint' hupper hslowrev
  -- `hgrowth` from the upper bound (`vflag`), the lower bound (via `hident`), and the
  -- Furstenberg–Kesten boundedness.
  have hbdd :=
    isBoundedUnder_inv_mul_log_norm_cocycle_apply_of_mem_stratum hT A hA hAmeas hint hint'
  have hub := limsup_log_norm_cocycle_apply_le_specList_of_mem_stratum hT hA hAmeas hint hint'
  have hlb :=
    specList_le_liminf_inv_mul_log_norm_cocycle_apply_of_slowflag hT hA hAmeas hint hint' hident
      hslowflag
  have hgrowth := tendsto_inv_mul_log_norm_cocycle_apply_of_upper_lower A hub hlb hbdd
  -- Assemble through `oseledets_filtration_of_slowflag`.
  exact oseledets_filtration_of_slowflag hT A hA hAmeas hTmeas hint hint' lam0
    hspec hslowflag hgrowth

end ErgodicTheory
