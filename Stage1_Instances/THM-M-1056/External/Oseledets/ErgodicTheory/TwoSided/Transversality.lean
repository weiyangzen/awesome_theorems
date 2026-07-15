/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.TwoSided.Invertible
import ErgodicTheory.TwoSided.StrongExport
import ErgodicTheory.TwoSided.RestrictedExponent

/-!
# The transversality crux of the two-sided Oseledets theorem

This module establishes the **transversality crux** `χ⁺ + χ⁻ ≥ 0`: if a
nonzero vector has forward (restricted) growth rate `≤ a` along the backward orbit and backward
decay rate `≤ b` with `a + b < 0`, then it cannot exist.  Concretely the opposite-sign
sublevels of the forward and backward Oseledets filtrations are transverse, and the resulting
dimension count is the combinatorial input consumed by `reflect_of_counting_and_sum`.

The architecture:

* `inf_eq_bot_of_neg_sum` — the **per-point** crux.  For a forward level family `Vfam` whose
  backward-orbit envelope has limsup `≤ a` and a backward level `Ux` along which a nonzero
  vector decays with limsup `≤ b`, if `a + b < 0` then `Vfam x ⊓ Ux = ⊥`.  The argument writes
  `v = A⁽ⁿ⁾(Sⁿx) · (B⁽ⁿ⁾(x) v)` via the cocycle identity `cocycle_succ'`, uses forward
  equivariance to place `B⁽ⁿ⁾(x) v ∈ Vfam(Sⁿx)`, and bounds
  `log‖v‖ ≤ log‖A⁽ⁿ⁾(Sⁿx)·P‖ + log‖B⁽ⁿ⁾(x) v‖`, whose
  normalized limit is `≤ a + b < 0`, forcing `‖v‖ = 0`.

* `ae_crux` — assembles the per-point crux a.e., for all forward level / backward level pairs
  `(i, s)` with `λᵢ + μₛ < 0`: `V i.castSucc x ⊓ W s.castSucc x = ⊥`.  The envelope comes from
  `ae_tendsto_restricted_backward`, the backward decay from the backward strong
  export (`oseledets_filtration_dims` applied to `(T.symm, backwardGen A T)`), and all the a.e.
  facts are bundled onto a single conull good set; the
  level quantifiers range over finite `Fin k × Fin l`.

* `ae_counting` — the **counting bound**, holding a.e. and hence (being a deterministic
  inequality on the spectra) outright:
  `∀ a b, a + b < 0 → #{j<d | lam0 j ≤ a} + #{j<d | mu0 j ≤ b} ≤ d`.  Thresholds are converted to
  levels via the largest enumerated exponent `≤ a` (resp. `≤ b`), the dimension formula
  `oseledets_filtration_dims` identifies the filtration finranks with the counts, and the
  Grassmann identity `Submodule.finrank_sup_add_finrank_inf_eq` with `V ⊓ W = ⊥` from `ae_crux`
  closes the count.

-/

open MeasureTheory Filter Topology
open scoped Matrix.Norms.L2Operator RealInnerProductSpace

namespace ErgodicTheory

variable {X : Type*} {d : ℕ}

/-! ### The per-point transversality crux -/

section PerPoint

variable [MeasurableSpace X] [NeZero d]

/-- **The per-point transversality crux.**

Let `A` be an everywhere-invertible generator over the invertible system `T : X ≃ᵐ X`, with
backward generator `B = backwardGen A T` running over `S = T.symm`.  Suppose:

* `henv` : the backward-orbit envelope of a forward level family `Vfam` at the point `x` has
  limsup at most `a`, i.e. `limsup (1/n) log ‖A⁽ⁿ⁾(Sⁿx) · P_{Vfam(Sⁿx)}‖ ≤ a` (with the
  sequence bounded above, `henvbdd`);
* `hmem` : forward equivariance places the backward image of any intersection vector into the
  forward level along the backward orbit, `B⁽ⁿ⁾(x) v ∈ Vfam(Sⁿx)`;
* `hdec` : every nonzero intersection vector decays backward with limsup at most `b` (bounded
  above, `hdecbdd`);
* `hsum` : `a + b < 0`.

