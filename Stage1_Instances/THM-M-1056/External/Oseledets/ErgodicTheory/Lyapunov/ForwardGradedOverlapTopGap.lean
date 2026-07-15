/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.RuelleCore
import ErgodicTheory.Lyapunov.OseledetsLimit.Limit
import ErgodicTheory.Lyapunov.Forward
import ErgodicTheory.Lyapunov.ForwardAngle
import ErgodicTheory.Lyapunov.ForwardV
import ErgodicTheory.Lyapunov.SpectrumResiduals
import ErgodicTheory.Lyapunov.ChainRecursion
import ErgodicTheory.Lyapunov.ForwardGradedOverlap

/-!
# `forward_graded_overlap_of_topGapEnvelope` — forward graded overlap via the top-gap
envelope (Ruelle Lemma 1.4)

This module proves the forward graded overlap estimate using the envelope `TopGapMassEnvelope`,
in which the cut `c₀` is restricted to the **top gap** below `λ_e`: no stratum value of `lam0`
lies in `(log c₀, λ_e)` (encoded `∀ i, lam0 i ≤ log c₀ ∨ lam0 e ≤ lam0 i`). An
arbitrary-cut chain envelope is *not* available here: at a cut interior to the spectrum,
directions belonging to intermediate strata can oscillate in and out of the band under
singular-value fluctuations, so the band mass need not decay. Restricting the cut to the top
gap removes that obstruction.

* `forward_graded_overlap_of_topGapEnvelope` carries the single isolated analytic hypothesis
  `htopgap : ∀ᵐ x ∂μ, TopGapMassEnvelope A T lam0 x`. The gap-pair cut selection goes through
  `exists_topgap_cut` (a top-gap, spectrum-avoiding cut).
* The remainder of the module is the Step-A engine for discharging `htopgap` via Ruelle's
  per-stratum strong induction: qpow↔rpow singular-value comparisons, σ-localization at all
  times, the tempered one-step operator factor, the per-step band-mass recursion
  (`bandMass_oneStep_recursion`, built on `ErgodicTheory.RuelleCofactor.SVDData.oneStep_recursion`
  and
  `toEuclideanLin_bandProjector_eq_fastProj`), and the `a₀ = 0` initialization
  (`bandMass_init_zero`).

## Main definitions

* `ErgodicTheory.TopGapMassEnvelope` — the top-gap band-mass envelope predicate along an orbit.

## Main results

* `ErgodicTheory.forward_graded_overlap_of_topGapEnvelope` — the forward graded-overlap
  bound obtained
  from the top-gap band-mass envelope (the headline result of the module).
* `ErgodicTheory.exists_topgap_cut` — existence of a top-gap spectral cut.

## Implementation notes

With the top-gap cut `c₀ = exp(λ_e − g/2)` (`g` the top gap), the direct bottom-stratum leakage
rate is `log c₀ − λ_a = λ_e − g/2 − λ_a`, which misses the target rate `λ_e − λ_a − δ`
whenever `δ < g/2`. The leakage source is not of mass one: it is itself the graded overlap of
`u_a(n)` with the intermediate strata, decaying at rate `λ_r − λ_a`, so the recursion is
self-referential and Ruelle's strong induction over distinct stratum values is mathematically
required. Slacks must be quantized against the minimum distinct-stratum gap, since raw
index-adjacent gaps can vanish under multiplicity.
-/

open MeasureTheory Filter Topology Matrix
open scoped RealInnerProductSpace BigOperators Matrix.Norms.L2Operator

noncomputable section

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {μ : MeasureTheory.Measure X} {d : ℕ} {T : X → X}

/-! ## σ-cap helpers: converting qpow-eigenvalue (= σ^{1/m}) comparisons to σ comparisons -/

