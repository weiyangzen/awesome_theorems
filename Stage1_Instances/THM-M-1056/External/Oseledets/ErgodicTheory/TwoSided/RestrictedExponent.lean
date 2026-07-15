/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.TwoSided.RestrictedCocycle
import ErgodicTheory.TwoSided.StrongExport
import ErgodicTheory.Lyapunov.Forward

/-!
# The restricted Lyapunov exponent (two-sided MET)

This module identifies the **restricted Kingman constant** of the restricted cocycle
`restGen A V x = A x · P_{V x}` on the forward Oseledets level `V := Vᵢ`, showing it equals the
Lyapunov exponent `λᵢ = expEnum lam0 d i`.

The architecture:

* `exists_stratum` — every nonzero `v ∈ Vᵢ(x)` lies in a stratum `j ≥ i` of the flag
  (pure order logic on the `oseledets_filtration_dims` flag), so its growth rate `≤ λᵢ`.
* `restricted_const_eq` — the Kingman constant `c` of `restLog A V T` (`restLog_kingman`)
  equals `λᵢ`.  Both bounds are evaluated at the base point through the
  floor-absorbed identity `restLog_eq_on_good`:
  the `≥` direction uses a stratum witness, the `≤` direction the orthonormal-basis
  bound `‖A⁽ⁿ⁾ · P‖ ≤ Σⱼ ‖A⁽ⁿ⁾ eⱼ‖` (`norm_mul_orthProj_le_sum`).

-/

open MeasureTheory Filter Topology
open scoped Matrix.Norms.L2Operator RealInnerProductSpace

namespace ErgodicTheory

variable {X : Type*} {d : ℕ}

/-! ### The orthonormal-basis norm bound -/

