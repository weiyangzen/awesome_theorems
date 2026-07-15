/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.ForwardGradedOverlapTopGap
import ErgodicTheory.Lyapunov.ChainRecursion
import ErgodicTheory.Lyapunov.OseledetsLimit.Limit

/-!
# The top-gap band-mass envelope `topGapMassEnvelope_ae`

This file assembles the deterministic and almost-everywhere statements behind the
top-gap fast-band-mass envelope used in the Oseledets multiplicative ergodic theorem.
The target theorem is

    theorem topGapMassEnvelope_ae : ∀ᵐ x ∂μ, TopGapMassEnvelope A T lam0 x.

The proof is organized in three layers.

* PART A (`ChainCore`) is pure real analysis: it solves the band-mass recursion and
  bounds the accumulated multi-source geometric leakage.  Its central statement,
  `multi_source_envelope`, converts the per-step multi-source recursion directly into
  an `m`-uniform per-stratum-rate sum.
* PART B is measure-free: the dynamical facts enter only through the plain predicates
  `Localized` and `Tempered`, so each sub-lemma is provable in isolation without any
  measure theory.
* PART C performs band stabilization, transfers the per-stratum bound to all
  gap-interior cuts, and wraps the result into the almost-everywhere statement.

## Main definitions

* `ErgodicTheory.Localized`, `ErgodicTheory.Tempered` — the per-orbit localization and temperedness
  predicates on the singular-value spectrum.
* `ErgodicTheory.stratumBand` — the spectral band associated with a stratum.
* `ErgodicTheory.canonSlack`, `ErgodicTheory.canonCut`, `ErgodicTheory.PerStratumEnvelope` —
  the canonical
  per-stratum slack and cut, and the inductively-built per-stratum band-mass envelope.

## Main results

* `ErgodicTheory.topGapMassEnvelope_ae` — the almost-everywhere top-gap band-mass envelope (the
  headline result of the module).
* `ErgodicTheory.topGapMassEnvelope_of_perStratum`, `ErgodicTheory.perStratumEnvelope_step` — the
  deterministic per-stratum envelope and the inductive step it is built from.

## Implementation notes

Fix the pair `(λ_a, v)`, the canonical slack `δ* = canonSlack = min(δ/4, G/2, (v−λ_a)/4)`,
the canonical cut `log c_v = v − δ*`, and `δ' = δ/4` for the induction hypothesis.  A single
slack `η ≤ min(δ, G)/16` simultaneously discharges all six constraints below (worst cases
shown; uses `w ≤ pred(v) ≤ v − G` for slow strata and `v − λ_a ≥ G`):

1. **ρ_w < 1** (geometric convergence): need `(v−δ*) − w − 2η > 0`; worst `w = v−G`
   gives `G − δ* − 2η ≥ G − G/2 − G/8 = 3G/8 > 0`.
2. **bottom-stratum slack** (`w ≤ λ_a`, mass ≤ 1): rate `(v−δ*) − w − 2η`
   `≥ (v−λ_a) − δ* − 2η`; need `δ* + 2η ≤ δ`; `δ/4 + δ/8 = 3δ/8 ≤ δ`.
3. **intermediate slack** (`λ_a < w < v`, IH mass): combined rate
   `v − λ_a − δ* − δ' − 2η`; need `δ* + δ' + 2η ≤ δ`; `δ/4 + δ/4 + δ/8 ≤ δ`.
4. **canonical-cut gap separation** (`mem_hiBand_iff_of_localized` at `γ = v − δ*`): slow
   side `η < (v−δ*) − λ_j ≥ G/2`; fast side (incl. `λ_j = v`) `η < δ* + (λ_j − v)`, worst
   `λ_j = v` gives `η < δ*`; both follow from `η ≤ min(δ,G)/16 < δ*`.
5. **intermediate sub-band inclusion** `stratumBand w ⊆ hiBand(m, canonCut_w)`: need
   `η < δ*_w = min(δ'/4, G/2, (w−λ_a)/4) ≥ min(δ/16, G/4)`; `η ≤ min(δ,G)/16`.  This is the
   binding constraint, which is why the slack is `min(δ,G)/16` rather than `min(δ/8, G/8)`.
6. **initialization `a_0 = 0`** (`canonCut_init_zero`): need `λ_a + η < v − δ*`, i.e.
   `η < (v−λ_a) − δ* ≥ G/2`.

Note `η < δ*` always holds: `δ* = min(δ/4, G/2, (v−λ_a)/4) ≥ min(δ/4, G/4)` (using
`v−λ_a ≥ G`), and `η ≤ min(δ,G)/16 < min(δ/4, G/4) ≤ δ*`.

Conventions: the cast `Fintype.card (Fin d) = d` is realized via
`⟨(a : ℕ), lt_of_lt_of_eq a.isLt (Fintype.card_fin d).symm⟩`; `hiBand` membership is
`σ_j(t)^{1/t} > c`; `bandProjector` cuts the exponential scale.

Key points to keep in mind:

1. The slack `δ*` is quantized against the minimal distinct-stratum gap `G`
   (`exists_distinctGap`), never against raw index-adjacent gaps.
2. The `qpow` scale `σ^{1/t}` and `σ^{1/(t+1)}` are never mixed; the conversion happens at
   each fixed time.
3. The cut stays strictly gap-interior.
4. All `Eventually` thresholds are collected once and threaded as a single `n₀`.
5. The envelope is two-time: a fixed `n` controls all `m ≥ n`.
6. The single slack is `η ≤ min(δ,G)/16`.
-/

open MeasureTheory Filter Topology Matrix
open scoped RealInnerProductSpace BigOperators Matrix.Norms.L2Operator

noncomputable section

namespace ErgodicTheory

/-! ## PART A — abstract deterministic chain core (measure-free, matrix-free)

These lemmas are pure real-analysis: they solve the band-mass recursion and bound the
accumulated multi-source geometric leakage.  No matrices, no measure, no
inner-product space.  They are the easiest sub-lemmas to prove in isolation and the
analytic crux of the whole argument. -/

namespace ChainCore

/-- **A1 — telescoping chain solver.**  If `a 0 = 0` and `a (k+1) ≤ a k + src k` for all
`k`, then `a k ≤ ∑_{i<k} src i` for every `k`.  (Elementary induction; we keep the raw
partial-sum form so the geometric bound can be applied separately.) -/
theorem chain_le_partial_sum (a src : ℕ → ℝ) (h0 : a 0 = 0)
    (hrec : ∀ k, a (k + 1) ≤ a k + src k) (k : ℕ) :
    a k ≤ ∑ i ∈ Finset.range k, src i := by
  induction k with
  | zero => simp [h0]
  | succ k ih =>
    refine (hrec k).trans ?_
    rw [Finset.sum_range_succ]
    linarith [ih]

/-- **A2 — tail geometric bound.**  For `0 ≤ r < 1` and `0 ≤ K`, the partial sums of the
geometric series `∑_{i<k} K·r^i` are bounded uniformly by `K/(1-r)`. -/
theorem geom_partial_sum_le {r K : ℝ} (hr0 : 0 ≤ r) (hr1 : r < 1) (hK : 0 ≤ K) (k : ℕ) :
    ∑ i ∈ Finset.range k, K * r ^ i ≤ K / (1 - r) := by
  have h1r : (0 : ℝ) < 1 - r := by linarith
  rw [← Finset.mul_sum]
  have hgeo : ∑ i ∈ Finset.range k, r ^ i ≤ (1 - r)⁻¹ := by
    have heq : ∑ i ∈ Finset.range k, r ^ i = (1 - r ^ k) / (1 - r) := by
      rw [geom_sum_eq (by linarith : r ≠ 1)]
      rw [div_eq_div_iff (by linarith : r - 1 ≠ 0) (by linarith : (1:ℝ) - r ≠ 0)]
      ring
    rw [heq, div_le_iff₀ h1r, inv_mul_cancel₀ (by linarith : (1:ℝ) - r ≠ 0)]
    nlinarith [pow_nonneg hr0 k]
  calc K * ∑ i ∈ Finset.range k, r ^ i ≤ K * (1 - r)⁻¹ := mul_le_mul_of_nonneg_left hgeo hK
    _ = K / (1 - r) := by rw [div_eq_mul_inv]

/-- **A4 — multi-source geometric envelope.**  PART B's recursion has the multi-source form
`a (k+1) ≤ a k + ∑_{w ∈ W} srcw w k` with finitely many strata `W`, each source geometric:
`srcw w k ≤ Mw w · (ρw w) ^ (n + k)` with `0 ≤ ρw w < 1`, `0 ≤ Mw w`.  Then, with
`a 0 = 0`, for all `k`,
`a k ≤ ∑_{w ∈ W} (Mw w / (1 - ρw w)) · (ρw w) ^ n`.

This is the central abstract statement: it converts the per-step multi-source recursion
into a single k-uniform bound whose RHS is a finite sum of per-stratum geometric envelopes,
each with its OWN rate.  Proof: A1 (with `src k = ∑_w srcw w k`), then `Finset.sum_comm` to
reorder `∑_{i<k} ∑_w` into `∑_w ∑_{i<k}`, then A2 per stratum. -/
theorem multi_source_envelope {W : Type*} (Wf : Finset W) (a : ℕ → ℝ) (srcw : W → ℕ → ℝ)
    (Mw ρw : W → ℝ) (n : ℕ)
    (hM : ∀ w ∈ Wf, 0 ≤ Mw w) (hρ0 : ∀ w ∈ Wf, 0 ≤ ρw w) (hρ1 : ∀ w ∈ Wf, ρw w < 1)
    (h0 : a 0 = 0)
    (hrec : ∀ k, a (k + 1) ≤ a k + ∑ w ∈ Wf, srcw w k)
    (hsrc : ∀ w ∈ Wf, ∀ k, srcw w k ≤ Mw w * (ρw w) ^ (n + k)) (k : ℕ) :
    a k ≤ ∑ w ∈ Wf, (Mw w / (1 - ρw w)) * (ρw w) ^ n := by
  -- a k ≤ ∑_{i<k} (∑_w srcw w i)  [A1]
  refine (chain_le_partial_sum a (fun i => ∑ w ∈ Wf, srcw w i) h0 hrec k).trans ?_
  -- reorder: ∑_{i<k} ∑_w = ∑_w ∑_{i<k}
  rw [Finset.sum_comm]
  -- bound each inner sum by the per-stratum envelope
  refine Finset.sum_le_sum (fun w hw => ?_)
  -- ∑_{i<k} srcw w i ≤ ∑_{i<k} Mw w · ρw w^(n+i) = ρw^n · ∑ Mw ρw^i ≤ (Mw/(1-ρw))·ρw^n
  have hstep1 : ∑ i ∈ Finset.range k, srcw w i
      ≤ ∑ i ∈ Finset.range k, Mw w * (ρw w) ^ (n + i) :=
    Finset.sum_le_sum (fun i _ => hsrc w hw i)
  refine hstep1.trans ?_
  have hfac : ∑ i ∈ Finset.range k, Mw w * (ρw w) ^ (n + i)
      = (ρw w) ^ n * ∑ i ∈ Finset.range k, Mw w * (ρw w) ^ i := by
    rw [Finset.mul_sum]
    refine Finset.sum_congr rfl (fun i _ => ?_)
    rw [pow_add]; ring
  rw [hfac]
  have hgeo := geom_partial_sum_le (hρ0 w hw) (hρ1 w hw) (hM w hw) k
  calc (ρw w) ^ n * ∑ i ∈ Finset.range k, Mw w * (ρw w) ^ i
      ≤ (ρw w) ^ n * (Mw w / (1 - ρw w)) :=
        mul_le_mul_of_nonneg_left hgeo (pow_nonneg (hρ0 w hw) n)
    _ = (Mw w / (1 - ρw w)) * (ρw w) ^ n := by ring

end ChainCore

/-! ## PART B — deterministic SVD layer at a fixed `x`

Everything here is at a FIXED point `x` on an eventual time window.  The dynamical
localization/tempering facts are TAKEN AS PLAIN HYPOTHESES (no measure theory), so each
sub-lemma is independently provable.  We build:
* the per-stratum sub-band finsets `stratumBand`;
* the sub-band mass comparison (`subband_mass_le_bandMass`);
* the multi-source one-step recursion (`bandMass_oneStep_multisource`);
* the per-stratum envelope `detPerStratumEnvelope`, by strong induction over distinct
  stratum values, consuming PART A.

### Notation / windows packaged as hypotheses

For a fixed `x`, set `σ_j(t) = (toEuclideanLin (cocycle A T t x)).singularValues j`.
We work with the abstract *localization predicate*

  `Localized A T x lam0 η N : ∀ t ≥ N, ∀ j < d, exp(λ_j − η) < σ_j(t)^{1/t} < exp(λ_j + η)`

and the *tempering predicate*

  `Tempered A T x η N : ∀ t ≥ N, ‖A(T^[t] x)‖ ≤ exp(t·η)`

both produced (a.e.) in PART C from `eventually_qpow_eigenvalue_localized` and
`tendsto_logNorm_orbit_div_atTop_zero`. -/

variable {X : Type*} [MeasurableSpace X] {μ : MeasureTheory.Measure X} {d : ℕ} {T : X → X}

/-- Localization window predicate (the σ-localization fact, abstracted as a hypothesis). -/
def Localized [NeZero d] (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X)
    (lam0 : ℕ → ℝ) (η : ℝ) (N : ℕ) : Prop :=
  ∀ t : ℕ, N ≤ t → ∀ j : ℕ, (hj : j < d) →
    Real.exp (lam0 j - η)
        < (Matrix.toEuclideanLin (cocycle A T t x)).singularValues j ^ ((t : ℝ)⁻¹)
      ∧ (Matrix.toEuclideanLin (cocycle A T t x)).singularValues j ^ ((t : ℝ)⁻¹)
        < Real.exp (lam0 j + η)