Then `Vfam x ⊓ Ux = ⊥`.  Indeed for a nonzero `v` in the intersection,
`v = A⁽ⁿ⁾(Sⁿx) · (B⁽ⁿ⁾(x) v)` (the cocycle identity `cocycle_succ'`), so
`log‖v‖ ≤ log ‖A⁽ⁿ⁾(Sⁿx) · P‖ + log ‖B⁽ⁿ⁾(x) v‖`; dividing by `n` and letting `n → ∞` the right
side has limsup `≤ a + b < 0` while the left side tends to `0`, a contradiction. -/
theorem inf_eq_bot_of_neg_sum
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (T : X ≃ᵐ X)
    {Vfam : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))}
    {Ux : Submodule ℝ (EuclideanSpace ℝ (Fin d))} {x : X} {a b : ℝ}
    (henvbdd : IsBoundedUnder (· ≤ ·) atTop
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log
        ‖cocycle A (⇑T) n ((⇑T.symm)^[n] x) * orthProjMatrix (Vfam ((⇑T.symm)^[n] x))‖))
    (henv : limsup (fun n : ℕ => (n : ℝ)⁻¹ * Real.log
        ‖cocycle A (⇑T) n ((⇑T.symm)^[n] x) * orthProjMatrix (Vfam ((⇑T.symm)^[n] x))‖)
      atTop ≤ a)
    (hmem : ∀ v ∈ Vfam x ⊓ Ux, ∀ n : ℕ,
      Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle (backwardGen A T) (⇑T.symm) n x) v
        ∈ Vfam ((⇑T.symm)^[n] x))
    (hdecbdd : ∀ v ∈ Vfam x ⊓ Ux, v ≠ 0 → IsBoundedUnder (· ≤ ·) atTop
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log
        ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle (backwardGen A T) (⇑T.symm) n x) v‖))
    (hdec : ∀ v ∈ Vfam x ⊓ Ux, v ≠ 0 →
      limsup (fun n : ℕ => (n : ℝ)⁻¹ * Real.log
        ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle (backwardGen A T) (⇑T.symm) n x) v‖) atTop ≤ b)
    (hsum : a + b < 0) :
    Vfam x ⊓ Ux = ⊥ := by
  classical
  rw [Submodule.eq_bot_iff]
  intro v hvmem
  by_contra hv0
  -- Abbreviations for the two normalized-log sequences.
  set env : ℕ → ℝ := fun n => (n : ℝ)⁻¹ * Real.log
    ‖cocycle A (⇑T) n ((⇑T.symm)^[n] x) * orthProjMatrix (Vfam ((⇑T.symm)^[n] x))‖ with henvdef
  set wseq : ℕ → EuclideanSpace ℝ (Fin d) :=
    fun n => Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle (backwardGen A T) (⇑T.symm) n x) v with hwdef
  set dec : ℕ → ℝ := fun n => (n : ℝ)⁻¹ * Real.log ‖wseq n‖ with hdecdef
  have hdecbdd' := hdecbdd v hvmem hv0
  have hdec' := hdec v hvmem hv0
  -- The decay sequence value at each `n`.
  have hmemv : ∀ n : ℕ, wseq n ∈ Vfam ((⇑T.symm)^[n] x) := fun n => hmem v hvmem n
  -- `A⁽ⁿ⁾(Sⁿx) · B⁽ⁿ⁾(x) = 1`, so `v = A⁽ⁿ⁾(Sⁿx) · (B⁽ⁿ⁾(x) v)`.
  have hrecon : ∀ n : ℕ,
      Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A (⇑T) n ((⇑T.symm)^[n] x)) (wseq n) = v := by
    intro n
    rw [hwdef]
    simp only
    rw [← ContinuousLinearMap.mul_apply, ← map_mul]
    have hmuleq : cocycle A (⇑T) n ((⇑T.symm)^[n] x)
        * cocycle (backwardGen A T) (⇑T.symm) n x = 1 := by
      rw [cocycle_backwardGen]
      exact Matrix.mul_nonsing_inv _ (Ne.isUnit (det_cocycle_ne_zero hA n _))
    rw [hmuleq, map_one, ContinuousLinearMap.one_apply]
  -- The key per-`n` bound: `‖v‖ ≤ ‖A⁽ⁿ⁾(Sⁿx)·P‖ · ‖wseq n‖`.
  have hkey : ∀ n : ℕ, ‖v‖ ≤
      ‖cocycle A (⇑T) n ((⇑T.symm)^[n] x) * orthProjMatrix (Vfam ((⇑T.symm)^[n] x))‖
        * ‖wseq n‖ := by
    intro n
    set P := orthProjMatrix (Vfam ((⇑T.symm)^[n] x)) with hP
    set N := cocycle A (⇑T) n ((⇑T.symm)^[n] x) with hNdef
    -- `P (wseq n) = wseq n`.
    have hPw : Matrix.toEuclideanCLM (𝕜 := ℝ) P (wseq n) = wseq n := by
      rw [hP, orthProjMatrix, StarAlgEquiv.apply_symm_apply]
      exact Submodule.starProjection_eq_self_iff.mpr (hmemv n)
    -- `v = (N · P) (wseq n)`.
    have hvNP : v = Matrix.toEuclideanCLM (𝕜 := ℝ) (N * P) (wseq n) := by
      rw [map_mul, ContinuousLinearMap.mul_apply, hPw, hrecon n]
    rw [hvNP]
    calc ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (N * P) (wseq n)‖
        ≤ ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (N * P)‖ * ‖wseq n‖ :=
          (Matrix.toEuclideanCLM (𝕜 := ℝ) (N * P)).le_opNorm (wseq n)
      _ = ‖N * P‖ * ‖wseq n‖ := by rw [Matrix.l2_opNorm_toEuclideanCLM]
  -- `wseq n ≠ 0`, so `log‖wseq n‖` is defined and `‖v‖ > 0`.
  have hvpos : 0 < ‖v‖ := norm_pos_iff.mpr hv0
  have hB : ∀ y, (backwardGen A T y).det ≠ 0 := backwardGen_det_ne_zero hA T
  have hwpos : ∀ n : ℕ, 0 < ‖wseq n‖ := by
    intro n
    rw [hwdef]; simp only [norm_pos_iff, ne_eq]
    intro h
    refine cocycle_apply_ne_zero (T := (⇑T.symm)) hB n x hv0 ?_
    rwa [← Matrix.coe_toEuclideanCLM_eq_toEuclideanLin]
  -- Conclude `0 ≤ a + b`, contradicting `hsum`.
  have hfinal : (0 : ℝ) ≤ a + b := by
    -- For each `ε > 0`, eventually `(1/n) log‖v‖ ≤ env n + dec n ≤ (a+ε) + (b+ε)`.
    refine le_of_forall_pos_le_add (fun ε hε => ?_)
    have hε2 : (0 : ℝ) < ε / 2 := by linarith
    -- Eventual envelope bound.
    have henvle : ∀ᶠ n : ℕ in atTop, env n ≤ a + ε / 2 :=
      eventually_lt_of_limsup_lt (lt_of_le_of_lt henv (by linarith)) henvbdd |>.mono
        fun n hn => hn.le
    -- Eventual decay bound.
    have hdecle : ∀ᶠ n : ℕ in atTop, dec n ≤ b + ε / 2 :=
      eventually_lt_of_limsup_lt (lt_of_le_of_lt hdec' (by linarith)) hdecbdd' |>.mono
        fun n hn => hn.le
    -- The normalized log of `‖v‖` tends to `0`.
    have hlogv : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖v‖) atTop (𝓝 0) := by
      have hinv : Tendsto (fun n : ℕ => (n : ℝ)⁻¹) atTop (𝓝 0) :=
        tendsto_natCast_atTop_atTop.inv_tendsto_atTop
      simpa using hinv.mul_const (Real.log ‖v‖)
    -- Eventually `(1/n) log‖v‖ ≤ env n + dec n`.
    have hsplit : ∀ᶠ n : ℕ in atTop,
        (n : ℝ)⁻¹ * Real.log ‖v‖ ≤ env n + dec n := by
      filter_upwards [eventually_ge_atTop 1] with n hn
      have hnpos : (0 : ℝ) < (n : ℝ) := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hn
      have hninv : (0 : ℝ) ≤ (n : ℝ)⁻¹ := by positivity
      have hNPpos : 0 < ‖cocycle A (⇑T) n ((⇑T.symm)^[n] x)
          * orthProjMatrix (Vfam ((⇑T.symm)^[n] x))‖ := by
        have hprod : 0 < ‖cocycle A (⇑T) n ((⇑T.symm)^[n] x)
            * orthProjMatrix (Vfam ((⇑T.symm)^[n] x))‖ * ‖wseq n‖ :=
          lt_of_lt_of_le hvpos (hkey n)
        have hwn := hwpos n
        nlinarith [norm_nonneg (cocycle A (⇑T) n ((⇑T.symm)^[n] x)
          * orthProjMatrix (Vfam ((⇑T.symm)^[n] x)))]
      have hloglev : Real.log ‖v‖
          ≤ Real.log ‖cocycle A (⇑T) n ((⇑T.symm)^[n] x)
              * orthProjMatrix (Vfam ((⇑T.symm)^[n] x))‖ + Real.log ‖wseq n‖ := by
        have hle := Real.log_le_log hvpos (hkey n)
        rwa [Real.log_mul (ne_of_gt hNPpos) (ne_of_gt (hwpos n))] at hle
      rw [henvdef, hdecdef]
      simp only
      rw [← mul_add]
      exact mul_le_mul_of_nonneg_left hloglev hninv
    -- Combine: eventually `(1/n) log‖v‖ ≤ (a+b) + ε`.
    have hcomb : ∀ᶠ n : ℕ in atTop,
        (n : ℝ)⁻¹ * Real.log ‖v‖ ≤ (a + b) + ε := by
      filter_upwards [hsplit, henvle, hdecle] with n h1 h2 h3
      calc (n : ℝ)⁻¹ * Real.log ‖v‖ ≤ env n + dec n := h1
        _ ≤ (a + ε / 2) + (b + ε / 2) := add_le_add h2 h3
        _ = (a + b) + ε := by ring
    -- Take the limit on the left.
    have hle0 : (0 : ℝ) ≤ (a + b) + ε :=
      le_of_tendsto_of_tendsto hlogv tendsto_const_nhds hcomb
    linarith
  linarith

