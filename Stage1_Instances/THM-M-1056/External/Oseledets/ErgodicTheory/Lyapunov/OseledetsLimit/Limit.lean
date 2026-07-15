/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.OseledetsLimit.ProjectorIncrement

/-!
# Assembling the Oseledets limit

The final assembly of the singular-value layer. The eigenvalues `μᵢ,ₙ = σᵢ^{1/n}` of `qpow A T n x`
converge a.e. to the exponentials `e^{λᵢ}` of the Lyapunov exponents `λᵢ = Γ_{i+1} − Γ_i`, so the
candidate matrices `qpow A T n x` converge a.e. to a limiting positive semidefinite matrix
`oseledetsLimit`, assembled from the block approximant `stepVal` and the convergent band projectors.
This produces the orbit log-growth limits along the eigenspace filtration.

## Main definitions

* `ErgodicTheory.stepVal` — the block-value step function whose CFC on `qpow` is the block
  approximant.
* `ErgodicTheory.oseledetsLimit` — the limiting matrix `Λ x = lim_n qpow A T n x`.

## Main results

* `ErgodicTheory.tendsto_qpow`, `ErgodicTheory.tendsto_oseledetsLimit` — a.e. convergence of the
  candidates.
* `ErgodicTheory.oseledetsLimit_isSelfAdjoint`, `ErgodicTheory.oseledetsLimit_posSemidef`,
  `ErgodicTheory.oseledetsLimit_eigenvalues₀_eq` — structure of the limit and its eigenvalues.
* `ErgodicTheory.ae_tendsto_log_cocycle_apply_of_eq_exponents` — the two-sided orbit log-growth
  limit in the equal-exponents (conformal) regime.
-/

open Module InnerProductSpace MeasureTheory Filter Topology
open scoped Matrix.Norms.L2Operator Matrix MatrixOrder RealInnerProductSpace

noncomputable section

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ}
variable [NeZero d]
variable {μ : Measure X} {T : X → X}

/-! ## Assembling the Oseledets limit `qpow A T n x → Λ x`

The final assembly. The eigenvalues `μᵢ,ₙ = σᵢ^{1/n}` of `qpow A T n x` converge a.e. to the
exponentials `e^{λᵢ}` of the (deterministic, antitone) Lyapunov exponents `λᵢ = Γ_{i+1} − Γ_i`. We
group the spectrum at thresholds `cₖ = exp((λₖ + λₖ₋₁)/2)`, one per index `1 ≤ k < d`. The candidate
limit at level `n` is the **block approximant**
`Λₙ x := e^{λ_{d-1}} • 1 + ∑_{k=1}^{d-1} (e^{λₖ₋₁} − e^{λₖ}) • bandProjector (Ioi cₖ) n x`.
Two facts combine:
* `‖qpow A T n x − Λₙ x‖ ≤ maxᵢ |μᵢ,ₙ − e^{λᵢ}| → 0` (the spectral-block operator-norm bound
  `norm_cfc_le_of_forall_eigenvalue_abs_le`, since `Λₙ = cfc h (qpow…)` for the block-value step
  function `h`, and on the spectrum `h` reproduces the right exponential);
* `Λₙ x → Λ x` because each band projector converges a.e. (`tendsto_bandProjector_of_gap` at the
  genuine gaps; the non-gap terms have coefficient `0`).
Hence `qpow A T n x → Λ x` a.e., discharging `oseledetsLimitExists`. -/

/-- **Telescoping of the exponential increments.** For any `f : ℕ → ℝ` and `j < d`,
`f (d-1) + ∑_{k ∈ Ico (j+1) d} (f (k-1) − f k) = f j`. The Abel-summation identity behind the block
approximant: summing the increments `e^{λₖ₋₁} − e^{λₖ}` over the indices above `j` telescopes to
`e^{λⱼ} − e^{λ_{d-1}}`. -/
theorem sum_Ico_increment_telescope (f : ℕ → ℝ) {D : ℕ} {j : ℕ} (hj : j < D) :
    f (D - 1) + ∑ k ∈ Finset.Ico (j + 1) D, (f (k - 1) - f k) = f j := by
  have htel : ∑ k ∈ Finset.Ico (j + 1) D, (f (k - 1) - f k) = f j - f (D - 1) := by
    rw [Finset.sum_Ico_eq_sum_range]
    have hcongr : ∀ i ∈ Finset.range (D - (j + 1)), f (j + 1 + i - 1) - f (j + 1 + i)
        = -(f (j + (i + 1)) - f (j + i)) := by
      intro i _
      have h1 : j + 1 + i - 1 = j + i := by omega
      have h2 : j + 1 + i = j + (i + 1) := by omega
      rw [h1, h2]; ring
    rw [Finset.sum_congr rfl hcongr, Finset.sum_neg_distrib,
      Finset.sum_range_sub (fun m => f (j + m))]
    have hd1 : j + (D - (j + 1)) = D - 1 := by omega
    simp only [hd1, Nat.add_zero]
    ring
  rw [htel]; ring

/-- The **block-value step function** for an antitone exponent sequence `lam`. On `ℝ`,
`stepVal lam D t = e^{λ_{D-1}} + ∑_{k=1}^{D-1} (e^{λₖ₋₁} − e^{λₖ}) · 𝟙_{(cₖ, ∞)}(t)`, where
`cₖ = exp((λₖ + λₖ₋₁)/2)` is the threshold strictly inside the `k`-th gap. It is the function whose
continuous functional calculus on `qpow A T n x` produces the block approximant. -/
noncomputable def stepVal (lam : ℕ → ℝ) (D : ℕ) (t : ℝ) : ℝ :=
  Real.exp (lam (D - 1)) +
    ∑ k ∈ Finset.Ico 1 D, (Real.exp (lam (k - 1)) - Real.exp (lam k)) *
      Set.indicator (Set.Ioi (Real.exp ((lam k + lam (k - 1)) / 2))) (1 : ℝ → ℝ) t