/-- Tempering window predicate (the one-step operator factor, abstracted as a hypothesis). -/
def Tempered (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X) (η : ℝ) (N : ℕ) : Prop :=
  ∀ t : ℕ, N ≤ t → ‖A (T^[t] x)‖ ≤ Real.exp ((t : ℝ) * η)

/-- **B0a — localization is producible.**  From the σ-convergence at `x` we get, for each `η > 0`,
a localization threshold `N`.  (Thin wrapper around `eventually_qpow_eigenvalue_localized`.) -/
theorem exists_localized [NeZero d] {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0)
    (x : X) (lam0 : ℕ → ℝ)
    (hconv : ∀ j : ℕ, j < d → Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues j))
      Filter.atTop (𝓝 (lam0 j)))
    {η : ℝ} (hη : 0 < η) :
    ∃ N : ℕ, Localized A T x lam0 η N := by
  -- The eventual σ-localization fact has a body that is exactly `Localized`'s window.
  obtain ⟨N, hN⟩ :=
    Filter.eventually_atTop.mp (eventually_qpow_eigenvalue_localized hA x lam0 hconv hη)
  exact ⟨N, fun t ht j hj => hN t ht j hj⟩

omit [MeasurableSpace X] in
/-- **B0b — tempering is producible.**  From `(1/t)·log‖A(T^[t]x)‖ → 0` at `x` we get, for each
`η > 0`, a tempering threshold `N`.  (`Tendsto.eventually` of `· < η` then exp-monotone; the `t = 0`
slot is harmless because the window only constrains `t ≥ N` and we can take `N ≥ 1`.) -/
theorem exists_tempered {A : X → Matrix (Fin d) (Fin d) ℝ} (x : X)
    (htemp : Filter.Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖A (T^[n] x)‖)
      Filter.atTop (𝓝 0))
    {η : ℝ} (hη : 0 < η) :
    ∃ N : ℕ, Tempered A T x η N := by
  -- Eventually `(1/t)·log‖A(T^[t]x)‖ < η`, combined with `t ≥ 1`.
  have hev : ∀ᶠ t : ℕ in Filter.atTop,
      (t : ℝ)⁻¹ * Real.log ‖A (T^[t] x)‖ < η ∧ 1 ≤ t := by
    have habs := htemp.eventually (eventually_abs_sub_lt (0 : ℝ) hη)
    filter_upwards [habs, Filter.eventually_ge_atTop 1] with t ht ht1
    rw [abs_sub_lt_iff] at ht
    exact ⟨by simpa using ht.1, ht1⟩
  obtain ⟨N, hN⟩ := Filter.eventually_atTop.mp hev
  refine ⟨N, fun t ht => ?_⟩
  obtain ⟨hlt, ht1⟩ := hN t ht
  -- For `t ≥ 1`, `(t:ℝ) > 0`.
  have htpos : (0 : ℝ) < (t : ℝ) := by
    have : (1 : ℝ) ≤ (t : ℝ) := by exact_mod_cast ht1
    linarith
  -- Multiply `(1/t)·log‖A‖ < η` by `t > 0` to get `log‖A‖ < t·η`.
  have hlog : Real.log ‖A (T^[t] x)‖ < (t : ℝ) * η := by
    have hmul := mul_lt_mul_of_pos_left hlt htpos
    rw [← mul_assoc, mul_inv_cancel₀ (ne_of_gt htpos), one_mul] at hmul
    exact hmul
  -- Then `‖A‖ ≤ exp(t·η)`.  Split on whether the norm is positive.
  rcases le_or_gt ‖A (T^[t] x)‖ 0 with hle0 | hpos
  · -- `‖A‖ ≤ 0 ≤ exp(t·η)`.
    exact hle0.trans (Real.exp_pos _).le
  · -- `‖A‖ > 0`: rewrite via `Real.exp_log` and exp-monotonicity.
    have : ‖A (T^[t] x)‖ < Real.exp ((t : ℝ) * η) := by
      rw [← Real.exp_log hpos]
      exact Real.exp_lt_exp.mpr hlog
    exact le_of_lt this

/-! ### Per-stratum sub-bands -/

/-- The time-`m` sub-band of stratum value `v`: indices `j` whose Lyapunov value `lam0 j` equals
`v`.  This is a time-independent finset (it depends only on `lam0`), but we keep `m` for symmetry
with `hiBand`; the localization hypothesis is what ties it to the actual time-`m` band. -/
def stratumBand [NeZero d] (lam0 : ℕ → ℝ) (v : ℝ) :
    Finset (Fin (Fintype.card (Fin d))) :=
  Finset.univ.filter (fun j : Fin (Fintype.card (Fin d)) => lam0 (j : ℕ) = v)

/-! ### Sub-band mass and its comparison to a band-projector mass

`subBandMass S m B u := ‖S.fastProj m B u‖`, the projection of `u` onto the sub-band `B` at time
`m`.  When `B ⊆ hiBand A T m x c` the sub-band sits inside the fast band of cut `c`, so its mass is
dominated by the full band mass (Pythagoras over an index subset). -/

/-- **B1 — sub-band mass ≤ band mass (Pythagoras over index subsets).**  If `B ⊆ hiBand A T m x c`
then the projection of `u` onto `B` is dominated by the cut-`c` band projector mass. -/
theorem subband_mass_le_bandMass [NeZero d] (A : X → Matrix (Fin d) (Fin d) ℝ) (m : ℕ) (x : X)
    (c : ℝ) (B : Finset (Fin (Fintype.card (Fin d))))
    (hB : B ⊆ hiBand A T m x c) (u : EuclideanSpace ℝ (Fin d)) :
    ‖(chainSVD A T x).fastProj m B u‖
      ≤ ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c) 1) m x) u‖ := by
  classical
  rw [toEuclideanLin_bandProjector_eq_fastProj]
  set S := chainSVD A T x with hS
  have h0 : ‖S.fastProj m B u‖ ^ 2 = ∑ j ∈ B, ⟪S.e m j, u⟫ ^ 2 :=
    S.normSq_fastProj m _ u
  have h1 : ‖S.fastProj m (hiBand A T m x c) u‖ ^ 2
      = ∑ j ∈ hiBand A T m x c, ⟪S.e m j, u⟫ ^ 2 := S.normSq_fastProj m _ u
  have hle : ∑ j ∈ B, ⟪S.e m j, u⟫ ^ 2
      ≤ ∑ j ∈ hiBand A T m x c, ⟪S.e m j, u⟫ ^ 2 := by
    apply Finset.sum_le_sum_of_subset_of_nonneg hB
    intro j _ _; positivity
  have hsq : ‖S.fastProj m B u‖ ^ 2 ≤ ‖S.fastProj m (hiBand A T m x c) u‖ ^ 2 := by
    rw [h0, h1]; exact hle
  nlinarith [norm_nonneg (S.fastProj m B u),
    norm_nonneg (S.fastProj m (hiBand A T m x c) u), hsq]

/-! ### The slow band partitions into per-stratum sub-bands

Under localization with `η` small relative to the distinct-stratum gap `G`, and a cut `c` whose
`log c` is STRICTLY between consecutive strata, `(hiBand A T m x c)ᶜ` is the disjoint union of the
`stratumBand`s of distinct stratum values `w` with `w < log c`.  We package the per-step
slow-cap-and-floor data this needs into one combinatorial lemma. -/

/-- **B2 — slow-band stratum decomposition.**  Under localization at time `t` with `η`, if `log c`
avoids every stratum then the complement of `hiBand A T t x c` is `{j : lam0 j < log c}` (membership
characterization).  Stated as the membership equivalence at a single time `t` past the localization
threshold, with `c = exp γ`, `γ` strictly gap-separated from every stratum by more than `η`. -/
theorem mem_hiBand_iff_of_localized [NeZero d] {A : X → Matrix (Fin d) (Fin d) ℝ}
    (_hA : ∀ x, (A x).det ≠ 0) (x : X) (lam0 : ℕ → ℝ) {η : ℝ} (hη : 0 < η) {N : ℕ}
    (hloc : Localized A T x lam0 η N) {γ : ℝ}
    (hgapsep : ∀ j : ℕ, j < d → lam0 j + η < γ ∨ γ < lam0 j - η)
    {t : ℕ} (ht : N ≤ t) (_ht1 : 1 ≤ t) (j : Fin (Fintype.card (Fin d))) :
    j ∈ hiBand A T t x (Real.exp γ) ↔ γ < lam0 (j : ℕ) := by
  -- The index `(j : ℕ)` is `< d`.
  have hjd : (j : ℕ) < d := lt_of_lt_of_eq j.isLt (Fintype.card_fin d)
  -- Membership in `hiBand` at cut `exp γ` rewrites to a comparison with `σ_j(t)^{1/t}`.
  rw [hiBand, Finset.mem_filter]
  rw [qpow_eigenvalue_eq_rpow]
  -- Localization brackets `σ_j(t)^{1/t}` between `exp(λ_j ± η)`.
  obtain ⟨hlo, hhi⟩ := hloc t ht (j : ℕ) hjd
  simp only [Finset.mem_univ, true_and]
  constructor
  · -- `exp γ < σ^{1/t} ⟹ γ < λ_j`.
    intro hgt
    rcases hgapsep (j : ℕ) hjd with hsep | hsep
    · -- `λ_j + η < γ`: then `exp γ < σ^{1/t} < exp(λ_j+η) < exp γ`, contradiction.
      exfalso
      have : Real.exp γ < Real.exp (lam0 (j : ℕ) + η) := lt_trans hgt hhi
      have hcontra : γ < lam0 (j : ℕ) + η := Real.exp_lt_exp.mp this
      linarith
    · -- `γ < λ_j - η < λ_j`.
      linarith
  · -- `γ < λ_j ⟹ exp γ < σ^{1/t}`.
    intro hlt
    rcases hgapsep (j : ℕ) hjd with hsep | hsep
    · -- `λ_j + η < γ` contradicts `γ < λ_j` (since `η > 0`).
      linarith
    · -- `γ < λ_j - η`: then `exp γ < exp(λ_j-η) < σ^{1/t}`.
      have : Real.exp γ < Real.exp (lam0 (j : ℕ) - η) := Real.exp_lt_exp.mpr hsep
      exact lt_trans this hlo

/-! ### Per-stratum sub-band caps from localization

The slow sub-band `stratumBand lam0 w` of stratum value `w` has every singular value capped at time
`t` by `σ_j(t) ≤ exp(t(w+η))` (from `σ_j(t)^{1/t} < exp(λ_j+η) = exp(w+η)` and
`rpow_inv_le_iff_le_pow`).  The fast floor at `t+1` for the cut `c = exp γ` is `c^{t+1}`. -/

omit [MeasurableSpace X] in
/-- **B3 — per-stratum slow cap.**  Under localization, every index in `stratumBand lam0 w` has, at
time `t ≥ N`, `σ_j(t) ≤ exp(t(w+η))`. -/
theorem stratum_sigma_cap [NeZero d] {A : X → Matrix (Fin d) (Fin d) ℝ} (_hA : ∀ x, (A x).det ≠ 0)
    (x : X) (lam0 : ℕ → ℝ) {η : ℝ} (_hη : 0 < η) {N : ℕ} (hloc : Localized A T x lam0 η N)
    {w : ℝ} {t : ℕ} (ht : N ≤ t) (ht1 : 1 ≤ t)
    (j : Fin (Fintype.card (Fin d))) (hj : j ∈ stratumBand lam0 w) :
    (Matrix.toEuclideanLin (cocycle A T t x)).singularValues j
      ≤ Real.exp ((t : ℝ) * (w + η)) := by
  -- `hj` unfolds to `lam0 (j : ℕ) = w`.
  simp only [stratumBand, Finset.mem_filter, Finset.mem_univ, true_and] at hj
  -- The natural-number index `(j : ℕ)` is `< d`.
  have hjd : (j : ℕ) < d := lt_of_lt_of_eq j.isLt (Fintype.card_fin d)
  -- Localization at time `t` for index `(j : ℕ)`: the upper bound `σ^{1/t} < exp(lam0 j + η)`.
  have hupper := (hloc t ht (j : ℕ) hjd).2
  -- Rewrite `lam0 (j : ℕ) = w`.
  rw [hj] at hupper
  -- Nonnegativity of the singular value, positivity of the cap.
  have hσnn : 0 ≤ (Matrix.toEuclideanLin (cocycle A T t x)).singularValues j :=
    (Matrix.toEuclideanLin (cocycle A T t x)).singularValues_nonneg j
  have hexp_pos : (0 : ℝ) < Real.exp (w + η) := Real.exp_pos _
  -- From the strict `<` get `≤`, then transport across the `rpow_inv_le_iff_le_pow` iff.
  have hpow : (Matrix.toEuclideanLin (cocycle A T t x)).singularValues j
      ≤ Real.exp (w + η) ^ t :=
    (rpow_inv_le_iff_le_pow hσnn hexp_pos ht1).mp (le_of_lt hupper)
  -- Convert `exp(w+η)^t = exp(t·(w+η))`.
  rwa [← Real.exp_nat_mul] at hpow

/-! ### The multi-source one-step recursion

This refines the single-cap `bandMass_oneStep_recursion`.  Instead of bounding the slow-projection
norm `‖slowProj_t u‖` by a single cap, we split the slow band into per-stratum sub-bands and bound
the leakage source as a sum over strata, each with its own sub-band mass and its own σ-cap.  We use
the triangle-inequality route: write `slowProj_t u = ∑_w fastProj_t (B_w) u` over the partition
`{B_w}` of `(hiBand)ᶜ`, so that the operator step bound distributes; each sub-band term is bounded
via `oneStep_sandwich` applied to that sub-band's span (each `fastProj_t (B_w) u` lies in the span
of `e_t` over `B_w ⊆ (hiBand)ᶜ`). -/