/-- The `j`-th qpow eigenvalue at time `m` equals `σ_j(m)^{1/m}`. -/
theorem qpow_eigenvalue_eq_rpow [NeZero d] (A : X → Matrix (Fin d) (Fin d) ℝ) (m : ℕ) (x : X)
    (j : Fin (Fintype.card (Fin d))) :
    (qpow_isSelfAdjoint A T m x).isHermitian.eigenvalues₀ j
      = (Matrix.toEuclideanLin (cocycle A T m x)).singularValues j ^ ((m : ℝ)⁻¹) :=
  eigenvalues₀_qpow_eq A T m x j

/-- For `m ≥ 1` and `c₀ > 0`: `σ^{1/m} ≤ c₀ ↔ σ ≤ c₀^m`. -/
theorem rpow_inv_le_iff_le_pow {σ c₀ : ℝ} (hσ : 0 ≤ σ) (hc₀ : 0 < c₀) {m : ℕ}
    (hm : 1 ≤ m) :
    σ ^ ((m : ℝ)⁻¹) ≤ c₀ ↔ σ ≤ c₀ ^ m := by
  have hmpos : (0 : ℝ) < (m : ℝ) := by exact_mod_cast hm
  constructor
  · intro h
    have h2 : (σ ^ ((m : ℝ)⁻¹)) ^ (m : ℝ) ≤ c₀ ^ (m : ℝ) :=
      Real.rpow_le_rpow (Real.rpow_nonneg hσ _) h hmpos.le
    rw [← Real.rpow_mul hσ, inv_mul_cancel₀ (ne_of_gt hmpos), Real.rpow_one,
      Real.rpow_natCast] at h2
    exact h2
  · intro h
    have h2 : σ ^ ((m : ℝ)⁻¹) ≤ (c₀ ^ m) ^ ((m : ℝ)⁻¹) :=
      Real.rpow_le_rpow hσ h (by positivity)
    rwa [← Real.rpow_natCast c₀ m, ← Real.rpow_mul hc₀.le,
      mul_inv_cancel₀ (ne_of_gt hmpos), Real.rpow_one] at h2

/-- For `m ≥ 1` and `c₀ > 0`: `c₀ < σ^{1/m} ↔ c₀^m < σ`. -/
theorem lt_rpow_inv_iff_pow_lt {σ c₀ : ℝ} (hσ : 0 ≤ σ) (hc₀ : 0 < c₀) {m : ℕ}
    (hm : 1 ≤ m) :
    c₀ < σ ^ ((m : ℝ)⁻¹) ↔ c₀ ^ m < σ := by
  rw [← not_le, ← not_le, rpow_inv_le_iff_le_pow hσ hc₀ hm]

/-! ## σ-localization: the qpow eigenvalue σ_j(t)^{1/t} converges to exp(λ_j) -/

/-- `σ_j(t)^{1/t} = exp((1/t)·log σ_j(t))` for `t ≥ 1` (the singular value is positive). -/
theorem rpow_inv_eq_exp_log [NeZero d] {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0)
    (x : X) {j : ℕ} (hj : j < d) {t : ℕ} (_ht : 1 ≤ t) :
    (Matrix.toEuclideanLin (cocycle A T t x)).singularValues j ^ ((t : ℝ)⁻¹)
      = Real.exp ((t : ℝ)⁻¹ *
          Real.log ((Matrix.toEuclideanLin (cocycle A T t x)).singularValues j)) := by
  have hpos : 0 < (Matrix.toEuclideanLin (cocycle A T t x)).singularValues j :=
    singularValues_cocycle_pos hA t x hj
  rw [Real.rpow_def_of_pos hpos]
  ring_nf

