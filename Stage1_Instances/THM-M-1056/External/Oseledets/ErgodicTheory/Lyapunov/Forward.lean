/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.OseledetsLimit.Limit
import ErgodicTheory.Lyapunov.Filtration
import ErgodicTheory.Lyapunov.Measurable

/-!
# Forward exact growth and the measurable Oseledets filtration

This module connects the analytic core of the one-sided Oseledets multiplicative ergodic
theorem (the Oseledets limit `Λ = lim ((A⁽ⁿ⁾)ᵀA⁽ⁿ⁾)^{1/2n}` of `OseledetsLimit.lean`, its
band-projector convergence, and the limsup flag of `Filtration.lean`) to the target theorem
`oseledets_filtration`.

The mathematical content of this module is the **per-vector exact growth limit**
`(1/n) log‖A⁽ⁿ⁾(x) v‖ → λᵢ` for `v` in the stratum `Vᵢ \ Vᵢ₊₁`:

* **Lower bound** `liminf ≥ λᵢ`: the Gram quadratic-form band bound
  `⟪gramₙ v, v⟫ ≥ c^{2n} ‖Pᶜₙ v‖²` (`inner_cfc_ge_band`), the band-projector convergence
  `Pᶜₙ v → Pᶜ_∞ v ≠ 0`, and taking the threshold `c ↑ e^{λᵢ}`.
* **Upper bound** `limsup ≤ λᵢ`: a spectral decomposition over the sorted Gram eigenbasis,
  with each overlap term controlled by the tilt of the band projector at its
  straddling-gap rate, paired against the block's singular-value growth.

Together they upgrade the limsup flag's `lambdaBar = λᵢ` (`lambdaBar_eq_on_stratum`) to a
genuine limit, identify the Λ-spectral filtration with `lambdaSublevel` a.e. (so it inherits
strict antitonicity and `A`-equivariance), and — with the deterministic exponents from
`exists_lam_tendsto_singularValue` and the CFC measurability of `Measurable.lean` — yield
the target theorem.

## Main results

* `inner_cfc_ge_band`: the Gram quadratic-form band bound for a self-adjoint matrix.
* `log_le_liminf_log_cocycle_apply`: the per-vector liminf lower bound
  `log c ≤ liminf (1/n) log‖A⁽ⁿ⁾ v‖` from band-projector convergence.
* `limitBandProjector_apply_eq_zero_of_le`: kernel propagation between limit band
  projectors of nested thresholds.
* `limsup_inv_mul_log_norm_cocycle_apply_le`: the per-vector growth upper bound,
  conditional on per-index leakage envelopes.
* `tendsto_inv_mul_log_norm_cocycle_apply`: the assembled per-vector exact growth limit,
  squeezing the upper and lower per-vector bounds.
-/

open MeasureTheory Filter Topology
open scoped Matrix Matrix.Norms.L2Operator

namespace ErgodicTheory

variable {d : ℕ}

/-! ## Distinct descending exponent enumeration

The deterministic singular-value exponents `lam : ℕ → ℝ` (from
`exists_lam_tendsto_singularValue`) are antitone on `[0, d)`; their distinct values,
enumerated **descending**, are the `k` Lyapunov exponents `λ₀ > ⋯ > λ_{k-1}` of the target
theorem. This mirrors `Filtration.specList`. -/

/-- The finite set of distinct exponent values on `[0, d)`. -/
noncomputable def distinctExp (lam : ℕ → ℝ) (d : ℕ) : Finset ℝ :=
  (Finset.range d).image lam

/-- The number of distinct exponents. -/
noncomputable def numExp (lam : ℕ → ℝ) (d : ℕ) : ℕ := (distinctExp lam d).card

/-- The descending enumeration of the distinct exponents (index `0` = largest). -/
noncomputable def expEnum (lam : ℕ → ℝ) (d : ℕ) : Fin (numExp lam d) → ℝ :=
  fun i => (distinctExp lam d).orderEmbOfFin rfl i.rev

theorem expEnum_strictAnti (lam : ℕ → ℝ) (d : ℕ) : StrictAnti (expEnum lam d) :=
  fun _ _ hij => (distinctExp lam d).orderEmbOfFin rfl |>.strictMono (Fin.rev_lt_rev.mpr hij)

theorem expEnum_mem (lam : ℕ → ℝ) (d : ℕ) (i : Fin (numExp lam d)) :
    expEnum lam d i ∈ distinctExp lam d :=
  (distinctExp lam d).orderEmbOfFin_mem rfl i.rev

/-- Membership: `r` is an enumerated value iff `r = lam j` for some `j < d`. -/
theorem mem_distinctExp (lam : ℕ → ℝ) (d : ℕ) {r : ℝ} :
    r ∈ distinctExp lam d ↔ ∃ j : ℕ, j < d ∧ lam j = r := by
  rw [distinctExp, Finset.mem_image]
  constructor
  · rintro ⟨j, hj, hjr⟩; exact ⟨j, Finset.mem_range.mp hj, hjr⟩
  · rintro ⟨j, hj, hjr⟩; exact ⟨j, Finset.mem_range.mpr hj, hjr⟩

/-- Every exponent `lam j` (`j < d`) is one of the enumerated distinct values. -/
theorem exists_expEnum_eq (lam : ℕ → ℝ) {d : ℕ} {j : ℕ} (hj : j < d) :
    ∃ i : Fin (numExp lam d), expEnum lam d i = lam j := by
  have hr : lam j ∈ distinctExp lam d := (mem_distinctExp lam d).mpr ⟨j, hj, rfl⟩
  have hrange :
      lam j ∈ Set.range ⇑((distinctExp lam d).orderEmbOfFin (rfl : _ = numExp lam d)) := by
    rw [Finset.range_orderEmbOfFin]; exact hr
  obtain ⟨k, hk⟩ := hrange
  exact ⟨k.rev, by simpa [expEnum] using hk⟩

/-- Every enumerated value is realized by some `lam j`. -/
theorem expEnum_eq_lam (lam : ℕ → ℝ) (d : ℕ) (i : Fin (numExp lam d)) :
    ∃ j : ℕ, j < d ∧ expEnum lam d i = lam j := by
  obtain ⟨j, hj, hjr⟩ := (mem_distinctExp lam d).mp (expEnum_mem lam d i)
  exact ⟨j, hj, hjr.symm⟩

theorem numExp_pos (lam : ℕ → ℝ) {d : ℕ} (hd : 0 < d) : 0 < numExp lam d := by
  rw [numExp, Finset.card_pos]; exact ⟨lam 0, (mem_distinctExp lam d).mpr ⟨0, hd, rfl⟩⟩

theorem numExp_le (lam : ℕ → ℝ) (d : ℕ) : numExp lam d ≤ d := by
  rw [numExp, distinctExp]
  calc ((Finset.range d).image lam).card ≤ (Finset.range d).card := Finset.card_image_le
    _ = d := Finset.card_range d

/-! ## The Gram quadratic-form band bound (lower-bound foundation)

For a self-adjoint `Q` and a `0/1` band indicator `χ = 𝟙_{(c,∞)}`, a continuous shape
`f ≥ 0` with `f ≥ a` above `c` controls the band projection:
`a · ‖(cfc χ Q) v‖² ≤ ⟪(cfc f Q) v, v⟫`. Applied with `Q = qpow`, `f = (·)^{2n}`
(so `cfc f Q = gram`) and `a = c^{2n}` it gives the per-vector lower bound
`c^{2n} ‖Pᶜₙ v‖² ≤ ‖A⁽ⁿ⁾ v‖²`. -/