/-! ### Private SVDData-level helpers for the multi-source recursion (prefix `htgmulti_`) -/

open ErgodicTheory.RuelleCofactor in
/-- `fastProj t B u` lies in the span of `e t j`, `j ∈ B` (mirror of `slowProj_mem_span`). -/
private lemma htgmulti_fastProj_mem_span {E : Type*} [NormedAddCommGroup E]
    [InnerProductSpace ℝ E] {D : ℕ} (S : ErgodicTheory.RuelleCofactor.SVDData E D) (t : ℕ)
    (B : Finset (Fin D))
    (u : E) :
    S.fastProj t B u
      ∈ Submodule.span ℝ (Set.range (fun j : (B : Finset (Fin D)) => S.e t (j : Fin D))) := by
  classical
  rw [ErgodicTheory.RuelleCofactor.SVDData.fastProj]
  apply Submodule.sum_mem
  intro j hj
  apply Submodule.smul_mem
  apply Submodule.subset_span
  exact ⟨⟨j, hj⟩, rfl⟩

open ErgodicTheory.RuelleCofactor in
/-- `fastProj t hi` distributes over a finite sum (folded from binary `fastProj_add`). -/
private lemma htgmulti_fastProj_sum {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {D : ℕ} (S : ErgodicTheory.RuelleCofactor.SVDData E D) (t : ℕ) (hi : Finset (Fin D)) {W : Type*}
    (Wf : Finset W) (f : W → E) :
    S.fastProj t hi (∑ w ∈ Wf, f w) = ∑ w ∈ Wf, S.fastProj t hi (f w) := by
  classical
  induction Wf using Finset.induction with
  | empty => simp [ErgodicTheory.RuelleCofactor.SVDData.fastProj]
  | insert w Wf hw ih =>
    rw [Finset.sum_insert hw, Finset.sum_insert hw, S.fastProj_add, ih]

open ErgodicTheory.RuelleCofactor in
/-- The slow projection at time `t` decomposes over a disjoint cover of the slow indices `hiᶜ`. -/
private lemma htgmulti_slowProj_eq_sum {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E]
    {D : ℕ} (S : ErgodicTheory.RuelleCofactor.SVDData E D) (t : ℕ) (hiT : Finset (Fin D))
    {W : Type*}
    (Wf : Finset W) (Bw : W → Finset (Fin D)) (hcover : hiTᶜ = Wf.biUnion Bw)
    (hdisj : (Wf : Set W).PairwiseDisjoint Bw) (u : E) :
    S.slowProj t hiT u = ∑ w ∈ Wf, S.fastProj t (Bw w) u := by
  classical
  rw [ErgodicTheory.RuelleCofactor.SVDData.slowProj, hcover, Finset.sum_biUnion hdisj]
  refine Finset.sum_congr rfl (fun w _ => ?_)
  rw [ErgodicTheory.RuelleCofactor.SVDData.fastProj]

open ErgodicTheory.RuelleCofactor in
/-- The SVDData-level multi-source one-step recursion.  Generalizes
`ErgodicTheory.RuelleCofactor.SVDData.oneStep_recursion` to a disjoint sub-partition
`{Bw w : w ∈ Wf}`
of the slow indices `hiTᶜ`: the fast band mass at `t+1` is bounded by the fast band mass at `t` plus
a sum of
per-sub-band leakage sources, each with its own cap `sval w`. -/
private lemma htgmulti_oneStep_recursion_multiSource {E : Type*} [NormedAddCommGroup E]
    [InnerProductSpace ℝ E] {D : ℕ} (S : ErgodicTheory.RuelleCofactor.SVDData E D) (t : ℕ)
    (hiT hiT1 : Finset (Fin D))
    {W : Type*} (Wf : Finset W) (Bw : W → Finset (Fin D)) (sval : W → ℝ) (b tt : ℝ)
    (hsval : ∀ w ∈ Wf, 0 ≤ sval w) (htt : 0 < tt) (hb : 0 ≤ b)
    (hcover : hiTᶜ = Wf.biUnion Bw) (hdisj : (Wf : Set W).PairwiseDisjoint Bw)
    (hcap : ∀ w ∈ Wf, ∀ j ∈ Bw w, S.σ t j ≤ sval w)
    (hfloor : ∀ j ∈ hiT1, tt ≤ S.σ (t + 1) j) (u : E)
    (hstep : ∀ w ∈ Wf,
      ‖S.apply (t + 1) (S.fastProj t (Bw w) u)‖ ≤ b * ‖S.apply t (S.fastProj t (Bw w) u)‖) :
    ‖S.fastProj (t + 1) hiT1 u‖
      ≤ ‖S.fastProj t hiT u‖
        + ∑ w ∈ Wf, (b * sval w / tt) * ‖S.fastProj t (Bw w) u‖ := by
  classical
  -- (a) u = fast_t + slow_t ; (b) slow_t = ∑_w fastProj t (Bw w) u.
  have hdecomp : u = S.fastProj t hiT u + ∑ w ∈ Wf, S.fastProj t (Bw w) u := by
    rw [← htgmulti_slowProj_eq_sum S t hiT Wf Bw hcover hdisj u]
    exact (S.fastProj_add_slowProj t hiT u).symm
  -- (c) split fastProj (t+1) hiT1 over the decomposition.
  have hsplit : S.fastProj (t + 1) hiT1 u
      = S.fastProj (t + 1) hiT1 (S.fastProj t hiT u)
        + ∑ w ∈ Wf, S.fastProj (t + 1) hiT1 (S.fastProj t (Bw w) u) := by
    conv_lhs => rw [hdecomp]
    rw [S.fastProj_add, htgmulti_fastProj_sum S (t + 1) hiT1 Wf
      (fun w => S.fastProj t (Bw w) u)]
  rw [hsplit]
  refine (norm_add_le _ _).trans ?_
  gcongr
  · -- the fast-at-`t` term: contractive.
    exact S.norm_fastProj_le (t + 1) hiT1 (S.fastProj t hiT u)
  · -- the per-sub-band sum: triangle inequality then per-term sandwich.
    refine (norm_sum_le _ _).trans ?_
    refine Finset.sum_le_sum (fun w hw => ?_)
    -- each term: ‖fastProj (t+1) hiT1 (fastProj t (Bw w) u)‖ ≤ (b·sval w/tt)·‖fastProj t (Bw w) u‖.
    have hsand : tt * ‖S.fastProj (t + 1) hiT1 (S.fastProj t (Bw w) u)‖
        ≤ b * sval w * ‖S.fastProj t (Bw w) u‖ :=
      S.oneStep_sandwich t (Bw w) hiT1 (sval w) tt b (hsval w hw) htt.le hb
        (fun j hj => hcap w hw j hj) hfloor (S.fastProj t (Bw w) u)
        (htgmulti_fastProj_mem_span S t (Bw w) u) (hstep w hw)
    rw [div_mul_eq_mul_div, le_div_iff₀ htt]
    calc ‖S.fastProj (t + 1) hiT1 (S.fastProj t (Bw w) u)‖ * tt
        = tt * ‖S.fastProj (t + 1) hiT1 (S.fastProj t (Bw w) u)‖ := by ring
      _ ≤ b * sval w * ‖S.fastProj t (Bw w) u‖ := hsand

/-- **B4 — multi-source one-step band-mass recursion.**  Fix a cut `c = exp γ > 0` and a finite set
of distinct stratum values `Wf` whose sub-bands `{stratumBand lam0 w : w ∈ Wf}` partition the slow
band `(hiBand A T t x c)ᶜ` at time `t` (hypothesis `hpart`).  With per-stratum slow caps
`sw : ℝ` (`σ_j(t) ≤ sw w` for `j ∈ stratumBand lam0 w`), the fast floor `c^{t+1}`, and the tempered
step factor `b = ‖A(T^[t]x)‖`, the band mass satisfies

  `‖P^{>c}_{t+1} u‖ ≤ ‖P^{>c}_t u‖`
  `  + ∑_{w∈Wf} (b·(sw w)/c^{t+1}) · ‖fastProj_t (stratumBand lam0 w) u‖`.

Route: `bandMass_oneStep_recursion` reduces `P^{>c}_{t+1}` to `P^{>c}_t + (b·s/c^{t+1})·‖slowProj‖`
with a single cap; here we instead expand `slowProj` over the partition and apply the SVD sandwich
per sub-band (each sub-band is a slow span), summing.  The cleanest formalization re-runs the
`oneStep_recursion` derivation once per sub-band against `hiT1 = hiBand (t+1)` and uses additivity
of `fastProj (t+1)` over the partition pieces. -/
theorem bandMass_oneStep_multisource [NeZero d] {W : Type*} (A : X → Matrix (Fin d) (Fin d) ℝ)
    {c₀ : ℝ} (hc₀ : 0 < c₀) {t : ℕ} (x : X) (Wf : Finset W) (sval : W → ℝ)
    (hsval : ∀ w ∈ Wf, 0 ≤ sval w) (Bw : W → Finset (Fin (Fintype.card (Fin d))))
    (hcap : ∀ w ∈ Wf, ∀ j ∈ Bw w,
      (Matrix.toEuclideanLin (cocycle A T t x)).singularValues j ≤ sval w)
    (hpart : (hiBand A T t x c₀)ᶜ = Wf.biUnion Bw)
    (hdisj : (Wf : Set W).PairwiseDisjoint Bw)
    (u : EuclideanSpace ℝ (Fin d)) :
    ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c₀) 1) (t + 1) x) u‖
      ≤ ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c₀) 1) t x) u‖
        + ∑ w ∈ Wf, (‖A (T^[t] x)‖ * sval w / c₀ ^ (t + 1))
            * ‖(chainSVD A T x).fastProj t (Bw w) u‖ := by
  classical
  -- Wire the SVDData-level multi-source recursion to the cocycle band level.
  set S := chainSVD A T x with hS
  have hrec := htgmulti_oneStep_recursion_multiSource S t (hiBand A T t x c₀)
    (hiBand A T (t + 1) x c₀) Wf Bw sval (‖A (T^[t] x)‖) (c₀ ^ (t + 1))
    hsval (by positivity) (norm_nonneg _) hpart hdisj
    (by intro w hw j hj; simpa [hS, chainSVD_σ] using hcap w hw j hj)
    (by intro j hj; simpa [hS, chainSVD_σ] using fast_sigma_floor A hc₀ x j hj)
    u
    (by
      -- per-sub-band step bound: the operator factor is the same ‖A(T^[t]x)‖ regardless of vector.
      intro w hw
      simpa [hS, chainSVD_apply] using
        chain_oneStep_opNorm A t x (S.fastProj t (Bw w) u))
  rw [toEuclideanLin_bandProjector_eq_fastProj, toEuclideanLin_bandProjector_eq_fastProj]
  exact hrec

/-! ## PART B (continued) — the per-stratum envelope by strong induction

### The conclusion shape

`PerStratumEnvelope A T lam0 x a v` says: for every `δ > 0` there is `C ≥ 1` such that
eventually in `n`, for all `m ≥ n`, the time-`m` mass of the time-`n` slow eigenvector `u_a(n)` at
the *canonical* δ-dependent cut for the pair `(lam0 a, v)` decays like `exp(−n(v − lam0 a − δ))`.

The cut is not a free parameter inside the predicate; it is the canonical cut
`canonCut a v δ = exp(v − δ*)` with `δ* = min(δ/4, G/2, (v − lam0 a)/4)`.  Running the recursion at
this δ-dependent cut is what makes the induction close.  We carry the distinct-stratum gap
`G = distinctGap lam0` as a parameter. -/