/-- **σ-localization.**  If at `x` the normalized log of `σ_j(·)` converges to `λ_j` for every
`j < d`, then for any `η > 0` there is `N` such that for all `t ≥ N` and all `j < d`,
`exp(λ_j − η) < σ_j(t)^{1/t} < exp(λ_j + η)`. -/
theorem eventually_qpow_eigenvalue_localized [NeZero d] {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) (x : X) (lam0 : ℕ → ℝ)
    (hconv : ∀ j : ℕ, j < d → Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues j))
      Filter.atTop (𝓝 (lam0 j)))
    {η : ℝ} (hη : 0 < η) :
    ∀ᶠ t : ℕ in Filter.atTop, ∀ j : ℕ, (hj : j < d) →
      Real.exp (lam0 j - η)
          < (Matrix.toEuclideanLin (cocycle A T t x)).singularValues j ^ ((t : ℝ)⁻¹)
        ∧ (Matrix.toEuclideanLin (cocycle A T t x)).singularValues j ^ ((t : ℝ)⁻¹)
          < Real.exp (lam0 j + η) := by
  -- For each j < d, eventually |(1/t)logσ_j − λ_j| < η.
  have hloc : ∀ j : ℕ, j < d → ∀ᶠ t : ℕ in Filter.atTop,
      lam0 j - η < (t : ℝ)⁻¹ *
          Real.log ((Matrix.toEuclideanLin (cocycle A T t x)).singularValues j)
        ∧ (t : ℝ)⁻¹ *
          Real.log ((Matrix.toEuclideanLin (cocycle A T t x)).singularValues j) < lam0 j + η := by
    intro j hj
    have := (hconv j hj).eventually
      (eventually_abs_sub_lt (lam0 j) hη)
    filter_upwards [this] with t ht
    rw [abs_sub_lt_iff] at ht
    constructor <;> [linarith [ht.2]; linarith [ht.1]]
  -- Combine over the finitely many j < d, plus t ≥ 1.
  have hfin : ∀ᶠ t : ℕ in Filter.atTop, ∀ j : ℕ, (hj : j < d) →
      lam0 j - η < (t : ℝ)⁻¹ *
          Real.log ((Matrix.toEuclideanLin (cocycle A T t x)).singularValues j)
        ∧ (t : ℝ)⁻¹ *
          Real.log ((Matrix.toEuclideanLin (cocycle A T t x)).singularValues j) < lam0 j + η := by
    have : ∀ᶠ t : ℕ in Filter.atTop, ∀ j : Fin d,
        lam0 (j : ℕ) - η < (t : ℝ)⁻¹ *
            Real.log ((Matrix.toEuclideanLin (cocycle A T t x)).singularValues (j : ℕ))
          ∧ (t : ℝ)⁻¹ *
            Real.log ((Matrix.toEuclideanLin (cocycle A T t x)).singularValues (j : ℕ))
            < lam0 (j : ℕ) + η :=
      eventually_all.2 (fun j => hloc (j : ℕ) j.isLt)
    filter_upwards [this] with t ht j hj
    exact ht ⟨j, hj⟩
  filter_upwards [hfin, Filter.eventually_ge_atTop 1] with t ht ht1 j hj
  rw [rpow_inv_eq_exp_log hA x hj ht1]
  obtain ⟨h1, h2⟩ := ht j hj
  exact ⟨Real.exp_lt_exp.mpr h1, Real.exp_lt_exp.mpr h2⟩

/-! ## The one-step recursion specialised to the cocycle SVD chain at a fixed cut

We instantiate `ErgodicTheory.RuelleCofactor.SVDData.oneStep_recursion` on `chainSVD A T x` with
slow cap `c₀^t`, fast floor `c₀^{t+1}`, and step factor `b = ‖A(T^[t] x)‖`, identifying
`fastProj` with the band projector via `toEuclideanLin_bandProjector_eq_fastProj`.  This
produces the per-step inequality on the band masses.  -/