/-- **Basis bound for the restricted operator.** For a subspace `K` with orthonormal basis
`e = stdOrthonormalBasis ℝ K`, the restricted-operator norm is bounded by the sum of the
norms of the images of the basis vectors: `‖M · P_K‖ ≤ Σⱼ ‖M eⱼ‖`. The proof bounds
`‖(M·P_K) w‖` for unit `w` by expanding `P_K w` in the basis and using Bessel
(`|⟪eⱼ, P_K w⟫| ≤ ‖w‖`). -/
theorem norm_mul_orthProj_le_sum {M : Matrix (Fin d) (Fin d) ℝ}
    (K : Submodule ℝ (EuclideanSpace ℝ (Fin d))) :
    ‖M * orthProjMatrix K‖
      ≤ ∑ j, ‖Matrix.toEuclideanCLM (𝕜 := ℝ) M
          ((stdOrthonormalBasis ℝ K) j : EuclideanSpace ℝ (Fin d))‖ := by
  set b := stdOrthonormalBasis ℝ K with hb
  rw [← Matrix.l2_opNorm_toEuclideanCLM]
  refine ContinuousLinearMap.opNorm_le_bound _
    (Finset.sum_nonneg fun j _ => norm_nonneg _) (fun w => ?_)
  rw [map_mul]
  simp only [ContinuousLinearMap.mul_apply]
  set u : EuclideanSpace ℝ (Fin d) :=
    Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix K) w with hu
  have huK : u ∈ K := by
    change Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix K) w ∈ K
    rw [orthProjMatrix, StarAlgEquiv.apply_symm_apply]
    exact K.starProjection_apply_mem w
  have hunorm : ‖u‖ ≤ ‖w‖ := by
    change ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix K) w‖ ≤ ‖w‖
    have hP1 : ‖orthProjMatrix K‖ ≤ 1 := by
      rw [← Matrix.l2_opNorm_toEuclideanCLM, orthProjMatrix, StarAlgEquiv.apply_symm_apply]
      exact K.starProjection_norm_le
    calc ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix K) w‖
        ≤ ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix K)‖ * ‖w‖ :=
          (Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix K)).le_opNorm w
      _ ≤ 1 * ‖w‖ := by
          rw [Matrix.l2_opNorm_toEuclideanCLM]; gcongr
      _ = ‖w‖ := one_mul _
  set uK : K := ⟨u, huK⟩ with huK'
  have hexp : u = ∑ j, (inner ℝ (b j) uK : ℝ) • (b j : EuclideanSpace ℝ (Fin d)) := by
    have hr : ∑ j, (inner ℝ (b j) uK : ℝ) • b j = uK := b.sum_repr' uK
    have h2 := congrArg (Submodule.subtype K) hr
    rw [map_sum] at h2
    simp only [map_smul, Submodule.coe_subtype] at h2
    exact h2.symm
  have hMu : Matrix.toEuclideanCLM (𝕜 := ℝ) M u
      = ∑ j, (inner ℝ (b j) uK : ℝ) •
          Matrix.toEuclideanCLM (𝕜 := ℝ) M (b j : EuclideanSpace ℝ (Fin d)) := by
    conv_lhs => rw [hexp]
    rw [map_sum]
    simp only [map_smul]
  change ‖Matrix.toEuclideanCLM (𝕜 := ℝ) M u‖ ≤ _
  rw [hMu]
  calc ‖∑ j, (inner ℝ (b j) uK : ℝ) •
          Matrix.toEuclideanCLM (𝕜 := ℝ) M (b j : EuclideanSpace ℝ (Fin d))‖
      ≤ ∑ j, ‖(inner ℝ (b j) uK : ℝ) •
          Matrix.toEuclideanCLM (𝕜 := ℝ) M (b j : EuclideanSpace ℝ (Fin d))‖ := norm_sum_le _ _
    _ = ∑ j, |(inner ℝ (b j) uK : ℝ)| *
          ‖Matrix.toEuclideanCLM (𝕜 := ℝ) M (b j : EuclideanSpace ℝ (Fin d))‖ := by
        refine Finset.sum_congr rfl (fun j _ => ?_)
        rw [norm_smul, Real.norm_eq_abs]
    _ ≤ ∑ j, ‖Matrix.toEuclideanCLM (𝕜 := ℝ) M (b j : EuclideanSpace ℝ (Fin d))‖ * ‖w‖ := by
        refine Finset.sum_le_sum (fun j _ => ?_)
        have hbess : |(inner ℝ (b j) uK : ℝ)| ≤ ‖w‖ := by
          have h1 : |(inner ℝ (b j) uK : ℝ)| ≤ ‖b j‖ * ‖uK‖ := abs_real_inner_le_norm _ _
          have hbn : ‖b j‖ = 1 := b.orthonormal.1 j
          have huKn : ‖uK‖ = ‖u‖ := rfl
          rw [hbn, one_mul, huKn] at h1
          exact le_trans h1 hunorm
        rw [mul_comm]
        exact mul_le_mul_of_nonneg_left hbess (norm_nonneg _)
    _ = (∑ j, ‖Matrix.toEuclideanCLM (𝕜 := ℝ) M (b j : EuclideanSpace ℝ (Fin d))‖) * ‖w‖ := by
        rw [Finset.sum_mul]

/-! ### Flag descent and projection equivariance -/