end PerPoint

/-! ### The a.e. crux and the counting bound -/

section AeMain

variable [MeasurableSpace X] [NeZero d] {μ : Measure X} [IsProbabilityMeasure μ] {T : X ≃ᵐ X}

omit [NeZero d] in
/-- Membership equivariance along the backward orbit, derived from forward equivariance.
If `B⁽ᵏ⁾(x) v ∈ Vfam(Sᵏx)` is to be shown for all `k`, it suffices to know one-step
equivariance of `A`/`Vfam` along the backward orbit (the projection-conjugation form) together
with `v ∈ Vfam x`. -/
theorem mem_iterate_backward_of_orbit
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0)
    {Vfam : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} {x : X}
    (hmap : ∀ m : ℕ, Submodule.map
      (Matrix.toEuclideanCLM (𝕜 := ℝ) (A ((⇑T.symm)^[m + 1] x))).toLinearMap
        (Vfam ((⇑T.symm)^[m + 1] x)) = Vfam ((⇑T.symm)^[m] x))
    {v : EuclideanSpace ℝ (Fin d)} (hv : v ∈ Vfam x) (n : ℕ) :
    Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle (backwardGen A T) (⇑T.symm) n x) v
      ∈ Vfam ((⇑T.symm)^[n] x) := by
  induction n with
  | zero => simpa using hv
  | succ n ih =>
    -- `B⁽ⁿ⁺¹⁾(x) = B(Sⁿx) · B⁽ⁿ⁾(x)`; the new factor `B(Sⁿx) = (A(S^{n+1}x))⁻¹` carries
    -- `Vfam(Sⁿx)` into `Vfam(S^{n+1}x)`.
    rw [cocycle_succ' (backwardGen A T) (⇑T.symm) n x, map_mul, ContinuousLinearMap.mul_apply]
    set w := Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle (backwardGen A T) (⇑T.symm) n x) v with hw
    have hwmem : w ∈ Vfam ((⇑T.symm)^[n] x) := ih
    -- `B(Sⁿx) = (A(S^{n+1}x))⁻¹` and `A(S^{n+1}x) · Vfam(S^{n+1}x) = Vfam(Sⁿx)`,
    -- so `(A(S^{n+1}x))⁻¹ · Vfam(Sⁿx) = Vfam(S^{n+1}x)`.
    have hBeq : backwardGen A T ((⇑T.symm)^[n] x) = (A ((⇑T.symm)^[n + 1] x))⁻¹ := by
      rw [backwardGen, ← Function.iterate_succ_apply' (⇑T.symm) n x]
    -- The image of `w` under `(A(S^{n+1}x))⁻¹` lies in `Vfam(S^{n+1}x)`.
    rw [hBeq]
    set M := A ((⇑T.symm)^[n + 1] x) with hM
    have hMdet : M.det ≠ 0 := hA ((⇑T.symm)^[n + 1] x)
    -- `M` maps `Vfam(S^{n+1}x)` onto `Vfam(Sⁿx)`; pull `w` back.
    have hmapn := hmap n
    rw [← hM] at hmapn
    -- `w ∈ Vfam(Sⁿx) = M · Vfam(S^{n+1}x)`, so `w = M u` for some `u ∈ Vfam(S^{n+1}x)`,
    -- hence `M⁻¹ w = u ∈ Vfam(S^{n+1}x)`.
    rw [← hmapn] at hwmem
    obtain ⟨u, hu, hMu⟩ := hwmem
    rw [ContinuousLinearMap.coe_coe] at hMu
    have hMinvw : Matrix.toEuclideanCLM (𝕜 := ℝ) M⁻¹ w = u := by
      rw [← hMu, ← ContinuousLinearMap.mul_apply, ← map_mul,
        Matrix.nonsing_inv_mul _ (Ne.isUnit hMdet), map_one, ContinuousLinearMap.one_apply]
    rw [hMinvw]; exact hu

/-- **The backward-orbit envelope converges (a.e.).**  For the forward Oseledets level
`Vᵢ = V i.castSucc`, the floor-absorbed restricted operator norm along the backward orbit
converges to the Lyapunov exponent `λᵢ`:
`(1/n) log ‖A⁽ⁿ⁾(Sⁿx) · P_{Vᵢ(Sⁿx)}‖ → λᵢ` a.e.

This is the convergent form of the backward-orbit envelope (`limsup ≤ λᵢ`): it is obtained from
the backward Kingman limit `restLog_backward_kingman` (shared constant `c`), the identification
`c = λᵢ` (`restricted_const_eq`), and the floor absorption along the backward orbit
(`restLog_eq_on_good`).  The convergence supplies both the `IsBoundedUnder` proviso that the crux
needs and the rate bound itself (via `limsup_eq`). -/
theorem ae_tendsto_restricted_backward
    (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0)
    (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (lam0 : ℕ → ℝ)
    (V : Fin (numExp lam0 d + 1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin d)))
    (hVmeas : ∀ i, MeasurableSubspace fun x => V i x)
    (hVae : ∀ᵐ x ∂μ,
      V 0 x = ⊤ ∧ V (Fin.last (numExp lam0 d)) x = ⊥ ∧
      (∀ i : Fin (numExp lam0 d), V i.succ x < V i.castSucc x) ∧
      (∀ i : Fin (numExp lam0 d + 1),
        Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap (V i x)
          = V i ((⇑T) x)) ∧
      (∀ i : Fin (numExp lam0 d),
        ∀ v ∈ (V i.castSucc x : Set (EuclideanSpace ℝ (Fin d))), v ∉ V i.succ x →
          Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
            Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A (⇑T) n x) v‖)
            atTop (𝓝 (expEnum lam0 d i))))
    (i : Fin (numExp lam0 d)) :
    ∀ᵐ x ∂μ, Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log
      ‖cocycle A (⇑T) n ((⇑T.symm)^[n] x) * orthProjMatrix (V i.castSucc ((⇑T.symm)^[n] x))‖)
      atTop (𝓝 (expEnum lam0 d i)) := by
  classical
  have hmp : MeasurePreserving T μ μ := hT.toMeasurePreserving
  set Vi : X → Submodule ℝ (EuclideanSpace ℝ (Fin d)) := fun x => V i.castSucc x with hVi
  obtain ⟨c, _hcmean, hcfwd, hcbwd⟩ :=
    restLog_backward_kingman hT hA hAmeas (hVmeas i.castSucc) hint hint'
  have hceq : c = expEnum lam0 d i :=
    restricted_const_eq hT hA lam0 V hVae i c hcfwd
  have hmapVi_ae : ∀ᵐ x ∂μ, Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap
      (Vi x) = Vi (T x) := by
    filter_upwards [hVae] with x hx; exact hx.2.2.2.1 i.castSucc
  have hVne_ae : ∀ᵐ x ∂μ, Vi x ≠ ⊥ := by
    filter_upwards [hVae] with x hx
    intro hbot
    have hlt := hx.2.2.1 i
    rw [show V i.castSucc x = Vi x from rfl, hbot] at hlt
    exact absurd hlt (by simp)
  have horbit : ∀ᵐ x ∂μ, ∀ k : ℕ,
      Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A (T^[k] x))).toLinearMap
        (Vi (T^[k] x)) = Vi (T (T^[k] x)) :=
    ae_forall_iterate_of_ae hmp _ hmapVi_ae
  have hGood : ∀ᵐ x ∂μ, Vi x ≠ ⊥ ∧ ∀ k : ℕ,
      Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A (T^[k] x))).toLinearMap
        (Vi (T^[k] x)) = Vi (T (T^[k] x)) := by
    filter_upwards [hVne_ae, horbit] with x h1 h2 using ⟨h1, h2⟩
  have hGoodbwd : ∀ᵐ x ∂μ, ∀ m : ℕ, Vi ((⇑T.symm)^[m] x) ≠ ⊥ ∧ ∀ k : ℕ,
      Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A (T^[k] ((⇑T.symm)^[m] x)))).toLinearMap
        (Vi (T^[k] ((⇑T.symm)^[m] x))) = Vi (T (T^[k] ((⇑T.symm)^[m] x))) :=
    ae_forall_iterate_of_ae (hmp.symm T) _ hGood
  filter_upwards [hcbwd, hGoodbwd] with x hxc hxgood
  have hcongr : (fun n : ℕ => (n : ℝ)⁻¹ * restLog A Vi (⇑T) n ((⇑T.symm)^[n] x))
      =ᶠ[atTop] fun n : ℕ => (n : ℝ)⁻¹ * Real.log
        ‖cocycle A (⇑T) n ((⇑T.symm)^[n] x) * orthProjMatrix (Vi ((⇑T.symm)^[n] x))‖ := by
    filter_upwards [eventually_ge_atTop 1] with n hn
    obtain ⟨m, rfl⟩ := Nat.exists_eq_add_of_lt (Nat.lt_of_lt_of_le Nat.zero_lt_one hn)
    rw [Nat.zero_add]
    congr 1
    obtain ⟨hVy, hmapy⟩ := hxgood (m + 1)
    exact restLog_eq_on_good hA
      (fun k => orthProj_equivariant_of_map (T := (⇑T)) (V := Vi) (hmapy k)) hVy m
  rw [← hceq]
  exact hxc.congr' hcongr