omit [MeasurableSpace X] in
/-- The one-step operator factor along the orbit: `‖toEuclideanLin (cocycle (t+1) x) w‖
≤ ‖A(T^[t] x)‖ · ‖toEuclideanLin (cocycle t x) w‖`. -/
theorem chain_oneStep_opNorm [NeZero d] (A : X → Matrix (Fin d) (Fin d) ℝ) (t : ℕ) (x : X)
    (w : EuclideanSpace ℝ (Fin d)) :
    ‖Matrix.toEuclideanLin (cocycle A T (t + 1) x) w‖
      ≤ ‖A (T^[t] x)‖ * ‖Matrix.toEuclideanLin (cocycle A T t x) w‖ := by
  have hcoc : cocycle A T (t + 1) x = A (T^[t] x) * cocycle A T t x := by
    rw [show t + 1 = 1 + t from by omega, cocycle_add, cocycle_one]
  have hmul : Matrix.toEuclideanLin (cocycle A T (t + 1) x) w
      = Matrix.toEuclideanLin (A (T^[t] x)) (Matrix.toEuclideanLin (cocycle A T t x) w) := by
    rw [hcoc]
    simp only [Matrix.toLpLin_apply, Matrix.mulVec_mulVec]
  rw [hmul]
  exact ExteriorNorm.norm_toEuclideanLin_apply_le (A (T^[t] x))
    (Matrix.toEuclideanLin (cocycle A T t x) w)

/-! ## Step A — the top-gap fast-band-mass envelope (Ruelle Lemma 1.4 core)

In this envelope the cut `c₀` is restricted to the top gap below `λ_e`, i.e. no stratum value
lies in `(log c₀, λ_e)`. It is stated here as the single isolated analytic hypothesis
`TopGapMassEnvelope`, established by Ruelle's band-distance strong induction over strata
(eqns (1.3)/(1.4)); the deterministic engine
`ErgodicTheory.RuelleCofactor.SVDData.oneStep_recursion` and the
σ-localization layer above are its ingredients. Everything downstream (Step B) is discharged
from it. -/

/-- **Top-gap fast-band-mass envelope.** For a gap pair `λ_a < λ_e` and any cut `c₀` in the open
interior of the top gap below `λ_e` (`exp λ_a < c₀ < exp λ_e`, with every stratum value of
`lam0` either strictly below `log c₀` or at least `λ_e`, encoded
`∀ i, lam0 i < Real.log c₀ ∨ lam0 e ≤ lam0 i`), the time-`m` band mass of the time-`n` slow
eigenvector `u_a(n)` decays like `exp(−n(λ_e − λ_a − δ))` uniformly in `m ≥ n`.

The strictness in the first disjunct is essential: at a boundary cut `log c₀ = λ_p` (the largest
stratum below `λ_e`) the `λ_p`-directions can oscillate in and out of the band under
σ-fluctuations, so the envelope fails there. Gap-interior cuts are all the Step-B consumer ever
uses (`exists_topgap_cut` produces the gap midpoint). -/
def TopGapMassEnvelope [NeZero d] (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X)
    (lam0 : ℕ → ℝ) (x : X) : Prop :=
  ∀ δ : ℝ, 0 < δ → ∃ C : ℝ, 1 ≤ C ∧ ∀ a e : Fin d,
    lam0 (a : ℕ) < lam0 (e : ℕ) →
    ∀ c₀ : ℝ, Real.exp (lam0 (a : ℕ)) < c₀ → c₀ < Real.exp (lam0 (e : ℕ)) →
      (∀ i : Fin d, lam0 (i : ℕ) < Real.log c₀ ∨ lam0 (e : ℕ) ≤ lam0 (i : ℕ)) →
      ∀ᶠ n : ℕ in Filter.atTop, ∀ m : ℕ, n ≤ m →
        ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c₀) 1) m x)
            (sortedGramEigenbasis A T n x
              ⟨(a : ℕ), lt_of_lt_of_eq a.isLt (Fintype.card_fin d).symm⟩)‖
          ≤ C * Real.exp (-(n : ℝ) * (lam0 (e : ℕ) - lam0 (a : ℕ) - δ))

/-! ## Top-gap cut selection for `lam0` -/