/-- **B-gap — existence of a positive distinct-stratum gap.**  The slacks are quantized against this
gap, never against raw index-adjacent gaps.  There is `G > 0` below every gap between distinct
stratum values: `lam0 i < lam0 j ⟹ lam0 i + G ≤ lam0 j`.  (The min over the finitely many positive
differences `lam0 j − lam0 i` is positive; if there is at most one distinct stratum the statement is
vacuous and any `G = 1` works.)  Kept as a producer so `G` stays an abstract parameter elsewhere. -/
theorem exists_distinctGap [NeZero d] (lam0 : ℕ → ℝ) :
    ∃ G : ℝ, 0 < G ∧ ∀ i j : Fin d,
      lam0 (i : ℕ) < lam0 (j : ℕ) → lam0 (i : ℕ) + G ≤ lam0 (j : ℕ) := by
  classical
  -- the finset of "gap pairs" `(i, j)` with `lam0 i < lam0 j`
  set D : Finset (Fin d × Fin d) :=
    (Finset.univ : Finset (Fin d × Fin d)).filter
      (fun p => lam0 (p.1 : ℕ) < lam0 (p.2 : ℕ)) with hD
  -- the image of D under the (positive) difference map
  set diffs : Finset ℝ := D.image (fun p => lam0 (p.2 : ℕ) - lam0 (p.1 : ℕ)) with hdiffs
  by_cases hne : diffs.Nonempty
  · -- there is at least one gap pair: take G = min of the (all-positive) differences
    refine ⟨diffs.min' hne, ?_, ?_⟩
    · -- the minimum is positive because every element of `diffs` is positive
      rw [Finset.lt_min'_iff]
      intro y hy
      rw [hdiffs, Finset.mem_image] at hy
      obtain ⟨p, hp, hpeq⟩ := hy
      rw [hD, Finset.mem_filter] at hp
      rw [← hpeq]
      linarith [hp.2]
    · -- the bound: for any gap pair (i,j) its difference is in `diffs`, so `min' ≤ difference`
      intro i j hij
      have hmem : lam0 (j : ℕ) - lam0 (i : ℕ) ∈ diffs := by
        rw [hdiffs, Finset.mem_image]
        exact ⟨(i, j), by rw [hD, Finset.mem_filter]; exact ⟨Finset.mem_univ _, hij⟩, rfl⟩
      have := diffs.min'_le _ hmem
      linarith
  · -- no gap pair: the statement is vacuous, take G = 1
    refine ⟨1, one_pos, ?_⟩
    intro i j hij
    -- (i,j) would be a gap pair, contradicting emptiness of `diffs`
    exfalso
    apply hne
    refine ⟨lam0 (j : ℕ) - lam0 (i : ℕ), ?_⟩
    rw [hdiffs, Finset.mem_image]
    exact ⟨(i, j), by rw [hD, Finset.mem_filter]; exact ⟨Finset.mem_univ _, hij⟩, rfl⟩

/-- The canonical δ-dependent slack `δ*` for the pair `(lam0 a, v)`: strictly positive,
≤ δ/4, ≤ G/2, ≤ (v − lam0 a)/4. -/
def canonSlack (lam0 : ℕ → ℝ) (a : ℕ) (v G δ : ℝ) : ℝ :=
  min (min (δ / 4) (G / 2)) ((v - lam0 a) / 4)

/-- The canonical cut for the pair `(lam0 a, v)` at slack `δ`: `exp(v − δ*)`, strictly interior to
the gap below `v` (since `δ* ≤ G/2 < G` and the predecessor stratum is `≤ v − G`). -/
def canonCut (lam0 : ℕ → ℝ) (a : ℕ) (v G δ : ℝ) : ℝ :=
  Real.exp (v - canonSlack lam0 a v G δ)

/-- **The per-stratum envelope (conclusion shape).**  For index `a` and distinct stratum value
`v > lam0 a`: for every `δ > 0` there is `C ≥ 1` with eventually-in-`n`, for-all-`m ≥ n`, the
canonical-cut band mass `≤ C·exp(−n(v − lam0 a − δ))`. -/
def PerStratumEnvelope [NeZero d] (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (lam0 : ℕ → ℝ)
    (x : X) (G : ℝ) (a : Fin d) (v : ℝ) : Prop :=
  ∀ δ : ℝ, 0 < δ → ∃ C : ℝ, 1 ≤ C ∧ ∀ᶠ n : ℕ in Filter.atTop, ∀ m : ℕ, n ≤ m →
    ‖Matrix.toEuclideanLin
        (bandProjector A T (Set.indicator (Set.Ioi (canonCut lam0 (a : ℕ) v G δ)) 1) m x)
        (sortedGramEigenbasis A T n x
          ⟨(a : ℕ), lt_of_lt_of_eq a.isLt (Fintype.card_fin d).symm⟩)‖
      ≤ C * Real.exp (-(n : ℝ) * (v - lam0 (a : ℕ) - δ))

/-! ### Initialization (`a_0 = 0`) at the canonical cut

At time `n` past localization with `η` small, `σ_a(n)^{1/n} < exp(lam0 a + η) < canonCut a v G δ`
(because `log(canonCut) = v − δ* > lam0 a + η` for `η` small), so `a ∉ hiBand(n, canonCut)` and
`bandMass_init_zero` gives `a_0 = 0`. -/

/-- **B5 — initialization.**  Under localization with `η` small relative to `v − lam0 a − δ*`, the
index `a` is below the canonical cut at time `n`, so the band projector annihilates `u_a(n)`. -/
theorem canonCut_init_zero [NeZero d] {A : X → Matrix (Fin d) (Fin d) ℝ}
    (_hA : ∀ x, (A x).det ≠ 0) (x : X) (lam0 : ℕ → ℝ) (a : Fin d) {v G δ η : ℝ} {N n : ℕ}
    (hloc : Localized A T x lam0 η N) (hn : N ≤ n) (_hn1 : 1 ≤ n)
    (_hav : lam0 (a : ℕ) < v) (_hη : 0 < η)
    (hηsmall : lam0 (a : ℕ) + η < v - canonSlack lam0 (a : ℕ) v G δ) :
    Matrix.toEuclideanLin
        (bandProjector A T (Set.indicator (Set.Ioi (canonCut lam0 (a : ℕ) v G δ)) 1) n x)
        (sortedGramEigenbasis A T n x
          ⟨(a : ℕ), lt_of_lt_of_eq a.isLt (Fintype.card_fin d).symm⟩) = 0 := by
  -- The constructed `Fin (Fintype.card (Fin d))` index whose ℕ-coercion is `(a : ℕ)`.
  set j : Fin (Fintype.card (Fin d)) :=
    ⟨(a : ℕ), lt_of_lt_of_eq a.isLt (Fintype.card_fin d).symm⟩ with hj
  -- Reduce to: `j ∉ hiBand A T n x (canonCut …)`.
  apply bandMass_init_zero A n x (canonCut lam0 (a : ℕ) v G δ)
  -- `hiBand` membership unfolds to `canonCut < eigenvalues₀ j` = `canonCut < σ_a(n)^{1/n}`.
  rw [hiBand, Finset.mem_filter]
  rw [qpow_eigenvalue_eq_rpow]
  rintro ⟨-, hmem⟩
  -- `hmem : canonCut < σ_a(n)^{1/n}` (note `(j : ℕ) = (a : ℕ)` definitionally).
  -- From localization: `σ_a(n)^{1/n} < exp(lam0 a + η)`.
  have hupper := (hloc n hn (a : ℕ) a.isLt).2
  -- From `hηsmall`: `exp(lam0 a + η) < canonCut`.
  have hcanon : Real.exp (lam0 (a : ℕ) + η) < canonCut lam0 (a : ℕ) v G δ := by
    rw [canonCut]
    exact Real.exp_lt_exp.mpr hηsmall
  -- Chain: canonCut < σ^{1/n} < exp(lam0 a + η) < canonCut, contradiction.
  exact absurd (hmem.trans (hupper.trans hcanon)) (lt_irrefl _)

/-! ### The inductive step

The heart of PART B.  Given the localization/tempering windows and the inductive hypothesis — the
per-stratum envelope `PerStratumEnvelope … a w` for every distinct stratum value `w` with
`lam0 a < w < v` — produce `PerStratumEnvelope … a v`.

Mechanism:
* Run the recursion at `c = canonCut a v G δ = exp(v − δ*)`, `δ* = canonSlack`.
* The slow band of `c` at time `m` is (by `mem_hiBand_iff_of_localized`) exactly the disjoint union
  of `stratumBand lam0 w` over distinct strata `w < v − δ*`, i.e. all distinct `w ≤ pred(v) < v`.
* Per-step source for stratum `w` (B4 term):
    `(‖A(T^[m]x)‖ · exp(m(w+η)) / c^{m+1}) · mass_w(m)`,
  with `‖A(T^[m]x)‖ ≤ exp(mη)` (Tempered), σ-cap `exp(m(w+η))` (B3), `c^{m+1} = exp((m+1)(v−δ*))`.
  The coefficient is `≤ exp(mη)·exp(m(w+η))/exp((m+1)(v−δ*)) = exp(−(m+1)(v−δ*))·exp(m(w+2η))`
  `= exp(−(v−δ*)) · exp(−m((v−δ*) − w − 2η))`, a geometric factor in `m` with ratio
  `ρ_w = exp(−((v−δ*) − w − 2η)) < 1` once `η < ((v−δ*)−w)/2` (guaranteed: `w ≤ pred(v) ≤ v−G`,
  `δ* ≤ G/2`, so `(v−δ*)−w ≥ G/2 > 0`; satisfied by the single slack `η ≤ min(δ,G)/16`, see
  η-budget point 5 in the file header).
* mass_w(m) bound:
  - bottom strata `w ≤ lam0 a`: `mass_w(m) ≤ ‖u_a(n)‖ = 1` (B1 with the trivial cut, or directly
    `norm_fastProj_le`).  Contribution geometric envelope: `Mw = exp(−(v−δ*))`, `ρ_w` as above; the
    `single_source` sum gives `≈ K·exp(−n((v−δ*) − w − 2η)) ≤ K·exp(−n(v − lam0 a − δ))`
    (since `w ≤ lam0 a`, `δ* + 2η ≤ δ`).
  - intermediate strata `lam0 a < w < v`: by the IH `PerStratumEnvelope … a w` at `δ' = δ/4`,
    the mass at its own canonical cut `canonCut_w = exp(w − δ*_w) ≤ C_w·exp(−n(w − lam0 a − δ'))`,
    uniformly in `m ≥ n`; transfer `mass_w(m) ≤ ‖P^{>canonCut_w}_m u_a(n)‖` via B1, which needs
    `stratumBand lam0 w ⊆ hiBand(m, canonCut_w)`: under localization `σ_j(m)^{1/m} > exp(w − η)` for
    `j ∈ stratumBand w`, and `canonCut_w = exp(w − δ*_w) < exp(w − η)` provided `η < δ*_w`.  Since
    `δ*_w = min(δ'/4, G/2, (w−lam0 a)/4) ≥ min(δ/16, G/4)` (using `w − lam0 a ≥ G`), it suffices to
    take `η ≤ min(G, δ)/16`; the binding constraint is this intermediate sub-band inclusion, not
    the `ρ_w < 1` one.  The geometric source then has
    `Mw = C_w·exp(−n(w − lam0 a − δ'))·exp(−(v−δ*))` and the m-sum gives
    `≈ K_w·exp(−n((v−δ*) − w − 2η))·exp(−n(w − lam0 a − δ'))`
    `= K_w·exp(−n(v − lam0 a − δ* − δ' − 2η)) ≤ K_w·exp(−n(v − lam0 a − δ))`
    (δ* + δ' + 2η ≤ δ/4 + δ/4 + δ/8 ≤ δ).
* Assemble via A4 (multi-source envelope): `a_k ≤ ∑_w (Mw/(1−ρw))·ρw^n`, each term
  `≤ C_w'·exp(−n·rate_v)`
  with `rate_v = v − lam0 a − δ`; the final `C = max over w of C_w'` (finite sum bounded by
  (#strata)·max), with `1 ≤ C`. -/

/-- Helper: the per-step coefficient bound (exp algebra).  With slow cap `sval = exp(m(w+η))`,
operator factor `b ≤ exp(mη)`, canonical floor `c^{m+1} = (exp(v−δ*))^{m+1}`, the coefficient is
controlled by `exp(−(v−δ*))·ρ^m` with `ρ = exp(w+2η−(v−δ*))`. -/
private lemma htgstep_coeff (η w v δstar b : ℝ) (m : ℕ)
    (_hb0 : 0 ≤ b) (hb : b ≤ Real.exp ((m : ℝ) * η)) :
    b * Real.exp ((m : ℝ) * (w + η)) / (Real.exp (v - δstar)) ^ (m + 1)
      ≤ Real.exp (-(v - δstar)) * (Real.exp (w + 2 * η - (v - δstar))) ^ m := by
  have hcpos : (0 : ℝ) < (Real.exp (v - δstar)) ^ (m + 1) := by positivity
  rw [div_le_iff₀ hcpos]
  -- RHS·c^{m+1} = exp(-(v-δ*)) · exp(m(w+2η-(v-δ*))) · exp((m+1)(v-δ*))
  rw [← Real.exp_nat_mul (v - δstar) (m + 1), ← Real.exp_nat_mul (w + 2 * η - (v - δstar)) m]
  -- LHS = b · exp(m(w+η)) ≤ exp(mη)·exp(m(w+η)) = exp(m(w+η)+mη)
  have hstep : b * Real.exp ((m : ℝ) * (w + η))
      ≤ Real.exp ((m : ℝ) * η) * Real.exp ((m : ℝ) * (w + η)) :=
    mul_le_mul_of_nonneg_right hb (Real.exp_pos _).le
  refine hstep.trans ?_
  rw [← Real.exp_add, ← Real.exp_add, ← Real.exp_add]
  apply le_of_eq
  congr 1
  push_cast
  ring

/-- Helper: each ratio `ρw = exp(w+2η−(v−δ*))` is in `[0,1)` provided `w + 2η < v − δ*`. -/
private lemma htgstep_rho_lt_one (η w v δstar : ℝ) (h : w + 2 * η - (v - δstar) < 0) :
    Real.exp (w + 2 * η - (v - δstar)) < 1 := by
  rw [← Real.exp_zero]
  exact Real.exp_lt_exp.2 h

/-- **B6 — the inductive step.**  All windows + IH ⟹ the per-stratum envelope for `v`.  The IH is
phrased over the finite set of distinct stratum values strictly between `lam0 a` and `v`. -/
theorem perStratumEnvelope_step [NeZero d] {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0)
    (x : X) (lam0 : ℕ → ℝ) {G : ℝ} (hG : 0 < G)
    (hGgap : ∀ i j : Fin d, lam0 (i : ℕ) < lam0 (j : ℕ) → lam0 (i : ℕ) + G ≤ lam0 (j : ℕ))
    (hconv : ∀ j : ℕ, j < d → Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues j))
      Filter.atTop (𝓝 (lam0 j)))
    (htemp : Filter.Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖A (T^[n] x)‖) Filter.atTop (𝓝 0))
    (a : Fin d) (v : ℝ) (hav : lam0 (a : ℕ) < v)
    (hvstratum : ∃ j : Fin d, lam0 (j : ℕ) = v)
    (IH : ∀ w : ℝ, lam0 (a : ℕ) < w → w < v → (∃ j : Fin d, lam0 (j : ℕ) = w) →
      PerStratumEnvelope A T lam0 x G a w) :
    PerStratumEnvelope A T lam0 x G a v := by
  classical
  intro δ hδ
  -- The single localization slack η ≤ min(δ,G)/16, and the canonical slack/cut δ*, c, δ'.
  set η : ℝ := min δ G / 16 with hηdef
  have hηpos : 0 < η := by
    rw [hηdef]; positivity
  set δstar : ℝ := canonSlack lam0 (a : ℕ) v G δ with hδstardef
  set c : ℝ := canonCut lam0 (a : ℕ) v G δ with hcdef
  have hcval : c = Real.exp (v - δstar) := rfl
  set δ' : ℝ := δ / 4 with hδ'def
  have hδ'pos : 0 < δ' := by rw [hδ'def]; positivity
  -- Basic facts about δ* (canonSlack): positive, ≤ δ/4, ≤ G/2, ≤ (v−λ_a)/4, and ≥ min(δ/4,G/4).
  have hvla : 0 < v - lam0 (a : ℕ) := by linarith [hav]
  have hδstar_pos : 0 < δstar := by
    rw [hδstardef, canonSlack]; positivity
  have hδstar_le_d4 : δstar ≤ δ / 4 := by
    rw [hδstardef, canonSlack]; exact le_trans (min_le_left _ _) (min_le_left _ _)
  have hδstar_le_G2 : δstar ≤ G / 2 := by
    rw [hδstardef, canonSlack]; exact le_trans (min_le_left _ _) (min_le_right _ _)
  have hδstar_le_vla4 : δstar ≤ (v - lam0 (a : ℕ)) / 4 := by
    rw [hδstardef, canonSlack]; exact min_le_right _ _
  -- v − λ_a ≥ G (distinct strata gap), so δ* ≥ min(δ/4, G/4).
  have hvla_ge_G : G ≤ v - lam0 (a : ℕ) := by
    obtain ⟨jv, hjv⟩ := hvstratum
    have : lam0 (a : ℕ) + G ≤ lam0 (jv : ℕ) := hGgap a jv (by rw [hjv]; exact hav)
    rw [hjv] at this; linarith
  have hδstar_ge : min (δ / 4) (G / 4) ≤ δstar := by
    rw [hδstardef, canonSlack]
    refine le_min (le_min (min_le_left _ _) ?_) ?_
    · exact le_trans (min_le_right _ _) (by linarith [hG] : G / 4 ≤ G / 2)
    · exact le_trans (min_le_right _ _) (by linarith [hvla_ge_G] : G / 4 ≤ (v - lam0 (a : ℕ)) / 4)
  -- η bounds: η ≤ δ/16, η ≤ G/16, η < δ*, 2η + δ* ≤ δ, δ* + δ' + 2η ≤ δ.
  have hη_le_d16 : η ≤ δ / 16 := by
    rw [hηdef]; gcongr; exact min_le_left _ _
  have hη_le_G16 : η ≤ G / 16 := by
    rw [hηdef]; gcongr; exact min_le_right _ _
  -- η < δ* (strict): η ≤ min(δ,G)/16 < min(δ/4,G/4) ≤ δ*.
  have hη_lt_δstar : η < δstar := by
    refine lt_of_lt_of_le ?_ hδstar_ge
    rw [hηdef]
    rcases le_total δ G with hdg | hdg
    · rw [min_eq_left hdg, min_eq_left (by linarith : δ / 4 ≤ G / 4)]; linarith [hδ]
    · rw [min_eq_right hdg, min_eq_right (by linarith : G / 4 ≤ δ / 4)]; linarith [hG]
  have h2η_δstar_le_δ : 2 * η + δstar ≤ δ := by
    have : 2 * η ≤ δ / 8 := by linarith [hη_le_d16]
    linarith [hδstar_le_d4]
  have hsum_le_δ : δstar + δ' + 2 * η ≤ δ := by
    have : 2 * η ≤ δ / 8 := by linarith [hη_le_d16]
    rw [hδ'def]; linarith [hδstar_le_d4]
  -- Obtain the localization and tempering windows at η.
  obtain ⟨Nloc, hloc⟩ := exists_localized hA x lam0 hconv hηpos
  obtain ⟨Ntmp, htmp⟩ := exists_tempered x htemp hηpos
  -- The finite set of distinct slow stratum values below the cut, and the per-stratum sub-bands.
  set Wf : Finset ℝ :=
    (Finset.univ.image (fun j : Fin d => lam0 (j : ℕ))).filter (· < v - δstar) with hWfdef
  set Bw : ℝ → Finset (Fin (Fintype.card (Fin d))) := fun w => stratumBand lam0 w with hBwdef
  -- Membership in Wf: a distinct stratum value strictly below v − δ*.
  have hWf_mem : ∀ w : ℝ, w ∈ Wf ↔ (∃ j : Fin d, lam0 (j : ℕ) = w) ∧ w < v - δstar := by
    intro w
    rw [hWfdef, Finset.mem_filter, Finset.mem_image]
    constructor
    · rintro ⟨⟨j, _, hj⟩, hlt⟩; exact ⟨⟨j, hj⟩, hlt⟩
    · rintro ⟨⟨j, hj⟩, hlt⟩; exact ⟨⟨j, Finset.mem_univ _, hj⟩, hlt⟩
  -- Membership in a stratum sub-band.
  have hBw_mem : ∀ (w : ℝ) (j : Fin (Fintype.card (Fin d))),
      j ∈ Bw w ↔ lam0 (j : ℕ) = w := by
    intro w j
    simp only [hBwdef, stratumBand, Finset.mem_filter, Finset.mem_univ, true_and]
  -- The canonical-cut gap separation at γ = v − δ* (header point 4).
  have hgapsep : ∀ j : ℕ, j < d →
      lam0 j + η < v - δstar ∨ v - δstar < lam0 j - η := by
    intro j hjd
    obtain ⟨jv, hjv⟩ := hvstratum
    set jf : Fin d := ⟨j, hjd⟩ with hjf
    have hlam_jf : lam0 (jf : ℕ) = lam0 j := by rw [hjf]
    rcases lt_or_ge (lam0 j) v with hlt | hge
    · -- slow stratum: lam0 j ≤ v − G, so lam0 j + η < v − δ*.
      left
      have hgap : lam0 (jf : ℕ) + G ≤ lam0 (jv : ℕ) :=
        hGgap jf jv (by rw [hlam_jf, hjv]; exact hlt)
      rw [hlam_jf, hjv] at hgap
      -- η + δ* < G ≤ v − lam0 j
      have : η + δstar < G := by linarith [hη_le_G16, hδstar_le_G2, hG]
      linarith
    · -- fast stratum lam0 j ≥ v: v − δ* < lam0 j − η since η < δ*.
      right; linarith [hη_lt_δstar]
  -- For every m past localization, the slow band of cut c decomposes into the sub-bands of Wf.
  have hpart : ∀ m : ℕ, Nloc ≤ m → 1 ≤ m →
      (hiBand A T m x c)ᶜ = Wf.biUnion Bw := by
    intro m hm hm1
    ext j
    rw [Finset.mem_compl, Finset.mem_biUnion, hcval]
    have hjd : (j : ℕ) < d := lt_of_lt_of_eq j.isLt (Fintype.card_fin d)
    have hmem := mem_hiBand_iff_of_localized hA x lam0 hηpos hloc hgapsep hm hm1 j
    constructor
    · intro hnotin
      rw [hmem] at hnotin
      push Not at hnotin
      -- lam0 j ≤ v − δ*; combined with gapsep ⟹ lam0 j < v − δ*.
      have hne : lam0 (j : ℕ) ≠ v - δstar := by
        rcases hgapsep (j : ℕ) hjd with h | h
        · linarith
        · linarith
      have hlt : lam0 (j : ℕ) < v - δstar := lt_of_le_of_ne hnotin hne
      refine ⟨lam0 (j : ℕ), (hWf_mem _).2 ⟨⟨⟨(j : ℕ), hjd⟩, rfl⟩, hlt⟩, (hBw_mem _ j).2 rfl⟩
    · rintro ⟨w, hwWf, hjBw⟩
      have hjw : lam0 (j : ℕ) = w := (hBw_mem w j).1 hjBw
      have hwlt : w < v - δstar := ((hWf_mem w).1 hwWf).2
      rw [hmem]; push Not; rw [hjw]; linarith
  -- Disjointness of the sub-bands (different stratum values).
  have hdisj : (Wf : Set ℝ).PairwiseDisjoint Bw := by
    intro w hw w' hw' hne
    simp only [Function.onFun, Finset.disjoint_left]
    intro j hjw hjw'
    exact hne (((hBw_mem w j).1 hjw).symm.trans ((hBw_mem w' j).1 hjw'))
  -- The time-`n` slow eigenvector, abbreviated.
  set ua : ℕ → EuclideanSpace ℝ (Fin d) := fun n =>
    sortedGramEigenbasis A T n x ⟨(a : ℕ), lt_of_lt_of_eq a.isLt (Fintype.card_fin d).symm⟩
    with huadef
  -- Each w ∈ Wf is a distinct slow stratum: w + G ≤ v, and w < v.
  have hw_le_vG : ∀ w ∈ Wf, w + G ≤ v := by
    intro w hw
    obtain ⟨⟨jw, hjw⟩, hwlt⟩ := (hWf_mem w).1 hw
    obtain ⟨jv, hjv⟩ := hvstratum
    have hwv : w < v := lt_trans hwlt (by linarith [hδstar_pos])
    have : lam0 (jw : ℕ) + G ≤ lam0 (jv : ℕ) := hGgap jw jv (by rw [hjw, hjv]; exact hwv)
    rw [hjw, hjv] at this; linarith
  -- The per-stratum geometric ratio ρw = exp(w + 2η − (v − δ*)) ∈ [0,1) for w ∈ Wf.
  set ρw : ℝ → ℝ := fun w => Real.exp (w + 2 * η - (v - δstar)) with hρwdef
  have hρw_pos : ∀ w, 0 ≤ ρw w := fun w => (Real.exp_pos _).le
  have hρw_lt1 : ∀ w ∈ Wf, ρw w < 1 := by
    intro w hw
    refine htgstep_rho_lt_one η w v δstar ?_
    -- w + 2η ≤ (v − G) + G/8 < v − δ*  (uses w ≤ v − G, 2η ≤ G/8, δ* ≤ G/2)
    have h1 : w + G ≤ v := hw_le_vG w hw
    have h2 : 2 * η ≤ G / 8 := by linarith [hη_le_G16]
    linarith [hδstar_le_G2, hG]
  have h1mρw_pos : ∀ w ∈ Wf, 0 < 1 - ρw w := fun w hw => by linarith [hρw_lt1 w hw]
  -- The per-stratum IH constant Cfun w (= 1 on bottom strata, the IH choose on intermediate ones).
  set Cfun : ℝ → ℝ := fun w =>
    if h : lam0 (a : ℕ) < w ∧ w < v ∧ (∃ j : Fin d, lam0 (j : ℕ) = w)
    then (IH w h.1 h.2.1 h.2.2 δ' hδ'pos).choose else 1 with hCfundef
  have hCfun_ge1 : ∀ w, 1 ≤ Cfun w := by
    intro w; rw [hCfundef]; dsimp only
    split
    · rename_i h; exact (IH w h.1 h.2.1 h.2.2 δ' hδ'pos).choose_spec.1
    · exact le_refl 1
  have hCfun_nonneg : ∀ w, 0 ≤ Cfun w := fun w => le_trans zero_le_one (hCfun_ge1 w)
  -- The collected intermediate-IH eventual bounds, one threshold for the whole finset Wf.
  have hev : ∀ᶠ n : ℕ in Filter.atTop, ∀ w ∈ Wf, lam0 (a : ℕ) < w →
      ∀ m : ℕ, n ≤ m →
        ‖Matrix.toEuclideanLin
            (bandProjector A T (Set.indicator (Set.Ioi (canonCut lam0 (a : ℕ) w G δ')) 1) m x)
            (ua n)‖
          ≤ Cfun w * Real.exp (-(n : ℝ) * (w - lam0 (a : ℕ) - δ')) := by
    rw [Filter.eventually_all_finset]
    intro w hw
    by_cases hlt : lam0 (a : ℕ) < w
    · -- intermediate stratum: use the IH eventual bound, with Cfun w = the IH choose.
      obtain ⟨⟨jw, hjw⟩, hwlt⟩ := (hWf_mem w).1 hw
      have hwv : w < v := lt_trans hwlt (by linarith [hδstar_pos])
      have hex : ∃ j : Fin d, lam0 (j : ℕ) = w := ⟨jw, hjw⟩
      have hdcond : lam0 (a : ℕ) < w ∧ w < v ∧ (∃ j : Fin d, lam0 (j : ℕ) = w) := ⟨hlt, hwv, hex⟩
      have hCval : Cfun w = (IH w hlt hwv hex δ' hδ'pos).choose := by
        rw [hCfundef]; dsimp only; rw [dif_pos hdcond]
      have hspec := (IH w hlt hwv hex δ' hδ'pos).choose_spec.2
      filter_upwards [hspec] with n hn
      intro _
      rw [hCval]; exact hn
    · -- bottom stratum: the statement is vacuous (the `lam0 a < w` premise fails).
      filter_upwards with n hcontra
      exact absurd hcontra hlt
  -- The per-stratum n-independent prefactors and the final constant C.
  set Dw : ℝ → ℝ := fun w => Real.exp (-(v - δstar)) * Cfun w / (1 - ρw w) with hDwdef
  set C : ℝ := max 1 (∑ w ∈ Wf, Dw w) with hCdef
  refine ⟨C, le_max_left _ _, ?_⟩
  -- Eventually in n past localization, tempering, 1, and the intermediate IH thresholds.
  filter_upwards [hev, Filter.eventually_ge_atTop (max (max Nloc Ntmp) 1)]
    with n hevn hnge
  have hnNloc : Nloc ≤ n := le_trans (le_trans (le_max_left _ _) (le_max_left _ _)) hnge
  have hnNtmp : Ntmp ≤ n := le_trans (le_trans (le_max_right _ _) (le_max_left _ _)) hnge
  have hn1 : 1 ≤ n := le_trans (le_max_right _ _) hnge
  -- δ*_w ≥ η for intermediate strata w (the binding sub-band inclusion bound, header point 5).
  have hδstarw_ge : ∀ w ∈ Wf, lam0 (a : ℕ) < w → η ≤ canonSlack lam0 (a : ℕ) w G δ' := by
    intro w hw hlt
    obtain ⟨⟨jw, hjw⟩, _⟩ := (hWf_mem w).1 hw
    have hwG : G ≤ w - lam0 (a : ℕ) := by
      have : lam0 (a : ℕ) + G ≤ lam0 (jw : ℕ) := hGgap a jw (by rw [hjw]; exact hlt)
      rw [hjw] at this; linarith
    rw [canonSlack]
    refine le_min (le_min ?_ ?_) ?_
    · rw [hδ'def]; linarith [hη_le_d16]
    · linarith [hη_le_G16, hG]
    · linarith [hη_le_G16, hwG]
  -- Sub-band inclusion: stratumBand w ⊆ hiBand at the IH cut, for intermediate w and m past Nloc.
  have hincl : ∀ w ∈ Wf, lam0 (a : ℕ) < w → ∀ mm : ℕ, Nloc ≤ mm → 1 ≤ mm →
      Bw w ⊆ hiBand A T mm x (canonCut lam0 (a : ℕ) w G δ') := by
    intro w hw hlt mm hmm hmm1 j hjBw
    have hjw : lam0 (j : ℕ) = w := (hBw_mem w j).1 hjBw
    have hjd : (j : ℕ) < d := lt_of_lt_of_eq j.isLt (Fintype.card_fin d)
    rw [hiBand, Finset.mem_filter]
    refine ⟨Finset.mem_univ _, ?_⟩
    rw [qpow_eigenvalue_eq_rpow]
    have hloc_j := (hloc mm hmm (j : ℕ) hjd).1
    rw [hjw] at hloc_j
    -- canonCut_w = exp(w − δ*_w) ≤ exp(w − η) < σ^{1/mm}
    refine lt_of_le_of_lt ?_ hloc_j
    rw [canonCut, Real.exp_le_exp]
    have := hδstarw_ge w hw hlt
    linarith
  -- Now fix the time m ≥ n and run the band-mass chain at the canonical cut c.
  intro m hm
  -- The band-mass sequence a_k = ‖P^{>c}_{n+k} (u_a(n))‖.
  set aseq : ℕ → ℝ := fun k =>
    ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c) 1) (n + k) x) (ua n)‖
    with haseqdef
  -- The mass bound massBnd and source prefactor Mw for the multi-source envelope.
  set massBnd : ℝ → ℝ := fun w =>
    Cfun w * (if lam0 (a : ℕ) < w then Real.exp (-(n : ℝ) * (w - lam0 (a : ℕ) - δ')) else 1)
    with hmassBnddef
  set Mw : ℝ → ℝ := fun w => Real.exp (-(v - δstar)) * massBnd w with hMwdef
  have hmassBnd_nonneg : ∀ w, 0 ≤ massBnd w := by
    intro w; rw [hmassBnddef]; dsimp only
    apply mul_nonneg (hCfun_nonneg w)
    split <;> positivity
  have hMw_nonneg : ∀ w, 0 ≤ Mw w := by
    intro w; rw [hMwdef]; dsimp only
    exact mul_nonneg (Real.exp_nonneg _) (hmassBnd_nonneg w)
  -- The per-step source family.
  set srcw : ℝ → ℕ → ℝ := fun w k =>
    (‖A (T^[n + k] x)‖ * Real.exp ((↑(n + k) : ℝ) * (w + η)) / c ^ (n + k + 1))
      * ‖(chainSVD A T x).fastProj (n + k) (Bw w) (ua n)‖ with hsrcwdef
  have hc_pos : 0 < c := by rw [hcval]; exact Real.exp_pos _
  -- Initialization a_0 = 0 (B5).
  have h0 : aseq 0 = 0 := by
    rw [haseqdef]; dsimp only; rw [Nat.add_zero]
    have hηsmall : lam0 (a : ℕ) + η < v - canonSlack lam0 (a : ℕ) v G δ := by
      rw [← hδstardef]
      have hη16 : η ≤ (v - lam0 (a : ℕ)) / 16 := by
        refine le_trans hη_le_G16 ?_; linarith [hvla_ge_G]
      linarith [hδstar_le_vla4]
    rw [canonCut_init_zero hA x lam0 a hloc hnNloc hn1 hav hηpos hηsmall, norm_zero]
  -- One-step recursion (B4) at each absolute time n + k.
  have hrec : ∀ k : ℕ, aseq (k + 1) ≤ aseq k + ∑ w ∈ Wf, srcw w k := by
    intro k
    have hmm : Nloc ≤ n + k := le_trans hnNloc (Nat.le_add_right _ _)
    have hmm1 : 1 ≤ n + k := le_trans hn1 (Nat.le_add_right _ _)
    have hstep := bandMass_oneStep_multisource (T := T) A hc_pos x Wf
      (fun w => Real.exp ((↑(n + k) : ℝ) * (w + η)))
      (fun w _ => (Real.exp_pos _).le) Bw
      (fun w hwWf j hjBw => stratum_sigma_cap hA x lam0 hηpos hloc hmm hmm1 j hjBw)
      (hpart (n + k) hmm hmm1) hdisj (ua n)
    -- align time indices: n + (k+1) = (n+k)+1, and the sources match srcw.
    have he1 : n + (k + 1) = n + k + 1 := by ring
    change aseq (k + 1) ≤ aseq k + ∑ w ∈ Wf, srcw w k
    rw [haseqdef, hsrcwdef]; dsimp only; rw [he1]
    exact hstep
  -- Cfun is 1 on bottom strata.
  have hCfun_bottom : ∀ w, ¬ lam0 (a : ℕ) < w → Cfun w = 1 := by
    intro w hnlt; rw [hCfundef]; dsimp only
    rw [dif_neg (fun h => hnlt h.1)]
  -- The per-stratum source bound: srcw w k ≤ Mw w · ρw w ^ (n+k).
  have hsrc : ∀ w ∈ Wf, ∀ k : ℕ, srcw w k ≤ Mw w * ρw w ^ (n + k) := by
    intro w hw k
    have hmm : Nloc ≤ n + k := le_trans hnNloc (Nat.le_add_right _ _)
    have hmmtmp : Ntmp ≤ n + k := le_trans hnNtmp (Nat.le_add_right _ _)
    have hmm1 : 1 ≤ n + k := le_trans hn1 (Nat.le_add_right _ _)
    have hnk : n ≤ n + k := Nat.le_add_right _ _
    -- coefficient bound (exp algebra).
    have hcoeff : ‖A (T^[n + k] x)‖ * Real.exp ((↑(n + k) : ℝ) * (w + η)) / c ^ (n + k + 1)
        ≤ Real.exp (-(v - δstar)) * ρw w ^ (n + k) := by
      rw [hcval, hρwdef]; dsimp only
      have hb := htmp (n + k) hmmtmp
      exact htgstep_coeff η w v δstar _ (n + k) (norm_nonneg _) hb
    have hcoeff_nonneg :
        0 ≤ ‖A (T^[n + k] x)‖ * Real.exp ((↑(n + k) : ℝ) * (w + η)) / c ^ (n + k + 1) := by
      apply div_nonneg (mul_nonneg (norm_nonneg _) (Real.exp_pos _).le)
      exact pow_nonneg hc_pos.le _
    have hrhs_nonneg : 0 ≤ Real.exp (-(v - δstar)) * ρw w ^ (n + k) :=
      mul_nonneg (Real.exp_nonneg _) (pow_nonneg (hρw_pos w) _)
    -- mass bound: ‖fastProj (n+k) (Bw w) (ua n)‖ ≤ massBnd w.
    have hmass : ‖(chainSVD A T x).fastProj (n + k) (Bw w) (ua n)‖ ≤ massBnd w := by
      rw [hmassBnddef]; dsimp only
      by_cases hlt : lam0 (a : ℕ) < w
      · rw [if_pos hlt]
        -- B1 + the IH eventual bound.
        refine le_trans (subband_mass_le_bandMass (T := T) A (n + k) x
          (canonCut lam0 (a : ℕ) w G δ') (Bw w) (hincl w hw hlt (n + k) hmm hmm1) (ua n)) ?_
        exact hevn w hw hlt (n + k) hnk
      · rw [if_neg hlt, hCfun_bottom w hlt, mul_one]
        refine le_trans ((chainSVD A T x).norm_fastProj_le (n + k) (Bw w) (ua n)) ?_
        rw [huadef]; dsimp only
        exact le_of_eq ((sortedGramEigenbasis A T n x).orthonormal.1 _)
    have hmass_nonneg : 0 ≤ ‖(chainSVD A T x).fastProj (n + k) (Bw w) (ua n)‖ := norm_nonneg _
    -- combine: srcw = coeff · mass ≤ (exp(-(v-δ*))·ρw^(n+k)) · massBnd w = Mw w · ρw^(n+k).
    rw [hsrcwdef]; dsimp only
    calc (‖A (T^[n + k] x)‖ * Real.exp ((↑(n + k) : ℝ) * (w + η)) / c ^ (n + k + 1))
            * ‖(chainSVD A T x).fastProj (n + k) (Bw w) (ua n)‖
        ≤ (Real.exp (-(v - δstar)) * ρw w ^ (n + k)) * massBnd w :=
          mul_le_mul hcoeff hmass hmass_nonneg hrhs_nonneg
      _ = Mw w * ρw w ^ (n + k) := by rw [hMwdef]; dsimp only; ring
  -- Apply the multi-source envelope (A4).
  have henv := ChainCore.multi_source_envelope Wf aseq srcw Mw ρw n
    (fun w _ => hMw_nonneg w) (fun w _ => hρw_pos w) hρw_lt1 h0 hrec hsrc (m - n)
  -- Per-stratum: (Mw w/(1-ρw w))·ρw^n ≤ Dw w · exp(-n(v-λ_a-δ)).
  have hterm : ∀ w ∈ Wf,
      Mw w / (1 - ρw w) * ρw w ^ n ≤ Dw w * Real.exp (-(n : ℝ) * (v - lam0 (a : ℕ) - δ)) := by
    intro w hw
    have h1mρ := h1mρw_pos w hw
    -- numerator inequality: Mw w · ρw^n ≤ exp(-(v-δ*)) · Cfun w · exp(-n(v-λ_a-δ)).
    have hnum : Mw w * ρw w ^ n
        ≤ (Real.exp (-(v - δstar)) * Cfun w) * Real.exp (-(n : ℝ) * (v - lam0 (a : ℕ) - δ)) := by
      rw [hMwdef, hmassBnddef, hρwdef]; dsimp only
      rw [← Real.exp_nat_mul (w + 2 * η - (v - δstar)) n]
      have hncast : (0 : ℝ) ≤ (n : ℝ) := Nat.cast_nonneg _
      by_cases hlt : lam0 (a : ℕ) < w
      · rw [if_pos hlt]
        -- group to (exp(-(v-δ*))·Cfun w) · [exp(-n(w-λ_a-δ'))·exp(n(w+2η-(v-δ*)))]
        have hcombine : Real.exp (-(v - δstar))
              * (Cfun w * Real.exp (-(n : ℝ) * (w - lam0 (a : ℕ) - δ')))
            * Real.exp ((n : ℝ) * (w + 2 * η - (v - δstar)))
            = (Real.exp (-(v - δstar)) * Cfun w)
              * (Real.exp (-(n : ℝ) * (w - lam0 (a : ℕ) - δ'))
                 * Real.exp ((n : ℝ) * (w + 2 * η - (v - δstar)))) := by ring
        rw [hcombine]
        apply mul_le_mul_of_nonneg_left _ (mul_nonneg (Real.exp_nonneg _) (hCfun_nonneg w))
        rw [← Real.exp_add, Real.exp_le_exp]
        nlinarith [hsum_le_δ, hncast]
      · rw [if_neg hlt, hCfun_bottom w hlt, mul_one, mul_one]
        push Not at hlt
        apply mul_le_mul_of_nonneg_left _ (Real.exp_nonneg _)
        rw [Real.exp_le_exp]
        nlinarith [h2η_δstar_le_δ, hncast, hlt]
    -- divide by 1 - ρw > 0.
    have hgoal_rhs : Dw w * Real.exp (-(n : ℝ) * (v - lam0 (a : ℕ) - δ))
        = ((Real.exp (-(v - δstar)) * Cfun w) * Real.exp (-(n : ℝ) * (v - lam0 (a : ℕ) - δ)))
          / (1 - ρw w) := by
      rw [hDwdef]; dsimp only; ring
    rw [hgoal_rhs, div_mul_eq_mul_div]
    gcongr
  -- The final sum bound: ∑ (Mw/(1-ρw))·ρw^n ≤ C · exp(-n(v-λ_a-δ)).
  have hsum_bound : ∑ w ∈ Wf, Mw w / (1 - ρw w) * ρw w ^ n
      ≤ C * Real.exp (-(n : ℝ) * (v - lam0 (a : ℕ) - δ)) := by
    refine le_trans (Finset.sum_le_sum hterm) ?_
    rw [← Finset.sum_mul]
    exact mul_le_mul_of_nonneg_right (le_max_right _ _) (Real.exp_nonneg _)
  -- Conclude: aseq (m-n) = goal mass; chain henv → hsum_bound.
  have hmeq : n + (m - n) = m := Nat.add_sub_cancel' hm
  refine le_trans ?_ (le_trans henv hsum_bound)
  rw [haseqdef]; dsimp only; rw [hmeq]

/-- The finset of distinct stratum values strictly between `lam0 a` and `v`. -/
private def htgind_S [NeZero d] (lam0 : ℕ → ℝ) (a : Fin d) (v : ℝ) : Finset ℝ :=
  (Finset.univ.image (fun j : Fin d => lam0 (j : ℕ))).filter (fun w => lam0 (a : ℕ) < w ∧ w < v)

/-- Membership characterization of `htgind_S`: a value `w` lies in the set iff it is a stratum
value (`∃ j, lam0 j = w`) strictly between `lam0 a` and `v`. -/
private lemma htgind_mem_S [NeZero d] (lam0 : ℕ → ℝ) (a : Fin d) (v w : ℝ) :
    w ∈ htgind_S lam0 a v ↔ (∃ j : Fin d, lam0 (j : ℕ) = w) ∧ lam0 (a : ℕ) < w ∧ w < v := by
  unfold htgind_S
  rw [Finset.mem_filter, Finset.mem_image]
  constructor
  · rintro ⟨⟨j, _, hj⟩, hbnds⟩
    exact ⟨⟨j, hj⟩, hbnds⟩
  · rintro ⟨⟨j, hj⟩, hbnds⟩
    exact ⟨⟨j, Finset.mem_univ j, hj⟩, hbnds⟩

/-- Generalized form proved by induction on a cardinality budget `M`: the per-stratum envelope holds
for every distinct stratum value `v > lam0 a` whose number of intermediate strata `N(v) ≤ M`. -/
private lemma htgind_aux [NeZero d] {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) (x : X) (lam0 : ℕ → ℝ) {G : ℝ} (hG : 0 < G)
    (hGgap : ∀ i j : Fin d, lam0 (i : ℕ) < lam0 (j : ℕ) → lam0 (i : ℕ) + G ≤ lam0 (j : ℕ))
    (hconv : ∀ j : ℕ, j < d → Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues j))
      Filter.atTop (𝓝 (lam0 j)))
    (htemp : Filter.Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖A (T^[n] x)‖) Filter.atTop (𝓝 0))
    (a : Fin d) (M : ℕ) :
    ∀ v : ℝ, (htgind_S lam0 a v).card ≤ M → lam0 (a : ℕ) < v →
      (∃ j : Fin d, lam0 (j : ℕ) = v) → PerStratumEnvelope A T lam0 x G a v := by
  induction M with
  | zero =>
    intro v hcard hav hvstratum
    -- The set of intermediate strata is empty (card ≤ 0), so the IH for
    -- `perStratumEnvelope_step` is vacuous.
    refine perStratumEnvelope_step hA x lam0 hG hGgap hconv htemp a v hav hvstratum ?_
    intro w hlt hwv hex
    have hwmem : w ∈ htgind_S lam0 a v := (htgind_mem_S lam0 a v w).2 ⟨hex, hlt, hwv⟩
    have hempty : htgind_S lam0 a v = ∅ := Finset.card_eq_zero.mp (Nat.le_zero.mp hcard)
    rw [hempty] at hwmem
    exact absurd hwmem (Finset.notMem_empty w)
  | succ M ih =>
    intro v hcard hav hvstratum
    refine perStratumEnvelope_step hA x lam0 hG hGgap hconv htemp a v hav hvstratum ?_
    intro w hlt hwv hex
    -- `htgind_S lam0 a w ⊂ htgind_S lam0 a v`: subset by transitivity, strict since `w ∈ Sᵥ \ S_w`.
    have hsub : htgind_S lam0 a w ⊆ htgind_S lam0 a v := by
      intro w' hw'
      rw [htgind_mem_S] at hw' ⊢
      obtain ⟨hex', hlt', hw'w⟩ := hw'
      exact ⟨hex', hlt', hw'w.trans hwv⟩
    have hwmem : w ∈ htgind_S lam0 a v := (htgind_mem_S lam0 a v w).2 ⟨hex, hlt, hwv⟩
    have hwnmem : w ∉ htgind_S lam0 a w := by
      rw [htgind_mem_S]; rintro ⟨_, _, hcontra⟩; exact (lt_irrefl w) hcontra
    have hssub : htgind_S lam0 a w ⊂ htgind_S lam0 a v :=
      (Finset.ssubset_iff_of_subset hsub).2 ⟨w, hwmem, hwnmem⟩
    have hcardlt : (htgind_S lam0 a w).card < (htgind_S lam0 a v).card :=
      Finset.card_lt_card hssub
    exact ih w (Nat.le_of_lt_succ (lt_of_lt_of_le hcardlt hcard)) hlt hex

/-- **B7 — the strong induction.**  For every index `a` and every distinct stratum value `v` with
`lam0 a < v`, the per-stratum envelope holds.  Strong induction on the number of distinct stratum
values in `(lam0 a, v)` (equivalently `Finset` well-founded recursion), discharging each level by
`perStratumEnvelope_step`. -/
theorem perStratumEnvelope_of_lt [NeZero d] {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) (x : X) (lam0 : ℕ → ℝ) {G : ℝ} (hG : 0 < G)
    (hGgap : ∀ i j : Fin d, lam0 (i : ℕ) < lam0 (j : ℕ) → lam0 (i : ℕ) + G ≤ lam0 (j : ℕ))
    (hconv : ∀ j : ℕ, j < d → Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues j))
      Filter.atTop (𝓝 (lam0 j)))
    (htemp : Filter.Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖A (T^[n] x)‖) Filter.atTop (𝓝 0))
    (a : Fin d) (v : ℝ) (hav : lam0 (a : ℕ) < v) (hvstratum : ∃ j : Fin d, lam0 (j : ℕ) = v) :
    PerStratumEnvelope A T lam0 x G a v :=
  htgind_aux hA x lam0 hG hGgap hconv htemp a (htgind_S lam0 a v).card v le_rfl hav hvstratum

/-! ## PART C — band stabilization + transfer to all gap-interior cuts + a.e. wrapper -/

/-! ### Band stabilization

Under localization with `η` small, the band at any cut whose `log` is strictly gap-separated from
every stratum stabilizes: `j ∈ hiBand A T m x c ↔ log c < lam0 j`, for all `m` past the localization
threshold.  Hence two gap-interior cuts to the same top gap below `lam0 e` give equal bands, so
equal band-projector masses. -/

/-- **C1 — band mass equality for two gap-interior cuts** (band stabilization).  If `log c₀` and
`log c₁` are both strictly gap-separated from every stratum by more than `η` (`hsep0`, `hsep1`) and
they have the same membership pattern (`hsame : ∀ j, log c₀ < lam0 j ↔ log c₁ < lam0 j`), then for
every `m` past the localization threshold the band-projector masses agree. -/
theorem bandMass_eq_of_gap_interior [NeZero d] {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) (x : X) (lam0 : ℕ → ℝ) {η : ℝ} (hη : 0 < η) {N : ℕ}
    (hloc : Localized A T x lam0 η N) {c₀ c₁ : ℝ} (hc₀ : 0 < c₀) (hc₁ : 0 < c₁)
    (hsep0 : ∀ j : ℕ, j < d → lam0 j + η < Real.log c₀ ∨ Real.log c₀ < lam0 j - η)
    (hsep1 : ∀ j : ℕ, j < d → lam0 j + η < Real.log c₁ ∨ Real.log c₁ < lam0 j - η)
    (hsame : ∀ j : Fin (Fintype.card (Fin d)),
      Real.log c₀ < lam0 (j : ℕ) ↔ Real.log c₁ < lam0 (j : ℕ))
    {m : ℕ} (hm : N ≤ m) (hm1 : 1 ≤ m) (u : EuclideanSpace ℝ (Fin d)) :
    ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c₀) 1) m x) u‖
      = ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c₁) 1) m x) u‖ := by
  -- The two fast bands coincide as index finsets.
  have hband : hiBand A T m x c₀ = hiBand A T m x c₁ := by
    apply Finset.ext
    intro j
    -- Membership at `c₀ = exp (log c₀)`.
    have h0 : j ∈ hiBand A T m x c₀ ↔ Real.log c₀ < lam0 (j : ℕ) := by
      have := mem_hiBand_iff_of_localized hA x lam0 hη hloc hsep0 hm hm1 j
      rwa [Real.exp_log hc₀] at this
    -- Membership at `c₁ = exp (log c₁)`.
    have h1 : j ∈ hiBand A T m x c₁ ↔ Real.log c₁ < lam0 (j : ℕ) := by
      have := mem_hiBand_iff_of_localized hA x lam0 hη hloc hsep1 hm hm1 j
      rwa [Real.exp_log hc₁] at this
    rw [h0, h1, hsame j]
  -- Equal bands ⟹ equal fast projections ⟹ equal norms.
  rw [toEuclideanLin_bandProjector_eq_fastProj, toEuclideanLin_bandProjector_eq_fastProj, hband]

/-! ### Transfer: per-stratum envelope (canonical cuts) ⟹ TopGapMassEnvelope (all cuts)

For the pair `(a, e)` with `lam0 a < lam0 e` and a gap-interior cut `c₀`
(`∀ i, lam0 i < log c₀ ∨ lam0 e ≤ lam0 i`), the canonical cut `canonCut a (lam0 e) G δ` is also
gap-interior to the same top gap below `lam0 e` (its `log = lam0 e − δ*` with `δ* ≤ G/2`, and the
predecessor stratum is `≤ lam0 e − G`).  Both cuts have membership `lam0 j > cut ↔ lam0 e ≤ lam0 j`,
so by C1 their band masses agree past localization, and the per-stratum envelope at `v = lam0 e`
transfers.  The constant `C` is uniform over the finitely many pairs via a `Finset` max. -/

/-- **C2 — transfer to a single gap-interior cut.**  From `PerStratumEnvelope … a (lam0 e)` and
localization, the TopGap-style bound holds at the arbitrary gap-interior cut `c₀`. -/
theorem topGap_bound_at_cut_of_perStratum [NeZero d] {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) (x : X) (lam0 : ℕ → ℝ) {G : ℝ} (hG : 0 < G)
    (hGgap : ∀ i j : Fin d, lam0 (i : ℕ) < lam0 (j : ℕ) → lam0 (i : ℕ) + G ≤ lam0 (j : ℕ))
    (hconv : ∀ j : ℕ, j < d → Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues j))
      Filter.atTop (𝓝 (lam0 j)))
    (a e : Fin d) (hgap : lam0 (a : ℕ) < lam0 (e : ℕ))
    (_henv : PerStratumEnvelope A T lam0 x G a (lam0 (e : ℕ)))
    {δ : ℝ} (hδ : 0 < δ) {C : ℝ} (_hC1 : 1 ≤ C)
    (hCenv : ∀ᶠ n : ℕ in Filter.atTop, ∀ m : ℕ, n ≤ m →
      ‖Matrix.toEuclideanLin
          (bandProjector A T
            (Set.indicator (Set.Ioi (canonCut lam0 (a : ℕ) (lam0 (e : ℕ)) G δ)) 1) m x)
          (sortedGramEigenbasis A T n x
            ⟨(a : ℕ), lt_of_lt_of_eq a.isLt (Fintype.card_fin d).symm⟩)‖
        ≤ C * Real.exp (-(n : ℝ) * (lam0 (e : ℕ) - lam0 (a : ℕ) - δ)))
    (c₀ : ℝ) (hc₀lo : Real.exp (lam0 (a : ℕ)) < c₀) (hc₀hi : c₀ < Real.exp (lam0 (e : ℕ)))
    (hc₀gap : ∀ i : Fin d, lam0 (i : ℕ) < Real.log c₀ ∨ lam0 (e : ℕ) ≤ lam0 (i : ℕ)) :
    ∀ᶠ n : ℕ in Filter.atTop, ∀ m : ℕ, n ≤ m →
      ‖Matrix.toEuclideanLin (bandProjector A T (Set.indicator (Set.Ioi c₀) 1) m x)
          (sortedGramEigenbasis A T n x
            ⟨(a : ℕ), lt_of_lt_of_eq a.isLt (Fintype.card_fin d).symm⟩)‖
        ≤ C * Real.exp (-(n : ℝ) * (lam0 (e : ℕ) - lam0 (a : ℕ) - δ)) := by
  -- Abbreviations: the canonical slack δ* and the canonical cut κ.
  set δstar : ℝ := canonSlack lam0 (a : ℕ) (lam0 (e : ℕ)) G δ with hδstar_def
  set κ : ℝ := canonCut lam0 (a : ℕ) (lam0 (e : ℕ)) G δ with hκ_def
  -- positivity of c₀
  have hc₀pos : 0 < c₀ := (Real.exp_pos _).trans hc₀lo
  -- log c₀ strictly between lam0 a and lam0 e
  have hloga_lt : lam0 (a : ℕ) < Real.log c₀ := (Real.lt_log_iff_exp_lt hc₀pos).mpr hc₀lo
  have hlogc₀_lt : Real.log c₀ < lam0 (e : ℕ) := (Real.log_lt_iff_lt_exp hc₀pos).mpr hc₀hi
  -- the three positive components of δ*
  have hgap_pos : 0 < lam0 (e : ℕ) - lam0 (a : ℕ) := by linarith
  have hδstar_pos : 0 < δstar := by
    rw [hδstar_def, canonSlack]
    have : (0:ℝ) < (lam0 (e : ℕ) - lam0 (a : ℕ)) / 4 := by linarith
    positivity
  have hδstar_le_G2 : δstar ≤ G / 2 := by
    rw [hδstar_def, canonSlack]
    exact le_trans (min_le_left _ _) (min_le_right _ _)
  have hδstar_le_q : δstar ≤ (lam0 (e : ℕ) - lam0 (a : ℕ)) / 4 := by
    rw [hδstar_def, canonSlack]; exact min_le_right _ _
  -- κ = exp(lam0 e - δ*) > 0 and its log
  have hκpos : 0 < κ := by rw [hκ_def, canonCut]; exact Real.exp_pos _
  have hlogκ : Real.log κ = lam0 (e : ℕ) - δstar := by
    rw [hκ_def, canonCut, ← hδstar_def, Real.log_exp]
  -- log κ strictly between lam0 a and lam0 e
  have hlogκ_lt_e : Real.log κ < lam0 (e : ℕ) := by rw [hlogκ]; linarith
  have hloga_lt_κ : lam0 (a : ℕ) < Real.log κ := by
    rw [hlogκ]; nlinarith [hδstar_le_q]
  -- The same-membership pattern: both cuts agree with the threshold `lam0 e ≤ lam0 j`.
  -- For each `i : Fin d`, classify by `hc₀gap`, then deduce the position of `lam0 i` relative to
  -- both `log c₀` and `log κ`.
  have hclass : ∀ i : Fin d,
      (lam0 (e : ℕ) ≤ lam0 (i : ℕ) ∧ Real.log c₀ < lam0 (i : ℕ) ∧ Real.log κ < lam0 (i : ℕ))
        ∨ (lam0 (i : ℕ) < Real.log c₀ ∧ lam0 (i : ℕ) < Real.log κ
            ∧ lam0 (i : ℕ) < lam0 (e : ℕ)
            ∧ ¬ (lam0 (e : ℕ) ≤ lam0 (i : ℕ))) := by
    intro i
    rcases hc₀gap i with hlo | hhi
    · -- lam0 i < log c₀, so lam0 i < lam0 e ⟹ lam0 i + G ≤ lam0 e
      -- ⟹ lam0 i ≤ lam0 e − G ≤ log κ - G/2
      right
      have hi_lt_e : lam0 (i : ℕ) < lam0 (e : ℕ) := lt_trans hlo hlogc₀_lt
      have hG_bound : lam0 (i : ℕ) + G ≤ lam0 (e : ℕ) := hGgap i e hi_lt_e
      have hi_lt_κ : lam0 (i : ℕ) < Real.log κ := by rw [hlogκ]; linarith
      exact ⟨hlo, hi_lt_κ, hi_lt_e, by linarith⟩
    · -- lam0 e ≤ lam0 i, so log c₀ < lam0 e ≤ lam0 i and log κ < lam0 e ≤ lam0 i
      left
      exact ⟨hhi, lt_of_lt_of_le hlogc₀_lt hhi, lt_of_lt_of_le hlogκ_lt_e hhi⟩
  -- The same-membership equivalence used by `bandMass_eq_of_gap_interior`.
  have hsame : ∀ j : Fin (Fintype.card (Fin d)),
      Real.log c₀ < lam0 (j : ℕ) ↔ Real.log κ < lam0 (j : ℕ) := by
    intro j
    -- recast the Fin (card (Fin d)) index as a Fin d index
    set i : Fin d := ⟨(j : ℕ), lt_of_lt_of_eq j.isLt (Fintype.card_fin d)⟩ with hi_def
    have hij : (i : ℕ) = (j : ℕ) := rfl
    rcases hclass i with ⟨_, h1, h2⟩ | ⟨h1, h2, _, _⟩
    · simp only [hij] at h1 h2; exact ⟨fun _ => h2, fun _ => h1⟩
    · simp only [hij] at h1 h2
      constructor
      · intro hcon; exact absurd hcon (not_lt.mpr (le_of_lt h1))
      · intro hcon; exact absurd hcon (not_lt.mpr (le_of_lt h2))
  -- The per-index separation gaps; each is strictly positive.
  set seps : Fin d → ℝ :=
    fun i => min |Real.log c₀ - lam0 (i : ℕ)| |Real.log κ - lam0 (i : ℕ)| with hseps_def
  have hseps_pos : ∀ i : Fin d, 0 < seps i := by
    intro i
    rw [hseps_def]
    have h0 : 0 < |Real.log c₀ - lam0 (i : ℕ)| := by
      rw [abs_pos]; intro hcon
      rcases hclass i with ⟨_, h1, _⟩ | ⟨h1, _, _, _⟩ <;> linarith [sub_eq_zero.mp hcon]
    have h1 : 0 < |Real.log κ - lam0 (i : ℕ)| := by
      rw [abs_pos]; intro hcon
      rcases hclass i with ⟨_, _, h2⟩ | ⟨_, h2, _, _⟩ <;> linarith [sub_eq_zero.mp hcon]
    exact lt_min h0 h1
  -- η := half the minimum separation over the (nonempty) finite index set.
  have hne : (Finset.univ : Finset (Fin d)).Nonempty := Finset.univ_nonempty
  set η : ℝ := (Finset.univ.inf' hne seps) / 2 with hη_def
  have hinf_pos : 0 < Finset.univ.inf' hne seps := by
    rw [Finset.lt_inf'_iff]; intro i _; exact hseps_pos i
  have hη : 0 < η := by rw [hη_def]; positivity
  have hη_lt : ∀ i : Fin d, η < seps i := by
    intro i
    have hle : Finset.univ.inf' hne seps ≤ seps i := Finset.inf'_le _ (Finset.mem_univ i)
    rw [hη_def]; linarith
  -- η-separation of `log c₀` from every stratum.
  have hsep0 : ∀ j : ℕ, j < d → lam0 j + η < Real.log c₀ ∨ Real.log c₀ < lam0 j - η := by
    intro j hj
    set i : Fin d := ⟨j, hj⟩ with hi_def
    have hηs : η < |Real.log c₀ - lam0 j| :=
      lt_of_lt_of_le (hη_lt i) (by rw [hseps_def]; exact min_le_left _ _)
    rcases le_or_gt (lam0 j) (Real.log c₀) with hle | hlt
    · -- lam0 j ≤ log c₀, abs = log c₀ - lam0 j
      left
      rw [abs_of_nonneg (by linarith)] at hηs; linarith
    · right
      rw [abs_of_neg (by linarith)] at hηs; linarith
  -- η-separation of `log κ` from every stratum.
  have hsep1 : ∀ j : ℕ, j < d → lam0 j + η < Real.log κ ∨ Real.log κ < lam0 j - η := by
    intro j hj
    set i : Fin d := ⟨j, hj⟩ with hi_def
    have hηs : η < |Real.log κ - lam0 j| :=
      lt_of_lt_of_le (hη_lt i) (by rw [hseps_def]; exact min_le_right _ _)
    rcases le_or_gt (lam0 j) (Real.log κ) with hle | hlt
    · left
      rw [abs_of_nonneg (by linarith)] at hηs; linarith
    · right
      rw [abs_of_neg (by linarith)] at hηs; linarith
  -- Produce the localization threshold for this single η.
  obtain ⟨N, hloc⟩ := exists_localized hA x lam0 hconv hη
  -- Combine with the canonical-cut envelope; eventually n ≥ max N 1 and m ≥ n gives m ≥ N, m ≥ 1.
  filter_upwards [hCenv, Filter.eventually_ge_atTop (max N 1)] with n hn hnN
  intro m hm
  have hmN : N ≤ m := le_trans (le_trans (le_max_left N 1) hnN) hm
  have hm1 : 1 ≤ m := le_trans (le_trans (le_max_right N 1) hnN) hm
  -- The band masses at c₀ and κ agree at time m.
  have heq := bandMass_eq_of_gap_interior hA x lam0 hη hloc hc₀pos hκpos hsep0
    hsep1 hsame hmN hm1
    (sortedGramEigenbasis A T n x
      ⟨(a : ℕ), lt_of_lt_of_eq a.isLt (Fintype.card_fin d).symm⟩)
  rw [heq]
  exact hn m hm

/-- **C3 — uniform-`C` transfer (the per-`x` deterministic TopGapMassEnvelope).**  Assembling C2
across the finitely many gap pairs `(a, e)` with a single constant `C` via a `Finset` max over
`Fin d × Fin d` gives `TopGapMassEnvelope A T lam0 x`, given the per-stratum envelopes for all
gap pairs. -/
theorem topGapMassEnvelope_of_perStratum [NeZero d] {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) (x : X) (lam0 : ℕ → ℝ) {G : ℝ} (hG : 0 < G)
    (hGgap : ∀ i j : Fin d, lam0 (i : ℕ) < lam0 (j : ℕ) → lam0 (i : ℕ) + G ≤ lam0 (j : ℕ))
    (hconv : ∀ j : ℕ, j < d → Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues j))
      Filter.atTop (𝓝 (lam0 j)))
    (henv : ∀ a e : Fin d, lam0 (a : ℕ) < lam0 (e : ℕ) →
      PerStratumEnvelope A T lam0 x G a (lam0 (e : ℕ))) :
    TopGapMassEnvelope A T lam0 x := by
  classical
  intro δ hδ
  -- The per-pair canonical-cut constant, built before refining the `∃ C` (so that non-gap pairs
  -- are handled): for a gap pair use the constant produced by the per-stratum envelope; otherwise
  -- `1`.
  set Cp : Fin d × Fin d → ℝ := fun p =>
    if h : lam0 (p.1 : ℕ) < lam0 (p.2 : ℕ) then (henv p.1 p.2 h δ hδ).choose else 1 with hCp
  -- `Fin d × Fin d` is nonempty (NeZero d gives Inhabited (Fin d)).
  have hne : (Finset.univ : Finset (Fin d × Fin d)).Nonempty :=
    ⟨(default, default), Finset.mem_univ _⟩
  set C : ℝ := max 1 (Finset.univ.sup' hne Cp) with hC
  refine ⟨C, le_max_left _ _, ?_⟩
  intro a e hgap c₀ hc₀lo hc₀hi hc₀gap
  -- Spec of the canonical-cut constant for this gap pair (rewrite the `dif`).
  have hCpval : Cp (a, e) = (henv a e hgap δ hδ).choose := by
    simp only [hCp, dif_pos hgap]
  have hspec := (henv a e hgap δ hδ).choose_spec
  obtain ⟨hCp1, hCpenv⟩ := hspec
  -- `Cp (a,e) ≤ C` (sup' over the universe, then bumped by `max`).
  have hle : Cp (a, e) ≤ C := by
    refine le_trans (Finset.le_sup' Cp (Finset.mem_univ (a, e))) ?_
    exact le_max_right _ _
  -- Feed C2 (`topGap_bound_at_cut_of_perStratum`) with the canonical-cut constant `Cp (a,e)`.
  have hbound := topGap_bound_at_cut_of_perStratum (T := T) hA x lam0 hG hGgap hconv a e hgap
    (henv a e hgap) hδ (C := (henv a e hgap δ hδ).choose) hCp1 hCpenv c₀ hc₀lo hc₀hi hc₀gap
  -- Bump the per-pair constant up to `C`.
  filter_upwards [hbound] with n hn m hm
  refine (hn m hm).trans ?_
  refine mul_le_mul_of_nonneg_right ?_ (Real.exp_nonneg _)
  -- `(henv a e hgap δ hδ).choose = Cp (a,e) ≤ C`.
  rw [← hCpval]; exact hle

/-! ### The a.e. wrapper — assembling the target theorem

Collect the a.e. windows (σ-convergence for every `j < d`, tempering) from `hlam0` and
`tendsto_logNorm_orbit_div_atTop_zero`, fix the distinct gap `G` (deterministic), build all
per-stratum envelopes via `perStratumEnvelope_of_lt`, and transfer via
`topGapMassEnvelope_of_perStratum`. -/

/-- The top-gap band-mass envelope `topGapMassEnvelope_ae`: almost everywhere the top-gap
fast-band-mass envelope holds, discharging `htopgap` in
`forward_graded_overlap_of_topGapEnvelope`. -/
theorem topGapMassEnvelope_ae [MeasureTheory.IsProbabilityMeasure μ] [NeZero d]
    (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (lam0 : ℕ → ℝ)
    (hlam0 : ∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
      Filter.atTop (𝓝 (lam0 i))) :
    ∀ᵐ x ∂μ, TopGapMassEnvelope A T lam0 x := by
  -- Deterministic distinct gap.
  obtain ⟨G, hG, hGgap⟩ := exists_distinctGap (d := d) lam0
  -- a.e. tempering.
  have hMP : MeasureTheory.MeasurePreserving T μ μ := hT.toMeasurePreserving
  have hTmeas : Measurable T := hMP.measurable
  have htemp_ae : ∀ᵐ x ∂μ, Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖A (T^[n] x)‖) Filter.atTop (𝓝 0) :=
    tendsto_logNorm_orbit_div_atTop_zero hMP hA hAmeas hTmeas hint hint'
  -- a.e. σ-convergence for all `j < d` simultaneously.
  have hconv_ae : ∀ᵐ x ∂μ, ∀ j : ℕ, j < d → Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues j))
      Filter.atTop (𝓝 (lam0 j)) := by
    filter_upwards [(MeasureTheory.ae_all_iff (ι := Fin d)).2
      (fun j => hlam0 (j : ℕ) j.isLt)] with x hx j hj
    exact hx ⟨j, hj⟩
  filter_upwards [htemp_ae, hconv_ae] with x htemp hconv
  exact topGapMassEnvelope_of_perStratum hA x lam0 hG hGgap hconv
    (fun a e hgap => perStratumEnvelope_of_lt hA x lam0 hG hGgap hconv htemp a (lam0 (e : ℕ))
      hgap ⟨e, rfl⟩)

end ErgodicTheory
