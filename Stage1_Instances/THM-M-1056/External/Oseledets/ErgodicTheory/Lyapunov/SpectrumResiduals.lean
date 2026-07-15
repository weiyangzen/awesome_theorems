/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.FiltrationFromSpectralUpper

/-!
# Spectral residuals: `hub_spec`, `hlb_spec`, and the per-stratum lower bound

This module discharges three residuals of the MET final composer
`ErgodicTheory.oseledets_filtration_of_upper'`:

* `lyapunovSpectrum_subset_distinctExp_of_slowflag` — every realized exponent is one of the
  deterministic `lam0 i`;
* `distinctExp_subset_lyapunovSpectrum_of_slowflag` — every deterministic exponent is realized;
* `specList_le_liminf_inv_mul_log_norm_cocycle_apply_of_slowflag` — the per-stratum liminf lower
  bound.

All three are derived from two hypotheses with fixed shapes: `hident` (band-projector
convergence to the indicator CFC of `lambdaHat`) and `hslowflag`
(`vslow (exp t) = lambdaSublevel t`).
-/

open MeasureTheory Filter Topology Matrix

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ} [NeZero d]

/-! ## Spectral foundation: eigenvalues of `lambdaHat` are `exp (lamSing i)` -/

/-- **The spectrum of the sanitized limit is `{exp (lamSing i)}`.**  A.e., the Oseledets limit is
Hermitian, so `lambdaHat A T x = oseledetsLimit A T x`; the `ℝ`-spectrum of a Hermitian matrix is
the range of its eigenvalues (`spectrum_real_eq_range_eigenvalues`), the (unsorted) eigenvalue range
equals the sorted-eigenvalue range, and the sorted eigenvalues are `exp (lamSing i)`
(`oseledetsLimit_eigenvalues₀_eq`). -/
theorem spectrum_lambdaHat_eq_ae
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X} (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∀ᵐ x ∂μ, _root_.spectrum ℝ (lambdaHat A T x)
      = Set.range (fun i : Fin d => Real.exp (lamSing A T x (i : ℕ))) := by
  filter_upwards [oseledetsLimit_isSelfAdjoint hT hA hAmeas hint hint',
    oseledetsLimit_eigenvalues₀_eq hT hA hAmeas hint hint'] with x hsa heig
  -- On the Hermitian set, `lambdaHat = oseledetsLimit`.
  have hH : (oseledetsLimit A T x).IsHermitian := Matrix.isHermitian_iff_isSelfAdjoint.mpr hsa
  have hlh : lambdaHat A T x = oseledetsLimit A T x := by rw [lambdaHat, if_pos hH]
  rw [hlh, hH.spectrum_real_eq_range_eigenvalues]
  -- `range eigenvalues = range eigenvalues₀` (composition with a bijection).
  have hrange : Set.range hH.eigenvalues = Set.range hH.eigenvalues₀ := by
    have : hH.eigenvalues
        = hH.eigenvalues₀ ∘ (Fintype.equivOfCardEq (Fintype.card_fin _)).symm := rfl
    rw [this, Set.range_comp, Equiv.range_eq_univ, Set.image_univ]
  rw [hrange]
  -- `eigenvalues₀ i = exp (lamSing (i:ℕ))`, and reindex `Fin (card (Fin d)) ≃ Fin d`.
  ext r
  simp only [Set.mem_range]
  constructor
  · rintro ⟨i, rfl⟩
    refine ⟨Fin.cast (Fintype.card_fin d) i, ?_⟩
    rw [heig hH i]
    congr 1
  · rintro ⟨i, rfl⟩
    refine ⟨Fin.cast (Fintype.card_fin d).symm i, ?_⟩
    rw [heig hH (Fin.cast (Fintype.card_fin d).symm i)]
    congr 1

/-! ## Local constancy of the slow projector across an eigenvalue-free gap -/

omit [MeasurableSpace X] [NeZero d] in
/-- **`slowProjector` is constant across a gap with no eigenvalue.**  If the spectrum of
`lambdaHat A T x` is `{exp (lamSing j)}` and no `lamSing j` lies in the half-open interval
`(t₁, t₂]` (i.e. each is `≤ t₁` or `> t₂`), then the two indicator cutoffs `Iic (exp t₁)`
and `Iic (exp t₂)` agree on the spectrum, so the corresponding slow projectors coincide. -/
theorem slowProjector_eq_of_gap
    {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} {x : X} {t₁ t₂ : ℝ}
    (hspec : _root_.spectrum ℝ (lambdaHat A T x)
      = Set.range (fun i : Fin d => Real.exp (lamSing A T x (i : ℕ))))
    (ht : t₁ ≤ t₂)
    (hgap : ∀ j : Fin d, lamSing A T x (j : ℕ) ≤ t₁ ∨ t₂ < lamSing A T x (j : ℕ)) :
    slowProjector A T (Real.exp t₁) x = slowProjector A T (Real.exp t₂) x := by
  refine cfc_congr (g := Set.indicator (Set.Iic (Real.exp t₂)) (1 : ℝ → ℝ)) ?_
  rw [hspec]
  rintro _ ⟨j, rfl⟩
  set e := Real.exp (lamSing A T x (j : ℕ)) with he
  rcases hgap j with hle | hlt
  · -- `lamSing j ≤ t₁`: eigenvalue ≤ exp t₁ ≤ exp t₂, both indicators are `1`.
    have h1 : e ≤ Real.exp t₁ := Real.exp_le_exp.mpr hle
    have h2 : e ≤ Real.exp t₂ := h1.trans (Real.exp_le_exp.mpr ht)
    rw [Set.indicator_of_mem (Set.mem_Iic.mpr h1), Set.indicator_of_mem (Set.mem_Iic.mpr h2)]
  · -- `t₂ < lamSing j`: eigenvalue > exp t₂ ≥ exp t₁, both indicators are `0`.
    have h2 : Real.exp t₂ < e := Real.exp_lt_exp.mpr hlt
    have h1 : Real.exp t₁ < e := (Real.exp_le_exp.mpr ht).trans_lt h2
    rw [Set.indicator_of_notMem (by simp [Set.mem_Iic]; linarith),
      Set.indicator_of_notMem (by simp [Set.mem_Iic]; linarith)]

omit [MeasurableSpace X] [NeZero d] in
/-- `vslow` inherits local constancy from `slowProjector`. -/
theorem vslow_eq_of_gap
    {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} {x : X} {t₁ t₂ : ℝ}
    (hspec : _root_.spectrum ℝ (lambdaHat A T x)
      = Set.range (fun i : Fin d => Real.exp (lamSing A T x (i : ℕ))))
    (ht : t₁ ≤ t₂)
    (hgap : ∀ j : Fin d, lamSing A T x (j : ℕ) ≤ t₁ ∨ t₂ < lamSing A T x (j : ℕ)) :
    vslow A T (Real.exp t₁) x = vslow A T (Real.exp t₂) x := by
  unfold vslow
  rw [slowProjector_eq_of_gap hspec ht hgap]

/-! ## Nested slow projectors and the difference (band) projector -/

omit [MeasurableSpace X] [NeZero d] in
/-- **Nested slow projectors multiply to the smaller.**  For `t₁ ≤ t₂`,
`slowProjector (exp t₁) · slowProjector (exp t₂) = slowProjector (exp t₁)`, since the smaller
sublevel indicator absorbs the larger on the spectrum. -/
theorem slowProjector_mul_le
    {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} {x : X} {t₁ t₂ : ℝ}
    (h : t₁ ≤ t₂) :
    slowProjector A T (Real.exp t₁) x * slowProjector A T (Real.exp t₂) x
      = slowProjector A T (Real.exp t₁) x := by
  have hidem : (_root_.spectrum ℝ (lambdaHat A T x)).EqOn
      (fun e => Set.indicator (Set.Iic (Real.exp t₁)) (1 : ℝ → ℝ) e
        * Set.indicator (Set.Iic (Real.exp t₂)) (1 : ℝ → ℝ) e)
      (Set.indicator (Set.Iic (Real.exp t₁)) (1 : ℝ → ℝ)) := by
    intro e _
    by_cases he : e ∈ Set.Iic (Real.exp t₁)
    · have he2 : e ∈ Set.Iic (Real.exp t₂) :=
        Set.mem_Iic.mpr ((Set.mem_Iic.mp he).trans (Real.exp_le_exp.mpr h))
      simp [Set.indicator_of_mem he, Set.indicator_of_mem he2]
    · simp [Set.indicator_of_notMem he]
  have hcont₁ : ContinuousOn (Set.indicator (Set.Iic (Real.exp t₁)) (1 : ℝ → ℝ))
      (_root_.spectrum ℝ (lambdaHat A T x)) :=
    (Matrix.finite_real_spectrum (A := lambdaHat A T x)).continuousOn _
  have hcont₂ : ContinuousOn (Set.indicator (Set.Iic (Real.exp t₂)) (1 : ℝ → ℝ))
      (_root_.spectrum ℝ (lambdaHat A T x)) :=
    (Matrix.finite_real_spectrum (A := lambdaHat A T x)).continuousOn _
  simp only [slowProjector]
  rw [← cfc_mul _ _ _ hcont₁ hcont₂, cfc_congr hidem]

omit [MeasurableSpace X] [NeZero d] in
/-- **The complementary (fast) projector.**  `1 - slowProjector (exp t)` is the CFC of the
indicator of `(exp t, ∞)`, since `1 - 𝟙_{Iic} = 𝟙_{Ioi}` pointwise. -/
theorem one_sub_slowProjector
    {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} {x : X} {c : ℝ} :
    (1 : Matrix (Fin d) (Fin d) ℝ) - slowProjector A T c x
      = cfc (Set.indicator (Set.Ioi c) (1 : ℝ → ℝ)) (lambdaHat A T x) := by
  have hfun : (fun e => (1 : ℝ → ℝ) e - Set.indicator (Set.Iic c) (1 : ℝ → ℝ) e)
      = Set.indicator (Set.Ioi c) (1 : ℝ → ℝ) := by
    funext e
    by_cases he : e ∈ Set.Iic c
    · have hne : e ∉ Set.Ioi c := by simp only [Set.mem_Ioi, not_lt]; exact Set.mem_Iic.mp he
      simp [Set.indicator_of_mem he, Set.indicator_of_notMem hne]
    · have hin : e ∈ Set.Ioi c := by
        simp only [Set.mem_Ioi]; exact lt_of_not_ge (by simpa [Set.mem_Iic] using he)
      simp [Set.indicator_of_notMem he, Set.indicator_of_mem hin]
  have hcontIic : ContinuousOn (Set.indicator (Set.Iic c) (1 : ℝ → ℝ))
      (_root_.spectrum ℝ (lambdaHat A T x)) :=
    (Matrix.finite_real_spectrum (A := lambdaHat A T x)).continuousOn _
  have hcontOne : ContinuousOn (1 : ℝ → ℝ) (_root_.spectrum ℝ (lambdaHat A T x)) :=
    continuousOn_const
  have hsa : IsSelfAdjoint (lambdaHat A T x) := lambdaHat_isSelfAdjoint A T x
  have hsub : cfc (fun e => (1 : ℝ → ℝ) e - Set.indicator (Set.Iic c) (1 : ℝ → ℝ) e)
      (lambdaHat A T x)
      = cfc (1 : ℝ → ℝ) (lambdaHat A T x)
        - cfc (Set.indicator (Set.Iic c) (1 : ℝ → ℝ)) (lambdaHat A T x) :=
    cfc_sub _ _ (lambdaHat A T x) hcontOne hcontIic
  rw [slowProjector, ← cfc_one (R := ℝ) (a := lambdaHat A T x) hsa, ← hsub, hfun]

omit [MeasurableSpace X] [NeZero d] in
/-- **A CFC is nonzero if its symbol is nonzero at some eigenvalue.**  If `g` is continuous on the
spectrum of `lambdaHat A T x` and `g (exp (lamSing j)) ≠ 0`, then `cfc g (lambdaHat A T x) ≠ 0`
(via `eqOn_of_cfc_eq_cfc` against `cfc 0`). -/
theorem cfc_ne_zero_of_eigenvalue
    {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} {x : X} {g : ℝ → ℝ} {j : Fin d}
    (hspec : _root_.spectrum ℝ (lambdaHat A T x)
      = Set.range (fun i : Fin d => Real.exp (lamSing A T x (i : ℕ))))
    (hcont : ContinuousOn g (_root_.spectrum ℝ (lambdaHat A T x)))
    (hg : g (Real.exp (lamSing A T x (j : ℕ))) ≠ 0) :
    cfc g (lambdaHat A T x) ≠ 0 := by
  intro h0
  have hsa : IsSelfAdjoint (lambdaHat A T x) := lambdaHat_isSelfAdjoint A T x
  have hmem : Real.exp (lamSing A T x (j : ℕ)) ∈ _root_.spectrum ℝ (lambdaHat A T x) := by
    rw [hspec]; exact ⟨j, rfl⟩
  have hcfceq : cfc g (lambdaHat A T x) = cfc (0 : ℝ → ℝ) (lambdaHat A T x) := by
    rw [cfc_zero]; exact h0
  have heqon := eqOn_of_cfc_eq_cfc (R := ℝ) (a := lambdaHat A T x) hcfceq hcont
    continuousOn_const hsa
  exact hg (heqon hmem)

/-! ## Range membership for idempotent matrices -/

omit [NeZero d] in
/-- `toEuclideanLin` turns matrix multiplication into composition (applied form). -/
theorem toEuclideanLin_mul_apply
    (M N : Matrix (Fin d) (Fin d) ℝ) (w : EuclideanSpace ℝ (Fin d)) :
    Matrix.toEuclideanLin (M * N) w
      = Matrix.toEuclideanLin M (Matrix.toEuclideanLin N w) := by
  have hcoe : ∀ (P : Matrix (Fin d) (Fin d) ℝ) (u : EuclideanSpace ℝ (Fin d)),
      Matrix.toEuclideanLin P u = Matrix.toEuclideanCLM (𝕜 := ℝ) P u := fun P u => by
    rw [← Matrix.coe_toEuclideanCLM_eq_toEuclideanLin]; rfl
  rw [hcoe, hcoe, hcoe, map_mul]; rfl

omit [NeZero d] in
theorem mem_range_toEuclideanCLM_iff
    {Q : Matrix (Fin d) (Fin d) ℝ} (hidem : Q * Q = Q) {v : EuclideanSpace ℝ (Fin d)} :
    v ∈ LinearMap.range (Matrix.toEuclideanCLM (𝕜 := ℝ) Q).toLinearMap
      ↔ Matrix.toEuclideanLin Q v = v := by
  have hcoe : ∀ w, (Matrix.toEuclideanCLM (𝕜 := ℝ) Q).toLinearMap w
      = Matrix.toEuclideanLin Q w :=
    fun w => rfl
  -- idempotency at the CLM level, via `toEuclideanLin_mul_apply`.
  have hLidem : ∀ w, Matrix.toEuclideanLin Q (Matrix.toEuclideanLin Q w)
      = Matrix.toEuclideanLin Q w := by
    intro w; rw [← toEuclideanLin_mul_apply, hidem]
  rw [LinearMap.mem_range]
  constructor
  · rintro ⟨u, rfl⟩
    simp only [hcoe]; exact hLidem u
  · intro hv; exact ⟨v, by simp only [hcoe]; exact hv⟩

omit [MeasurableSpace X] [NeZero d] in
/-- **Finding a gap strictly below a non-eigenvalue.**  If `s` is not among the `lamSing` values,
there is `t' < s` with no `lamSing j` in `(t', s]`. -/
theorem exists_gap_below
    {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} {x : X} {s : ℝ}
    (hnot : ∀ j : Fin d, lamSing A T x (j : ℕ) ≠ s) :
    ∃ t' : ℝ, t' < s ∧
      ∀ j : Fin d, lamSing A T x (j : ℕ) ≤ t' ∨ s < lamSing A T x (j : ℕ) := by
  classical
  set L : Finset ℝ :=
    (Finset.univ.image (fun j : Fin d => lamSing A T x (j : ℕ))).filter (· < s) with hL
  by_cases hne : L.Nonempty
  · refine ⟨L.max' hne, ?_, ?_⟩
    · -- `max' < s` since every element of `L` is `< s`.
      have hm := L.max'_mem hne
      have : L.max' hne
          ∈ (Finset.univ.image (fun j : Fin d => lamSing A T x (j : ℕ))).filter (· < s) := hm
      exact (Finset.mem_filter.mp this).2
    · intro j
      by_cases hlt : lamSing A T x (j : ℕ) < s
      · left
        refine Finset.le_max' L _ ?_
        rw [hL, Finset.mem_filter]
        exact ⟨Finset.mem_image_of_mem _ (Finset.mem_univ j), hlt⟩
      · right
        exact lt_of_le_of_ne (not_lt.mp hlt) (Ne.symm (hnot j))
  · refine ⟨s - 1, by linarith, ?_⟩
    intro j
    right
    -- `L` empty means no `lamSing j < s`.
    have : lamSing A T x (j : ℕ) ∉ L := by
      rw [Finset.not_nonempty_iff_eq_empty] at hne; simp [hne]
    rw [hL, Finset.mem_filter, not_and] at this
    have hge : ¬ lamSing A T x (j : ℕ) < s :=
      this (Finset.mem_image_of_mem _ (Finset.mem_univ j))
    exact lt_of_le_of_ne (not_lt.mp hge) (Ne.symm (hnot j))

omit [MeasurableSpace X] [NeZero d] in
/-- **Finding a gap with no eigenvalue in the open interval `(t', s)`.**  For ANY `s` there is
`t' < s` with no `lamSing j` strictly between `t'` and `s` (each `lamSing j` is `≤ t'` or
`≥ s`). -/
theorem exists_gap_below_open
    {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} {x : X} (s : ℝ) :
    ∃ t' : ℝ, t' < s ∧
      ∀ j : Fin d, lamSing A T x (j : ℕ) ≤ t' ∨ s ≤ lamSing A T x (j : ℕ) := by
  classical
  set L : Finset ℝ :=
    (Finset.univ.image (fun j : Fin d => lamSing A T x (j : ℕ))).filter (· < s) with hL
  by_cases hne : L.Nonempty
  · refine ⟨L.max' hne, ?_, ?_⟩
    · have hm := L.max'_mem hne
      have : L.max' hne
          ∈ (Finset.univ.image (fun j : Fin d => lamSing A T x (j : ℕ))).filter (· < s) := hm
      exact (Finset.mem_filter.mp this).2
    · intro j
      by_cases hlt : lamSing A T x (j : ℕ) < s
      · left
        refine Finset.le_max' L _ ?_
        rw [hL, Finset.mem_filter]
        exact ⟨Finset.mem_image_of_mem _ (Finset.mem_univ j), hlt⟩
      · right; exact not_lt.mp hlt
  · refine ⟨s - 1, by linarith, ?_⟩
    intro j
    right
    have hnotmem : lamSing A T x (j : ℕ) ∉ L := by
      rw [Finset.not_nonempty_iff_eq_empty] at hne; simp [hne]
    rw [hL, Finset.mem_filter, not_and] at hnotmem
    exact not_lt.mp (hnotmem (Finset.mem_image_of_mem _ (Finset.mem_univ j)))

/-! ## a.e. identification `lamSing = lam0` -/

/-- A.e., the per-point exponents `lamSing A T x j` equal the deterministic `lam0 j` for every
`j : Fin d`. -/
theorem ae_lamSing_eq_lam0
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X}
    {A : X → Matrix (Fin d) (Fin d) ℝ}
    (lam0 : ℕ → ℝ)
    (hlam0 : ∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
      Filter.atTop (𝓝 (lam0 i))) :
    ∀ᵐ x ∂μ, ∀ j : Fin d, lamSing A T x (j : ℕ) = lam0 (j : ℕ) := by
  rw [ae_all_iff]
  intro j
  filter_upwards [hlam0 (j : ℕ) j.isLt] with x hx
  exact lamSing_eq_of_tendsto hx

/-! ## Upper spectral bound: `hub_spec` -/

/-- **`hub_spec`: every realized exponent is deterministic.**  A.e., the limsup spectrum is
contained in the deterministic distinct-exponent set `distinctExp lam0 d`. -/
theorem lyapunovSpectrum_subset_distinctExp_of_slowflag
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X} (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (hslowflag : ∀ᵐ x ∂μ, ∀ t : ℝ, vslow A T (Real.exp t) x = lambdaSublevel A T x t)
    (lam0 : ℕ → ℝ)
    (hlam0 : ∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
      Filter.atTop (𝓝 (lam0 i))) :
    ∀ᵐ x ∂μ, lyapunovSpectrum A T x ⊆ distinctExp lam0 d := by
  filter_upwards [isUltrametricGrowth_lambdaBar hT hA hAmeas hint hint',
    spectrum_lambdaHat_eq_ae hT hA hAmeas hint hint', hslowflag,
    ae_lamSing_eq_lam0 lam0 hlam0] with x hx hspec hflag hlameq
  rw [lyapunovSpectrum_subset_iff_lambdaBar_mem hx]
  intro v hv
  set s := lambdaBar A T x v with hs
  -- Step 1: `s` is one of the `lamSing` values.
  have hattained : ∃ j : Fin d, lamSing A T x (j : ℕ) = s := by
    by_contra hcon
    push Not at hcon
    obtain ⟨t', ht'lt, hgap⟩ := exists_gap_below (s := s) hcon
    -- `vslow (exp t') = vslow (exp s)`.
    have hVeq : vslow A T (Real.exp t') x = vslow A T (Real.exp s) x :=
      vslow_eq_of_gap hspec ht'lt.le hgap
    -- `v ∈ vslow (exp s)` since `lambdaBar v = s ≤ s`.
    have hmem_s : v ∈ vslow A T (Real.exp s) x := by
      rw [hflag s, mem_lambdaSublevel hx]; exact Or.inr le_rfl
    -- transport to `vslow (exp t') = lambdaSublevel t'`, giving `lambdaBar v ≤ t'`.
    rw [← hVeq, hflag t', mem_lambdaSublevel hx] at hmem_s
    rcases hmem_s with h0 | hle
    · exact hv h0
    · exact absurd hle (not_le.mpr ht'lt)
  obtain ⟨j, hj⟩ := hattained
  exact ⟨(j : ℕ), j.isLt, by rw [← hlameq j, hj]⟩

/-! ## Lower spectral bound: `hlb_spec` -/

/-- **`hlb_spec`: every deterministic exponent is realized.**  A.e., the deterministic
distinct-exponent set is contained in the limsup spectrum: each `lam0 j` (`j < d`) is the value
`lambdaBar A T x v` of some nonzero `v`, exhibited by the rank-jump of the slow projector at the
eigenvalue `exp (lamSing j) = exp (lam0 j)`. -/
theorem distinctExp_subset_lyapunovSpectrum_of_slowflag
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X} (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (hslowflag : ∀ᵐ x ∂μ, ∀ t : ℝ, vslow A T (Real.exp t) x = lambdaSublevel A T x t)
    (lam0 : ℕ → ℝ)
    (hlam0 : ∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
      Filter.atTop (𝓝 (lam0 i))) :
    ∀ᵐ x ∂μ, distinctExp lam0 d ⊆ lyapunovSpectrum A T x := by
  filter_upwards [isUltrametricGrowth_lambdaBar hT hA hAmeas hint hint',
    spectrum_lambdaHat_eq_ae hT hA hAmeas hint hint', hslowflag,
    ae_lamSing_eq_lam0 lam0 hlam0] with x hx hspec hflag hlameq
  rw [distinctExp_subset_iff_lambdaBar_attained hx]
  intro j hj
  -- The eigenvalue index and the target exponent `s = lamSing ⟨j,hj⟩ = lam0 j`.
  set j' : Fin d := ⟨j, hj⟩ with hj'
  set s : ℝ := lamSing A T x (j' : ℕ) with hsdef
  have hsval : s = lam0 j := by rw [hsdef, hlameq j']
  -- Choose a gap `t' < s` with no eigenvalue strictly between.
  obtain ⟨t', ht'lt, hgap⟩ := exists_gap_below_open (A := A) (T := T) (x := x) s
  -- The two nested projectors and their difference.
  set Qs := slowProjector A T (Real.exp s) x with hQs
  set Qt := slowProjector A T (Real.exp t') x with hQt
  have hQsidem : Qs * Qs = Qs := slowProjector_mul_self A T (Real.exp s) x
  have hQtidem : Qt * Qt = Qt := slowProjector_mul_self A T (Real.exp t') x
  have hQtQs : Qt * Qs = Qt := slowProjector_mul_le ht'lt.le
  have hQsQt : Qs * Qt = Qt := by
    have hsaS : IsSelfAdjoint Qs := slowProjector_isSelfAdjoint A T (Real.exp s) x
    have hsaT : IsSelfAdjoint Qt := slowProjector_isSelfAdjoint A T (Real.exp t') x
    have hstar := congrArg star hQtQs
    rw [Matrix.star_mul, hsaS.star_eq, hsaT.star_eq] at hstar
    exact hstar
  -- The difference `D := Qs - Qt`, written as a single CFC.
  have hcontS : ContinuousOn (Set.indicator (Set.Iic (Real.exp s)) (1 : ℝ → ℝ))
      (_root_.spectrum ℝ (lambdaHat A T x)) :=
    (Matrix.finite_real_spectrum (A := lambdaHat A T x)).continuousOn _
  have hcontT : ContinuousOn (Set.indicator (Set.Iic (Real.exp t')) (1 : ℝ → ℝ))
      (_root_.spectrum ℝ (lambdaHat A T x)) :=
    (Matrix.finite_real_spectrum (A := lambdaHat A T x)).continuousOn _
  set g : ℝ → ℝ := fun e => Set.indicator (Set.Iic (Real.exp s)) (1 : ℝ → ℝ) e
    - Set.indicator (Set.Iic (Real.exp t')) (1 : ℝ → ℝ) e with hg
  have hDcfc : Qs - Qt = cfc g (lambdaHat A T x) := by
    rw [hQs, hQt, slowProjector, slowProjector, hg]
    exact (cfc_sub _ _ (lambdaHat A T x) hcontS hcontT).symm
  -- `D ≠ 0`: its symbol `g` is `1` at the eigenvalue `exp s = exp (lamSing j')`.
  have hcontg : ContinuousOn g (_root_.spectrum ℝ (lambdaHat A T x)) := hcontS.sub hcontT
  have hgval : g (Real.exp (lamSing A T x (j' : ℕ))) ≠ 0 := by
    have h1 : Set.indicator (Set.Iic (Real.exp s)) (1 : ℝ → ℝ) (Real.exp s) = 1 :=
      Set.indicator_of_mem (Set.mem_Iic.mpr le_rfl) _
    have h0 : Set.indicator (Set.Iic (Real.exp t')) (1 : ℝ → ℝ) (Real.exp s) = 0 := by
      refine Set.indicator_of_notMem ?_ _
      simp only [Set.mem_Iic, not_le]
      exact Real.exp_lt_exp.mpr ht'lt
    change g (Real.exp s) ≠ 0
    rw [hg]
    change Set.indicator (Set.Iic (Real.exp s)) (1 : ℝ → ℝ) (Real.exp s)
      - Set.indicator (Set.Iic (Real.exp t')) (1 : ℝ → ℝ) (Real.exp s) ≠ 0
    rw [h1, h0]; norm_num
  have hDne : Qs - Qt ≠ 0 := by
    rw [hDcfc]; exact cfc_ne_zero_of_eigenvalue (j := j') hspec hcontg hgval
  -- Pick `w` with `toEuclideanLin D w ≠ 0`; set `v := toEuclideanLin D w`.
  have hlinne : Matrix.toEuclideanLin (Qs - Qt) ≠ 0 := by
    intro h; exact hDne (by
      have := congrArg (Matrix.toEuclideanLin (𝕜 := ℝ)).symm h
      simpa using this)
  obtain ⟨w, hw⟩ := DFunLike.ne_iff.mp hlinne
  set v : EuclideanSpace ℝ (Fin d) := Matrix.toEuclideanLin (Qs - Qt) w with hvdef
  have hvne : v ≠ 0 := hw
  -- `Qs * D = D` and `Qt * D = 0`.
  have hQsD : Qs * (Qs - Qt) = Qs - Qt := by
    rw [Matrix.mul_sub, hQsidem, hQsQt]
  have hQtD : Qt * (Qs - Qt) = 0 := by
    rw [Matrix.mul_sub, hQtQs, hQtidem, sub_self]
  -- `v ∈ vslow (exp s)`.
  have hmem_s : v ∈ vslow A T (Real.exp s) x := by
    rw [vslow, mem_range_toEuclideanCLM_iff hQsidem, hvdef, ← toEuclideanLin_mul_apply, hQsD]
  -- `v ∉ vslow (exp t')`: `Qt v = Qt D w = 0 ≠ v`.
  have hnmem_t : v ∉ vslow A T (Real.exp t') x := by
    rw [vslow, mem_range_toEuclideanCLM_iff hQtidem, hvdef, ← toEuclideanLin_mul_apply, hQtD,
      map_zero]
    exact fun h => hvne h.symm
  -- Translate through `hslowflag`: `lambdaBar v ≤ s` and `¬ (lambdaBar v ≤ t')`.
  have hle : lambdaBar A T x v ≤ s := by
    rw [hflag s, mem_lambdaSublevel hx] at hmem_s
    rcases hmem_s with h0 | hle
    · exact absurd h0 hvne
    · exact hle
  have hgt : t' < lambdaBar A T x v := by
    rw [hflag t', mem_lambdaSublevel hx] at hnmem_t
    push Not at hnmem_t
    exact hnmem_t.2
  -- `lambdaBar v` is some `lamSing k`, hence (no eigenvalue in `(t', s)`) equals `s`.
  have hbarmem : lambdaBar A T x v ∈ lyapunovSpectrum A T x :=
    lambdaBar_mem_lyapunovSpectrum hx hvne
  -- Using `lambdaBar v ∈ {lamSing k}`, we prove `lambdaBar v = s` directly.
  have hbareq : lambdaBar A T x v = s := by
    -- Suppose `lambdaBar v ≠ s`.  It lies in `(t', s]`, hence in `(t', s)`, but it is an
    -- eigenvalue (a `lamSing k`), contradicting the gap.
    by_contra hne
    have hlt : lambdaBar A T x v < s := lt_of_le_of_ne hle hne
    -- `lambdaBar v` is realized so it is some `lamSing k` (the attainment argument).
    have hk : ∃ k : Fin d, lamSing A T x (k : ℕ) = lambdaBar A T x v := by
      by_contra hcon
      push Not at hcon
      obtain ⟨u', hu'lt, hgapu⟩ := exists_gap_below (s := lambdaBar A T x v) hcon
      have hVeq : vslow A T (Real.exp u') x = vslow A T (Real.exp (lambdaBar A T x v)) x :=
        vslow_eq_of_gap hspec hu'lt.le hgapu
      have hmem_b : v ∈ vslow A T (Real.exp (lambdaBar A T x v)) x := by
        rw [hflag (lambdaBar A T x v), mem_lambdaSublevel hx]; exact Or.inr le_rfl
      rw [← hVeq, hflag u', mem_lambdaSublevel hx] at hmem_b
      rcases hmem_b with h0 | hble
      · exact hvne h0
      · exact absurd hble (not_le.mpr hu'lt)
    obtain ⟨k, hk⟩ := hk
    -- `t' < lamSing k = lambdaBar v < s`, contradicting `hgap k` (which says `≤ t'` or `≥ s`).
    rcases hgap k with hkle | hkge
    · rw [hk] at hkle; exact absurd hkle (not_le.mpr hgt)
    · rw [hk] at hkge; exact absurd hkge (not_le.mpr hlt)
  exact ⟨v, hvne, by rw [hbareq, hsval]⟩

/-! ## Per-stratum liminf lower bound -/

/-- **Per-stratum liminf lower bound (`hlb`).**  On each stratum `vflag i.castSucc \ vflag i.succ`,
the cocycle grows at least at rate `specList A T x i`.  The argument sweeps thresholds
`c = exp (specList i − ε')` strictly below the stratum eigenvalue up to it: for each such `c`
(not an eigenvalue), `1 - slowProjector c = cfc (indicator (Ioi c)) lambdaHat` has nonzero
action on `v` (else `v ∈ vslow c`, contradicting `lambdaBar v = specList i > log c`), and
`hident` supplies the band-projector convergence feeding `log_le_liminf_log_cocycle_apply`. -/
theorem specList_le_liminf_inv_mul_log_norm_cocycle_apply_of_slowflag
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X} (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (hident : ∀ᵐ x ∂μ, ∀ c : ℝ, 0 < c →
      (∀ i : Fin d, Real.exp (lamSing A T x (i : ℕ)) ≠ c) →
      Filter.Tendsto (fun n => bandProjector A T (Set.indicator (Set.Ioi c) 1) n x)
        Filter.atTop (𝓝 (cfc (Set.indicator (Set.Ioi c) (1 : ℝ → ℝ)) (lambdaHat A T x))))
    (hslowflag : ∀ᵐ x ∂μ, ∀ t : ℝ, vslow A T (Real.exp t) x = lambdaSublevel A T x t) :
    ∀ᵐ x ∂μ, ∀ i : Fin (specCard A T x),
      ∀ v ∈ (vflag A T x i.castSucc : Set (EuclideanSpace ℝ (Fin d))),
        v ∉ vflag A T x i.succ →
        specList A T x i ≤ Filter.liminf (fun n : ℕ => (n : ℝ)⁻¹ *
          Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) Filter.atTop := by
  filter_upwards [isUltrametricGrowth_lambdaBar hT hA hAmeas hint hint',
    spectrum_lambdaHat_eq_ae hT hA hAmeas hint hint', hident, hslowflag,
    isBoundedUnder_log_norm_cocycle_apply hT A hA hAmeas hint hint']
    with x hx hspec hidentx hflag hbddx i v hv hvnot
  -- `v ≠ 0` and `lambdaBar v = specList i =: s*`.
  have hvne : v ≠ 0 := fun h => hvnot (h ▸ Submodule.zero_mem _)
  set sstar : ℝ := specList A T x i with hsstar
  have hbar : lambdaBar A T x v = sstar := lambdaBar_eq_on_stratum hx i hv hvnot
  -- cobounded-below from FK boundedness.
  obtain ⟨hba, _hbb⟩ := hbddx v hvne
  have hcob : IsCoboundedUnder (· ≥ ·) atTop
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) :=
    hba.isCoboundedUnder_ge
  set L : ℝ := Filter.liminf (fun n : ℕ => (n : ℝ)⁻¹ *
    Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) Filter.atTop with hL
  -- The gap below `sstar` with no eigenvalue in `(t', sstar)`.
  obtain ⟨t', ht'lt, hgap⟩ := exists_gap_below_open (A := A) (T := T) (x := x) sstar
  -- Suffices: `r ≤ L` for every `r < sstar`.
  refine le_of_forall_lt fun r hr => ?_
  -- Choose `r' ∈ (max r t', sstar)`; then `r < r'`, `t' < r'`, `r' < sstar`.
  set m : ℝ := max r t' with hm
  have hmlt : m < sstar := max_lt hr ht'lt
  set r' : ℝ := (m + sstar) / 2 with hr'
  have hr'm : m < r' := by rw [hr']; linarith
  have hr'lt : r' < sstar := by rw [hr']; linarith
  have hrr' : r < r' := lt_of_le_of_lt (le_max_left _ _) hr'm
  have ht'r' : t' < r' := lt_of_le_of_lt (le_max_right _ _) hr'm
  -- `c := exp r'`, positive and not an eigenvalue.
  set c : ℝ := Real.exp r' with hc
  have hcpos : 0 < c := Real.exp_pos _
  have hcne : ∀ k : Fin d, Real.exp (lamSing A T x (k : ℕ)) ≠ c := by
    intro k
    rw [hc, ne_eq, Real.exp_eq_exp]
    rcases hgap k with hkle | hkge
    · exact ne_of_lt (lt_of_le_of_lt hkle ht'r')
    · exact ne_of_gt (lt_of_lt_of_le hr'lt hkge)
  -- The band projector limit is `1 - slowProjector c = cfc (indicator (Ioi c)) lambdaHat`.
  have htend := hidentx c hcpos hcne
  set P : Matrix (Fin d) (Fin d) ℝ :=
    cfc (Set.indicator (Set.Ioi c) (1 : ℝ → ℝ)) (lambdaHat A T x) with hP
  have hPeq : P = (1 : Matrix (Fin d) (Fin d) ℝ) - slowProjector A T c x :=
    (one_sub_slowProjector).symm
  -- `v ∉ vslow c`: else `lambdaBar v ≤ r' < sstar`, contradiction.
  have hvnotslow : v ∉ vslow A T c x := by
    rw [hc, hflag r', mem_lambdaSublevel hx]
    push Not
    exact ⟨hvne, by rw [hbar]; exact hr'lt⟩
  -- `toEuclideanLin P v ≠ 0`: `P v = v - Qs v`; if `0` then `Qs v = v`, i.e. `v ∈ vslow c`.
  have hPv : Matrix.toEuclideanLin P v ≠ 0 := by
    intro h0
    apply hvnotslow
    rw [vslow, mem_range_toEuclideanCLM_iff (slowProjector_mul_self A T c x)]
    -- `P = 1 - Qs`, `toEuclideanLin P v = v - toEuclideanLin Qs v = 0 ⟹ toEuclideanLin Qs v = v`.
    have hmapsub : Matrix.toEuclideanLin ((1 : Matrix (Fin d) (Fin d) ℝ) - slowProjector A T c x)
        = Matrix.toEuclideanLin 1 - Matrix.toEuclideanLin (slowProjector A T c x) :=
      map_sub _ _ _
    have hone : Matrix.toEuclideanLin (1 : Matrix (Fin d) (Fin d) ℝ) v = v := by
      rw [← Matrix.coe_toEuclideanCLM_eq_toEuclideanLin (𝕜 := ℝ)]
      simp
    have hsplit : Matrix.toEuclideanLin P v
        = v - Matrix.toEuclideanLin (slowProjector A T c x) v := by
      rw [hPeq, hmapsub, LinearMap.sub_apply, hone]
    rw [hsplit, sub_eq_zero] at h0
    exact h0.symm
  -- Apply the liminf lower bound.
  have hkey := log_le_liminf_log_cocycle_apply A T hA hcpos htend hPv hcob
  rw [hc, Real.log_exp] at hkey
  -- `r < r' ≤ L`.
  exact lt_of_lt_of_le hrr' hkey

end ErgodicTheory