section QuadForm
open scoped InnerProductSpace
open ComplexOrder

/-- The norm identity `‖toEuclideanLin M v‖² = ⟪toEuclideanLin (Mᵀ * M) v, v⟫` (generic
real matrix; the cocycle specialization is `norm_sq_cocycle_apply_eq_inner_gram`). -/
theorem norm_sq_toEuclideanLin_eq_inner_gram
    (M : Matrix (Fin d) (Fin d) ℝ) (v : EuclideanSpace ℝ (Fin d)) :
    ‖Matrix.toEuclideanLin M v‖ ^ 2 = ⟪Matrix.toEuclideanLin (Mᵀ * M) v, v⟫_ℝ := by
  rw [← real_inner_self_eq_norm_sq]
  have hadj : ⟪Matrix.toEuclideanLin M v, Matrix.toEuclideanLin M v⟫_ℝ
      = ⟪((Matrix.toEuclideanLin M).adjoint ∘ₗ (Matrix.toEuclideanLin M)) v, v⟫_ℝ := by
    rw [LinearMap.comp_apply, LinearMap.adjoint_inner_left]
  rw [hadj]
  congr 1
  have hadjM := Matrix.toEuclideanLin_conjTranspose_eq_adjoint M
  rw [Matrix.conjTranspose_eq_transpose_of_trivial] at hadjM
  calc
    ((Matrix.toEuclideanLin M).adjoint ∘ₗ Matrix.toEuclideanLin M) v
        = (Matrix.toEuclideanLin Mᵀ ∘ₗ Matrix.toEuclideanLin M) v := by
          exact congrArg (fun f => (f ∘ₗ Matrix.toEuclideanLin M) v) hadjM.symm
    _ = Matrix.toEuclideanLin (Mᵀ * M) v := by
      ext i
      simp only [LinearMap.comp_apply, Matrix.toLpLin_apply, Matrix.mulVec_mulVec]