/-- **Stratum descent on the flag.** In a decreasing flag from `⊤` to `⊥`, every nonzero
vector `v` determines a stratum `i : Fin k`: the levels containing `v` are exactly those
of index `≤ i`. (Order logic, identical to the one-sided `Corollaries.exists_stratum`.) -/
theorem exists_stratum {k : ℕ}
    {W : Fin (k + 1) → Submodule ℝ (EuclideanSpace ℝ (Fin d))}
    (hanti : Antitone W) (htop : W 0 = ⊤) (hbot : W (Fin.last k) = ⊥)
    {v : EuclideanSpace ℝ (Fin d)} (hv : v ≠ 0) :
    ∃ i : Fin k, ∀ j : Fin (k + 1), v ∈ W j ↔ (j : ℕ) ≤ (i : ℕ) := by
  classical
  have h0 : (0 : Fin (k + 1)) ∈ Finset.univ.filter (fun j => v ∈ W j) := by simp [htop]
  have hSne : (Finset.univ.filter (fun j => v ∈ W j)).Nonempty := ⟨0, h0⟩
  set j₀ := (Finset.univ.filter (fun j => v ∈ W j)).max' hSne with hj₀
  have hmem : v ∈ W j₀ := by
    have h := Finset.max'_mem _ hSne
    rw [Finset.mem_filter] at h; exact h.2
  have hmax : ∀ j : Fin (k + 1), v ∈ W j → j ≤ j₀ := fun j hj =>
    Finset.le_max' _ j (by simp [hj])
  have hne : (j₀ : ℕ) ≠ k := by
    intro h
    have hlast : j₀ = Fin.last k := Fin.ext (by simpa using h)
    rw [hlast, hbot, Submodule.mem_bot] at hmem
    exact hv hmem
  have hlt : (j₀ : ℕ) < k := lt_of_le_of_ne (Nat.lt_succ_iff.mp j₀.isLt) hne
  refine ⟨⟨(j₀ : ℕ), hlt⟩, fun j => ⟨fun hj => Fin.le_def.mp (hmax j hj), fun hj => ?_⟩⟩
  exact hanti (Fin.le_def.mpr hj) hmem

/-- **Map-equivariance promotes to projection conjugation.** From the flag equivariance
`map (toEuclideanCLM (A x)) (V x) = V (T x)` follows the matrix identity
`P_{V (T x)} · A x · P_{V x} = A x · P_{V x}`: `A x` maps `V x` into `V (T x)`, so the
projection `P_{V (T x)}` fixes the image of `A x · P_{V x}`. -/
theorem orthProj_equivariant_of_map {A : X → Matrix (Fin d) (Fin d) ℝ}
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} {T : X → X} {x : X}
    (hmap : Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap (V x) = V (T x)) :
    orthProjMatrix (V (T x)) * A x * orthProjMatrix (V x)
      = A x * orthProjMatrix (V x) := by
  have hinj : Function.Injective (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d)) :=
    (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d)).injective
  apply hinj
  simp only [map_mul]
  refine ContinuousLinearMap.ext (fun w => ?_)
  simp only [ContinuousLinearMap.mul_apply]
  have hPxw : Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix (V x)) w ∈ V x := by
    rw [orthProjMatrix, StarAlgEquiv.apply_symm_apply]
    exact (V x).starProjection_apply_mem w
  have hAmem : Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)
      (Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix (V x)) w) ∈ V (T x) := by
    rw [← hmap]
    exact Submodule.mem_map_of_mem hPxw
  conv_lhs => rw [orthProjMatrix, StarAlgEquiv.apply_symm_apply]
  exact Submodule.starProjection_eq_self_iff.mpr hAmem

/-! ### Extracting measurable conull sets and forward-orbit a.e. facts -/

section AeOrbit

variable [MeasurableSpace X] {μ : Measure X}

/-- A measurable conull set on which a given a.e. property holds. -/
theorem exists_measurable_conull_of_ae (P : X → Prop) (h : ∀ᵐ x ∂μ, P x) :
    ∃ G : Set X, MeasurableSet G ∧ μ Gᶜ = 0 ∧ ∀ x ∈ G, P x := by
  have hNmeas : μ {x | P x}ᶜ = 0 := by
    have := h; rwa [ae_iff] at this
  refine ⟨(toMeasurable μ {x | P x}ᶜ)ᶜ, (measurableSet_toMeasurable μ _).compl, ?_, ?_⟩
  · rw [compl_compl, measure_toMeasurable]; exact hNmeas
  · intro x hx
    have hxN : x ∉ {x | P x}ᶜ := fun hxN => hx (subset_toMeasurable μ _ hxN)
    simpa using hxN