/-- **Top-gap cut below `lam0 e`.**  For a gap pair `lam0 a < lam0 e`, there is a cut `c₀` with
`exp (lam0 a) < c₀ < exp (lam0 e)`, strictly interior to the top spectral gap below `lam0 e`
(encoded `∀ i, lam0 i < log c₀ ∨ lam0 e ≤ lam0 i`), and with `c₀` avoiding every
`exp (lam0 i)`. -/
theorem exists_topgap_cut (lam0 : ℕ → ℝ) {a e : Fin d}
    (hgap : lam0 (a : ℕ) < lam0 (e : ℕ)) :
    ∃ c₀ : ℝ, Real.exp (lam0 (a : ℕ)) < c₀ ∧ c₀ < Real.exp (lam0 (e : ℕ))
      ∧ (∀ i : Fin d, lam0 (i : ℕ) < Real.log c₀ ∨ lam0 (e : ℕ) ≤ lam0 (i : ℕ))
      ∧ (∀ i : Fin d, Real.exp (lam0 (i : ℕ)) ≠ c₀) := by
  classical
  set L : Finset ℝ :=
    (Finset.univ.image (fun i : Fin d => lam0 (i : ℕ))).filter (· < lam0 (e : ℕ)) with hL
  have hmem : ∀ i : Fin d, lam0 (i : ℕ) < lam0 (e : ℕ) → lam0 (i : ℕ) ∈ L := by
    intro i hi
    rw [hL, Finset.mem_filter]
    exact ⟨Finset.mem_image_of_mem _ (Finset.mem_univ i), hi⟩
  have hLne : L.Nonempty := ⟨lam0 (a : ℕ), hmem a hgap⟩
  set t' := L.max' hLne with ht'
  have ht'lt : t' < lam0 (e : ℕ) := (Finset.mem_filter.mp (L.max'_mem hLne)).2
  have ht'ge : lam0 (a : ℕ) ≤ t' := Finset.le_max' L _ (hmem a hgap)
  have hgapcond : ∀ i : Fin d, lam0 (i : ℕ) ≤ t' ∨ lam0 (e : ℕ) ≤ lam0 (i : ℕ) := by
    intro i
    by_cases hlt : lam0 (i : ℕ) < lam0 (e : ℕ)
    · left; exact Finset.le_max' L _ (hmem i hlt)
    · right; exact not_lt.mp hlt
  set lc := (t' + lam0 (e : ℕ)) / 2 with hlc
  have hlc1 : t' < lc := by rw [hlc]; linarith
  have hlc2 : lc < lam0 (e : ℕ) := by rw [hlc]; linarith
  refine ⟨Real.exp lc, ?_, ?_, ?_, ?_⟩
  · exact Real.exp_lt_exp.mpr (lt_of_le_of_lt ht'ge hlc1)
  · exact Real.exp_lt_exp.mpr hlc2
  · intro i
    rw [Real.log_exp]
    rcases hgapcond i with h | h
    · left; linarith
    · right; exact h
  · intro i heq
    have hii : lam0 (i : ℕ) = lc := Real.exp_injective heq
    rcases hgapcond i with h | h
    · rw [hii] at h; linarith
    · rw [hii] at h; linarith

/-! ## Step B — the almost-everywhere wrapper

This is the theorem `forward_graded_overlap_of_topGapEnvelope`. It carries the single isolated
analytic hypothesis `htopgap` (the top-gap envelope `TopGapMassEnvelope`). The gap-cut is
selected by
`exists_topgap_cut` (the top-gap selection). -/

theorem forward_graded_overlap_of_topGapEnvelope [MeasureTheory.IsProbabilityMeasure μ] [NeZero d]
    (_hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (_hA : ∀ x, (A x).det ≠ 0) (_hAmeas : Measurable A)
    (_hint : IntegrableLogNorm A μ) (_hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (lam0 : ℕ → ℝ)
    (hlam0 : ∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
      Filter.atTop (𝓝 (lam0 i)))
    (b' : X → OrthonormalBasis (Fin d) ℝ (EuclideanSpace ℝ (Fin d)))
    (hb' : ∀ᵐ x ∂μ, ∀ e : Fin d,
      Matrix.toEuclideanLin (lambdaHat A T x) (b' x e)
        = Real.exp (lamSing A T x (e : ℕ)) • b' x e)
    (hident : ∀ᵐ x ∂μ, ∀ c : ℝ, 0 < c →
        (∀ i : Fin d, Real.exp (lamSing A T x (i : ℕ)) ≠ c) →
      Filter.Tendsto (fun n : ℕ => bandProjector A T (Set.indicator (Set.Ioi c) 1) n x)
        Filter.atTop (𝓝 (cfc (Set.indicator (Set.Ioi c) (1 : ℝ → ℝ)) (lambdaHat A T x))))
    -- The isolated analytic hypothesis: the top-gap fast-band-mass envelope.
    (htopgap : ∀ᵐ x ∂μ, TopGapMassEnvelope A T lam0 x) :
    ∀ᵐ x ∂μ, ∀ δ : ℝ, 0 < δ → ∃ c : ℝ, 1 ≤ c ∧
      ∀ᶠ n : ℕ in Filter.atTop, ∀ a e : Fin d,
        |(inner ℝ (b' x e) (sortedGramEigenbasis A T n x
            ⟨(a : ℕ), lt_of_lt_of_eq a.isLt (Fintype.card_fin d).symm⟩) : ℝ)|
          ≤ c * Real.exp (-(n : ℝ) * (max (lam0 (e : ℕ) - lam0 (a : ℕ)) 0 - δ)) := by
  filter_upwards [hb', hident, htopgap,
    ae_lamSing_eq_lam0 lam0 hlam0] with x hb'x hidentx htopgapx hlameq
  intro δ hδ
  obtain ⟨C, hC1, hCpair⟩ := htopgapx δ hδ
  refine ⟨C, hC1, ?_⟩
  have hpair : ∀ p : Fin d × Fin d, ∀ᶠ n : ℕ in Filter.atTop,
      |(inner ℝ (b' x p.2) (sortedGramEigenbasis A T n x
          ⟨(p.1 : ℕ), lt_of_lt_of_eq p.1.isLt (Fintype.card_fin d).symm⟩) : ℝ)|
        ≤ C * Real.exp (-(n : ℝ) * (max (lam0 (p.2 : ℕ) - lam0 (p.1 : ℕ)) 0 - δ)) := by
    rintro ⟨a, e⟩
    by_cases hgap : lam0 (a : ℕ) < lam0 (e : ℕ)
    · -- GAP pair: top-gap cut, then chain + limit transfer.
      obtain ⟨c₀, hc₀lo, hc₀hi, hc₀gap, hc₀avoid⟩ := exists_topgap_cut lam0 hgap
      have hc₀pos : 0 < c₀ := lt_trans (Real.exp_pos _) hc₀lo
      have hc₀spec : ∀ i : Fin d, Real.exp (lamSing A T x (i : ℕ)) ≠ c₀ := by
        intro i; rw [hlameq i]; exact hc₀avoid i
      have hc₀lt : c₀ < Real.exp (lamSing A T x (e : ℕ)) := by rw [hlameq e]; exact hc₀hi
      have hmass := hCpair a e hgap c₀ hc₀lo hc₀hi hc₀gap
      set Pinf := cfc (Set.indicator (Set.Ioi c₀) (1 : ℝ → ℝ)) (lambdaHat A T x) with hPinf
      have hfix : Matrix.toEuclideanLin Pinf (b' x e) = b' x e := by
        apply toEuclideanLin_cfc_fix_eigenvector (lambdaHat A T x)
          (lambdaHat_isSelfAdjoint A T x).isHermitian
          (Set.indicator (Set.Ioi c₀) (1 : ℝ → ℝ)) (b' x e) (hb'x e)
        rw [Set.indicator_of_mem (Set.mem_Ioi.mpr hc₀lt), Pi.one_apply]
      have hPinfsa : IsSelfAdjoint Pinf := cfc_predicate _ _
      have htend := hidentx c₀ hc₀pos hc₀spec
      have hmaxeq : max (lam0 (e : ℕ) - lam0 (a : ℕ)) 0 = lam0 (e : ℕ) - lam0 (a : ℕ) :=
        max_eq_left (by linarith)
      filter_upwards [hmass] with n hmassn
      rw [hmaxeq]
      exact abs_inner_le_of_bandProjector_mass_bound htend hPinfsa (b' x e)
        (sortedGramEigenbasis A T n x
          ⟨(a : ℕ), lt_of_lt_of_eq a.isLt (Fintype.card_fin d).symm⟩)
        (le_of_eq ((b' x).orthonormal.1 e)) hfix
        (Filter.eventually_atTop.2 ⟨n, hmassn⟩)
    · -- TRIVIAL pair.
      have hmaxeq : max (lam0 (e : ℕ) - lam0 (a : ℕ)) 0 = 0 :=
        max_eq_right (by linarith [not_lt.mp hgap])
      filter_upwards with n
      rw [hmaxeq]
      have hCS : |(inner ℝ (b' x e) (sortedGramEigenbasis A T n x
          ⟨(a : ℕ), lt_of_lt_of_eq a.isLt (Fintype.card_fin d).symm⟩) : ℝ)| ≤ 1 := by
        calc |(inner ℝ (b' x e) (sortedGramEigenbasis A T n x
            ⟨(a : ℕ), lt_of_lt_of_eq a.isLt (Fintype.card_fin d).symm⟩) : ℝ)|
            ≤ ‖b' x e‖ * ‖sortedGramEigenbasis A T n x
                ⟨(a : ℕ), lt_of_lt_of_eq a.isLt (Fintype.card_fin d).symm⟩‖ :=
              abs_real_inner_le_norm _ _
          _ = 1 := by
              rw [(b' x).orthonormal.1 e,
                (sortedGramEigenbasis A T n x).orthonormal.1
                  ⟨(a : ℕ), lt_of_lt_of_eq a.isLt (Fintype.card_fin d).symm⟩, one_mul]
      refine hCS.trans ?_
      have hexp1 : (1 : ℝ) ≤ Real.exp (-(n : ℝ) * (0 - δ)) :=
        Real.one_le_exp (by nlinarith [Nat.cast_nonneg (α := ℝ) n, hδ.le])
      calc (1 : ℝ) = 1 * 1 := (one_mul 1).symm
        _ ≤ C * Real.exp (-(n : ℝ) * (0 - δ)) :=
            mul_le_mul hC1 hexp1 (by norm_num) (le_trans (by norm_num) hC1)
  have hall : ∀ᶠ n : ℕ in Filter.atTop, ∀ p : Fin d × Fin d,
      |(inner ℝ (b' x p.2) (sortedGramEigenbasis A T n x
          ⟨(p.1 : ℕ), lt_of_lt_of_eq p.1.isLt (Fintype.card_fin d).symm⟩) : ℝ)|
        ≤ C * Real.exp (-(n : ℝ) * (max (lam0 (p.2 : ℕ) - lam0 (p.1 : ℕ)) 0 - δ)) :=
    Filter.eventually_all.2 hpair
  filter_upwards [hall] with n hn a e
  exact hn (a, e)

/-! ## The per-step band-mass recursion at a fixed cut (engine instantiation)

We instantiate `ErgodicTheory.RuelleCofactor.SVDData.oneStep_recursion` on `chainSVD A T x`.  The
fast band at time `t` is `hiBand A T t x c₀`; its complement is the slow band.  We supply:
* slow cap `s` valid at time `t`: every slow `σ_j(t) ≤ s`;
* fast floor `c₀^{t+1}` at time `t+1`: every fast `σ_j(t+1) ≥ c₀^{t+1}` (from the band
  definition);
* step factor `b = ‖A(T^[t] x)‖` (from `chain_oneStep_opNorm`).
The band projector mass is `fastProj` via `toEuclideanLin_bandProjector_eq_fastProj`. -/

/-- Fast indices at time `t+1` have `σ ≥ c₀^{t+1}`. -/
theorem fast_sigma_floor [NeZero d] (A : X → Matrix (Fin d) (Fin d) ℝ) {c₀ : ℝ} (hc₀ : 0 < c₀)
    {t : ℕ} (x : X)
    (j : Fin (Fintype.card (Fin d))) (hj : j ∈ hiBand A T (t + 1) x c₀) :
    c₀ ^ (t + 1) ≤ (Matrix.toEuclideanLin (cocycle A T (t + 1) x)).singularValues j := by
  simp only [hiBand, Finset.mem_filter, Finset.mem_univ, true_and] at hj
  rw [qpow_eigenvalue_eq_rpow] at hj
  have hσnn : 0 ≤ (Matrix.toEuclideanLin (cocycle A T (t + 1) x)).singularValues j :=
    (Matrix.toEuclideanLin (cocycle A T (t + 1) x)).singularValues_nonneg j
  exact le_of_lt ((lt_rpow_inv_iff_pow_lt hσnn hc₀ (by omega)).mp hj)

/-- The per-step band-mass recursion (one application of `oneStep_recursion`).  With slow cap `s`,
fast floor `c₀^{t+1}`, step factor `b = ‖A(T^[t]x)‖`:
`‖P^{>c₀}_{t+1} u‖ ≤ ‖P^{>c₀}_t u‖ + (b·s/c₀^{t+1})·‖slowProj_t u‖`. -/
theorem bandMass_oneStep_recursion [NeZero d] (A : X → Matrix (Fin d) (Fin d) ℝ) {c₀ : ℝ}
    (hc₀ : 0 < c₀) {t : ℕ} (x : X) {s : ℝ} (hs : 0 ≤ s)
    (hslow : ∀ j ∈ (hiBand A T t x c₀)ᶜ,
      (Matrix.toEuclideanLin (cocycle A T t x)).singularValues j ≤ s)
    (u : EuclideanSpace ℝ (Fin d)) :
    ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c₀) 1) (t + 1) x) u‖
      ≤ ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c₀) 1) t x) u‖
        + (‖A (T^[t] x)‖ * s / c₀ ^ (t + 1))
          * ‖(chainSVD A T x).slowProj t (hiBand A T t x c₀) u‖ := by
  set S := chainSVD A T x with hS
  have hrec := S.oneStep_recursion t (hiBand A T t x c₀) (hiBand A T (t + 1) x c₀)
    s (c₀ ^ (t + 1)) (‖A (T^[t] x)‖) hs (by positivity) (norm_nonneg _)
    (by intro j hj; simpa [hS, chainSVD_σ] using hslow j hj)
    (by intro j hj; simpa [hS, chainSVD_σ] using fast_sigma_floor A hc₀ x j hj)
    u
    (by
      -- step bound on the slow part
      simpa [hS, chainSVD_apply] using
        chain_oneStep_opNorm A t x (S.slowProj t (hiBand A T t x c₀) u))
  rw [toEuclideanLin_bandProjector_eq_fastProj, toEuclideanLin_bandProjector_eq_fastProj]
  exact hrec

/-! ## Initialization (`a_0 = 0`): the time-`n` slow eigenvector has no fast-band mass at
time `n` -/

/-- If the index `⟨a⟩` is NOT in the fast band at time `n` (i.e. `σ_a(n)^{1/n} ≤ c₀`), then the
band projector at cut `c₀`, time `n`, annihilates the basis vector `u_a(n)`. -/
theorem bandMass_init_zero [NeZero d] (A : X → Matrix (Fin d) (Fin d) ℝ) (n : ℕ) (x : X)
    (c₀ : ℝ) {a : Fin (Fintype.card (Fin d))} (ha : a ∉ hiBand A T n x c₀) :
    Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c₀) 1) n x)
        (sortedGramEigenbasis A T n x a) = 0 := by
  classical
  rw [toEuclideanLin_bandProjector_eq_fastProj, ErgodicTheory.RuelleCofactor.SVDData.fastProj]
  simp only [chainSVD_e]
  apply Finset.sum_eq_zero
  intro j hj
  have hne : j ≠ a := by rintro rfl; exact ha hj
  rw [(sortedGramEigenbasis A T n x).inner_eq_ite]
  simp only [hne, if_false, zero_smul]

end ErgodicTheory