/-- **The a.e. transversality crux.**

For the forward Oseledets filtration `V` (with exponents `expEnum lam0 d`) of the system
`(T, A)` and the backward Oseledets filtration `W` (with exponents `expEnum mu0 d`) of the
backward system `(T.symm, backwardGen A T)`, at a.e. `x` the opposite-sign interior sublevels
are transverse: for every forward level `i` and backward level `s` with
`λᵢ + μₛ < 0`, `V i.castSucc x ⊓ W s.castSucc x = ⊥`.

The proof bundles, on a single conull set, the backward-orbit envelope
(`ae_tendsto_restricted_backward`, which supplies both the `limsup ≤ λᵢ` bound and the
`IsBoundedUnder` proviso), the forward equivariance along the backward
orbit (`ae_forall_iterate_of_ae` over `T.symm` + `mem_iterate_backward_of_orbit`), and the
backward growth limits (the backward strong-export growth clause + flag descent
`exists_stratum`), then applies the per-point crux `inf_eq_bot_of_neg_sum`.  All quantifiers
over levels range over the finite types `Fin (numExp lam0 d)` and `Fin (numExp mu0 d)`. -/
theorem ae_crux
    (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0)
    (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (lam0 mu0 : ℕ → ℝ)
    (V : Fin (numExp lam0 d + 1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin d)))
    (W : Fin (numExp mu0 d + 1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin d)))
    (hVmeas : ∀ i, MeasurableSubspace fun x => V i x)
    (hVae : ∀ᵐ x ∂μ,
      V 0 x = ⊤ ∧ V (Fin.last (numExp lam0 d)) x = ⊥ ∧
      (∀ i : Fin (numExp lam0 d), V i.succ x < V i.castSucc x) ∧
      (∀ i : Fin (numExp lam0 d + 1),
        Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap (V i x)
          = V i ((⇑T) x)) ∧
      (∀ i : Fin (numExp lam0 d),
        ∀ v ∈ (V i.castSucc x : Set (EuclideanSpace ℝ (Fin d))), v ∉ V i.succ x →
          Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
            Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A (⇑T) n x) v‖)
            atTop (𝓝 (expEnum lam0 d i))))
    (hWae : ∀ᵐ x ∂μ,
      W 0 x = ⊤ ∧ W (Fin.last (numExp mu0 d)) x = ⊥ ∧
      (∀ s : Fin (numExp mu0 d), W s.succ x < W s.castSucc x) ∧
      (∀ s : Fin (numExp mu0 d),
        ∀ v ∈ (W s.castSucc x : Set (EuclideanSpace ℝ (Fin d))), v ∉ W s.succ x →
          Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log
            ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle (backwardGen A T) (⇑T.symm) n x) v‖)
            atTop (𝓝 (expEnum mu0 d s)))) :
    ∀ᵐ x ∂μ, ∀ (i : Fin (numExp lam0 d)) (s : Fin (numExp mu0 d)),
      expEnum lam0 d i + expEnum mu0 d s < 0 →
      V i.castSucc x ⊓ W s.castSucc x = ⊥ := by
  classical
  have hmp : MeasurePreserving T μ μ := hT.toMeasurePreserving
  -- The backward-orbit envelope convergence for every forward level, bundled a.e.
  have henvT : ∀ᵐ x ∂μ, ∀ i : Fin (numExp lam0 d),
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log
        ‖cocycle A (⇑T) n ((⇑T.symm)^[n] x)
          * orthProjMatrix (V i.castSucc ((⇑T.symm)^[n] x))‖)
        atTop (𝓝 (expEnum lam0 d i)) := by
    rw [ae_all_iff]
    exact fun i => ae_tendsto_restricted_backward hT hA hAmeas hint hint' lam0 V hVmeas hVae i
  -- The forward equivariance along the backward orbit, bundled a.e.
  have hmapAll_ae : ∀ᵐ x ∂μ, ∀ (i : Fin (numExp lam0 d)) (m : ℕ),
      Submodule.map
        (Matrix.toEuclideanCLM (𝕜 := ℝ) (A ((⇑T.symm)^[m + 1] x))).toLinearMap
        (V i.castSucc ((⇑T.symm)^[m + 1] x)) = V i.castSucc ((⇑T.symm)^[m] x) := by
    -- One-step equivariance a.e.; transport along the backward orbit.
    have hstep : ∀ᵐ x ∂μ, ∀ i : Fin (numExp lam0 d),
        Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A (T.symm x))).toLinearMap
          (V i.castSucc (T.symm x)) = V i.castSucc x := by
      have hmap_ae : ∀ᵐ y ∂μ, ∀ i : Fin (numExp lam0 d),
          Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A y)).toLinearMap
            (V i.castSucc y) = V i.castSucc (T y) := by
        filter_upwards [hVae] with y hy i; exact hy.2.2.2.1 i.castSucc
      have hSmp : MeasurePreserving (⇑T.symm) μ μ := hmp.symm T
      filter_upwards [hSmp.quasiMeasurePreserving.ae hmap_ae] with x hx i
      have := hx i
      rwa [T.apply_symm_apply] at this
    -- Iterate the one-step fact along the backward orbit.
    have hSmp : MeasurePreserving (⇑T.symm) μ μ := hmp.symm T
    have hiter : ∀ᵐ x ∂μ, ∀ (m : ℕ) (i : Fin (numExp lam0 d)),
        Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A (T.symm ((⇑T.symm)^[m] x)))).toLinearMap
          (V i.castSucc (T.symm ((⇑T.symm)^[m] x))) = V i.castSucc ((⇑T.symm)^[m] x) :=
      ae_forall_iterate_of_ae hSmp _ hstep
    filter_upwards [hiter] with x hx i m
    have h := hx m i
    rwa [← Function.iterate_succ_apply' (⇑T.symm) m x] at h
  -- Assemble the crux on the common conull set.
  filter_upwards [henvT, hmapAll_ae, hWae] with x hxenv hxmap hxW i s hsum
  -- The backward decay rate for `Wₛ` is `μₛ`, attained on the relevant stratum.
  obtain ⟨_hW0, _hWlast, hWstrict, hWgrow⟩ := hxW
  have hWanti : Antitone fun j => W j x :=
    (Fin.strictAnti_iff_succ_lt.mpr hWstrict).antitone
  -- The per-point crux ingredients.
  set Vfam : X → Submodule ℝ (EuclideanSpace ℝ (Fin d)) := fun y => V i.castSucc y with hVfam
  -- Envelope at rate `λᵢ`.
  have henv_t := hxenv i
  have henvbdd : IsBoundedUnder (· ≤ ·) atTop
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log
        ‖cocycle A (⇑T) n ((⇑T.symm)^[n] x) * orthProjMatrix (Vfam ((⇑T.symm)^[n] x))‖) :=
    henv_t.isBoundedUnder_le
  have henv : limsup (fun n : ℕ => (n : ℝ)⁻¹ * Real.log
      ‖cocycle A (⇑T) n ((⇑T.symm)^[n] x) * orthProjMatrix (Vfam ((⇑T.symm)^[n] x))‖)
      atTop ≤ expEnum lam0 d i := le_of_eq henv_t.limsup_eq
  -- Membership equivariance along the backward orbit.
  have hmem : ∀ v ∈ Vfam x ⊓ W s.castSucc x, ∀ n : ℕ,
      Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle (backwardGen A T) (⇑T.symm) n x) v
        ∈ Vfam ((⇑T.symm)^[n] x) := by
    intro v hv n
    exact mem_iterate_backward_of_orbit (T := T) hA (fun m => hxmap i m)
      (Submodule.mem_inf.mp hv).1 n
  -- Backward decay limit (Tendsto to a stratum value `≤ μₛ`).
  have hdecdata : ∀ v ∈ Vfam x ⊓ W s.castSucc x, v ≠ 0 →
      ∃ t : ℝ, t ≤ expEnum mu0 d s ∧ Tendsto
        (fun n : ℕ => (n : ℝ)⁻¹ * Real.log
          ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle (backwardGen A T) (⇑T.symm) n x) v‖)
        atTop (𝓝 t) := by
    intro v hv hv0
    have hvW : v ∈ W s.castSucc x := (Submodule.mem_inf.mp hv).2
    obtain ⟨u, hu⟩ := exists_stratum hWanti _hW0 _hWlast hv0
    have huW : v ∈ W u.castSucc x := (hu u.castSucc).mpr (by simp)
    have hunot : v ∉ W u.succ x := fun h => by
      have h' := (hu u.succ).mp h; rw [Fin.val_succ] at h'; omega
    refine ⟨expEnum mu0 d u, ?_, hWgrow u v huW hunot⟩
    -- `v ∈ Wₛ` ⟹ stratum `u ≥ s` ⟹ `μᵤ ≤ μₛ`.
    have hsu : (s : ℕ) ≤ (u : ℕ) := by
      have h' := (hu s.castSucc).mp hvW; simpa using h'
    exact (expEnum_strictAnti mu0 d).antitone (by exact_mod_cast hsu)
  have hdecbdd : ∀ v ∈ Vfam x ⊓ W s.castSucc x, v ≠ 0 → IsBoundedUnder (· ≤ ·) atTop
      (fun n : ℕ => (n : ℝ)⁻¹ * Real.log
        ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle (backwardGen A T) (⇑T.symm) n x) v‖) := by
    intro v hv hv0
    obtain ⟨_t, _, ht⟩ := hdecdata v hv hv0
    exact ht.isBoundedUnder_le
  have hdec : ∀ v ∈ Vfam x ⊓ W s.castSucc x, v ≠ 0 →
      limsup (fun n : ℕ => (n : ℝ)⁻¹ * Real.log
        ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle (backwardGen A T) (⇑T.symm) n x) v‖) atTop
        ≤ expEnum mu0 d s := by
    intro v hv hv0
    obtain ⟨t, htle, ht⟩ := hdecdata v hv hv0
    rw [ht.limsup_eq]; exact htle
  exact inf_eq_bot_of_neg_sum hA T henvbdd henv hmem hdecbdd hdec hsum