/-- From an a.e. property `P`, a.e. the property holds along the entire forward orbit
`∀ k, P (T^[k] x)`. Uses measure-preservation of each iterate. -/
theorem ae_forall_iterate_of_ae {T : X → X} (hT : MeasurePreserving T μ μ)
    (P : X → Prop) (h : ∀ᵐ x ∂μ, P x) :
    ∀ᵐ x ∂μ, ∀ k : ℕ, P (T^[k] x) := by
  obtain ⟨G, hGmeas, hGconull, hGP⟩ := exists_measurable_conull_of_ae P h
  have hpre : ∀ k : ℕ, ∀ᵐ x ∂μ, T^[k] x ∈ G := by
    intro k
    rw [ae_iff]
    have : μ ((T^[k])⁻¹' Gᶜ) = 0 := by
      rw [(hT.iterate k).measure_preimage hGmeas.compl.nullMeasurableSet]; exact hGconull
    convert this using 2
  rw [← ae_all_iff] at hpre
  filter_upwards [hpre] with x hx k
  exact hGP _ (hx k)

end AeOrbit

/-! ### Convergence of a finite supremum of sequences -/

/-- The pointwise finite supremum of finitely many convergent sequences converges to the
supremum of the limits. -/
theorem tendsto_finset_sup' {s : Type*} {t : Finset s} (ht : t.Nonempty)
    (g : s → ℕ → ℝ) (L : s → ℝ) (h : ∀ j ∈ t, Tendsto (g j) atTop (𝓝 (L j))) :
    Tendsto (fun n => t.sup' ht (fun j => g j n)) atTop (𝓝 (t.sup' ht L)) := by
  induction ht using Finset.Nonempty.cons_induction with
  | singleton a =>
    simp only [Finset.sup'_singleton]; exact h a (Finset.mem_singleton_self a)
  | cons a t ha ht' ih =>
    simp_rw [Finset.sup'_cons ht']
    refine Filter.Tendsto.max (h a (Finset.mem_cons_self a t)) (ih ?_)
    intro j hj; exact h j (Finset.mem_cons.mpr (Or.inr hj))

/-! ### The per-point bounds on the restricted growth -/

section PerPoint

variable [MeasurableSpace X] [NeZero d]

/-- **Per-point lower bound.** With the floor-absorbed restricted-growth limit `hw` and a
unit stratum witness `v ∈ Vᵢ(x)` whose unrestricted growth is `lam`, the restricted
constant `c` is at least `lam`: `‖A⁽ⁿ⁾ v‖ ≤ ‖A⁽ⁿ⁾ · P‖` since `P v = v` and `v` is a unit
vector. -/
theorem restricted_const_ge_aux
    {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} (hA : ∀ x, (A x).det ≠ 0)
    {Vi : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} {x : X} {c lam : ℝ}
    (hw : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
      Real.log ‖cocycle A T n x * orthProjMatrix (Vi x)‖) atTop (𝓝 c))
    (v : EuclideanSpace ℝ (Fin d)) (hvmem : v ∈ Vi x) (hvnorm : ‖v‖ = 1)
    (hgrow : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
      Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖) atTop (𝓝 lam)) :
    lam ≤ c := by
  refine le_of_tendsto_of_tendsto hgrow hw ?_
  filter_upwards [eventually_ge_atTop 1] with n _
  set N := cocycle A T n x * orthProjMatrix (Vi x) with hN
  have hPv : Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix (Vi x)) v = v := by
    rw [orthProjMatrix, StarAlgEquiv.apply_symm_apply]
    exact Submodule.starProjection_eq_self_iff.mpr hvmem
  have happ : Matrix.toEuclideanCLM (𝕜 := ℝ) N v
      = Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v := by
    rw [hN, map_mul, ContinuousLinearMap.mul_apply, hPv]
  have hle : ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖ ≤ ‖N‖ := by
    have h1 := (Matrix.toEuclideanCLM (𝕜 := ℝ) N).le_opNorm v
    rw [Matrix.l2_opNorm_toEuclideanCLM, hvnorm, mul_one, happ] at h1
    exact h1
  have hv0 : v ≠ 0 := by rw [← norm_pos_iff, hvnorm]; norm_num
  have hpos : 0 < ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖ := by
    rw [norm_pos_iff]
    exact cocycle_apply_ne_zero (T := T) hA n x hv0
  have hlog : Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖ ≤ Real.log ‖N‖ :=
    Real.log_le_log hpos hle
  gcongr