/-- **Gram quadratic-form band bound.** For self-adjoint `Q`, a `0/1` band indicator
`χ = 𝟙_{(c,∞)}`, and a continuous `f ≥ 0` on the spectrum with `a ≤ f t` whenever
`c < t`: `a · ‖(cfc χ Q) v‖² ≤ ⟪(cfc f Q) v, v⟫`. The band projector is a self-adjoint
idempotent (`‖Pv‖² = ⟪Pv,v⟫`); the gap `cfc (f − a·χ) Q` is `PosSemidef` since
`f − a·χ ≥ 0` on the spectrum. -/
theorem inner_cfc_ge_band [NeZero d]
    (Q : Matrix (Fin d) (Fin d) ℝ) (hQ : IsSelfAdjoint Q)
    (c a : ℝ) (f : ℝ → ℝ) (hf : ContinuousOn f (_root_.spectrum ℝ Q))
    (hfnn : ∀ t ∈ _root_.spectrum ℝ Q, 0 ≤ f t)
    (hfband : ∀ t ∈ _root_.spectrum ℝ Q, c < t → a ≤ f t)
    (v : EuclideanSpace ℝ (Fin d)) :
    a * ‖Matrix.toEuclideanLin (cfc (Set.indicator (Set.Ioi c) (1 : ℝ → ℝ)) Q) v‖ ^ 2
      ≤ inner ℝ (Matrix.toEuclideanLin (cfc f Q) v) v := by
  classical
  set χ : ℝ → ℝ := Set.indicator (Set.Ioi c) (1 : ℝ → ℝ) with hχ
  have hspecfin : (_root_.spectrum ℝ Q).Finite := Matrix.finite_real_spectrum (A := Q)
  have hcontχ : ContinuousOn χ (_root_.spectrum ℝ Q) := hspecfin.continuousOn _
  have hPsa : IsSelfAdjoint (cfc χ Q) := cfc_predicate χ Q
  have hPherm : (cfc χ Q).IsHermitian := Matrix.isHermitian_iff_isSelfAdjoint.mpr hPsa
  have hidem : (_root_.spectrum ℝ Q).EqOn (fun t => χ t * χ t) χ := by
    intro t _
    by_cases ht : t ∈ Set.Ioi c
    · simp [hχ, Set.indicator_of_mem ht]
    · simp [hχ, Set.indicator_of_notMem ht]
  have hPidem : cfc χ Q * cfc χ Q = cfc χ Q := by
    rw [← cfc_mul χ χ Q hcontχ hcontχ, cfc_congr hidem]
  have hPtranspose : (cfc χ Q)ᵀ = cfc χ Q := by
    have h := hPherm
    rw [Matrix.IsHermitian, Matrix.conjTranspose_eq_transpose_of_trivial] at h
    exact h
  have hstep1 : ‖Matrix.toEuclideanLin (cfc χ Q) v‖ ^ 2
      = ⟪Matrix.toEuclideanLin (cfc χ Q) v, v⟫_ℝ := by
    rw [norm_sq_toEuclideanLin_eq_inner_gram, hPtranspose, hPidem]
  set g : ℝ → ℝ := fun t => f t - a * χ t with hg
  have hgnn : ∀ t ∈ _root_.spectrum ℝ Q, 0 ≤ g t := by
    intro t ht
    by_cases hc : c < t
    · have h1 : χ t = 1 := by simp [hχ, Set.indicator_of_mem (Set.mem_Ioi.mpr hc)]
      rw [hg]; simp only [h1, mul_one]; linarith [hfband t ht hc]
    · have h0 : χ t = 0 := by
        rw [hχ, Set.indicator_of_notMem]; rw [Set.mem_Ioi]; exact hc
      rw [hg]; simp only [h0, mul_zero, sub_zero]; exact hfnn t ht
  have hgsplit : cfc g Q = cfc f Q - a • cfc χ Q := by
    have hca : ContinuousOn (fun t ↦ a * χ t) (_root_.spectrum ℝ Q) :=
      (continuousOn_const).mul hcontχ
    rw [hg, cfc_sub f (fun t ↦ a * χ t) Q hf hca, cfc_const_mul a χ Q hcontχ]
  have hgcont : ContinuousOn g (_root_.spectrum ℝ Q) := hf.sub ((continuousOn_const).mul hcontχ)
  have hgsa : IsSelfAdjoint (cfc g Q) := cfc_predicate g Q
  have hgherm : (cfc g Q).IsHermitian := Matrix.isHermitian_iff_isSelfAdjoint.mpr hgsa
  have hgPSD : (cfc g Q).PosSemidef := by
    rw [Matrix.posSemidef_iff_isHermitian_and_spectrum_nonneg]
    refine ⟨hgherm, ?_⟩
    rw [cfc_map_spectrum g Q hQ hgcont]
    rintro _ ⟨t, ht, rfl⟩
    exact hgnn t ht
  have hinner_dot : ⟪Matrix.toEuclideanLin (cfc g Q) v, v⟫_ℝ
      = star (v : Fin d → ℝ) ⬝ᵥ ((cfc g Q) *ᵥ (v : Fin d → ℝ)) := by
    change (v.ofLp ⬝ᵥ star (((Matrix.toEuclideanLin (cfc g Q)) v).ofLp)) = _
    rw [Matrix.ofLp_toLpLin, Matrix.toLin'_apply]
    simp only [star_trivial]
  have hPSDnn : (0 : ℝ) ≤ ⟪Matrix.toEuclideanLin (cfc g Q) v, v⟫_ℝ := by
    rw [hinner_dot]; exact hgPSD.dotProduct_mulVec_nonneg _
  have hsplit_inner : ⟪Matrix.toEuclideanLin (cfc g Q) v, v⟫_ℝ
      = ⟪Matrix.toEuclideanLin (cfc f Q) v, v⟫_ℝ
        - a * ⟪Matrix.toEuclideanLin (cfc χ Q) v, v⟫_ℝ := by
    rw [hgsplit, map_sub, map_smul, LinearMap.sub_apply, LinearMap.smul_apply,
      inner_sub_left, real_inner_smul_left]
  rw [show inner ℝ (Matrix.toEuclideanLin (cfc f Q) v) v
      = ⟪Matrix.toEuclideanLin (cfc f Q) v, v⟫_ℝ from rfl, hstep1]
  have hfin : (0 : ℝ) ≤ ⟪Matrix.toEuclideanLin (cfc f Q) v, v⟫_ℝ
      - a * ⟪Matrix.toEuclideanLin (cfc χ Q) v, v⟫_ℝ := by
    rw [← hsplit_inner]; exact hPSDnn
  linarith

end QuadForm

variable {X : Type*} [MeasurableSpace X]

/-! ## The per-vector lower bound: Gram–CFC identity, band bound, and liminf

The Gram matrix `gramₙ = (A⁽ⁿ⁾)ᵀA⁽ⁿ⁾` is recovered from `qpowₙ = (gramₙ)^{1/(2n)}` by
raising to the `2n`-th power (`gram_eq_cfc_qpow`). Feeding `qpowₙ` into the quadratic-form
band bound (`inner_cfc_ge_band`) with `f = (·)^{2n}` and threshold `c` then gives the
per-vector bound `c^{2n} ‖Pᶜₙ v‖² ≤ ‖A⁽ⁿ⁾ v‖²` (`cocycle_apply_sq_ge_band`). Taking logs,
dividing by `2n`, and sending the band-projector correction to `0`
(`tendsto_inv_mul_log_norm_bandProjector_apply`) yields the per-vector liminf lower bound
`log c ≤ liminf (1/n) log‖A⁽ⁿ⁾ v‖` (`log_le_liminf_log_cocycle_apply`). -/

section LowerBound
open scoped Matrix InnerProductSpace

/-- **Gram–CFC identity.** Raising `qpowₙ = (gramₙ)^{1/(2n)}` to the `2n`-th power (via the
CFC) recovers the Gram matrix `gramₙ`. -/
theorem gram_eq_cfc_qpow [NeZero d] (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X)
    {n : ℕ} (hn : 1 ≤ n) (x : X) :
    cfc (fun t : ℝ => t ^ (2 * (n : ℝ))) (qpow A T n x) = gram A T n x := by
  have hnR : (n : ℝ) ≠ 0 := by exact_mod_cast (Nat.one_le_iff_ne_zero.mp hn)
  have h2n : (2 * (n : ℝ)) ≠ 0 := by positivity
  have hgsa : IsSelfAdjoint (gram A T n x) := gram_isSelfAdjoint A T n x
  -- spectrum of gram is nonnegative
  have hspec : _root_.spectrum ℝ (gram A T n x) ⊆ {a : ℝ | 0 ≤ a} :=
    (Matrix.posSemidef_iff_isHermitian_and_spectrum_nonneg.mp (gram_posSemidef A T n x)).2
  -- global continuity of the two rpow shapes (exponents ≥ 0)
  have hcont_out : Continuous (fun t : ℝ => t ^ (2 * (n : ℝ))) :=
    Real.continuous_rpow_const (by positivity)
  have hcont_in : Continuous (fun t : ℝ => t ^ ((2 * (n : ℝ))⁻¹)) :=
    Real.continuous_rpow_const (by positivity)
  -- fold the two powers via `cfc_comp`
  have hfold :
      cfc (fun t : ℝ => t ^ (2 * (n : ℝ))) (qpow A T n x)
        = cfc (fun t : ℝ => (t ^ ((2 * (n : ℝ))⁻¹)) ^ (2 * (n : ℝ))) (gram A T n x) := by
    change cfc (fun t : ℝ ↦ t ^ (2 * (n : ℝ)))
        (cfc (fun t : ℝ ↦ t ^ ((2 * (n : ℝ))⁻¹)) (gram A T n x)) = _
    rw [← cfc_comp (fun t : ℝ ↦ t ^ (2 * (n : ℝ)))
      (fun t : ℝ ↦ t ^ ((2 * (n : ℝ))⁻¹)) (gram A T n x) hgsa hcont_out.continuousOn
      hcont_in.continuousOn]
    rfl
  rw [hfold]
  -- on the (nonneg) spectrum, the composed power is the identity
  have hid : (_root_.spectrum ℝ (gram A T n x)).EqOn
      (fun t : ℝ => (t ^ ((2 * (n : ℝ))⁻¹)) ^ (2 * (n : ℝ))) (id : ℝ → ℝ) := by
    intro t ht
    have ht0 : 0 ≤ t := hspec ht
    simp only [id]
    rw [← Real.rpow_mul ht0]
    rw [show ((2 * (n : ℝ))⁻¹ * (2 * (n : ℝ))) = 1 by field_simp]
    rw [Real.rpow_one]
  rw [cfc_congr hid, cfc_id ℝ (gram A T n x)]

/-- **Band lower bound.** For `c ≥ 0`, the band projection of `v` (for the band `(c,∞)` of
`qpowₙ`) is controlled by the cocycle growth:
`c^{2n} · ‖Pᶜₙ v‖² ≤ ‖A⁽ⁿ⁾ v‖²`. -/
theorem cocycle_apply_sq_ge_band [NeZero d] (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X)
    {n : ℕ} (hn : 1 ≤ n) (x : X) {c : ℝ} (hc : 0 ≤ c) (v : EuclideanSpace ℝ (Fin d)) :
    c ^ (2 * (n : ℝ)) *
        ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c) 1) n x) v‖ ^ 2
      ≤ ‖Matrix.toEuclideanLin (cocycle A T n x) v‖ ^ 2 := by
  set Q := qpow A T n x with hQ
  have hQsa : IsSelfAdjoint Q := qpow_isSelfAdjoint A T n x
  have h2n : (0 : ℝ) ≤ 2 * (n : ℝ) := by positivity
  -- spectrum of Q is nonnegative
  have hspec : _root_.spectrum ℝ Q ⊆ {a : ℝ | 0 ≤ a} :=
    (Matrix.posSemidef_iff_isHermitian_and_spectrum_nonneg.mp (qpow_posSemidef A T n x)).2
  have hf : ContinuousOn (fun t : ℝ => t ^ (2 * (n : ℝ))) (_root_.spectrum ℝ Q) :=
    (Real.continuous_rpow_const h2n).continuousOn
  have hfnn : ∀ t ∈ _root_.spectrum ℝ Q, 0 ≤ (fun t : ℝ => t ^ (2 * (n : ℝ))) t := by
    intro t ht; exact Real.rpow_nonneg (hspec ht) _
  have hfband : ∀ t ∈ _root_.spectrum ℝ Q, c < t →
      c ^ (2 * (n : ℝ)) ≤ (fun t : ℝ => t ^ (2 * (n : ℝ))) t := by
    intro t _ hct
    exact Real.rpow_le_rpow hc (le_of_lt hct) h2n
  have hmain := inner_cfc_ge_band Q hQsa c (c ^ (2 * (n : ℝ)))
    (fun t : ℝ => t ^ (2 * (n : ℝ))) hf hfnn hfband v
  -- `cfc f Q = gram` by the Gram–CFC identity; the RHS inner product is `‖cocycle v‖²`
  rw [gram_eq_cfc_qpow A T hn x] at hmain
  rw [← norm_sq_cocycle_apply_eq_inner_gram A n x v] at hmain
  -- `cfc χ Q = bandProjector` by def
  exact hmain