/-- **The step function reproduces the exponentials on the spectrum.** If `lam` is antitone on
`[0, D)` (`hanti`) and `j < D`, then `stepVal lam D (e^{λⱼ}) = e^{λⱼ}`: the threshold indicators
select exactly the increments above index `j`, which telescope (`sum_Ico_increment_telescope`). -/
theorem stepVal_exp_lam (lam : ℕ → ℝ) (D : ℕ)
    (hanti : ∀ a b : ℕ, a ≤ b → b < D → lam b ≤ lam a) {j : ℕ} (hj : j < D) :
    stepVal lam D (Real.exp (lam j)) = Real.exp (lam j) := by
  rw [stepVal]
  have hterm : ∀ k ∈ Finset.Ico 1 D,
      (Real.exp (lam (k - 1)) - Real.exp (lam k)) *
        Set.indicator (Set.Ioi (Real.exp ((lam k + lam (k - 1)) / 2))) (1 : ℝ → ℝ)
          (Real.exp (lam j))
      = (Real.exp (lam (k - 1)) - Real.exp (lam k)) *
          (if j + 1 ≤ k then (1 : ℝ) else 0) := by
    intro k hk
    rw [Finset.mem_Ico] at hk
    obtain ⟨hk1, hkD⟩ := hk
    -- antitone facts at indices k-1, k
    have hle : lam k ≤ lam (k - 1) := hanti (k - 1) k (by omega) hkD
    by_cases hgap : lam k = lam (k - 1)
    · -- non-gap: coefficient is 0
      rw [hgap]; ring
    · -- gap: lam k < lam (k-1)
      have hlt : lam k < lam (k - 1) := lt_of_le_of_ne hle hgap
      have hcoef_pos : 0 < Real.exp (lam (k - 1)) - Real.exp (lam k) := by
        have := Real.exp_lt_exp.mpr hlt; linarith
      congr 1
      by_cases hjk : j + 1 ≤ k
      · -- j ≤ k-1, so lam j ≥ lam (k-1) > threshold
        rw [if_pos hjk]
        have hlamj : lam (k - 1) ≤ lam j := hanti j (k - 1) (by omega) (by omega)
        have hmem : Real.exp (lam j) ∈ Set.Ioi (Real.exp ((lam k + lam (k - 1)) / 2)) := by
          rw [Set.mem_Ioi, Real.exp_lt_exp]
          have : (lam k + lam (k - 1)) / 2 < lam (k - 1) := by linarith
          linarith
        rw [Set.indicator_of_mem hmem, Pi.one_apply]
      · -- j ≥ k, so lam j ≤ lam k < threshold
        rw [if_neg hjk]
        have hjge : k ≤ j := by omega
        have hlamj : lam j ≤ lam k := hanti k j hjge hj
        have hnmem : Real.exp (lam j) ∉ Set.Ioi (Real.exp ((lam k + lam (k - 1)) / 2)) := by
          rw [Set.mem_Ioi, not_lt, Real.exp_le_exp]
          have : lam k < (lam k + lam (k - 1)) / 2 := by linarith
          linarith
        rw [Set.indicator_of_notMem hnmem]
  rw [Finset.sum_congr rfl hterm]
  -- restrict the if to the interval Ico (j+1) D
  have hsum : ∑ k ∈ Finset.Ico 1 D,
        (Real.exp (lam (k - 1)) - Real.exp (lam k)) * (if j + 1 ≤ k then (1 : ℝ) else 0)
      = ∑ k ∈ Finset.Ico (j + 1) D, (Real.exp (lam (k - 1)) - Real.exp (lam k)) := by
    have hmulite : ∀ k,
        (Real.exp (lam (k - 1)) - Real.exp (lam k)) * (if j + 1 ≤ k then (1 : ℝ) else 0)
        = if j + 1 ≤ k then (Real.exp (lam (k - 1)) - Real.exp (lam k)) else 0 := by
      intro k; rw [mul_ite, mul_one, mul_zero]
    simp_rw [hmulite]
    rw [← Finset.sum_filter]
    apply Finset.sum_congr _ (fun k _ => rfl)
    ext k
    simp only [Finset.mem_filter, Finset.mem_Ico]
    omega
  rw [hsum, sum_Ico_increment_telescope (fun m => Real.exp (lam m)) hj]

