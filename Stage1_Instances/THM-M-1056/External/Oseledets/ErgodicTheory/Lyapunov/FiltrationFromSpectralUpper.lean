/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.SlowFiltrationMeasurable
import ErgodicTheory.Lyapunov.SpectrumConstancy
import ErgodicTheory.Lyapunov.StratumLogGrowthBounds

/-!
# The Oseledets filtration theorem from the spectral upper bound

This file collects the slow-flag and per-stratum growth helper lemmas that feed the assembly
of the Oseledets filtration theorem from a single analytic input `hupper` — the per-vector
spectral upper bound: every nonzero vector of the slow space `vslow A T (Real.exp t) x` has
upper growth exponent at most `t`.  The full assembly (`oseledets_filtration_of_upper'`) is
carried out downstream in `FiltrationFromSpectralIdent`; here we prove the three pieces it uses.

* **Forward slow-flag inclusion.**  `vslow (exp t) ≤ lambdaSublevel t` is derived from
  `hupper`: a nonzero vector of the slow space grows slowly, hence lies in the growth sublevel
  (`vslow_subset_lambdaSublevel_of_upper`).

* **Per-stratum `limsup` upper half.**  On the `IsUltrametricGrowth` good set the per-stratum
  `limsup` equals the exact exponent `specList i`, so in particular `limsup ≤ specList i` holds
  unconditionally (`limsup_log_norm_cocycle_apply_le_specList_of_mem_stratum`); this is the
  upper half consumed by `tendsto_inv_mul_log_norm_cocycle_apply_of_upper_lower`.

* **Slow-flag identification.**  Combining the forward inclusion with a reverse-inclusion
  hypothesis `hslowrev` (`lambdaSublevel t ≤ vslow (exp t)`) yields the per-point identification
  `vslow (exp t) = lambdaSublevel t` (`vslow_eq_lambdaSublevel_of_upper`) consumed by
  `oseledets_filtration_of_slowflag`.

## Main results

* `ErgodicTheory.vslow_subset_lambdaSublevel_of_upper`: the forward slow-flag inclusion
  `vslow (exp t) ≤ lambdaSublevel t` from the spectral upper bound.
* `ErgodicTheory.limsup_log_norm_cocycle_apply_le_specList_of_mem_stratum`: the per-stratum
  `limsup` upper bound, almost everywhere.
* `ErgodicTheory.vslow_eq_lambdaSublevel_of_upper`: the slow-flag identification
  `vslow (exp t) = lambdaSublevel t` from the spectral upper bound and the reverse inclusion.
-/

open MeasureTheory Filter Topology Matrix
open scoped Matrix Matrix.Norms.L2Operator

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ} [NeZero d]

/-! ## Forward inclusion of `hslowflag` from `hupper` -/

omit [MeasurableSpace X] [NeZero d] in
/-- **`vslow (exp t) ⊆ lambdaSublevel t` from `hupper`.**  A nonzero vector in the Λ-slow band
at level `e^t` has, by `hupper`, `limsup (1/n) log‖A⁽ⁿ⁾ v‖ ≤ t`; that `limsup` *is*
`lambdaBar A T x v` (`limsup_log_norm_cocycle_eq_lambdaBar`), so `lambdaBar A T x v ≤ t`, i.e.
`v ∈ lambdaSublevel t`.  The zero vector lies in every submodule.  Requires only the
`IsUltrametricGrowth` good set (to use the sublevel membership criterion `mem_lambdaSublevel`). -/
theorem vslow_subset_lambdaSublevel_of_upper
    {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} {x : X}
    (hx : IsUltrametricGrowth (lambdaBar A T x))
    (hupperx : ∀ t : ℝ, ∀ v ∈ vslow A T (Real.exp t) x, v ≠ 0 →
      limsup (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) atTop ≤ t) :
    ∀ t : ℝ, vslow A T (Real.exp t) x ≤ lambdaSublevel A T x t := by
  intro t v hv
  rw [mem_lambdaSublevel hx]
  by_cases hv0 : v = 0
  · exact Or.inl hv0
  · refine Or.inr ?_
    have := hupperx t v hv hv0
    rwa [limsup_log_norm_cocycle_eq_lambdaBar] at this

/-! ## The `hgrowth` upper half from `vflag` membership

The upper half `hub` of `ErgodicTheory.tendsto_inv_mul_log_norm_cocycle_apply_of_upper_lower` is, in
fact, *unconditional* given the `IsUltrametricGrowth` good set: a vector in the stratum
`vflag i.castSucc \ vflag i.succ`
has `lambdaBar = specList i` exactly (`lambdaBar_eq_on_stratum`), and that `lambdaBar` is the
`limsup` (`limsup_log_norm_cocycle_eq_lambdaBar`).  So `limsup ≤ specList i` holds (with
equality) and `hub` needs no separate analytic input. -/

omit [NeZero d] in
/-- **`hub` from `vflag` membership (a.e.).**  On the `IsUltrametricGrowth` good set the
per-stratum `limsup` equals the exact exponent `specList i`, so in particular
`limsup ≤ specList i` — the upper half consumed by
`ErgodicTheory.tendsto_inv_mul_log_norm_cocycle_apply_of_upper_lower`. -/
theorem limsup_log_norm_cocycle_apply_le_specList_of_mem_stratum
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X}
    (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∀ᵐ x ∂μ, ∀ i : Fin (specCard A T x),
      ∀ v ∈ (vflag A T x i.castSucc : Set (EuclideanSpace ℝ (Fin d))),
        v ∉ vflag A T x i.succ →
        limsup (fun n : ℕ => (n : ℝ)⁻¹ *
          Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) atTop ≤ specList A T x i := by
  filter_upwards [isUltrametricGrowth_lambdaBar hT hA hAmeas hint hint'] with x hx i v hv hvnot
  rw [limsup_log_norm_cocycle_eq_lambdaBar]
  exact le_of_eq (lambdaBar_eq_on_stratum hx i hv hvnot)

/-! ## Assembling `hslowflag` from the forward (`hupper`) and reverse inclusions -/

omit [NeZero d] in
/-- **`hslowflag` from `hupper` and the reverse inclusion.**  Combines the forward inclusion
`vslow (exp t) ⊆ lambdaSublevel t` (derived from `hupper` via
`vslow_subset_lambdaSublevel_of_upper`) with the reverse inclusion `hslowrev`
(`lambdaSublevel t ⊆ vslow (exp t)`) into the per-point identification
`vslow (exp t) = lambdaSublevel t` consumed by `oseledets_filtration_of_slowflag`. -/
theorem vslow_eq_lambdaSublevel_of_upper
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X}
    (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (hupper : ∀ᵐ x ∂μ, ∀ t : ℝ, ∀ v ∈ vslow A T (Real.exp t) x, v ≠ 0 →
      limsup (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) atTop ≤ t)
    (hslowrev : ∀ᵐ x ∂μ, ∀ t : ℝ, lambdaSublevel A T x t ≤ vslow A T (Real.exp t) x) :
    ∀ᵐ x ∂μ, ∀ t : ℝ, vslow A T (Real.exp t) x = lambdaSublevel A T x t := by
  filter_upwards [isUltrametricGrowth_lambdaBar hT hA hAmeas hint hint', hupper, hslowrev]
    with x hx hupperx hrevx
  intro t
  exact le_antisymm (vslow_subset_lambdaSublevel_of_upper hx (hupperx) t) (hrevx t)

end ErgodicTheory