omit [MeasurableSpace X] in
/-- **Band correction vanishes.** If the band projectors `Pᶜₙ` converge to `P` with
`P v ≠ 0`, then the normalized log of the band projection `‖Pᶜₙ v‖` tends to `0`: the norm
converges to a positive limit, so its log is bounded, and dividing by `n → ∞` kills it. -/
theorem tendsto_inv_mul_log_norm_bandProjector_apply [NeZero d]
    (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) {c : ℝ} {x : X}
    {P : Matrix (Fin d) (Fin d) ℝ} {v : EuclideanSpace ℝ (Fin d)}
    (hP : Filter.Tendsto (fun n => bandProjector A T (Set.indicator (Set.Ioi c) 1) n x)
      Filter.atTop (nhds P))
    (hPv : Matrix.toEuclideanLin P v ≠ 0) :
    Filter.Tendsto
      (fun n : ℕ ↦ (n : ℝ)⁻¹ * Real.log
        ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c) 1) n x) v‖)
      Filter.atTop (nhds 0) := by
  -- the linear map `M ↦ toEuclideanLin M v` is continuous (finite-dimensional)
  set evalLin : Matrix (Fin d) (Fin d) ℝ →ₗ[ℝ] EuclideanSpace ℝ (Fin d) :=
    (LinearMap.applyₗ v) ∘ₗ (Matrix.toEuclideanLin).toLinearMap with heval
  have hcont : Continuous evalLin := evalLin.continuous_of_finiteDimensional
  have hevalP : evalLin P = Matrix.toEuclideanLin P v := rfl
  -- band projection applied to v converges to P v
  have htend : Filter.Tendsto
      (fun n => Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c) 1) n x) v)
      Filter.atTop (nhds (Matrix.toEuclideanLin P v)) := by
    have := (hcont.tendsto P).comp hP
    simpa [heval, Function.comp_def] using this
  -- norms converge to L = ‖P v‖ > 0
  have hL : (0 : ℝ) < ‖Matrix.toEuclideanLin P v‖ := norm_pos_iff.mpr hPv
  have hnorm : Filter.Tendsto
      (fun n => ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c) 1) n x) v‖)
      Filter.atTop (nhds ‖Matrix.toEuclideanLin P v‖) := htend.norm
  -- logs converge to log L (a finite number)
  have hlog : Filter.Tendsto
      (fun n ↦ Real.log
        ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c) 1) n x) v‖)
      Filter.atTop (nhds (Real.log ‖Matrix.toEuclideanLin P v‖)) :=
    (Real.continuousAt_log (ne_of_gt hL)).tendsto.comp hnorm
  -- (n)⁻¹ → 0, times bounded log → 0
  have hinv : Filter.Tendsto (fun n : ℕ => (n : ℝ)⁻¹) Filter.atTop (nhds 0) :=
    tendsto_natCast_atTop_atTop.inv_tendsto_atTop
  have := hinv.mul hlog
  simpa using this

/-- **Per-vector lower bound, eventual form (the analytic core of the liminf bound).** If
the band projectors for `(c,∞)` (with `c > 0`) converge to `P` with `P v ≠ 0`, then
*eventually* `log c + (1/n) log‖Pᶜₙ v‖ ≤ (1/n) log‖A⁽ⁿ⁾ v‖`, where the left band-correction
term tends to `0` (`tendsto_inv_mul_log_norm_bandProjector_apply`). Taking `n → ∞` (the
band correction vanishing) yields `log c ≤ liminf (1/n) log‖A⁽ⁿ⁾ v‖`, which is packaged as
`log_le_liminf_log_cocycle_apply` below. -/
theorem log_add_correction_le_inv_mul_log_cocycle_apply [NeZero d]
    (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (hA : ∀ x, (A x).det ≠ 0)
    {c : ℝ} (hc : 0 < c) {x : X} {P : Matrix (Fin d) (Fin d) ℝ} {v : EuclideanSpace ℝ (Fin d)}
    (hP : Filter.Tendsto (fun n => bandProjector A T (Set.indicator (Set.Ioi c) 1) n x)
      Filter.atTop (nhds P))
    (hPv : Matrix.toEuclideanLin P v ≠ 0) :
    ∀ᶠ n : ℕ in Filter.atTop,
      Real.log c + (n : ℝ)⁻¹ * Real.log
          ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c) 1) n x) v‖
        ≤ (n : ℝ)⁻¹ * Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖ := by
  -- v ≠ 0 since toEuclideanLin P v ≠ 0
  have hv : v ≠ 0 := by
    rintro rfl; exact hPv (by rw [map_zero])
  -- band projection applied to v converges to P v ≠ 0, hence eventually nonzero
  set evalLin : Matrix (Fin d) (Fin d) ℝ →ₗ[ℝ] EuclideanSpace ℝ (Fin d) :=
    (LinearMap.applyₗ v) ∘ₗ (Matrix.toEuclideanLin).toLinearMap with heval
  have hcont : Continuous evalLin := evalLin.continuous_of_finiteDimensional
  have htendBand : Filter.Tendsto
      (fun n => Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c) 1) n x) v)
      Filter.atTop (nhds (Matrix.toEuclideanLin P v)) := by
    have := (hcont.tendsto P).comp hP
    simpa [heval, Function.comp_def] using this
  have hL : (0 : ℝ) < ‖Matrix.toEuclideanLin P v‖ := norm_pos_iff.mpr hPv
  have hbandpos : ∀ᶠ n in Filter.atTop,
      0 < ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c) 1) n x) v‖ := by
    have hnorm := htendBand.norm
    have : ∀ᶠ n in Filter.atTop,
        ‖Matrix.toEuclideanLin P v‖ / 2 <
          ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c) 1) n x) v‖ :=
      hnorm.eventually_const_lt (by linarith)
    filter_upwards [this] with n hn
    linarith [hn, half_pos hL]
  -- the eventual inequality
  filter_upwards [eventually_ge_atTop 1, hbandpos] with n hn1 hbpos
  have hnpos : (0 : ℝ) < (n : ℝ) := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hn1
  -- the band bound `cocycle_apply_sq_ge_band`
  have hband := cocycle_apply_sq_ge_band A T hn1 x (le_of_lt hc) v
  set b := ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c) 1) n x) v‖
    with hb
  set M := ‖Matrix.toEuclideanLin (cocycle A T n x) v‖ with hM
  have hMpos : 0 < M := norm_pos_iff.mpr (cocycle_apply_ne_zero (T := T) hA n x hv)
  -- take logs of `c^(2n) * b^2 ≤ M^2`
  have hlhs_pos : 0 < c ^ (2 * (n : ℝ)) * b ^ 2 := by
    have : 0 < c ^ (2 * (n : ℝ)) := Real.rpow_pos_of_pos hc _
    positivity
  have hlog_le : Real.log (c ^ (2 * (n : ℝ)) * b ^ 2) ≤ Real.log (M ^ 2) :=
    Real.log_le_log hlhs_pos hband
  -- expand the LHS log
  rw [Real.log_mul (ne_of_gt (Real.rpow_pos_of_pos hc _)) (by positivity),
    Real.log_rpow hc, Real.log_pow, Real.log_pow] at hlog_le
  push_cast at hlog_le
  -- hlog_le : 2*n*log c + 2*log b ≤ 2*log M
  have h2n : (0 : ℝ) < 2 * (n : ℝ) := by positivity
  rw [← sub_nonneg]
  have hninv : (0 : ℝ) < (n : ℝ)⁻¹ := by positivity
  have hexpand : (n : ℝ)⁻¹ * Real.log M - (Real.log c + (n : ℝ)⁻¹ * Real.log b)
      = (n : ℝ)⁻¹ * (Real.log M - Real.log b - (n : ℝ) * Real.log c) := by
    field_simp
    ring
  rw [hexpand]
  apply mul_nonneg (le_of_lt hninv)
  nlinarith [hlog_le]