end AeMain

/-! ### Threshold-to-level conversion and the counting bound -/

section Counting

/-- **Threshold-to-level conversion.**  If the sublevel count `#{j < d | p j ≤ a}` of an
enumeration `p` is positive, then there is a distinct-exponent level `i` whose value is `≤ a`
and whose sublevel count agrees with the count at `a` (no realized `p`-value lies strictly
between `expEnum p d i` and `a`). -/
theorem exists_level_eq_countLe {p : ℕ → ℝ} {a : ℝ}
    (hpos : 0 < ((Finset.range d).filter (fun j => p j ≤ a)).card) :
    ∃ i : Fin (numExp p d), expEnum p d i ≤ a ∧
      ((Finset.range d).filter (fun j => p j ≤ a)).card
        = ((Finset.range d).filter (fun j => p j ≤ expEnum p d i)).card := by
  classical
  -- Some `p j ≤ a` with `j < d`.
  obtain ⟨j, hjmem⟩ := Finset.card_pos.mp hpos
  rw [Finset.mem_filter, Finset.mem_range] at hjmem
  obtain ⟨hjd, hja⟩ := hjmem
  -- The nonempty set of realized values `≤ a`.
  set D : Finset ℝ := (distinctExp p d).filter (fun r => r ≤ a) with hD
  have hpj : p j ∈ D := by
    rw [hD, Finset.mem_filter]
    exact ⟨(mem_distinctExp p d).mpr ⟨j, hjd, rfl⟩, hja⟩
  have hDne : D.Nonempty := ⟨p j, hpj⟩
  set m := D.max' hDne with hm
  have hmmem : m ∈ D := D.max'_mem hDne
  rw [hD, Finset.mem_filter] at hmmem
  obtain ⟨hmdist, hma⟩ := hmmem
  -- `m = p j'` for some `j' < d`, giving a level `i` with `expEnum p d i = m`.
  obtain ⟨j', hj'd, hj'm⟩ := (mem_distinctExp p d).mp hmdist
  obtain ⟨i, hi⟩ := exists_expEnum_eq p hj'd
  rw [hj'm] at hi
  refine ⟨i, by rw [hi]; exact hma, ?_⟩
  -- The two filters coincide.
  rw [hi]
  congr 1
  ext k
  simp only [Finset.mem_filter, Finset.mem_range, and_congr_right_iff]
  intro hkd
  constructor
  · intro hka
    -- `p k ≤ a` ⟹ `p k` is a realized value `≤ a` ⟹ `p k ≤ m`.
    have hpkD : p k ∈ D := by
      rw [hD, Finset.mem_filter]
      exact ⟨(mem_distinctExp p d).mpr ⟨k, hkd, rfl⟩, hka⟩
    exact D.le_max' _ hpkD
  · intro hkm
    exact le_trans hkm hma

variable [MeasurableSpace X] {μ : Measure X} [IsProbabilityMeasure μ]

/-- **The counting bound.**  At a.e. `x` — hence (being a deterministic inequality on the
spectra) outright — for all thresholds `a, b` with `a + b < 0`,
`#{j < d | lam0 j ≤ a} + #{j < d | mu0 j ≤ b} ≤ d`.

The bound is the combinatorial input consumed by `reflect_of_counting_and_sum`.
Each positive count is realized by a forward (resp. backward) interior level via
`exists_level_eq_countLe`, the dimension formula `oseledets_filtration_dims` identifies the
filtration finrank with the count, and the Grassmann identity
`Submodule.finrank_sup_add_finrank_inf_eq` with the crux
`V i.castSucc x ⊓ W s.castSucc x = ⊥` (from `ae_crux`) bounds the sum by
`finrank (V ⊔ W) ≤ d`. -/
theorem ae_counting
    (lam0 mu0 : ℕ → ℝ)
    (V : Fin (numExp lam0 d + 1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin d)))
    (W : Fin (numExp mu0 d + 1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin d)))
    (hVdim : ∀ᵐ x ∂μ, ∀ i : Fin (numExp lam0 d),
      Module.finrank ℝ (V i.castSucc x)
        = ((Finset.range d).filter (fun j => lam0 j ≤ expEnum lam0 d i)).card)
    (hWdim : ∀ᵐ x ∂μ, ∀ s : Fin (numExp mu0 d),
      Module.finrank ℝ (W s.castSucc x)
        = ((Finset.range d).filter (fun j => mu0 j ≤ expEnum mu0 d s)).card)
    (hcrux : ∀ᵐ x ∂μ, ∀ (i : Fin (numExp lam0 d)) (s : Fin (numExp mu0 d)),
      expEnum lam0 d i + expEnum mu0 d s < 0 →
      V i.castSucc x ⊓ W s.castSucc x = ⊥) :
    ∀ a b : ℝ, a + b < 0 →
      ((Finset.range d).filter (fun j => lam0 j ≤ a)).card
        + ((Finset.range d).filter (fun j => mu0 j ≤ b)).card ≤ d := by
  classical
  -- Extract a single conull point at which the three a.e. facts hold.
  obtain ⟨x, hVx, hWx, hcx⟩ : ∃ x, (∀ i : Fin (numExp lam0 d),
      Module.finrank ℝ (V i.castSucc x)
        = ((Finset.range d).filter (fun j => lam0 j ≤ expEnum lam0 d i)).card)
      ∧ (∀ s : Fin (numExp mu0 d),
        Module.finrank ℝ (W s.castSucc x)
          = ((Finset.range d).filter (fun j => mu0 j ≤ expEnum mu0 d s)).card)
      ∧ (∀ (i : Fin (numExp lam0 d)) (s : Fin (numExp mu0 d)),
        expEnum lam0 d i + expEnum mu0 d s < 0 →
        V i.castSucc x ⊓ W s.castSucc x = ⊥) :=
    (hVdim.and (hWdim.and hcrux)).exists
  intro a b hab
  set cntA := ((Finset.range d).filter (fun j => lam0 j ≤ a)).card with hcntA
  set cntB := ((Finset.range d).filter (fun j => mu0 j ≤ b)).card with hcntB
  -- The two counts are always `≤ d`.
  have hcntBle : cntB ≤ d := by
    rw [hcntB]
    calc ((Finset.range d).filter (fun j => mu0 j ≤ b)).card
        ≤ (Finset.range d).card := Finset.card_filter_le _ _
      _ = d := Finset.card_range d
  have hcntAle : cntA ≤ d := by
    rw [hcntA]
    calc ((Finset.range d).filter (fun j => lam0 j ≤ a)).card
        ≤ (Finset.range d).card := Finset.card_filter_le _ _
      _ = d := Finset.card_range d
  rcases Nat.eq_zero_or_pos cntA with hA0 | hApos
  · rw [hA0]; simpa using hcntBle
  rcases Nat.eq_zero_or_pos cntB with hB0 | hBpos
  · rw [hB0]; simpa using hcntAle
  -- Both counts positive: convert to levels.
  obtain ⟨i, hila, hicount⟩ := exists_level_eq_countLe (p := lam0) (a := a) (d := d) hApos
  obtain ⟨s, hsmu, hscount⟩ := exists_level_eq_countLe (p := mu0) (a := b) (d := d) hBpos
  have hsumlt : expEnum lam0 d i + expEnum mu0 d s < 0 := by
    have : expEnum lam0 d i + expEnum mu0 d s ≤ a + b := add_le_add hila hsmu
    linarith
  have hbot : (V i.castSucc x ⊓ W s.castSucc x : Submodule ℝ (EuclideanSpace ℝ (Fin d))) = ⊥ :=
    hcx i s hsumlt
  -- Grassmann: `finrank V + finrank W = finrank (V ⊔ W) + finrank (V ⊓ W) ≤ d + 0`.
  have hgrass := Submodule.finrank_sup_add_finrank_inf_eq (V i.castSucc x) (W s.castSucc x)
  rw [hbot, finrank_bot] at hgrass
  have hsuple : Module.finrank ℝ (V i.castSucc x) + Module.finrank ℝ (W s.castSucc x) ≤ d := by
    rw [← hgrass, add_zero]
    refine le_trans (Submodule.finrank_le _) ?_
    rw [finrank_euclideanSpace_fin]
  -- Identify the counts with the filtration finranks.
  have hicount' : cntA = Module.finrank ℝ (V i.castSucc x) := by
    rw [hcntA, hicount, hVx i]
  have hscount' : cntB = Module.finrank ℝ (W s.castSucc x) := by
    rw [hcntB, hscount, hWx s]
  -- `cntA + cntB = finrank V + finrank W ≤ d`.
  rw [hicount', hscount']
  exact hsuple

end Counting

end ErgodicTheory