/-- **Per-point upper bound.** With the floor-absorbed restricted-growth limit `hw`, an
orthonormal basis `eⱼ` of `Vᵢ(x)`, and each basis-vector growth `Lⱼ ≤ lam`, the restricted
constant `c` is at most `lam`. The proof bounds `‖A⁽ⁿ⁾ · P‖ ≤ Σⱼ ‖A⁽ⁿ⁾ eⱼ‖`
(`norm_mul_orthProj_le_sum`), writes each summand as `exp (n · gⱼ n)`, dominates the sum by
`N · exp (n · maxⱼ gⱼ n)`, and concludes via `le_of_tendsto_of_tendsto` against the
majorant `(1/n) log N + maxⱼ gⱼ n → maxⱼ Lⱼ`. -/
theorem restricted_const_le_aux
    {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} (hA : ∀ x, (A x).det ≠ 0)
    {Vi : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} {x : X} {c lam : ℝ}
    (hVx : Vi x ≠ ⊥)
    (hw : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
      Real.log ‖cocycle A T n x * orthProjMatrix (Vi x)‖) atTop (𝓝 c))
    (Lj : Fin (Module.finrank ℝ (Vi x)) → ℝ)
    (hLj : ∀ j, Lj j ≤ lam)
    (hgrowj : ∀ j, Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
      Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x)
        ((stdOrthonormalBasis ℝ (Vi x)) j : EuclideanSpace ℝ (Fin d))‖) atTop (𝓝 (Lj j))) :
    c ≤ lam := by
  have hpos : 0 < Module.finrank ℝ (Vi x) := by
    have : Nontrivial (Vi x) := by rwa [Submodule.nontrivial_iff_ne_bot]
    exact Module.finrank_pos
  have hne : Nonempty (Fin (Module.finrank ℝ (Vi x))) := ⟨⟨0, hpos⟩⟩
  set b := stdOrthonormalBasis ℝ (Vi x) with hb
  set aⱼ : Fin (Module.finrank ℝ (Vi x)) → ℕ → ℝ :=
    fun j n => ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x)
      (b j : EuclideanSpace ℝ (Fin d))‖ with haⱼ
  set gⱼ : Fin (Module.finrank ℝ (Vi x)) → ℕ → ℝ :=
    fun j n => (n : ℝ)⁻¹ * Real.log (aⱼ j n) with hgⱼ
  have hbj0 : ∀ j, (b j : EuclideanSpace ℝ (Fin d)) ≠ 0 := by
    intro j h
    have h1 := b.orthonormal.1 j
    have h2 : ‖(b j : EuclideanSpace ℝ (Fin d))‖ = ‖b j‖ := rfl
    rw [← h2, h, norm_zero] at h1; norm_num at h1
  have haⱼpos : ∀ j n, 0 < aⱼ j n := by
    intro j n; rw [haⱼ, norm_pos_iff]
    exact cocycle_apply_ne_zero (T := T) hA n x (hbj0 j)
  set Lsup := Finset.univ.sup' Finset.univ_nonempty Lj with hLsup
  set Ncard : ℝ := (Module.finrank ℝ (Vi x) : ℝ) with hNcard
  have hNpos : 0 < Ncard := by rw [hNcard]; exact_mod_cast hpos
  set Maj : ℕ → ℝ := fun n =>
    (n : ℝ)⁻¹ * Real.log Ncard + Finset.univ.sup' Finset.univ_nonempty (fun j => gⱼ j n) with hMaj
  have hMajlim : Tendsto Maj atTop (𝓝 (0 + Lsup)) := by
    refine Filter.Tendsto.add ?_ ?_
    · have hinv : Tendsto (fun n : ℕ => (n : ℝ)⁻¹) atTop (𝓝 0) :=
        tendsto_natCast_atTop_atTop.inv_tendsto_atTop
      simpa using hinv.mul_const (Real.log Ncard)
    · exact tendsto_finset_sup' Finset.univ_nonempty gⱼ Lj (fun j _ => hgrowj j)
  rw [zero_add] at hMajlim
  have hwle : ∀ᶠ n : ℕ in atTop,
      (n : ℝ)⁻¹ * Real.log ‖cocycle A T n x * orthProjMatrix (Vi x)‖ ≤ Maj n := by
    filter_upwards [eventually_ge_atTop 1] with n hn
    have hnpos : (0:ℝ) < (n:ℝ) := by exact_mod_cast Nat.lt_of_lt_of_le Nat.zero_lt_one hn
    have hninv : (0:ℝ) ≤ (n:ℝ)⁻¹ := by positivity
    have haexp : ∀ j, aⱼ j n = Real.exp ((n:ℝ) * gⱼ j n) := by
      intro j
      rw [hgⱼ, show (n:ℝ) * ((n : ℝ)⁻¹ * Real.log (aⱼ j n)) = Real.log (aⱼ j n) by field_simp,
        Real.exp_log (haⱼpos j n)]
    have hsupge : ∀ j, gⱼ j n ≤ Finset.univ.sup' Finset.univ_nonempty (fun k => gⱼ k n) :=
      fun j => Finset.le_sup' (fun k => gⱼ k n) (Finset.mem_univ j)
    have hSnle : ∑ j, aⱼ j n ≤ Ncard *
        Real.exp ((n:ℝ) * Finset.univ.sup' Finset.univ_nonempty (fun k => gⱼ k n)) := by
      calc ∑ j, aⱼ j n
          = ∑ j, Real.exp ((n:ℝ) * gⱼ j n) := Finset.sum_congr rfl (fun j _ => haexp j)
        _ ≤ ∑ _j : Fin (Module.finrank ℝ (Vi x)),
              Real.exp ((n:ℝ) * Finset.univ.sup' Finset.univ_nonempty (fun k => gⱼ k n)) :=
            Finset.sum_le_sum (fun j _ =>
              Real.exp_le_exp.mpr (mul_le_mul_of_nonneg_left (hsupge j) hnpos.le))
        _ = Ncard * Real.exp ((n:ℝ) *
              Finset.univ.sup' Finset.univ_nonempty (fun k => gⱼ k n)) := by
            rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul, hNcard]
    have hFle : ‖cocycle A T n x * orthProjMatrix (Vi x)‖ ≤ ∑ j, aⱼ j n :=
      norm_mul_orthProj_le_sum (Vi x)
    have hFpos : 0 < ‖cocycle A T n x * orthProjMatrix (Vi x)‖ :=
      lt_of_lt_of_le (sFloor_pos hA n x) (sFloor_le_norm_cocycle_mul_proj hA hVx n)
    have hlogle : Real.log ‖cocycle A T n x * orthProjMatrix (Vi x)‖
        ≤ Real.log (Ncard *
            Real.exp ((n:ℝ) * Finset.univ.sup' Finset.univ_nonempty (fun k => gⱼ k n))) :=
      Real.log_le_log hFpos (le_trans hFle hSnle)
    rw [Real.log_mul (ne_of_gt hNpos) (Real.exp_ne_zero _), Real.log_exp] at hlogle
    rw [hMaj]
    calc (n : ℝ)⁻¹ * Real.log ‖cocycle A T n x * orthProjMatrix (Vi x)‖
        ≤ (n : ℝ)⁻¹ * (Real.log Ncard +
            (n:ℝ) * Finset.univ.sup' Finset.univ_nonempty (fun k => gⱼ k n)) :=
          mul_le_mul_of_nonneg_left hlogle hninv
      _ = (n : ℝ)⁻¹ * Real.log Ncard +
            Finset.univ.sup' Finset.univ_nonempty (fun j => gⱼ j n) := by field_simp
  have hcle : c ≤ Lsup := le_of_tendsto_of_tendsto hw hMajlim hwle
  exact le_trans hcle (Finset.sup'_le _ _ (fun j _ => hLj j))

/-- **Absorbed restricted-growth limit.** On the good orbit (`Vᵢ(x) ≠ ⊥` and the one-step
flag equivariance along the forward orbit), the floored restricted-log Kingman limit equals
the limit of the floor-absorbed restricted operator norm
`(1/n) log ‖A⁽ⁿ⁾(x) · P_{Vᵢ(x)}‖`. (`restLog_eq_on_good` for `n ≥ 1`.) -/
theorem restLog_tendsto_absorbed
    {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} (hA : ∀ x, (A x).det ≠ 0)
    {Vi : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} {x : X} {c : ℝ}
    (hVx : Vi x ≠ ⊥)
    (hequiv : ∀ k : ℕ,
      orthProjMatrix (Vi (T (T^[k] x))) * A (T^[k] x) * orthProjMatrix (Vi (T^[k] x))
        = A (T^[k] x) * orthProjMatrix (Vi (T^[k] x)))
    (hc : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * restLog A Vi T n x) atTop (𝓝 c)) :
    Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
      Real.log ‖cocycle A T n x * orthProjMatrix (Vi x)‖) atTop (𝓝 c) := by
  refine hc.congr' ?_
  filter_upwards [eventually_ge_atTop 1] with n hn
  obtain ⟨m, rfl⟩ := Nat.exists_eq_add_of_lt (Nat.lt_of_lt_of_le Nat.zero_lt_one hn)
  rw [Nat.zero_add]
  congr 1
  exact restLog_eq_on_good hA hequiv hVx m

end PerPoint

/-! ### The restricted Kingman constant equals `λᵢ`, and the backward envelope -/

section Main

variable [MeasurableSpace X] [NeZero d] {μ : Measure X} [IsProbabilityMeasure μ] {T : X ≃ᵐ X}

/-- **The restricted Kingman constant equals `λᵢ`.** For the forward Oseledets level
`Vᵢ = V i.castSucc`, the Kingman constant `c` of the restricted cocycle `restLog A Vᵢ T`
(the forward a.e. limit of `(1/n) restLog n`) equals the Lyapunov exponent
`λᵢ = expEnum lam0 d i`.

The `≥` direction uses a stratum witness `v ∈ Vᵢ(x) ∖ Vᵢ₊₁(x)` with growth exactly `λᵢ`;
the `≤` direction bounds `‖A⁽ⁿ⁾ · P_{Vᵢ}‖` by the sum of growths of an orthonormal basis of
`Vᵢ(x)`, each basis vector lying in a stratum `≥ i` (hence with growth `≤ λᵢ`). Both bounds
are evaluated at the base point through the floor-absorbed identity (`restLog_eq_on_good`,
along the forward orbit made good by `ae_forall_iterate_of_ae`), and `c` is pinned down as a
constant via the a.e. Kingman limit. -/
theorem restricted_const_eq
    (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0)
    (lam0 : ℕ → ℝ)
    (V : Fin (numExp lam0 d + 1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin d)))
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
    (i : Fin (numExp lam0 d)) (c : ℝ)
    (hc : ∀ᵐ x ∂μ, Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ * restLog A (fun x => V i.castSucc x) (⇑T) n x) atTop (𝓝 c)) :
    c = expEnum lam0 d i := by
  classical
  have hmp : MeasurePreserving T μ μ := hT.toMeasurePreserving
  set Vi : X → Submodule ℝ (EuclideanSpace ℝ (Fin d)) := fun x => V i.castSucc x with hVi
  have hmapVi_ae : ∀ᵐ x ∂μ, Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap
      (Vi x) = Vi (T x) := by
    filter_upwards [hVae] with x hx
    exact hx.2.2.2.1 i.castSucc
  have horbit : ∀ᵐ x ∂μ, ∀ k : ℕ,
      Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A (T^[k] x))).toLinearMap
        (Vi (T^[k] x)) = Vi (T (T^[k] x)) :=
    ae_forall_iterate_of_ae hmp _ hmapVi_ae
  have hkey : ∀ᵐ x ∂μ, c = expEnum lam0 d i := by
    filter_upwards [hVae, horbit, hc] with x hx hxorbit hxc
    obtain ⟨_h0, _hlast, hstrict, _hmap, hgrow⟩ := hx
    have hVx : Vi x ≠ ⊥ := by
      intro hbot
      have hlt := hstrict i
      rw [show V i.castSucc x = Vi x from rfl, hbot] at hlt
      exact absurd hlt (by simp)
    have hequiv : ∀ k : ℕ,
        orthProjMatrix (Vi (T (T^[k] x))) * A (T^[k] x) * orthProjMatrix (Vi (T^[k] x))
          = A (T^[k] x) * orthProjMatrix (Vi (T^[k] x)) :=
      fun k => orthProj_equivariant_of_map (T := (⇑T)) (V := Vi) (hxorbit k)
    have hw := restLog_tendsto_absorbed hA hVx hequiv hxc
    have hanti : Antitone fun j => V j x := (Fin.strictAnti_iff_succ_lt.mpr hstrict).antitone
    -- lower bound: a unit stratum witness
    obtain ⟨v0, hv0mem, hv0not⟩ := SetLike.exists_of_lt (hstrict i)
    have hv00 : v0 ≠ 0 := fun h => hv0not (h ▸ Submodule.zero_mem _)
    set v := (‖v0‖)⁻¹ • v0 with hvdef
    have hvmemVi : v ∈ Vi x := (V i.castSucc x).smul_mem _ hv0mem
    have hvnorm : ‖v‖ = 1 := by
      rw [hvdef, norm_smul, norm_inv, norm_norm, inv_mul_cancel₀ (by simpa using hv00)]
    have hvnot : v ∉ V i.succ x := by
      intro hmem
      apply hv0not
      have hv0 : v0 = ‖v0‖ • v := by
        rw [hvdef, smul_smul, mul_inv_cancel₀ (by simpa using hv00), one_smul]
      rw [hv0]; exact (V i.succ x).smul_mem _ hmem
    have hge : expEnum lam0 d i ≤ c :=
      restricted_const_ge_aux hA hw v hvmemVi hvnorm (hgrow i v hvmemVi hvnot)
    -- upper bound: per-basis growths
    have hbasis : ∀ j : Fin (Module.finrank ℝ (Vi x)),
        ∃ Lj : ℝ, Lj ≤ expEnum lam0 d i ∧
          Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
            Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A (⇑T) n x)
              ((stdOrthonormalBasis ℝ (Vi x)) j : EuclideanSpace ℝ (Fin d))‖) atTop (𝓝 Lj) := by
      intro j
      set e := ((stdOrthonormalBasis ℝ (Vi x)) j : EuclideanSpace ℝ (Fin d)) with he
      have he0 : e ≠ 0 := by
        intro h
        have h1 := (stdOrthonormalBasis ℝ (Vi x)).orthonormal.1 j
        have h2 : ‖e‖ = ‖(stdOrthonormalBasis ℝ (Vi x)) j‖ := rfl
        rw [← h2, h, norm_zero] at h1; norm_num at h1
      have heVi : e ∈ Vi x := ((stdOrthonormalBasis ℝ (Vi x)) j).2
      obtain ⟨s, hs⟩ := exists_stratum hanti _h0 _hlast he0
      have hsmem : e ∈ V s.castSucc x := (hs s.castSucc).mpr (by simp)
      have hsnot : e ∉ V s.succ x := fun h => by
        have h' := (hs s.succ).mp h; rw [Fin.val_succ] at h'; omega
      refine ⟨expEnum lam0 d s, ?_, hgrow s e hsmem hsnot⟩
      have hisle : (i : ℕ) ≤ (s : ℕ) := by
        have hmem : e ∈ V i.castSucc x := heVi
        have h' := (hs i.castSucc).mp hmem
        simpa using h'
      exact (expEnum_strictAnti lam0 d).antitone (by exact_mod_cast hisle)
    choose Lj hLjle hLjtendsto using hbasis
    have hle : c ≤ expEnum lam0 d i :=
      restricted_const_le_aux hA hVx hw Lj hLjle hLjtendsto
    exact le_antisymm hle hge
  exact hkey.exists.choose_spec

end Main

end ErgodicTheory