/-- **Per-vector liminf lower bound.** If the band projectors for `(c,∞)` (with `c > 0`)
converge to `P` with `P v ≠ 0`, then `log c ≤ liminf (1/n) log‖A⁽ⁿ⁾ v‖`.

The proof combines the eventual lower bound `log_add_correction_le_inv_mul_log_cocycle_apply`
(whose left side converges to `log c`, the band correction vanishing by
`tendsto_inv_mul_log_norm_bandProjector_apply`) with `liminf` monotonicity. The
`IsCoboundedUnder (· ≥ ·)` side-condition on the right-hand cocycle sequence — which fails
in general without an a-priori upper growth bound on `(1/n) log‖A⁽ⁿ⁾‖`, a Furstenberg–Kesten
input — is taken as a hypothesis `hcobdd`; at the application site it is supplied by the
integrability of the top Furstenberg–Kesten exponent. -/
theorem log_le_liminf_log_cocycle_apply [NeZero d]
    (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (hA : ∀ x, (A x).det ≠ 0)
    {c : ℝ} (hc : 0 < c) {x : X} {P : Matrix (Fin d) (Fin d) ℝ} {v : EuclideanSpace ℝ (Fin d)}
    (hP : Filter.Tendsto (fun n => bandProjector A T (Set.indicator (Set.Ioi c) 1) n x)
      Filter.atTop (nhds P))
    (hPv : Matrix.toEuclideanLin P v ≠ 0)
    (hcobdd : Filter.atTop.IsCoboundedUnder (· ≥ ·)
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖)) :
    Real.log c ≤ Filter.liminf
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖)
      Filter.atTop := by
  have hcorr := tendsto_inv_mul_log_norm_bandProjector_apply A T hP hPv
  set LHS : ℕ → ℝ := fun n ↦ Real.log c + (n : ℝ)⁻¹ * Real.log
      ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c) 1) n x) v‖
    with hLHS
  set RHS : ℕ → ℝ := fun n =>
      (n : ℝ)⁻¹ * Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖ with hRHS
  have hLHStend : Filter.Tendsto LHS Filter.atTop (nhds (Real.log c)) := by
    have := (tendsto_const_nhds (x := Real.log c) (f := Filter.atTop (α := ℕ))).add hcorr
    simpa [hLHS] using this
  have hineq : ∀ᶠ n in Filter.atTop, LHS n ≤ RHS n :=
    log_add_correction_le_inv_mul_log_cocycle_apply A T hA hc hP hPv
  have hLHSbdd : Filter.atTop.IsBoundedUnder (· ≥ ·) LHS := hLHStend.isBoundedUnder_ge
  calc Real.log c = Filter.liminf LHS Filter.atTop := hLHStend.liminf_eq.symm
    _ ≤ Filter.liminf RHS Filter.atTop := Filter.liminf_le_liminf hineq hLHSbdd hcobdd

/-! ## Band-projector nesting

For `c ≤ c'`, the spectral bands satisfy `Ioi c' ⊆ Ioi c`, so the finer band projector
(threshold `c'`) has range contained in the coarser one (threshold `c`); algebraically
`Pᶜₙ · Pᶜ'ₙ = Pᶜ'ₙ`. Passing to the limit and applying to a vector gives the
kernel-propagation form consumed by the upper-bound proof: a vector killed by the coarser
(lower-threshold) limit projector is killed by every finer (higher-threshold) one above
it. -/