/-- **The block approximant `cfc (stepVal) (qpow)` as a band-projector combination.** Expanding the
step function `stepVal lam D` through the linearity of the continuous functional calculus (valid on
the finite matrix spectrum): the CFC of the block-value step function on `qpow A T n x` is the
explicit linear combination of band projectors
`e^{λ_{D-1}} • 1 + ∑_{k=1}^{D-1} (e^{λₖ₋₁} − e^{λₖ}) • bandProjector (Ioi cₖ) n x`. This is the form
whose a.e. convergence follows from the per-gap band-projector convergence. -/
theorem cfc_stepVal_qpow_eq (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (lam : ℕ → ℝ) (D n : ℕ)
    (x : X) :
    cfc (stepVal lam D) (qpow A T n x)
      = Real.exp (lam (D - 1)) • (1 : Matrix (Fin d) (Fin d) ℝ)
        + ∑ k ∈ Finset.Ico 1 D, (Real.exp (lam (k - 1)) - Real.exp (lam k)) •
            bandProjector A T
              (Set.indicator (Set.Ioi (Real.exp ((lam k + lam (k - 1)) / 2))) 1) n x := by
  set M := qpow A T n x with hM
  have hMsa : IsSelfAdjoint M := qpow_isSelfAdjoint A T n x
  have hcont : ∀ f : ℝ → ℝ, ContinuousOn f (_root_.spectrum ℝ M) :=
    fun f => (Matrix.finite_real_spectrum (A := M)).continuousOn _
  -- stepVal = const + ∑ (coef k) • indicator k, as functions
  let ind : ℕ → ℝ → ℝ := fun k =>
    Set.indicator (Set.Ioi (Real.exp ((lam k + lam (k - 1)) / 2))) (1 : ℝ → ℝ)
  let coef : ℕ → ℝ := fun k => Real.exp (lam (k - 1)) - Real.exp (lam k)
  have hsplit : stepVal lam D
      = fun t => Real.exp (lam (D - 1)) + (∑ k ∈ Finset.Ico 1 D, (coef k • ind k)) t := by
    funext t
    simp only [stepVal, Finset.sum_apply, Pi.smul_apply, smul_eq_mul, ind, coef]
  rw [hsplit,
    cfc_const_add (Real.exp (lam (D - 1))) (∑ k ∈ Finset.Ico 1 D, (coef k • ind k)) M
      (hcont _) hMsa]
  congr 1
  · rw [Algebra.algebraMap_eq_smul_one]
  · rw [cfc_sum (fun k => coef k • ind k) M (Finset.Ico 1 D) (fun k _ => hcont _)]
    apply Finset.sum_congr rfl
    intro k _
    rw [show (coef k • ind k) = (fun x => coef k • ind k x) from rfl,
      cfc_smul (coef k) (ind k) M (hcont _)]
    rfl

/-- **The spectral-deviation bound for `M − cfc g M`.** For a self-adjoint matrix `M`, the operator
norm of `M − cfc g M` is at most the sum over the sorted eigenvalues of `|μⱼ − g μⱼ|`. (Writing
`M = cfc id M` and `M − cfc g M = cfc (· − g ·) M`, this is
`norm_cfc_le_of_forall_eigenvalue_abs_le`
with the per-eigenvalue deviation bounded by the full sum of nonnegative deviations.) -/
theorem norm_sub_cfc_le_sum_eigenvalue_dev (M : Matrix (Fin d) (Fin d) ℝ) (hMsa : IsSelfAdjoint M)
    (g : ℝ → ℝ) :
    ‖M - cfc g M‖
      ≤ ∑ j : Fin (Fintype.card (Fin d)),
          |hMsa.isHermitian.eigenvalues₀ j - g (hMsa.isHermitian.eigenvalues₀ j)| := by
  classical
  set hM := hMsa.isHermitian with hMdef
  -- M - cfc g M = cfc (fun t => t - g t) M
  have hsub : M - cfc g M = cfc (fun t => t - g t) M := by
    rw [cfc_sub (fun t => t) g M
      ((Matrix.finite_real_spectrum (A := M)).continuousOn _)
      ((Matrix.finite_real_spectrum (A := M)).continuousOn _),
      cfc_id' ℝ M]
  rw [hsub]
  set c := ∑ j : Fin (Fintype.card (Fin d)),
    |hM.eigenvalues₀ j - g (hM.eigenvalues₀ j)| with hc
  have hcnn : 0 ≤ c := Finset.sum_nonneg (fun j _ => abs_nonneg _)
  apply norm_cfc_le_of_forall_eigenvalue_abs_le M hM (fun t => t - g t) hcnn
  intro i
  -- eigenvalues i = eigenvalues₀ (e.symm i)
  set e := (Fintype.equivOfCardEq (Fintype.card_fin (Fintype.card (Fin d))))
  have hei : hM.eigenvalues i = hM.eigenvalues₀ (e.symm i) := rfl
  rw [hei]
  exact Finset.single_le_sum (f := fun j => |hM.eigenvalues₀ j - g (hM.eigenvalues₀ j)|)
    (fun j _ => abs_nonneg _) (Finset.mem_univ (e.symm i))

/-- **The deterministic per-index Lyapunov exponents.** Packaged from the ergodic `Γ_k` limits: for
an ergodic, invertible, log-integrable cocycle there is an antitone constant sequence `lam : ℕ → ℝ`
(supported on `[0, d)`) such that, for `μ`-a.e. `x` and every `i < d`, the normalized log of the
`i`-th singular value of `A⁽ⁿ⁾` converges to `lam i`. The `lam i = Γ_{i+1} − Γ_i` are the logarithms
of the eigenvalues of the Oseledets limit. -/
theorem exists_lam_tendsto_singularValue [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∃ lam : ℕ → ℝ, (∀ a b : ℕ, a ≤ b → b < d → lam b ≤ lam a) ∧
      ∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Tendsto
        (fun n : ℕ => (n : ℝ)⁻¹ *
          Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
        atTop (𝓝 (lam i)) := by
  classical
  -- The Γ_k constants for 0 ≤ k ≤ d (and 0 for k > d).
  have hΓ : ∀ k : ℕ, k ≤ d → ∃ Γk : ℝ, ∀ᵐ x ∂μ,
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (sprod A T k n x)) atTop (𝓝 Γk) :=
    fun k hk => tendsto_gammaK_of_integrableLogNorm hT hA hAmeas hint hint' hk
  choose! Γ hΓspec using hΓ
  set lam : ℕ → ℝ := fun i => Γ (i + 1) - Γ i with hlamdef
  -- a.e., the σ-limit holds at every index `i < d`
  have hσlim : ∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
      atTop (𝓝 (lam i)) := by
    intro i hi
    have ha := hΓspec (i + 1) (by omega)
    have hb := hΓspec i (by omega)
    filter_upwards [ha, hb] with x hax hbx
    exact tendsto_log_singularValue hA hi hax hbx
  -- consecutive antitonicity, from the antitone singular values
  have hcons : ∀ i : ℕ, i + 1 < d → lam (i + 1) ≤ lam i := by
    intro i hi1
    have hae : ∀ᵐ x ∂μ,
        Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
            Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues (i + 1)))
          atTop (𝓝 (lam (i + 1)))
        ∧ Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
            Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
          atTop (𝓝 (lam i)) := by
      filter_upwards [hσlim (i + 1) (by omega), hσlim i (by omega)] with x h1 h2 using ⟨h1, h2⟩
    obtain ⟨x, hx1, hx2⟩ := hae.exists
    refine le_of_tendsto_of_tendsto' hx1 hx2 (fun n => ?_)
    rcases Nat.eq_zero_or_pos n with hn | hn
    · simp [hn]
    · have hpos : (0 : ℝ) ≤ (n : ℝ)⁻¹ := by positivity
      have hσi : 0 < (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i :=
        singularValues_cocycle_pos hA n x (by omega)
      have hσi1 : 0 < (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (i + 1) :=
        singularValues_cocycle_pos hA n x (by omega)
      have hle : (Matrix.toEuclideanLin (cocycle A T n x)).singularValues (i + 1)
          ≤ (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i :=
        (Matrix.toEuclideanLin (cocycle A T n x)).singularValues_antitone (by omega)
      exact mul_le_mul_of_nonneg_left (Real.log_le_log hσi1 hle) hpos
  refine ⟨lam, ?_, hσlim⟩
  -- chain consecutive inequalities to full antitonicity on [0, d)
  intro a b hab hbd
  induction b with
  | zero =>
    have : a = 0 := by omega
    rw [this]
  | succ m ih =>
    rcases Nat.lt_or_ge a (m + 1) with hlt | hge
    · have hstep : lam (m + 1) ≤ lam m := hcons m (by omega)
      have hrec : lam m ≤ lam a := ih (by omega) (by omega)
      exact le_trans hstep hrec
    · have : a = m + 1 := by omega
      rw [this]

/-- **The per-term band-projector convergence.** For `μ`-a.e. `x` and every threshold index
`k ∈ [1, d)`, the `k`-th block term `(e^{λₖ₋₁} − e^{λₖ}) • bandProjector (Ioi cₖ) n x` converges. At
a
genuine gap (`λₖ < λₖ₋₁`) this is the band-projector convergence `tendsto_bandProjector_of_gap`; at
a
non-gap the coefficient `e^{λₖ₋₁} − e^{λₖ}` vanishes, so the term is constantly `0`. -/
theorem ae_forall_tendsto_block_term [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (lam : ℕ → ℝ) (hanti : ∀ a b : ℕ, a ≤ b → b < d → lam b ≤ lam a)
    (hσ : ∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
      atTop (𝓝 (lam i))) :
    ∀ᵐ x ∂μ, ∀ k ∈ Finset.Ico 1 d, ∃ Q : Matrix (Fin d) (Fin d) ℝ, Tendsto
      (fun n => (Real.exp (lam (k - 1)) - Real.exp (lam k)) •
        bandProjector A T (Set.indicator (Set.Ioi (Real.exp ((lam k + lam (k - 1)) / 2))) 1) n x)
      atTop (𝓝 Q) := by
  rw [eventually_all_finset]
  intro k hk
  rw [Finset.mem_Ico] at hk
  obtain ⟨hk1, hkd⟩ := hk
  by_cases hgap : lam k < lam (k - 1)
  · -- genuine gap: band projector converges
    have hclo : Real.exp (lam k) < Real.exp ((lam k + lam (k - 1)) / 2) := by
      rw [Real.exp_lt_exp]; linarith
    have hchi : Real.exp ((lam k + lam (k - 1)) / 2) < Real.exp (lam (k - 1)) := by
      rw [Real.exp_lt_exp]; linarith
    have hband := tendsto_bandProjector_of_gap hT hA hAmeas hint hint'
      (Real.exp ((lam k + lam (k - 1)) / 2)) hk1 hkd (lam k) (lam (k - 1)) hgap hclo hchi
      (by
        have := hσ k hkd
        -- index k singular value, careful: hσ for k uses index k; need (k-1) handling below
        exact this)
      (by
        have := hσ (k - 1) (by omega)
        exact this)
    filter_upwards [hband] with x hx
    obtain ⟨P, hP⟩ := hx
    exact ⟨(Real.exp (lam (k - 1)) - Real.exp (lam k)) • P, hP.const_smul _⟩
  · -- non-gap: coefficient is zero, term is constantly 0
    have hcoef : Real.exp (lam (k - 1)) - Real.exp (lam k) = 0 := by
      have hle : lam k ≤ lam (k - 1) := hanti (k - 1) k (by omega) hkd
      have : lam (k - 1) = lam k := le_antisymm (not_lt.mp hgap) hle
      rw [this]; ring
    filter_upwards with x
    refine ⟨0, ?_⟩
    simp only [hcoef, zero_smul]
    exact tendsto_const_nhds

/-- **The Oseledets limit exists.** Discharges `oseledetsLimitExists`: for `μ`-a.e. `x`, the
candidate matrices `qpow A T n x = (Qₙ)^{1/(2n)}` converge in the matrix metric to a single
matrix `Λ x`.

The proof combines the four banked ingredients. The eigenvalues `μⱼ,ₙ = σⱼ^{1/n}` converge to the
exponentials `e^{λⱼ}` of the deterministic exponents (`exists_lam_tendsto_singularValue` +
`eigenvalues_qpow_tendsto`). The block approximant `Λₙ x = cfc (stepVal lam d) (qpow…)` then
satisfies
`‖qpow A T n x − Λₙ x‖ ≤ ∑ⱼ |μⱼ,ₙ − stepVal(μⱼ,ₙ)| → 0` (`norm_sub_cfc_le_sum_eigenvalue_dev`, with
each summand eventually `|μⱼ,ₙ − e^{λⱼ}|` since `stepVal` reproduces the exponentials on the
spectrum — `stepVal_exp_lam`), while `Λₙ x` converges as a finite combination of convergent
band projectors (`ae_forall_tendsto_block_term` + `cfc_stepVal_qpow_eq`). Hence `qpow A T n x`
converges; `Λ` is read off pointwise by `Classical.choice`. -/
theorem tendsto_qpow [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    oseledetsLimitExists μ T A := by
  classical
  obtain ⟨lam, hanti, hσ⟩ :=
    exists_lam_tendsto_singularValue hT hA hAmeas hint hint'
  -- a.e. per-term band-projector convergence
  have hblock := ae_forall_tendsto_block_term hT hA hAmeas hint hint' lam hanti hσ
  -- a.e. eigenvalue convergence μⱼ,ₙ → e^{λⱼ} for every sorted index j
  have hev : ∀ᵐ x ∂μ, ∀ i : Fin (Fintype.card (Fin d)),
      Tendsto (fun n : ℕ => (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ i)
        atTop (𝓝 (Real.exp (lam (i : ℕ)))) := by
    refine ae_all_iff.mpr (fun i => ?_)
    have hid : (i : ℕ) < d := lt_of_lt_of_eq i.isLt (Fintype.card_fin d)
    filter_upwards [hσ (i : ℕ) hid] with x hx
    exact eigenvalues_qpow_tendsto hA i (by simpa using hx)
  -- the good set: combine
  refine ⟨fun x => if h : ∃ L, Tendsto (fun n => qpow A T n x) atTop (𝓝 L) then h.choose else 0, ?_⟩
  filter_upwards [hblock, hev] with x hxblock hxev
  -- it suffices to show ∃ L, Tendsto (qpow · x) → L; then the dif picks it
  suffices hex : ∃ L, Tendsto (fun n => qpow A T n x) atTop (𝓝 L) by
    rw [dif_pos hex]; exact hex.choose_spec
  -- block approximant converges (finite sum of convergent terms + constant)
  obtain ⟨Lblock, hLblock⟩ :
      ∃ Lblock, Tendsto (fun n => Real.exp (lam (d - 1)) • (1 : Matrix (Fin d) (Fin d) ℝ)
          + ∑ k ∈ Finset.Ico 1 d, (Real.exp (lam (k - 1)) - Real.exp (lam k)) •
              bandProjector A T
                (Set.indicator (Set.Ioi (Real.exp ((lam k + lam (k - 1)) / 2))) 1) n x)
        atTop (𝓝 Lblock) := by
    refine ⟨Real.exp (lam (d - 1)) • (1 : Matrix (Fin d) (Fin d) ℝ)
        + ∑ k ∈ (Finset.Ico 1 d).attach, (hxblock k.1 k.2).choose, ?_⟩
    refine tendsto_const_nhds.add ?_
    rw [show (fun n => ∑ k ∈ Finset.Ico 1 d, (Real.exp (lam (k - 1)) - Real.exp (lam k)) •
          bandProjector A T
            (Set.indicator (Set.Ioi (Real.exp ((lam k + lam (k - 1)) / 2))) 1) n x)
        = (fun n => ∑ k ∈ (Finset.Ico 1 d).attach,
            (Real.exp (lam (k.1 - 1)) - Real.exp (lam k.1)) •
              bandProjector A T
                (Set.indicator (Set.Ioi (Real.exp ((lam k.1 + lam (k.1 - 1)) / 2))) 1) n x)
        from by funext n; rw [← Finset.sum_attach]]
    refine tendsto_finset_sum _ (fun k _ => ?_)
    exact (hxblock k.1 k.2).choose_spec
  -- the block approximant equals cfc (stepVal lam d) (qpow)
  have hLn_eq : ∀ n, Real.exp (lam (d - 1)) • (1 : Matrix (Fin d) (Fin d) ℝ)
          + ∑ k ∈ Finset.Ico 1 d, (Real.exp (lam (k - 1)) - Real.exp (lam k)) •
              bandProjector A T
                (Set.indicator (Set.Ioi (Real.exp ((lam k + lam (k - 1)) / 2))) 1) n x
        = cfc (stepVal lam d) (qpow A T n x) := by
    intro n; rw [cfc_stepVal_qpow_eq A T lam d n x]
  -- per-sorted-index deviation μⱼ,ₙ - stepVal(μⱼ,ₙ) → 0
  have hdevj : ∀ j : Fin (Fintype.card (Fin d)),
      Tendsto (fun n => (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ j
          - stepVal lam d ((qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ j))
        atTop (𝓝 0) := by
    intro j
    have hjd : (j : ℕ) < d := lt_of_lt_of_eq j.isLt (Fintype.card_fin d)
    -- eventually stepVal(μⱼ,ₙ) = e^{λⱼ}, so the deviation is eventually μⱼ,ₙ - e^{λⱼ} → 0
    have hμ := hxev j
    -- eventually each block term at μⱼ,ₙ equals the same term at e^{λⱼ}
    have hterm : ∀ k ∈ Finset.Ico 1 d, ∀ᶠ n in atTop,
        (Real.exp (lam (k - 1)) - Real.exp (lam k)) *
            Set.indicator (Set.Ioi (Real.exp ((lam k + lam (k - 1)) / 2))) (1 : ℝ → ℝ)
              ((qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ j)
          = (Real.exp (lam (k - 1)) - Real.exp (lam k)) *
            Set.indicator (Set.Ioi (Real.exp ((lam k + lam (k - 1)) / 2))) (1 : ℝ → ℝ)
              (Real.exp (lam (j : ℕ))) := by
      intro k hk
      rw [Finset.mem_Ico] at hk
      obtain ⟨hk1, hkd⟩ := hk
      by_cases hgap : lam k < lam (k - 1)
      · -- gap: the eigenvalue is eventually on the same side of the threshold cₖ as e^{λⱼ}
        set ck := Real.exp ((lam k + lam (k - 1)) / 2) with hck
        by_cases hside : Real.exp (lam (j : ℕ)) < ck
        · -- e^{λⱼ} < cₖ, so eventually μⱼ,ₙ < cₖ; both indicators 0
          filter_upwards [hμ.eventually (eventually_lt_nhds hside)] with n hn
          rw [Set.indicator_of_notMem (by rw [Set.mem_Ioi, not_lt]; exact le_of_lt hn),
            Set.indicator_of_notMem (by rw [Set.mem_Ioi, not_lt]; exact le_of_lt hside)]
        · -- otherwise ck < e^{λⱼ} (equality is impossible at a gap), so eventually μⱼ,ₙ > cₖ
          have hgt : ck < Real.exp (lam (j : ℕ)) := by
            rcases lt_trichotomy (Real.exp (lam (j : ℕ))) ck with h | h | h
            · exact absurd h hside
            · -- equality impossible: lam j ≠ (lam k + lam(k-1))/2
              exfalso
              have hlamj : lam (j : ℕ) = (lam k + lam (k - 1)) / 2 := by
                have := congrArg Real.log h
                rwa [Real.log_exp, Real.log_exp] at this
              rcases Nat.lt_or_ge (j : ℕ) k with hjk | hjk
              · have : lam (k - 1) ≤ lam (j : ℕ) := hanti (j : ℕ) (k - 1) (by omega) (by omega)
                rw [hlamj] at this; linarith
              · have : lam (j : ℕ) ≤ lam k := hanti k (j : ℕ) hjk hjd
                rw [hlamj] at this; linarith
            · exact h
          filter_upwards [hμ.eventually (eventually_gt_nhds hgt)] with n hn
          rw [Set.indicator_of_mem (by rw [Set.mem_Ioi]; exact hn),
            Set.indicator_of_mem (by rw [Set.mem_Ioi]; exact hgt), Pi.one_apply, Pi.one_apply]
      · -- non-gap: coefficient is 0
        have hle : lam k ≤ lam (k - 1) := hanti (k - 1) k (by omega) hkd
        have hcoef : Real.exp (lam (k - 1)) - Real.exp (lam k) = 0 := by
          have heqlam : lam (k - 1) = lam k := le_antisymm (not_lt.mp hgap) hle
          rw [heqlam]; ring
        filter_upwards with n
        rw [hcoef]; ring
    -- assemble: stepVal at μⱼ,ₙ equals stepVal at e^{λⱼ} = e^{λⱼ}
    have heq : ∀ᶠ n in atTop,
        (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ j
            - stepVal lam d ((qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ j)
          = (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ j - Real.exp (lam (j : ℕ)) := by
      rw [← eventually_all_finset] at hterm
      filter_upwards [hterm] with n hn
      have hstepeq : stepVal lam d ((qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ j)
          = stepVal lam d (Real.exp (lam (j : ℕ))) := by
        rw [stepVal, stepVal]
        congr 1
        exact Finset.sum_congr rfl hn
      rw [hstepeq, stepVal_exp_lam lam d hanti hjd]
    -- the target tendsto, via congruence with μⱼ,ₙ - e^{λⱼ} → 0
    have htgt : Tendsto (fun n => (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ j
        - Real.exp (lam (j : ℕ))) atTop (𝓝 0) := by
      have := hμ.sub_const (Real.exp (lam (j : ℕ)))
      simpa using this
    exact htgt.congr' (heq.mono (fun n hn => hn.symm))
  -- deviation qpow_n - blockApprox_n → 0
  have hdev : Tendsto
      (fun n => qpow A T n x - cfc (stepVal lam d) (qpow A T n x)) atTop (𝓝 0) := by
    rw [tendsto_zero_iff_norm_tendsto_zero]
    -- squeeze: 0 ≤ ‖·‖ ≤ ∑ⱼ |devⱼ| → 0
    have hsum0 : Tendsto (fun n => ∑ j : Fin (Fintype.card (Fin d)),
        |(qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ j
          - stepVal lam d ((qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ j)|)
        atTop (𝓝 0) := by
      have hcomp : Tendsto (fun n => ∑ j : Fin (Fintype.card (Fin d)),
          |(qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ j
            - stepVal lam d ((qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ j)|)
          atTop (𝓝 (∑ _j : Fin (Fintype.card (Fin d)), (0 : ℝ))) := by
        refine tendsto_finset_sum _ (fun j _ => ?_)
        have := (hdevj j).abs
        simpa using this
      simpa using hcomp
    refine squeeze_zero (fun n => norm_nonneg _) (fun n => ?_) hsum0
    exact norm_sub_cfc_le_sum_eigenvalue_dev (qpow A T n x) (qpow_isSelfAdjoint A T n x)
      (stepVal lam d)
  -- combine: qpow_n = (qpow_n - blockApprox_n) + blockApprox_n → 0 + Lblock
  refine ⟨Lblock, ?_⟩
  have hcombine : Tendsto (fun n => (qpow A T n x - cfc (stepVal lam d) (qpow A T n x))
      + cfc (stepVal lam d) (qpow A T n x)) atTop (𝓝 (0 + Lblock)) := by
    refine hdev.add ?_
    simp_rw [← hLn_eq]; exact hLblock
  simpa using hcombine

/-! ## A named, measurable Oseledets limit `Λ`

The existence statement `oseledetsLimitExists` (`tendsto_qpow`) only asserts an a.e.-existing limit
via `Classical.choice`. Here we pin a **concrete, measurable** representative `oseledetsLimit A T`,
defined entrywise as the real `limUnder` of the (measurable) matrix entries of `qpow A T n x`. On
the a.e.-full convergence set this entrywise limit equals the matrix limit, so `oseledetsLimit`
discharges `oseledetsLimitExists` while being genuinely (not merely a.e.) measurable. -/

variable [NeZero d]

set_option linter.unusedSectionVars false in
/-- The Gram matrix `x ↦ gram A T n x = (A⁽ⁿ⁾)ᵀ A⁽ⁿ⁾` is measurable. -/
theorem measurable_gram {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hAmeas : Measurable A) (hTmeas : Measurable T) (n : ℕ) :
    Measurable (fun x => gram A T n x) := by
  have hcoc : Measurable fun x => cocycle A T n x := measurable_cocycle hAmeas hTmeas n
  have htrans : Measurable fun x => (cocycle A T n x)ᵀ := by
    refine measurable_pi_iff.2 fun i => measurable_pi_iff.2 fun j => ?_
    simp only [Matrix.transpose_apply]
    exact ((measurable_pi_apply i).comp ((measurable_pi_apply j).comp hcoc))
  exact htrans.mul hcoc

set_option linter.unusedSectionVars false in
/-- The matrix root `x ↦ qpow A T n x = (Qₙ)^{1/(2n)} = cfc (·^{1/(2n)}) (gram A T n x)` is
measurable. The function `t ↦ t^{1/(2n)}` is continuous (nonnegative exponent), the Gram matrix is
measurable (`measurable_gram`) and self-adjoint (`gram_isSelfAdjoint`), so the continuous-functional
-calculus measurability crux `measurable_cfc_continuous` applies. -/
theorem measurable_qpow {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hAmeas : Measurable A) (hTmeas : Measurable T) (n : ℕ) :
    Measurable (fun x => qpow A T n x) := by
  have hcont : Continuous (fun t : ℝ => t ^ ((2 * (n : ℝ))⁻¹)) :=
    Real.continuous_rpow_const (by positivity)
  exact measurable_cfc_continuous _ hcont (fun x => gram A T n x)
    (measurable_gram hAmeas hTmeas n) (fun x => gram_isSelfAdjoint A T n x)

/-- **The named Oseledets limit.** Defined entrywise as the real `limUnder` of the matrix
entries of `qpow A T n x`. On the a.e.-full convergence set (`tendsto_qpow`) this equals the matrix
limit; off it the value is irrelevant (the construction is total and measurable regardless). -/
noncomputable def oseledetsLimit (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X) :
    Matrix (Fin d) (Fin d) ℝ :=
  Matrix.of fun i j => limUnder atTop (fun n : ℕ => qpow A T n x i j)

set_option linter.unusedSectionVars false in
/-- The named Oseledets limit `oseledetsLimit A T` is measurable: each entry is a real
`limUnder` of measurable functions (`measurable_qpow`), and a `limUnder` over `atTop` valued in the
completely metrizable space `ℝ` of measurable functions is measurable
(`StronglyMeasurable.limUnder`). -/
theorem measurable_oseledetsLimit {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hAmeas : Measurable A) (hTmeas : Measurable T) :
    Measurable (oseledetsLimit A T) := by
  refine measurable_pi_iff.2 fun i => measurable_pi_iff.2 fun j => ?_
  have hentry : ∀ n : ℕ, Measurable (fun x => qpow A T n x i j) := fun n =>
    (measurable_pi_apply j).comp ((measurable_pi_apply i).comp (measurable_qpow hAmeas hTmeas n))
  exact (StronglyMeasurable.limUnder
    (fun n => (hentry n).stronglyMeasurable)).measurable

set_option linter.unusedSectionVars false in
/-- **`oseledetsLimit` is the a.e. limit of `qpow`.** For `μ`-a.e. `x`,
`qpow A T n x → oseledetsLimit A T x` in the matrix metric. (On the a.e.-full convergence set the
entrywise `limUnder` recovers the matrix limit; matrix convergence reduces to entrywise
convergence in finite dimensions.) -/
theorem tendsto_oseledetsLimit [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∀ᵐ x ∂μ, Tendsto (fun n : ℕ => qpow A T n x) atTop (𝓝 (oseledetsLimit A T x)) := by
  obtain ⟨Λ, hΛ⟩ := tendsto_qpow hT hA hAmeas hint hint'
  filter_upwards [hΛ] with x hx
  -- On the good set, the entrywise limUnder equals the matrix limit, so the limit point is
  -- `oseledetsLimit A T x`.
  have hentry : oseledetsLimit A T x = Λ x := by
    refine Matrix.ext fun i j => ?_
    have hcoord : Tendsto (fun n : ℕ => qpow A T n x i j) atTop (𝓝 (Λ x i j)) :=
      ((continuous_matrix_entry i j).tendsto _).comp hx
    simp only [oseledetsLimit, Matrix.of_apply]
    exact hcoord.limUnder_eq
  rw [hentry]; exact hx

/-! ## Eigen-data of the Oseledets limit `Λ`

The named limit `oseledetsLimit A T x` inherits the self-adjointness and positive
semidefiniteness of the approximants `qpow A T n x` (both closed under the matrix limit, proved
entrywise / via the continuity of the quadratic form). The eigenvalue equality
`eigenvalues₀ (Λ x) i = e^{λᵢ}` additionally requires continuity of the sorted eigenvalues in the
Hermitian matrix. This was historically flagged as a blocker (no such lemma in Mathlib), but it is
now supplied in-repo by the Weyl-perturbation lemma `ErgodicTheory.Weyl.tendsto_eigenvalues₀`
(`ErgodicTheory/Lyapunov/ExteriorNorm/Weyl.lean`), so the equality `oseledetsLimit_eigenvalues₀_eq`
below is fully proved. -/

set_option linter.unusedSectionVars false in
/-- For `μ`-a.e. `x`, the Oseledets limit `oseledetsLimit A T x` is self-adjoint, as the
matrix-metric limit of the self-adjoint approximants `qpow A T n x` (self-adjointness `Mᴴ = M` is
an entrywise closed condition). -/
theorem oseledetsLimit_isSelfAdjoint [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∀ᵐ x ∂μ, IsSelfAdjoint (oseledetsLimit A T x) := by
  filter_upwards [tendsto_oseledetsLimit hT hA hAmeas hint hint'] with x hx
  -- `(·)ᴴ = (·)` is closed: entrywise `star ((Λ x) j i) = (Λ x) i j` as a limit of the same
  -- equation for `qpow A T n x`.
  rw [← Matrix.isHermitian_iff_isSelfAdjoint]
  refine Matrix.IsHermitian.ext fun i j => ?_
  have hcij : Tendsto (fun n : ℕ => qpow A T n x i j) atTop (𝓝 (oseledetsLimit A T x i j)) :=
    ((continuous_matrix_entry i j).tendsto _).comp hx
  have hcji : Tendsto (fun n : ℕ => qpow A T n x j i) atTop (𝓝 (oseledetsLimit A T x j i)) :=
    ((continuous_matrix_entry j i).tendsto _).comp hx
  -- `star = id` on ℝ; the approximants satisfy `qpow j i = qpow i j` (Hermitian).
  have heq : ∀ n : ℕ, qpow A T n x i j = qpow A T n x j i := fun n => by
    have hH := qpow_isSelfAdjoint A T n x
    rw [← Matrix.isHermitian_iff_isSelfAdjoint] at hH
    simpa using (hH.apply i j).symm
  have hval : oseledetsLimit A T x j i = oseledetsLimit A T x i j :=
    tendsto_nhds_unique hcji (hcij.congr heq)
  simpa using hval

set_option linter.unusedSectionVars false in
/-- For `μ`-a.e. `x`, the Oseledets limit `oseledetsLimit A T x` is positive semidefinite,
as the matrix-metric limit of the PSD approximants `qpow A T n x`: it is self-adjoint, and the
quadratic form `xᵀ Λ x = lim_n xᵀ (qpow A T n x) x ≥ 0` is a limit of nonnegatives (the quadratic
form is continuous in the matrix). -/
theorem oseledetsLimit_posSemidef [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∀ᵐ x ∂μ, (oseledetsLimit A T x).PosSemidef := by
  filter_upwards [tendsto_oseledetsLimit hT hA hAmeas hint hint',
    oseledetsLimit_isSelfAdjoint hT hA hAmeas hint hint'] with x hx hsa
  refine Matrix.PosSemidef.of_dotProduct_mulVec_nonneg
    ((Matrix.isHermitian_iff_isSelfAdjoint).mpr hsa) fun v => ?_
  -- `v ⬝ᵥ (Λ x *ᵥ v) = lim_n v ⬝ᵥ (qpow A T n x *ᵥ v) ≥ 0`.
  have hquad_cont : Continuous fun M : Matrix (Fin d) (Fin d) ℝ => star v ⬝ᵥ (M *ᵥ v) := by
    let L : Matrix (Fin d) (Fin d) ℝ →ₗ[ℝ] ℝ :=
      { toFun := fun M => star v ⬝ᵥ (M *ᵥ v)
        map_add' := fun M N => by simp [Matrix.add_mulVec, dotProduct_add]
        map_smul' := fun c M => by
          simp only [RingHom.id_apply, smul_eq_mul]
          rw [Matrix.smul_mulVec, dotProduct_smul, smul_eq_mul] }
    exact L.continuous_of_finiteDimensional
  have htq : Tendsto (fun n : ℕ => star v ⬝ᵥ (qpow A T n x *ᵥ v)) atTop
      (𝓝 (star v ⬝ᵥ (oseledetsLimit A T x *ᵥ v))) := (hquad_cont.tendsto _).comp hx
  refine ge_of_tendsto' htq fun n => ?_
  exact (qpow_posSemidef A T n x).dotProduct_mulVec_nonneg v

set_option linter.unusedSectionVars false in
/-- **The eigenvalues of `qpow` converge to `e^{lamSing}`.** For `μ`-a.e. `x` and every sorted
index `i`, the `i`-th sorted eigenvalue of the approximant `qpow A T n x` converges to
`e^{lamSing A T x i}`. This is the eigenvalue statement at the level of the *approximants*; the full
eigenvalue equality for `Λ` itself (`oseledetsLimit_eigenvalues₀_eq`, below) additionally needs
continuity of the sorted eigenvalues in the Hermitian matrix. That was historically a blocker (no
such Mathlib lemma), but it is now supplied in-repo by `ErgodicTheory.Weyl.tendsto_eigenvalues₀`,
so the
equality below is proved. -/
theorem eigenvalues₀_qpow_tendsto_exp_lamSing [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∀ᵐ x ∂μ, ∀ i : Fin (Fintype.card (Fin d)),
      Tendsto (fun n : ℕ => (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ i)
        atTop (𝓝 (Real.exp (lamSing A T x (i : ℕ)))) := by
  obtain ⟨lam, _hanti, hσ⟩ :=
    exists_lam_tendsto_singularValue hT hA hAmeas hint hint'
  refine ae_all_iff.mpr (fun i => ?_)
  have hid : (i : ℕ) < d := lt_of_lt_of_eq i.isLt (Fintype.card_fin d)
  filter_upwards [hσ (i : ℕ) hid] with x hx
  have hlam : lamSing A T x (i : ℕ) = lam (i : ℕ) := lamSing_eq_of_tendsto hx
  rw [hlam]
  exact eigenvalues_qpow_tendsto hA i (by simpa using hx)

set_option linter.unusedSectionVars false in
/-- **The eigenvalue equality `eigenvalues₀ (Λ x) i = e^{lamSing A T x i}`.** For `μ`-a.e. `x`
and every sorted index `i`, the `i`-th sorted eigenvalue of the Oseledets limit `Λ x` is exactly
`e^{lamSing A T x i}`.

This is the headline spectral statement of the Oseledets limit. The proof passes the
approximant-level eigenvalue convergence `eigenvalues₀ (qpow A T n x) i → e^{lamSing i}`
(`eigenvalues₀_qpow_tendsto_exp_lamSing`) through the matrix limit `qpow A T n x → Λ x`
(`tendsto_oseledetsLimit`) using **continuity of the sorted eigenvalues `eigenvalues₀`**
(`Weyl.tendsto_eigenvalues₀`, the new Weyl perturbation infrastructure in `ExteriorNorm.lean`):
`eigenvalues₀ (qpow A T n x) i → eigenvalues₀ (Λ x) i`, and uniqueness of limits forces the two
limits to agree. -/
theorem oseledetsLimit_eigenvalues₀_eq [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∀ᵐ x ∂μ, ∀ (hH : (oseledetsLimit A T x).IsHermitian) (i : Fin (Fintype.card (Fin d))),
      hH.eigenvalues₀ i = Real.exp (lamSing A T x (i : ℕ)) := by
  filter_upwards [tendsto_oseledetsLimit hT hA hAmeas hint hint',
    eigenvalues₀_qpow_tendsto_exp_lamSing hT hA hAmeas hint hint'] with x hx hexp
  intro hH i
  -- the i-th sorted eigenvalue of `qpow A T n x` converges to two things:
  -- (1) to `eigenvalues₀ (Λ x) i` by continuity (Weyl perturbation), and
  -- (2) to `e^{lamSing i}` by `eigenvalues₀_qpow_tendsto_exp_lamSing`. Uniqueness forces equality.
  have hcont : Tendsto (fun n : ℕ => (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ i)
      atTop (𝓝 (hH.eigenvalues₀ i)) :=
    Weyl.tendsto_eigenvalues₀ (fun n => (qpow_isSelfAdjoint A T n x).isHermitian) hH hx i
  exact tendsto_nhds_unique hcont (hexp i)

/-! ## The two-sided growth limit `(1/n)·log‖A⁽ⁿ⁾(x) v‖`

For a single nonzero vector `v`, the normalized log-growth of the cocycle image `A⁽ⁿ⁾(x) v`
**converges** (not merely `limsup`/`liminf`) to the largest Lyapunov exponent active on `v`. The
quadratic-form foundation `‖A⁽ⁿ⁾ v‖² = ⟪gram_n v, v⟫` ties the growth to the Gram spectrum
(`= qpow_n^{2n}`). We bank here:

* the foundational identity `norm_sq_cocycle_apply_eq_inner_gram`;
* the per-vector operator-norm sandwich
  `‖A⁽ⁿ⁾⁻¹‖⁻¹ ‖v‖ ≤ ‖A⁽ⁿ⁾ v‖ ≤ ‖A⁽ⁿ⁾‖ ‖v‖`;
* the **genuine two-sided limit** in the equal-exponents (conformal/isotropic) regime
  (`tendsto_log_cocycle_apply_of_eq_exponents`, and its a.e. ergodic packaging
  `ae_tendsto_log_cocycle_apply_of_eq_exponents`): when the top Furstenberg–Kesten exponent
  `ℓ_top = lim (1/n)log‖A⁽ⁿ⁾‖` and the bottom exponent `ℓ_bot = lim (1/n)log‖(A⁽ⁿ⁾)⁻¹‖` satisfy
  `ℓ_bot = -ℓ_top` (all Lyapunov exponents coincide), then **every** nonzero `v` grows at the
  common rate `ℓ_top`.

The fully general per-vector limit (with the top *active* Oseledets exponent depending on `v`'s
Λ-eigencomponents) needs the band-projector convergence `tendsto_bandProjector_of_gap` to control
the eigencomponent of `v` at the dominant exponent; that assembly is flagged in the module summary
and left for a follow-up. -/

set_option linter.unusedSectionVars false in
/-- **Foundation.** The squared norm of the cocycle image is the Gram quadratic form:
`‖A⁽ⁿ⁾(x) v‖² = ⟪gram_n v, v⟫`. (`‖f v‖² = ⟪f v, f v⟫ = ⟪(adjoint f ∘ f) v, v⟫`, and
`adjoint(toEuclideanLin M) ∘ toEuclideanLin M = toEuclideanLin (Mᵀ M) = toEuclideanLin (gram)`.) -/
theorem norm_sq_cocycle_apply_eq_inner_gram (A : X → Matrix (Fin d) (Fin d) ℝ)
    (n : ℕ) (x : X) (v : EuclideanSpace ℝ (Fin d)) :
    ‖Matrix.toEuclideanLin (cocycle A T n x) v‖ ^ 2
      = ⟪Matrix.toEuclideanLin (gram A T n x) v, v⟫ := by
  set M := cocycle A T n x with hM
  rw [← real_inner_self_eq_norm_sq]
  have hadj : ⟪Matrix.toEuclideanLin M v, Matrix.toEuclideanLin M v⟫_ℝ
      = ⟪((Matrix.toEuclideanLin M).adjoint ∘ₗ (Matrix.toEuclideanLin M)) v, v⟫_ℝ := by
    rw [LinearMap.comp_apply, LinearMap.adjoint_inner_left]
  rw [hadj, adjoint_comp_self_eq_gram]
  rw [gram]

set_option linter.unusedSectionVars false in
/-- **Upper bound.** `‖A⁽ⁿ⁾(x) v‖ ≤ ‖A⁽ⁿ⁾(x)‖ ‖v‖` — the per-vector L² operator-norm bound. -/
theorem norm_cocycle_apply_le (A : X → Matrix (Fin d) (Fin d) ℝ)
    (n : ℕ) (x : X) (v : EuclideanSpace ℝ (Fin d)) :
    ‖Matrix.toEuclideanLin (cocycle A T n x) v‖ ≤ ‖cocycle A T n x‖ * ‖v‖ :=
  ExteriorNorm.norm_toEuclideanLin_apply_le (cocycle A T n x) v

set_option linter.unusedSectionVars false in
/-- **Lower bound.** `‖v‖ ≤ ‖A⁽ⁿ⁾(x)⁻¹‖ · ‖A⁽ⁿ⁾(x) v‖` for an invertible cocycle, i.e.
`‖A⁽ⁿ⁾⁻¹‖⁻¹ ‖v‖ ≤ ‖A⁽ⁿ⁾ v‖`. (`v = A⁽ⁿ⁾⁻¹ (A⁽ⁿ⁾ v)`, then the op-norm bound.) -/
theorem norm_le_norm_inv_mul_norm_cocycle_apply {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) (n : ℕ) (x : X) (v : EuclideanSpace ℝ (Fin d)) :
    ‖v‖ ≤ ‖(cocycle A T n x)⁻¹‖ * ‖Matrix.toEuclideanLin (cocycle A T n x) v‖ := by
  have hdet : (cocycle A T n x).det ≠ 0 := det_cocycle_ne_zero hA n x
  have hinv : (cocycle A T n x)⁻¹ * cocycle A T n x = 1 :=
    Matrix.nonsing_inv_mul _ (Ne.isUnit hdet)
  have hround : Matrix.toEuclideanLin ((cocycle A T n x)⁻¹)
      (Matrix.toEuclideanLin (cocycle A T n x) v) = v := by
    rw [← LinearMap.comp_apply]
    have hcomp : Matrix.toEuclideanLin ((cocycle A T n x)⁻¹)
          ∘ₗ Matrix.toEuclideanLin (cocycle A T n x)
        = Matrix.toEuclideanLin ((cocycle A T n x)⁻¹ * cocycle A T n x) := by
      ext w i
      simp only [LinearMap.comp_apply, Matrix.toLpLin_apply, Matrix.mulVec_mulVec]
    rw [hcomp, hinv]
    ext i; simp
  calc ‖v‖ = ‖Matrix.toEuclideanLin ((cocycle A T n x)⁻¹)
              (Matrix.toEuclideanLin (cocycle A T n x) v)‖ := by rw [hround]
    _ ≤ ‖(cocycle A T n x)⁻¹‖ * ‖Matrix.toEuclideanLin (cocycle A T n x) v‖ :=
        ExteriorNorm.norm_toEuclideanLin_apply_le _ _

set_option linter.unusedSectionVars false in
/-- **Nonvanishing.** `A⁽ⁿ⁾(x) v ≠ 0` for `v ≠ 0` (invertibility ⟹ injectivity). -/
theorem cocycle_apply_ne_zero {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) (n : ℕ) (x : X) {v : EuclideanSpace ℝ (Fin d)} (hv : v ≠ 0) :
    Matrix.toEuclideanLin (cocycle A T n x) v ≠ 0 := by
  intro h
  exact hv (injective_toEuclideanLin (det_cocycle_ne_zero hA n x) (by rw [h, map_zero]))

set_option linter.unusedSectionVars false in
/-- **Equal-exponents two-sided limit.** If the top and (negated) bottom Furstenberg–Kesten
exponents coincide at `x` — i.e. `(1/n)log‖A⁽ⁿ⁾‖ → ℓ` and `(1/n)log‖(A⁽ⁿ⁾)⁻¹‖ → -ℓ` — then for
**every** nonzero `v` the normalized log-growth of `A⁽ⁿ⁾ v` converges to `ℓ`. This is the genuine
two-sided growth limit (not merely `limsup`) in the isotropic/conformal regime where all Lyapunov
exponents agree: the operator-norm sandwich `‖A⁽ⁿ⁾⁻¹‖⁻¹ ‖v‖ ≤ ‖A⁽ⁿ⁾ v‖ ≤ ‖A⁽ⁿ⁾‖ ‖v‖` squeezes the
normalized log between two sequences both tending to `ℓ` (the `(1/n)log‖v‖` correction vanishes). -/
theorem tendsto_log_cocycle_apply_of_eq_exponents {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) {x : X} {ℓ : ℝ}
    (htop : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖cocycle A T n x‖) atTop (𝓝 ℓ))
    (hbot : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖(cocycle A T n x)⁻¹‖) atTop (𝓝 (-ℓ)))
    {v : EuclideanSpace ℝ (Fin d)} (hv : v ≠ 0) :
    Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) atTop (𝓝 ℓ) := by
  have hvpos : 0 < ‖v‖ := norm_pos_iff.mpr hv
  have hcorr : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖v‖) atTop (𝓝 0) := by
    have := (tendsto_natCast_atTop_atTop (R := ℝ)).inv_tendsto_atTop.mul_const (Real.log ‖v‖)
    simpa using this
  have hcocpos : ∀ n, 0 < ‖cocycle A T n x‖ := fun n => norm_cocycle_pos hA n x
  have hinvpos : ∀ n, 0 < ‖(cocycle A T n x)⁻¹‖ := fun n => norm_inv_cocycle_pos hA n x
  have happly_pos : ∀ n, 0 < ‖Matrix.toEuclideanLin (cocycle A T n x) v‖ := fun n =>
    norm_pos_iff.mpr (cocycle_apply_ne_zero (T := T) hA n x hv)
  have hupperlim : Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖cocycle A T n x‖ + (n : ℝ)⁻¹ * Real.log ‖v‖)
      atTop (𝓝 ℓ) := by simpa using htop.add hcorr
  have hlowerlim : Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖v‖ - (n : ℝ)⁻¹ * Real.log ‖(cocycle A T n x)⁻¹‖)
      atTop (𝓝 ℓ) := by simpa using hcorr.sub hbot
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le' hlowerlim hupperlim ?_ ?_
  · filter_upwards [eventually_ge_atTop 1] with n _
    have hninv : (0:ℝ) ≤ (n:ℝ)⁻¹ := by positivity
    have hle := norm_le_norm_inv_mul_norm_cocycle_apply (T := T) hA n x v
    have hlog : Real.log ‖v‖
        ≤ Real.log ‖(cocycle A T n x)⁻¹‖
            + Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖ := by
      rw [← Real.log_mul (ne_of_gt (hinvpos n)) (ne_of_gt (happly_pos n))]
      exact Real.log_le_log hvpos hle
    nlinarith [mul_le_mul_of_nonneg_left hlog hninv]
  · filter_upwards [eventually_ge_atTop 1] with n _
    have hninv : (0:ℝ) ≤ (n:ℝ)⁻¹ := by positivity
    have hle := norm_cocycle_apply_le (T := T) A n x v
    have hlog : Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖
        ≤ Real.log ‖cocycle A T n x‖ + Real.log ‖v‖ := by
      rw [← Real.log_mul (ne_of_gt (hcocpos n)) (ne_of_gt hvpos)]
      exact Real.log_le_log (happly_pos n) hle
    nlinarith [mul_le_mul_of_nonneg_left hlog hninv]

set_option linter.unusedSectionVars false in
/-- **A.e. equal-exponents two-sided limit.** For an ergodic, integrable, invertible cocycle
whose top Furstenberg–Kesten exponent `ℓ_top` and bottom exponent `ℓ_bot` satisfy `ℓ_bot = -ℓ_top`
(all Lyapunov exponents equal — the conformal/isotropic regime), there is a single exponent `ℓ` such
that for `μ`-a.e. `x` and **every** nonzero `v`, `(1/n)log‖A⁽ⁿ⁾(x) v‖ → ℓ`. The two FK exponents are
produced internally by `furstenbergKesten_norm`/`_bot`; the hypothesis `heq` ties them together. -/
theorem ae_tendsto_log_cocycle_apply_of_eq_exponents [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (heq : ∀ (ℓtop ℓbot : ℝ),
      (∀ᵐ x ∂μ, Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖cocycle A T n x‖) atTop (𝓝 ℓtop)) →
      (∀ᵐ x ∂μ, Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖(cocycle A T n x)⁻¹‖) atTop (𝓝 ℓbot)) →
      ℓbot = -ℓtop) :
    ∃ ℓ : ℝ, ∀ᵐ x ∂μ, ∀ v : EuclideanSpace ℝ (Fin d), v ≠ 0 →
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
          Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) atTop (𝓝 ℓ) := by
  obtain ⟨ℓtop, htopval⟩ := furstenbergKesten_norm hT hA hAmeas hint hint'
  obtain ⟨ℓbot, hbotval⟩ := furstenbergKesten_norm_inv hT hA hAmeas hint hint'
  have hℓ : ℓbot = -ℓtop := heq ℓtop ℓbot htopval hbotval
  refine ⟨ℓtop, ?_⟩
  filter_upwards [htopval, hbotval] with x htop hbot
  intro v hv
  refine tendsto_log_cocycle_apply_of_eq_exponents hA htop ?_ hv
  rwa [← hℓ]

end ErgodicTheory

end