omit [MeasurableSpace X] in
/-- **Band-projector nesting (finite `n`, operator form).** For `c ≤ c'`, the band
projectors are nested: `cfc 𝟙_{(c,∞)} · cfc 𝟙_{(c',∞)} = cfc 𝟙_{(c',∞)}` on `qpow`. The
coarser band (threshold `c`) contains the finer one (threshold `c'`). -/
theorem bandProjector_mul_of_le (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X)
    (n : ℕ) (x : X) {c c' : ℝ} (h : c ≤ c') :
    bandProjector A T (Set.indicator (Set.Ioi c) 1) n x
        * bandProjector A T (Set.indicator (Set.Ioi c') 1) n x
      = bandProjector A T (Set.indicator (Set.Ioi c') 1) n x := by
  -- On the spectrum, `𝟙_{(c,∞)} t · 𝟙_{(c',∞)} t = 𝟙_{(c',∞)} t` because `Ioi c' ⊆ Ioi c`.
  have hidem : (_root_.spectrum ℝ (qpow A T n x)).EqOn
      (fun t => Set.indicator (Set.Ioi c) (1 : ℝ → ℝ) t * Set.indicator (Set.Ioi c') (1 : ℝ → ℝ) t)
      (Set.indicator (Set.Ioi c') (1 : ℝ → ℝ)) := by
    intro t _
    by_cases ht' : t ∈ Set.Ioi c'
    · have ht : t ∈ Set.Ioi c := lt_of_le_of_lt h ht'
      simp [Set.indicator_of_mem ht, Set.indicator_of_mem ht']
    · simp [Set.indicator_of_notMem ht']
  have hcont : ContinuousOn (Set.indicator (Set.Ioi c) (1 : ℝ → ℝ))
      (_root_.spectrum ℝ (qpow A T n x)) :=
    (Matrix.finite_real_spectrum (A := qpow A T n x)).continuousOn _
  have hcont' : ContinuousOn (Set.indicator (Set.Ioi c') (1 : ℝ → ℝ))
      (_root_.spectrum ℝ (qpow A T n x)) :=
    (Matrix.finite_real_spectrum (A := qpow A T n x)).continuousOn _
  simp only [bandProjector]
  rw [← cfc_mul _ _ _ hcont hcont', cfc_congr hidem]

omit [MeasurableSpace X] in
/-- **Band-projector nesting (limit, operator form).** Passing `bandProjector_mul_of_le`
through the two convergent band-projector sequences (matrix multiplication is continuous)
gives `P · P' = P'` for the limit projectors, where `c ≤ c'`. -/
theorem limitBandProjector_mul_of_le (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X)
    {x : X} {c c' : ℝ} (h : c ≤ c') {P P' : Matrix (Fin d) (Fin d) ℝ}
    (hP : Filter.Tendsto (fun n => bandProjector A T (Set.indicator (Set.Ioi c) 1) n x)
      Filter.atTop (nhds P))
    (hP' : Filter.Tendsto (fun n => bandProjector A T (Set.indicator (Set.Ioi c') 1) n x)
      Filter.atTop (nhds P')) :
    P * P' = P' := by
  -- The product sequence converges both to `P * P'` (by continuity of multiplication)
  -- and, by band nesting, to `P'`.
  have hmul : Filter.Tendsto
      (fun n => bandProjector A T (Set.indicator (Set.Ioi c) 1) n x
          * bandProjector A T (Set.indicator (Set.Ioi c') 1) n x)
      Filter.atTop (nhds (P * P')) := hP.mul hP'
  have heq : (fun n => bandProjector A T (Set.indicator (Set.Ioi c) 1) n x
          * bandProjector A T (Set.indicator (Set.Ioi c') 1) n x)
      = (fun n => bandProjector A T (Set.indicator (Set.Ioi c') 1) n x) := by
    funext m; exact bandProjector_mul_of_le A T m x h
  rw [heq] at hmul
  exact tendsto_nhds_unique hmul hP'

/-- **Band-projector nesting (limit, kernel-propagation form).** With `c ≤ c'`, a vector
with `P v = 0` for the coarser (threshold `c`) limit projector also has `P' v = 0` for the
finer (threshold `c'`) one: transposing `P · P' = P'` (both limit projectors are symmetric)
gives `P' · P = P'`, hence `P' v = P' (P v) = 0`. -/
theorem limitBandProjector_apply_eq_zero_of_le [NeZero d]
    (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X)
    {x : X} {c c' : ℝ} (h : c ≤ c') {P P' : Matrix (Fin d) (Fin d) ℝ}
    (hP : Filter.Tendsto (fun n => bandProjector A T (Set.indicator (Set.Ioi c) 1) n x)
      Filter.atTop (nhds P))
    (hP' : Filter.Tendsto (fun n => bandProjector A T (Set.indicator (Set.Ioi c') 1) n x)
      Filter.atTop (nhds P')) {v : EuclideanSpace ℝ (Fin d)}
    (hv : Matrix.toEuclideanLin P v = 0) :
    Matrix.toEuclideanLin P' v = 0 := by
  -- Since all band projectors are self-adjoint (hence the limits are symmetric),
  -- `P * P' = P'` transposes to `P' * P = P'`. Then `P' v = P' (P v) = P' 0 = 0`.
  have hPP' : P * P' = P' := limitBandProjector_mul_of_le A T h hP hP'
  -- symmetry of the limit projectors (limit of self-adjoint matrices is self-adjoint)
  have hPsym : Pᵀ = P := by
    have hsa : Filter.Tendsto
        (fun n => (bandProjector A T (Set.indicator (Set.Ioi c) 1) n x)ᵀ)
        Filter.atTop (nhds Pᵀ) := by
      have hcont : Continuous (fun M : Matrix (Fin d) (Fin d) ℝ => Mᵀ) := by fun_prop
      exact (hcont.continuousAt (x := P)).tendsto.comp hP
    have heqT : (fun n => (bandProjector A T (Set.indicator (Set.Ioi c) 1) n x)ᵀ)
        = (fun n => bandProjector A T (Set.indicator (Set.Ioi c) 1) n x) := by
      funext m
      have hsa : (bandProjector A T (Set.indicator (Set.Ioi c) 1) m x)ᴴ
          = bandProjector A T (Set.indicator (Set.Ioi c) 1) m x :=
        bandProjector_isSelfAdjoint A T (Set.indicator (Set.Ioi c) 1) m x
      rwa [Matrix.conjTranspose_eq_transpose_of_trivial] at hsa
    rw [heqT] at hsa
    exact tendsto_nhds_unique hsa hP
  have hP'sym : P'ᵀ = P' := by
    have hsa : Filter.Tendsto
        (fun n => (bandProjector A T (Set.indicator (Set.Ioi c') 1) n x)ᵀ)
        Filter.atTop (nhds P'ᵀ) := by
      have hcont : Continuous (fun M : Matrix (Fin d) (Fin d) ℝ => Mᵀ) := by fun_prop
      exact (hcont.continuousAt (x := P')).tendsto.comp hP'
    have heqT : (fun n => (bandProjector A T (Set.indicator (Set.Ioi c') 1) n x)ᵀ)
        = (fun n => bandProjector A T (Set.indicator (Set.Ioi c') 1) n x) := by
      funext m
      have hsa : (bandProjector A T (Set.indicator (Set.Ioi c') 1) m x)ᴴ
          = bandProjector A T (Set.indicator (Set.Ioi c') 1) m x :=
        bandProjector_isSelfAdjoint A T (Set.indicator (Set.Ioi c') 1) m x
      rwa [Matrix.conjTranspose_eq_transpose_of_trivial] at hsa
    rw [heqT] at hsa
    exact tendsto_nhds_unique hsa hP'
  -- transpose `P * P' = P'`: `(P * P')ᵀ = P'ᵀ`, i.e. `P'ᵀ * Pᵀ = P'ᵀ`, i.e. `P' * P = P'`.
  have hP'P : P' * P = P' := by
    have := congrArg Matrix.transpose hPP'
    rw [Matrix.transpose_mul, hPsym, hP'sym] at this
    exact this
  -- now `P' v = (P' * P) v = P' (P v) = P' 0 = 0`
  have hsplit : Matrix.toEuclideanLin (P' * P) v
      = Matrix.toEuclideanLin P' (Matrix.toEuclideanLin P v) := by
    simp only [Matrix.toLpLin_apply, Matrix.mulVec_mulVec]
  calc Matrix.toEuclideanLin P' v
      = Matrix.toEuclideanLin (P' * P) v := by rw [hP'P]
    _ = Matrix.toEuclideanLin P' (Matrix.toEuclideanLin P v) := hsplit
    _ = Matrix.toEuclideanLin P' 0 := by rw [hv]
    _ = 0 := map_zero _

end LowerBound

/-! ## The per-vector growth upper bound and the per-vector limit

The per-vector upper bound `limsup (1/n) log‖A⁽ⁿ⁾v‖ ≤ λᵢ`, conditional on the per-index
leakage envelopes, and the assembled per-vector exact-growth limit. -/

section Upper
open scoped InnerProductSpace

variable (T : X → X)

/-- **Helper (limsup ⟹ exp envelope).** If `a n ≥ 0` and `limsup_n (1/n) log (a n) ≤ M`, then for
every `ε > 0` eventually `a n ≤ exp (n (M + ε))`. -/
theorem eventually_le_exp_of_limsup_le {a : ℕ → ℝ} (hann : ∀ n, 0 ≤ a n) {M : ℝ}
    (hbdd : IsBoundedUnder (· ≤ ·) atTop (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (a n)))
    (hlim : limsup (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (a n)) atTop ≤ M)
    (ε : ℝ) (hε : 0 < ε) :
    ∀ᶠ n : ℕ in atTop, a n ≤ Real.exp ((n : ℝ) * (M + ε)) := by
  have hlt : limsup (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (a n)) atTop < M + ε := by linarith
  have hev := eventually_lt_of_limsup_lt hlt hbdd
  filter_upwards [hev, eventually_ge_atTop 1] with n hn hn1
  have hnpos : (0 : ℝ) < (n : ℝ) := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hn1
  rcases eq_or_lt_of_le (hann n) with h0 | hpos
  · rw [← h0]; positivity
  · have hloglt : Real.log (a n) < (n : ℝ) * (M + ε) := by
      have hmul : (n : ℝ) * ((n : ℝ)⁻¹ * Real.log (a n)) < (n : ℝ) * (M + ε) :=
        mul_lt_mul_of_pos_left hn hnpos
      rwa [← mul_assoc, mul_inv_cancel₀ (ne_of_gt hnpos), one_mul] at hmul
    have : a n < Real.exp ((n : ℝ) * (M + ε)) := by
      rw [← Real.exp_log hpos]; exact Real.exp_lt_exp.mpr hloglt
    exact le_of_lt this

/-- **Spectral Parseval for the Gram quadratic form** against the sorted Gram eigenbasis:
`⟪gram v, v⟫ = ∑ⱼ (eigenvalues₀ (gram) j) · ⟪v, uⱼ⟫²`. -/
theorem inner_gram_apply_eq_sum_eigenvalues₀ [NeZero d]
    (A : X → Matrix (Fin d) (Fin d) ℝ) (n : ℕ) (x : X) (v : EuclideanSpace ℝ (Fin d)) :
    ⟪Matrix.toEuclideanLin (gram A T n x) v, v⟫_ℝ
      = ∑ j : Fin (Fintype.card (Fin d)),
          (gram_posSemidef A T n x).isHermitian.eigenvalues₀ j *
            (inner ℝ v (sortedGramEigenbasis A T n x j) : ℝ) ^ 2 := by
  set b := sortedGramEigenbasis A T n x with hb
  set G := Matrix.toEuclideanLin (gram A T n x) with hG
  have hGsym : G.IsSymmetric :=
    Matrix.isHermitian_iff_isSymmetric.mp (gram_posSemidef A T n x).isHermitian
  rw [← b.sum_inner_mul_inner (G v) v]
  refine Finset.sum_congr rfl (fun j _ => ?_)
  have hGbj : G (b j) = (gram_posSemidef A T n x).isHermitian.eigenvalues₀ j • b j :=
    sortedGramEigenbasis_eigenpair A T n x j
  have h1 : (inner ℝ (G v) (b j) : ℝ) = (gram_posSemidef A T n x).isHermitian.eigenvalues₀ j *
      (inner ℝ v (b j) : ℝ) := by
    rw [hGsym v (b j), hGbj, inner_smul_right]
  have h2 : (inner ℝ (b j) v : ℝ) = (inner ℝ v (b j) : ℝ) := real_inner_comm _ _
  rw [h1, h2]; ring

/-- **Spectral Parseval (cocycle form).** The squared cocycle norm is the sum of squared singular
values times squared overlaps with the sorted Gram eigenbasis:
`‖A⁽ⁿ⁾ v‖² = ∑ⱼ σⱼ(n)² · ⟪v, uⱼ(n)⟫²`. -/
theorem norm_sq_cocycle_apply_eq_sum_singularValues [NeZero d]
    (A : X → Matrix (Fin d) (Fin d) ℝ) (n : ℕ) (x : X) (v : EuclideanSpace ℝ (Fin d)) :
    ‖Matrix.toEuclideanLin (cocycle A T n x) v‖ ^ 2
      = ∑ j : Fin (Fintype.card (Fin d)),
          ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues j) ^ 2 *
            (inner ℝ v (sortedGramEigenbasis A T n x j) : ℝ) ^ 2 := by
  rw [norm_sq_cocycle_apply_eq_inner_gram, inner_gram_apply_eq_sum_eigenvalues₀]
  refine Finset.sum_congr rfl (fun j _ => ?_)
  rw [gram_eigenvalues₀_eq_sq_singularValues]

/-- The `j`-th spectral term `σⱼ(n)² · ⟪v,uⱼ(n)⟫²`. -/
noncomputable def specTerm [NeZero d] (A : X → Matrix (Fin d) (Fin d) ℝ) (n : ℕ) (x : X)
    (v : EuclideanSpace ℝ (Fin d)) (j : Fin (Fintype.card (Fin d))) : ℝ :=
  ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues j) ^ 2 *
    (inner ℝ v (sortedGramEigenbasis A T n x j) : ℝ) ^ 2

/-- `∑ⱼ specTermⱼ = ‖A⁽ⁿ⁾ v‖²`. -/
theorem sum_specTerm_eq_norm_sq [NeZero d] (A : X → Matrix (Fin d) (Fin d) ℝ) (n : ℕ) (x : X)
    (v : EuclideanSpace ℝ (Fin d)) :
    ∑ j, specTerm T A n x v j = ‖Matrix.toEuclideanLin (cocycle A T n x) v‖ ^ 2 := by
  rw [norm_sq_cocycle_apply_eq_sum_singularValues]; rfl

theorem specTerm_nonneg [NeZero d] (A : X → Matrix (Fin d) (Fin d) ℝ) (n : ℕ) (x : X)
    (v : EuclideanSpace ℝ (Fin d)) (j : Fin (Fintype.card (Fin d))) :
    0 ≤ specTerm T A n x v j := by
  rw [specTerm]; positivity

/-- **Conditional upper bound.** Given, for each spectral index `j`, the per-index exp-envelope
`tⱼ(n) ≤ exp(n(2λᵢ + ε))`, and eventual positivity of `‖A⁽ⁿ⁾ v‖`, the per-vector growth limsup is
`≤ λᵢ`. -/
theorem limsup_inv_mul_log_norm_cocycle_apply_le [NeZero d]
    (A : X → Matrix (Fin d) (Fin d) ℝ) (x : X) (v : EuclideanSpace ℝ (Fin d)) (lami : ℝ)
    (henv : ∀ j : Fin (Fintype.card (Fin d)), ∀ ε > 0,
      ∀ᶠ n : ℕ in atTop, specTerm T A n x v j ≤ Real.exp ((n : ℝ) * (2 * lami + ε)))
    (hpos : ∀ᶠ n : ℕ in atTop, 0 < ‖Matrix.toEuclideanLin (cocycle A T n x) v‖)
    (hcobdd : IsCoboundedUnder (· ≤ ·) atTop
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖)) :
    limsup (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) atTop ≤ lami := by
  set g : ℕ → ℝ := fun n => (n : ℝ)⁻¹ *
    Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖ with hg
  set N := Fintype.card (Fin (Fintype.card (Fin d))) with hN
  have hcardpos : (0 : ℝ) < (N : ℝ) := by rw [hN]; exact_mod_cast Fintype.card_pos
  have hsumpos : ∀ᶠ n : ℕ in atTop, 0 < ∑ j, specTerm T A n x v j := by
    filter_upwards [hpos] with n hn
    rw [sum_specTerm_eq_norm_sq]; positivity
  have heq : ∀ᶠ n : ℕ in atTop, g n =
      (1/2 : ℝ) * ((n : ℝ)⁻¹ * Real.log (∑ j, specTerm T A n x v j)) := by
    filter_upwards [hpos] with n hn
    have hsq : ∑ j, specTerm T A n x v j
        = ‖Matrix.toEuclideanLin (cocycle A T n x) v‖ ^ 2 := sum_specTerm_eq_norm_sq T A n x v
    have hlog : Real.log (∑ j, specTerm T A n x v j)
        = 2 * Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖ := by
      rw [hsq, Real.log_pow]; push_cast; ring
    rw [hg, hlog]; ring
  have hcorr : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log N) atTop (𝓝 0) := by
    have hinv : Tendsto (fun n : ℕ => (n : ℝ)⁻¹) atTop (𝓝 0) :=
      tendsto_natCast_atTop_atTop.inv_tendsto_atTop
    simpa using hinv.mul_const (Real.log N)
  have hgkey : ∀ ε > 0, ∀ᶠ n : ℕ in atTop,
      g n ≤ lami + ε / 2 + (1/2 : ℝ) * ((n : ℝ)⁻¹ * Real.log N) := by
    intro ε hε
    have hall : ∀ᶠ n : ℕ in atTop, ∀ j,
        specTerm T A n x v j ≤ Real.exp ((n : ℝ) * (2 * lami + ε)) :=
      eventually_all.mpr (fun j => henv j ε hε)
    filter_upwards [hall, hsumpos, heq, eventually_ge_atTop 1] with n hn hsum_pos hen hn1
    have hnpos : (0 : ℝ) < (n : ℝ) := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hn1
    have hninv : (0 : ℝ) < (n : ℝ)⁻¹ := by positivity
    have hsum_le : ∑ j, specTerm T A n x v j ≤ (N : ℝ) * Real.exp ((n : ℝ) * (2 * lami + ε)) := by
      calc ∑ j, specTerm T A n x v j ≤ ∑ _j : Fin (Fintype.card (Fin d)),
              Real.exp ((n : ℝ) * (2 * lami + ε)) := Finset.sum_le_sum (fun j _ => hn j)
        _ = (N : ℝ) * Real.exp ((n : ℝ) * (2 * lami + ε)) := by
            rw [Finset.sum_const, Finset.card_univ, nsmul_eq_mul, hN]
    have hlog_le := Real.log_le_log hsum_pos hsum_le
    rw [Real.log_mul (ne_of_gt hcardpos) (Real.exp_ne_zero _), Real.log_exp] at hlog_le
    have hmul := mul_le_mul_of_nonneg_left hlog_le (le_of_lt hninv)
    rw [hen]
    have hstep : (n : ℝ)⁻¹ * Real.log (∑ j, specTerm T A n x v j)
        ≤ (n : ℝ)⁻¹ * Real.log N + (2 * lami + ε) := by
      calc (n : ℝ)⁻¹ * Real.log (∑ j, specTerm T A n x v j)
          ≤ (n : ℝ)⁻¹ * (Real.log N + (n : ℝ) * (2 * lami + ε)) := hmul
        _ = (n : ℝ)⁻¹ * Real.log N + (2 * lami + ε) := by
            rw [mul_add, ← mul_assoc, inv_mul_cancel₀ (ne_of_gt hnpos), one_mul]
    nlinarith [hstep]
  have hgbdd : IsBoundedUnder (· ≤ ·) atTop g := by
    obtain ⟨M, hM⟩ := (Filter.eventually_atTop.mp ((hgkey 1 one_pos).and
      (hcorr.eventually (gt_mem_nhds (show (0:ℝ) < 2 by norm_num)))))
    refine ⟨lami + 1 / 2 + 1, ?_⟩
    rw [Filter.eventually_map, Filter.eventually_atTop]
    refine ⟨M, fun n hn => ?_⟩
    obtain ⟨h1, h2⟩ := hM n hn
    have h2' : (n : ℝ)⁻¹ * Real.log N < 2 := by simpa using h2
    nlinarith [h1, h2']
  rw [limsup_le_iff' hcobdd hgbdd]
  intro y hy
  set ε := y - lami with hεdef
  have hεpos : 0 < ε := by rw [hεdef]; linarith
  filter_upwards [hgkey ε hεpos,
    hcorr.eventually (gt_mem_nhds (show (0:ℝ) < ε from hεpos))] with n h1 h2
  have h2' : (n : ℝ)⁻¹ * Real.log N < ε := by simpa using h2
  calc g n ≤ lami + ε / 2 + (1/2 : ℝ) * ((n : ℝ)⁻¹ * Real.log N) := h1
    _ ≤ y := by rw [hεdef] at *; nlinarith [h2']

omit [MeasurableSpace X] in
/-- **Singular-value square envelope.** If `(1/n) log σⱼ(n) → λⱼ` and each `σⱼ(n) > 0`, then
for every `δ > 0`, eventually `σⱼ(n)² ≤ exp(n(2λⱼ + δ))`. -/
theorem eventually_sq_singularValue_le_exp {A : X → Matrix (Fin d) (Fin d) ℝ} {x : X}
    (j : Fin (Fintype.card (Fin d)))
    (hσpos : ∀ n : ℕ, 1 ≤ n → 0 < (Matrix.toEuclideanLin (cocycle A T n x)).singularValues j)
    {lamj : ℝ}
    (hσ : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues j)) atTop (𝓝 lamj))
    (δ : ℝ) (hδ : 0 < δ) :
    ∀ᶠ n : ℕ in atTop,
      ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues j) ^ 2
        ≤ Real.exp ((n : ℝ) * (2 * lamj + δ)) := by
  have hev := hσ.eventually (gt_mem_nhds (show lamj < lamj + δ/2 by linarith))
  filter_upwards [hev, eventually_ge_atTop 1] with n hn hn1
  have hnpos : (0 : ℝ) < (n : ℝ) := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hn1
  set σ := (Matrix.toEuclideanLin (cocycle A T n x)).singularValues j with hσdef
  have hσp : 0 < σ := hσpos n hn1
  have hloglt : Real.log σ < (n : ℝ) * (lamj + δ/2) := by
    have hmul : (n : ℝ) * ((n : ℝ)⁻¹ * Real.log σ) < (n : ℝ) * (lamj + δ/2) :=
      mul_lt_mul_of_pos_left hn hnpos
    rwa [← mul_assoc, mul_inv_cancel₀ (ne_of_gt hnpos), one_mul] at hmul
  have hσsq : σ ^ 2 = Real.exp (2 * Real.log σ) := by
    rw [mul_comm, Real.exp_mul, Real.exp_log hσp]
    norm_num
  rw [hσsq]
  apply Real.exp_le_exp.mpr
  nlinarith [hloglt]

omit [MeasurableSpace X] in
/-- **Per-vector exact growth limit (from limsup ≤ λᵢ and λᵢ ≤ liminf).** -/
theorem tendsto_inv_mul_log_norm_cocycle_apply
    (A : X → Matrix (Fin d) (Fin d) ℝ) (x : X) (v : EuclideanSpace ℝ (Fin d)) (lami : ℝ)
    (hsup : limsup (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) atTop ≤ lami)
    (hinf : lami ≤ liminf (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) atTop)
    (hbddabove : IsBoundedUnder (· ≤ ·) atTop
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖))
    (hbddbelow : IsBoundedUnder (· ≥ ·) atTop
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖)) :
    Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ‖Matrix.toEuclideanLin (cocycle A T n x) v‖) atTop (𝓝 lami) :=
  tendsto_of_le_liminf_of_limsup_le hinf hsup hbddabove hbddbelow

end Upper

end ErgodicTheory
