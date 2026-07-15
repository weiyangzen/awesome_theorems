/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.MultiplicativeErgodic
import Mathlib.Data.Finset.Sort
import Mathlib.Dynamics.Ergodic.Function
import Mathlib.LinearAlgebra.Trace

/-!
# Companion corollaries of the Oseledets theorem

The target theorem `ErgodicTheory.oseledets_filtration` produces a witness `(k, lam, V)` of a
five-conjunct almost-everywhere block: a strictly decreasing measurable flag
`⊤ = V 0 ⊋ ⋯ ⊋ V k = ⊥`, equivariance under the cocycle generator, and the exact growth
rate `lam i` on each stratum `V i \ V (i+1)`. This file bundles that conclusion as the
predicate `ErgodicTheory.IsOseledetsFiltration` and derives the standard companion corollaries
from the *statement* alone, quantified over an arbitrary witness:

* **canonical characterization**: a.e., each level is exactly the sublevel set of the
  exponential growth rate, so the data `(k, lam, V)` is **unique**;
* **top exponent**: the operator norm of the cocycle grows at the exact rate `lam 0`, so
  the top Oseledets exponent is the Furstenberg–Kesten constant;
* **multiplicities**: for ergodic `T` the level dimensions are a.e. constant, yielding
  positive per-exponent multiplicities summing to `d`.

Only the multiplicity corollary uses ergodicity (an a.e.-invariant measurable `ℕ`-valued
function is a.e. constant); it is also where the `MeasurableSubspace` conjunct of the main
theorem becomes load-bearing, via the trace of the orthogonal projector.

## Main results

* `ErgodicTheory.IsOseledetsFiltration`: the conclusion of the main theorem as a predicate.
* `ErgodicTheory.oseledets_filtration'`: the main theorem repackaged through the predicate.
* `ErgodicTheory.IsOseledetsFiltration.ae_mem_iff_limsup_le`: a.e., `v ∈ V i` iff `v = 0` or
  the normalized log-growth of `‖A⁽ⁿ⁾(x) v‖` has `limsup ≤ lam i`.
* `ErgodicTheory.IsOseledetsFiltration.unique`: two Oseledets filtration data for the same
  cocycle have the same `k`, the same exponents, and a.e. the same subspaces.
* `ErgodicTheory.IsOseledetsFiltration.tendsto_log_opNorm_cocycle`:
  `(1/n) log ‖A⁽ⁿ⁾(x)‖ → lam 0` a.e.
* `ErgodicTheory.oseledets_top_exponent_eq_furstenbergKesten`: the top exponent equals any
  Furstenberg–Kesten constant for the cocycle.
* `ErgodicTheory.trace_orthProjMatrix`, `ErgodicTheory.MeasurableSubspace.measurable_finrank`:
  the dimension of a measurable family of subspaces is measurable.
* `ErgodicTheory.IsOseledetsFiltration.exists_finrank_ae_eq`: for ergodic `T`, the level
  dimensions are a.e. given by a deterministic strictly decreasing profile `d = m 0 > ⋯ >
  m k = 0`.
* `ErgodicTheory.IsOseledetsFiltration.exists_multiplicity`: per-exponent multiplicities,
  positive and summing to `d`.
* `ErgodicTheory.oseledets_filtration_with_multiplicities`: the strengthened existence
  statement combining the main theorem with the multiplicity profile.

## References

* L. Arnold, *Random Dynamical Systems*, Springer (1998), Theorem 3.4.1.
* M. Viana, *Lectures on Lyapunov Exponents*, Cambridge University Press (2014),
  Chapter 4.
-/

open MeasureTheory Filter Topology
open scoped Matrix.Norms.L2Operator

namespace Matrix

/-- The L2 operator norm of a square matrix is at most the sum of the norms of the images
of the standard basis vectors (the "columns") under the induced map on Euclidean space. -/
theorem l2_opNorm_le_sum_norm_basisFun {d : ℕ} (M : Matrix (Fin d) (Fin d) ℝ) :
    ‖M‖ ≤ ∑ j : Fin d,
      ‖Matrix.toEuclideanCLM (𝕜 := ℝ) M (EuclideanSpace.basisFun (Fin d) ℝ j)‖ := by
  rw [← Matrix.l2_opNorm_toEuclideanCLM]
  refine ContinuousLinearMap.opNorm_le_bound _
    (Finset.sum_nonneg fun j _ => norm_nonneg _) fun v => ?_
  have hv : (Matrix.toEuclideanCLM (𝕜 := ℝ) M) v
      = ∑ j : Fin d, v j • (Matrix.toEuclideanCLM (𝕜 := ℝ) M)
          (EuclideanSpace.basisFun (Fin d) ℝ j) := by
    have hrepr : v = ∑ j : Fin d, v j • EuclideanSpace.basisFun (Fin d) ℝ j := by
      ext i
      simp [EuclideanSpace.basisFun_apply, Pi.single_apply]
    conv_lhs => rw [hrepr]
    rw [map_sum]
    simp [map_smul]
  rw [hv]
  calc ‖∑ j : Fin d, v j • (Matrix.toEuclideanCLM (𝕜 := ℝ) M)
        (EuclideanSpace.basisFun (Fin d) ℝ j)‖
      ≤ ∑ j : Fin d, ‖v j • (Matrix.toEuclideanCLM (𝕜 := ℝ) M)
        (EuclideanSpace.basisFun (Fin d) ℝ j)‖ := norm_sum_le _ _
    _ ≤ ∑ j : Fin d, ‖(Matrix.toEuclideanCLM (𝕜 := ℝ) M)
        (EuclideanSpace.basisFun (Fin d) ℝ j)‖ * ‖v‖ := by
        refine Finset.sum_le_sum fun j _ => ?_
        rw [norm_smul, mul_comm]
        exact mul_le_mul_of_nonneg_left (PiLp.norm_apply_le v j) (norm_nonneg _)
    _ = (∑ j : Fin d, ‖(Matrix.toEuclideanCLM (𝕜 := ℝ) M)
        (EuclideanSpace.basisFun (Fin d) ℝ j)‖) * ‖v‖ := by rw [Finset.sum_mul]

end Matrix

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ}

/-! ## The bundled Oseledets predicate -/

/-- The conclusion of `oseledets_filtration`, bundled as a predicate on a candidate
exponent/filtration datum `(k, lam, V)`: the exponents are strictly decreasing, each level
is a measurable family of subspaces, and almost every `x` carries the strictly decreasing
`A`-equivariant flag `⊤ = V 0 ⊋ ⋯ ⊋ V k = ⊥` with exact growth rate `lam i` on the
stratum `V i \ V (i+1)`. -/
def IsOseledetsFiltration (μ : Measure X) (T : X → X) (A : X → Matrix (Fin d) (Fin d) ℝ)
    (k : ℕ) (lam : Fin k → ℝ)
    (V : Fin (k + 1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin d))) : Prop :=
  StrictAnti lam ∧
  (∀ i, MeasurableSubspace fun x => V i x) ∧
  ∀ᵐ x ∂μ,
    V 0 x = ⊤ ∧ V (Fin.last k) x = ⊥ ∧
    (∀ i : Fin k, V i.succ x < V i.castSucc x) ∧
    (∀ i : Fin (k + 1),
      Submodule.map (Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap (V i x) = V i (T x)) ∧
    (∀ i : Fin k, ∀ v ∈ (V i.castSucc x : Set (EuclideanSpace ℝ (Fin d))),
        v ∉ V i.succ x →
        Tendsto
          (fun n : ℕ => (n : ℝ)⁻¹ *
            Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖)
          atTop (𝓝 (lam i)))

/-- **The Oseledets multiplicative ergodic theorem**, repackaged through the bundled
predicate `IsOseledetsFiltration`. -/
theorem oseledets_filtration'
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X}
    (hT : Ergodic T μ)
    (A : X → Matrix (Fin d) (Fin d) ℝ)
    (hA : ∀ x, (A x).det ≠ 0)
    (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ)
    (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∃ (k : ℕ) (lam : Fin k → ℝ)
      (V : Fin (k + 1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin d))),
      IsOseledetsFiltration μ T A k lam V := by
  obtain ⟨k, lam, V, h1, h2, h3⟩ := oseledets_filtration hT A hA hAmeas hint hint'
  exact ⟨k, lam, V, h1, h2, h3⟩

variable {μ : Measure X} {T : X → X} {A : X → Matrix (Fin d) (Fin d) ℝ}
  {k : ℕ} {lam : Fin k → ℝ}
  {V : Fin (k + 1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin d))}

/-! ## Flag-order helpers

On the a.e. good set, membership in the flag is an initial segment of the index range:
every nonzero vector has a well-defined *stratum*, the last level containing it. -/

/-- In a decreasing flag from `⊤` to `⊥`, every nonzero vector `v` determines a stratum
`i : Fin k`: the levels containing `v` are exactly those of index `≤ i`. -/
private theorem exists_stratum {k : ℕ}
    {W : Fin (k + 1) → Submodule ℝ (EuclideanSpace ℝ (Fin d))}
    (hanti : Antitone W) (htop : W 0 = ⊤) (hbot : W (Fin.last k) = ⊥)
    {v : EuclideanSpace ℝ (Fin d)} (hv : v ≠ 0) :
    ∃ i : Fin k, ∀ j : Fin (k + 1), v ∈ W j ↔ (j : ℕ) ≤ (i : ℕ) := by
  classical
  have h0 : (0 : Fin (k + 1)) ∈ Finset.univ.filter (fun j => v ∈ W j) := by
    simp [htop]
  have hSne : (Finset.univ.filter (fun j => v ∈ W j)).Nonempty := ⟨0, h0⟩
  set j₀ := (Finset.univ.filter (fun j => v ∈ W j)).max' hSne with hj₀
  have hmem : v ∈ W j₀ := by
    have h := Finset.max'_mem _ hSne
    rw [Finset.mem_filter] at h
    exact h.2
  have hmax : ∀ j : Fin (k + 1), v ∈ W j → j ≤ j₀ := fun j hj =>
    Finset.le_max' _ j (by simp [hj])
  have hne : (j₀ : ℕ) ≠ k := by
    intro h
    have hlast : j₀ = Fin.last k := Fin.ext (by simpa using h)
    rw [hlast, hbot, Submodule.mem_bot] at hmem
    exact hv hmem
  have hlt : (j₀ : ℕ) < k := lt_of_le_of_ne (Nat.lt_succ_iff.mp j₀.isLt) hne
  refine ⟨⟨(j₀ : ℕ), hlt⟩,
    fun j => ⟨fun hj => Fin.le_def.mp (hmax j hj), fun hj => ?_⟩⟩
  exact hanti (Fin.le_def.mpr hj) hmem

omit [MeasurableSpace X] in
/-- At a good point, the set of growth rates realized by nonzero vectors is exactly the
set of exponents. -/
private theorem range_lam_eq_realized {x : X}
    (htop : V 0 x = ⊤) (hbot : V (Fin.last k) x = ⊥)
    (hanti : Antitone fun j => V j x)
    (hstrict : ∀ i : Fin k, V i.succ x < V i.castSucc x)
    (hgrow : ∀ i : Fin k, ∀ v ∈ (V i.castSucc x : Set (EuclideanSpace ℝ (Fin d))),
      v ∉ V i.succ x →
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
          Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖)
        atTop (𝓝 (lam i))) :
    Set.range lam = {r : ℝ | ∃ v : EuclideanSpace ℝ (Fin d), v ≠ 0 ∧
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
          Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖)
        atTop (𝓝 r)} := by
  ext r
  constructor
  · rintro ⟨i, rfl⟩
    obtain ⟨v, hvmem, hvnot⟩ := SetLike.exists_of_lt (hstrict i)
    exact ⟨v, fun h => hvnot (h ▸ Submodule.zero_mem _), hgrow i v hvmem hvnot⟩
  · rintro ⟨v, hv, hr⟩
    obtain ⟨j, hj⟩ := exists_stratum hanti htop hbot hv
    have hjmem : v ∈ V j.castSucc x := (hj j.castSucc).mpr (by simp)
    have hjnot : v ∉ V j.succ x := fun h => by
      have h' := (hj j.succ).mp h
      rw [Fin.val_succ] at h'
      omega
    exact ⟨j, tendsto_nhds_unique (hgrow j v hjmem hjnot) hr⟩

/-! ## Trace and rank of the orthogonal projector

The `MeasurableSubspace` conjunct of the main theorem encodes a subspace by its
orthogonal-projection matrix; the trace of that matrix is the dimension, which makes
`x ↦ finrank ℝ (V x)` measurable. -/

/-- The matrix of `Matrix.toEuclideanCLM M` in the standard orthonormal basis is `M`. -/
private theorem toMatrix_toEuclideanCLM (M : Matrix (Fin d) (Fin d) ℝ) :
    LinearMap.toMatrix (EuclideanSpace.basisFun (Fin d) ℝ).toBasis
      (EuclideanSpace.basisFun (Fin d) ℝ).toBasis
      (Matrix.toEuclideanCLM (𝕜 := ℝ) M :
        EuclideanSpace ℝ (Fin d) →ₗ[ℝ] EuclideanSpace ℝ (Fin d)) = M := by
  rw [Matrix.coe_toEuclideanCLM_eq_toEuclideanLin,
    Matrix.toEuclideanLin_eq_toLin_orthonormal, LinearMap.toMatrix_toLin]

/-- The trace of the orthogonal-projection matrix of a subspace is its dimension. -/
theorem trace_orthProjMatrix (K : Submodule ℝ (EuclideanSpace ℝ (Fin d))) :
    Matrix.trace (orthProjMatrix K) = (Module.finrank ℝ K : ℝ) := by
  have hproj : LinearMap.IsProj K
      (K.starProjection : EuclideanSpace ℝ (Fin d) →ₗ[ℝ] EuclideanSpace ℝ (Fin d)) :=
    ⟨fun v => K.starProjection_apply_mem v, fun v hv => K.starProjection_eq_self_iff.mpr hv⟩
  have hK : Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix K) = K.starProjection := by
    rw [orthProjMatrix, StarAlgEquiv.apply_symm_apply]
  have hmx : LinearMap.toMatrix (EuclideanSpace.basisFun (Fin d) ℝ).toBasis
      (EuclideanSpace.basisFun (Fin d) ℝ).toBasis
      (K.starProjection : EuclideanSpace ℝ (Fin d) →ₗ[ℝ] EuclideanSpace ℝ (Fin d))
      = orthProjMatrix K := by
    rw [← hK]
    exact toMatrix_toEuclideanCLM (orthProjMatrix K)
  rw [← hmx, ← LinearMap.trace_eq_matrix_trace]
  exact hproj.trace

/-- For a measurable family of subspaces, the dimension is a measurable map to `ℕ`. -/
theorem MeasurableSubspace.measurable_finrank
    {V : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))} (hV : MeasurableSubspace V) :
    Measurable fun x => Module.finrank ℝ (V x) := by
  have htr : Measurable fun x => Matrix.trace (orthProjMatrix (V x)) := by
    have hmt : Measurable (Matrix.trace : Matrix (Fin d) (Fin d) ℝ → ℝ) := by
      unfold Matrix.trace
      exact Finset.measurable_sum _ fun i _ =>
        (measurable_pi_apply i).comp (measurable_pi_apply i)
    exact hmt.comp hV
  refine measurable_to_countable' fun n => ?_
  have hpre : (fun x => Module.finrank ℝ (V x)) ⁻¹' {n}
      = (fun x => Matrix.trace (orthProjMatrix (V x))) ⁻¹' {(n : ℝ)} := by
    ext x
    simp only [Set.mem_preimage, Set.mem_singleton_iff, trace_orthProjMatrix (V x)]
    exact_mod_cast Iff.rfl
  rw [hpre]
  exact htr (measurableSet_singleton _)

/-! ## The canonical growth-sublevel characterization (uniqueness, part one) -/

/-- **Canonical characterization of the Oseledets filtration.** Almost everywhere, each
level is exactly the sublevel set of the exponential growth rate: `v ∈ V i x` iff `v = 0`
or `limsup (1/n) log ‖A⁽ⁿ⁾(x) v‖ ≤ lam i`. No hypotheses beyond the defining a.e. block
are needed. -/
theorem IsOseledetsFiltration.ae_mem_iff_limsup_le
    (hV : IsOseledetsFiltration μ T A k lam V) :
    ∀ᵐ x ∂μ, ∀ (i : Fin k) (v : EuclideanSpace ℝ (Fin d)),
      v ∈ V i.castSucc x ↔ v = 0 ∨
        limsup (fun n : ℕ => (n : ℝ)⁻¹ *
            Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖) atTop
          ≤ lam i := by
  filter_upwards [hV.2.2] with x hx i v
  obtain ⟨htop, hbot, hlt, -, hgrow⟩ := hx
  have hanti : Antitone fun j => V j x := (Fin.strictAnti_iff_succ_lt.mpr hlt).antitone
  rcases eq_or_ne v 0 with rfl | hv
  · simp
  obtain ⟨j, hj⟩ := exists_stratum hanti htop hbot hv
  have hjmem : v ∈ V j.castSucc x := (hj j.castSucc).mpr (by simp)
  have hjnot : v ∉ V j.succ x := fun h => by
    have h' := (hj j.succ).mp h
    rw [Fin.val_succ] at h'
    omega
  have hlimsup : limsup (fun n : ℕ => (n : ℝ)⁻¹ *
      Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖) atTop = lam j :=
    (hgrow j v hjmem hjnot).limsup_eq
  constructor
  · intro hmem
    have hij : (i : ℕ) ≤ (j : ℕ) := by simpa using (hj i.castSucc).mp hmem
    refine Or.inr ?_
    rw [hlimsup]
    exact hV.1.antitone (Fin.le_def.mpr hij)
  · rintro (rfl | hle)
    · exact absurd rfl hv
    refine (hj i.castSucc).mpr ?_
    rw [Fin.val_castSucc]
    by_contra hij
    have hji : lam i < lam j := hV.1 (Fin.lt_def.mpr (by omega))
    rw [hlimsup] at hle
    linarith

/-! ## Uniqueness of the filtration data -/

/-- Two strictly antitone enumerations of the same finite set of reals coincide. -/
private theorem strictAnti_fin_range_eq {k k₂ : ℕ} {f : Fin k → ℝ} {g : Fin k₂ → ℝ}
    (hf : StrictAnti f) (hg : StrictAnti g) (h : Set.range f = Set.range g) :
    ∃ hk : k = k₂, ∀ i : Fin k, f i = g (Fin.cast hk i) := by
  classical
  have hs : (Finset.univ.image f : Finset ℝ) = Finset.univ.image g := by
    apply Finset.coe_injective
    simpa [Set.image_univ] using h
  have hcardf : (Finset.univ.image f).card = k := by
    rw [Finset.card_image_of_injective _ hf.injective, Finset.card_univ, Fintype.card_fin]
  have hcardg : (Finset.univ.image g).card = k₂ := by
    rw [Finset.card_image_of_injective _ hg.injective, Finset.card_univ, Fintype.card_fin]
  have hk : k = k₂ := by rw [← hcardf, hs, hcardg]
  subst hk
  refine ⟨rfl, fun i => ?_⟩
  have hF : (fun i : Fin k => f i.rev) = (Finset.univ.image f).orderEmbOfFin hcardf :=
    Finset.orderEmbOfFin_unique hcardf
      (fun i => Finset.mem_image_of_mem f (Finset.mem_univ _))
      (fun a b hab => hf (Fin.rev_strictAnti hab))
  have hG : (fun i : Fin k => g i.rev) = (Finset.univ.image f).orderEmbOfFin hcardf := by
    refine Finset.orderEmbOfFin_unique hcardf (fun i => ?_)
      (fun a b hab => hg (Fin.rev_strictAnti hab))
    rw [hs]
    exact Finset.mem_image_of_mem g (Finset.mem_univ _)
  have hfg := congrFun (hF.trans hG.symm) i.rev
  simpa [Fin.rev_rev] using hfg

/-- **Uniqueness of the Oseledets data.** Two Oseledets filtration data for the same
cocycle agree: same number of exponents, same exponents, and a.e. the same subspaces. -/
theorem IsOseledetsFiltration.unique
    [IsProbabilityMeasure μ]
    {k₂ : ℕ} {lam₂ : Fin k₂ → ℝ}
    {V₂ : Fin (k₂ + 1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin d))}
    (hV : IsOseledetsFiltration μ T A k lam V)
    (hV₂ : IsOseledetsFiltration μ T A k₂ lam₂ V₂) :
    ∃ hk : k = k₂,
      (∀ i : Fin k, lam i = lam₂ (Fin.cast hk i)) ∧
      ∀ᵐ x ∂μ, ∀ i : Fin (k + 1), V i x = V₂ (Fin.cast (by omega) i) x := by
  -- a single good point identifies the two exponent sets
  obtain ⟨x₀, hx₀, hx₀'⟩ := (hV.2.2.and hV₂.2.2).exists
  obtain ⟨htop, hbot, hlt, -, hgrow⟩ := hx₀
  obtain ⟨htop₂, hbot₂, hlt₂, -, hgrow₂⟩ := hx₀'
  have hanti : Antitone fun j => V j x₀ := (Fin.strictAnti_iff_succ_lt.mpr hlt).antitone
  have hanti₂ : Antitone fun j => V₂ j x₀ := (Fin.strictAnti_iff_succ_lt.mpr hlt₂).antitone
  have hrange : Set.range lam = Set.range lam₂ := by
    rw [range_lam_eq_realized htop hbot hanti hlt hgrow,
      range_lam_eq_realized htop₂ hbot₂ hanti₂ hlt₂ hgrow₂]
  obtain ⟨hk, hlam⟩ := strictAnti_fin_range_eq hV.1 hV₂.1 hrange
  subst hk
  have hlam' : ∀ i : Fin k, lam i = lam₂ i := fun i => by simpa using hlam i
  refine ⟨rfl, fun i => by simpa using hlam i, ?_⟩
  -- levelwise identity from the canonical characterization
  filter_upwards [hV.ae_mem_iff_limsup_le, hV₂.ae_mem_iff_limsup_le, hV.2.2, hV₂.2.2]
    with x hc hc₂ hx hx₂ i
  change V i x = V₂ i x
  induction i using Fin.lastCases with
  | last => rw [hx.2.1, hx₂.2.1]
  | cast j =>
    ext v
    rw [hc j v, hc₂ j v, hlam' j]

/-! ## The top exponent is the operator-norm growth rate -/

/-- The Oseledets filtration is nontrivial in positive dimension. -/
theorem IsOseledetsFiltration.k_pos
    [IsProbabilityMeasure μ] (hd : 0 < d)
    (hV : IsOseledetsFiltration μ T A k lam V) : 0 < k := by
  obtain ⟨x, hx⟩ := hV.2.2.exists
  by_contra hk
  have hk0 : k = 0 := by omega
  subst hk0
  have hbot : V 0 x = ⊥ := by
    have h := hx.2.1
    rwa [show Fin.last 0 = 0 from rfl] at h
  have htb : (⊤ : Submodule ℝ (EuclideanSpace ℝ (Fin d))) = ⊥ := hx.1 ▸ hbot
  have hfr := finrank_top ℝ (EuclideanSpace ℝ (Fin d))
  rw [htb, finrank_bot, finrank_euclideanSpace_fin] at hfr
  omega

/-- **The top Lyapunov exponent is the operator-norm growth rate.** Almost everywhere,
`(1/n) log ‖A⁽ⁿ⁾(x)‖ → lam 0`: the top stratum gives the lower bound, and the column-sum
bound on the L2 operator norm gives the upper bound. Neither ergodicity nor integrability
is needed beyond the defining a.e. block. -/
theorem IsOseledetsFiltration.tendsto_log_opNorm_cocycle
    [IsProbabilityMeasure μ] (hA : ∀ x, (A x).det ≠ 0)
    (hV : IsOseledetsFiltration μ T A k lam V) (hk : 0 < k) :
    ∀ᵐ x ∂μ, Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖cocycle A T n x‖)
      atTop (𝓝 (lam ⟨0, hk⟩)) := by
  -- a good point with a strict inclusion forces positive dimension
  have hd : 0 < d := by
    obtain ⟨x₁, hx₁⟩ := hV.2.2.exists
    by_contra hd0
    have hd0' : d = 0 := by omega
    subst hd0'
    haveI : Subsingleton (EuclideanSpace ℝ (Fin 0)) :=
      ⟨fun a b => by ext i; exact i.elim0⟩
    exact (hx₁.2.2.1 ⟨0, hk⟩).ne (Subsingleton.elim _ _)
  haveI : NeZero d := ⟨hd.ne'⟩
  filter_upwards [hV.2.2] with x hx
  obtain ⟨htop, hbot, hlt, -, hgrow⟩ := hx
  have hanti : Antitone fun j => V j x := (Fin.strictAnti_iff_succ_lt.mpr hlt).antitone
  -- every nonzero vector grows at some rate `lam j ≤ lam 0`
  have hrate : ∀ v : EuclideanSpace ℝ (Fin d), v ≠ 0 → ∃ j : Fin k,
      lam j ≤ lam ⟨0, hk⟩ ∧ Tendsto (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖)
        atTop (𝓝 (lam j)) := by
    intro v hv
    obtain ⟨j, hj⟩ := exists_stratum hanti htop hbot hv
    have hjmem : v ∈ V j.castSucc x := (hj j.castSucc).mpr (by simp)
    have hjnot : v ∉ V j.succ x := fun h => by
      have h' := (hj j.succ).mp h
      rw [Fin.val_succ] at h'
      omega
    exact ⟨j, hV.1.antitone (Fin.le_def.mpr (Nat.zero_le _)), hgrow j v hjmem hjnot⟩
  rw [tendsto_order]
  constructor
  · -- lower bound: a top-stratum vector grows at the exact rate `lam 0`
    intro b hb
    obtain ⟨v, hvmem, hvnot⟩ := SetLike.exists_of_lt (hlt ⟨0, hk⟩)
    have hv : v ≠ 0 := fun h => hvnot (h ▸ Submodule.zero_mem _)
    have hvlim := hgrow ⟨0, hk⟩ v hvmem hvnot
    have hvnorm : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖v‖) atTop (𝓝 0) := by
      simpa using
        (tendsto_inv_atTop_zero.comp tendsto_natCast_atTop_atTop).mul_const (Real.log ‖v‖)
    have hglim : Tendsto (fun n : ℕ =>
        (n : ℝ)⁻¹ * Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖
          - (n : ℝ)⁻¹ * Real.log ‖v‖) atTop (𝓝 (lam ⟨0, hk⟩)) := by
      simpa using hvlim.sub hvnorm
    filter_upwards [hglim.eventually_const_lt hb] with n hn
    refine hn.trans_le ?_
    have hMvpos : 0 < ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖ := by
      rw [norm_pos_iff]
      intro h
      refine cocycle_apply_ne_zero (T := T) hA n x hv ?_
      rwa [← Matrix.coe_toEuclideanCLM_eq_toEuclideanLin]
    have hMv : ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖
        ≤ ‖cocycle A T n x‖ * ‖v‖ := by
      calc ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖
          ≤ ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x)‖ * ‖v‖ :=
            ContinuousLinearMap.le_opNorm _ v
        _ = ‖cocycle A T n x‖ * ‖v‖ := by rw [Matrix.l2_opNorm_toEuclideanCLM]
    have hlog : Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖
        ≤ Real.log ‖cocycle A T n x‖ + Real.log ‖v‖ := by
      calc Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖
          ≤ Real.log (‖cocycle A T n x‖ * ‖v‖) := Real.log_le_log hMvpos hMv
        _ = Real.log ‖cocycle A T n x‖ + Real.log ‖v‖ :=
            Real.log_mul (norm_cocycle_pos hA n x).ne' (norm_ne_zero_iff.mpr hv)
    have hn0 : (0 : ℝ) ≤ (n : ℝ)⁻¹ := by positivity
    calc (n : ℝ)⁻¹ * Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖
          - (n : ℝ)⁻¹ * Real.log ‖v‖
        = (n : ℝ)⁻¹ * (Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x) v‖
            - Real.log ‖v‖) := by ring
      _ ≤ (n : ℝ)⁻¹ * Real.log ‖cocycle A T n x‖ :=
          mul_le_mul_of_nonneg_left (by linarith) hn0
  · -- upper bound: all basis columns grow at rate `< c < b`, so the norm does too
    intro b hb
    set c := (lam ⟨0, hk⟩ + b) / 2 with hc
    have hcl : lam ⟨0, hk⟩ < c := by rw [hc]; linarith
    have hcb : c < b := by rw [hc]; linarith
    have hbasis : ∀ᶠ n : ℕ in atTop, ∀ j : Fin d, (n : ℝ)⁻¹ *
        Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x)
          (EuclideanSpace.basisFun (Fin d) ℝ j)‖ < c := by
      rw [eventually_all]
      intro j
      have hej : EuclideanSpace.basisFun (Fin d) ℝ j ≠ 0 := by
        intro h
        have h1 := (EuclideanSpace.basisFun (Fin d) ℝ).orthonormal.1 j
        rw [h, norm_zero] at h1
        norm_num at h1
      obtain ⟨i, hle, hlim⟩ := hrate _ hej
      exact hlim.eventually_lt_const (lt_of_le_of_lt hle hcl)
    have hsmall : ∀ᶠ n : ℕ in atTop, (n : ℝ)⁻¹ * Real.log d < b - c := by
      have h0 : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log d) atTop (𝓝 0) := by
        simpa using
          (tendsto_inv_atTop_zero.comp tendsto_natCast_atTop_atTop).mul_const (Real.log d)
      exact h0.eventually_lt_const (by linarith)
    filter_upwards [hbasis, hsmall, eventually_ge_atTop 1] with n hbn hsn hn1
    have hnpos : (0 : ℝ) < n := by exact_mod_cast hn1
    have hcol : ∀ j : Fin d, ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x)
        (EuclideanSpace.basisFun (Fin d) ℝ j)‖ ≤ Real.exp (n * c) := by
      intro j
      have hej : EuclideanSpace.basisFun (Fin d) ℝ j ≠ 0 := by
        intro h
        have h1 := (EuclideanSpace.basisFun (Fin d) ℝ).orthonormal.1 j
        rw [h, norm_zero] at h1
        norm_num at h1
      have hpos : 0 < ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x)
          (EuclideanSpace.basisFun (Fin d) ℝ j)‖ := by
        rw [norm_pos_iff]
        intro h
        refine cocycle_apply_ne_zero (T := T) hA n x hej ?_
        rwa [← Matrix.coe_toEuclideanCLM_eq_toEuclideanLin]
      have hlog : Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x)
          (EuclideanSpace.basisFun (Fin d) ℝ j)‖ < n * c := by
        have h3 := mul_lt_mul_of_pos_left (hbn j) hnpos
        rwa [mul_inv_cancel_left₀ hnpos.ne'] at h3
      calc ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x)
            (EuclideanSpace.basisFun (Fin d) ℝ j)‖
          = Real.exp (Real.log ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x)
              (EuclideanSpace.basisFun (Fin d) ℝ j)‖) := (Real.exp_log hpos).symm
        _ ≤ Real.exp (n * c) := Real.exp_le_exp.mpr hlog.le
    have hnorm : ‖cocycle A T n x‖ ≤ d * Real.exp (n * c) := by
      calc ‖cocycle A T n x‖
          ≤ ∑ j : Fin d, ‖Matrix.toEuclideanCLM (𝕜 := ℝ) (cocycle A T n x)
            (EuclideanSpace.basisFun (Fin d) ℝ j)‖ :=
            Matrix.l2_opNorm_le_sum_norm_basisFun _
        _ ≤ (Finset.univ : Finset (Fin d)).card • Real.exp (n * c) :=
            Finset.sum_le_card_nsmul _ _ _ (fun j _ => hcol j)
        _ = d * Real.exp (n * c) := by
            rw [Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    have hlogn : Real.log ‖cocycle A T n x‖ ≤ Real.log d + n * c := by
      calc Real.log ‖cocycle A T n x‖
          ≤ Real.log (d * Real.exp (n * c)) :=
            Real.log_le_log (norm_cocycle_pos hA n x) hnorm
        _ = Real.log d + n * c := by
            rw [Real.log_mul (Nat.cast_pos.mpr hd).ne' (Real.exp_ne_zero _), Real.log_exp]
    calc (n : ℝ)⁻¹ * Real.log ‖cocycle A T n x‖
        ≤ (n : ℝ)⁻¹ * (Real.log d + n * c) :=
          mul_le_mul_of_nonneg_left hlogn (by positivity)
      _ = (n : ℝ)⁻¹ * Real.log d + c := by
          rw [mul_add, inv_mul_cancel_left₀ hnpos.ne']
      _ < (b - c) + c := by linarith
      _ = b := by ring

/-- **The top Oseledets exponent is the Furstenberg–Kesten constant**: any constant to
which the normalized log operator norm of the cocycle converges a.e. — such as the one
produced by `furstenbergKesten_norm` — equals `lam 0`. -/
theorem oseledets_top_exponent_eq_furstenbergKesten
    [IsProbabilityMeasure μ] (hA : ∀ x, (A x).det ≠ 0)
    (hV : IsOseledetsFiltration μ T A k lam V) (hk : 0 < k) {c : ℝ}
    (hc : ∀ᵐ x ∂μ,
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log ‖cocycle A T n x‖) atTop (𝓝 c)) :
    lam ⟨0, hk⟩ = c := by
  obtain ⟨x, hx1, hx2⟩ := ((hV.tendsto_log_opNorm_cocycle hA hk).and hc).exists
  exact tendsto_nhds_unique hx1 hx2

/-! ## Almost-everywhere constant multiplicities -/

/-- Telescoping sum of consecutive differences of an antitone `ℕ`-valued profile. -/
private theorem sum_telescope_of_antitone : ∀ {k : ℕ} (m : Fin (k + 1) → ℕ), Antitone m →
    ∑ i : Fin k, (m i.castSucc - m i.succ) = m 0 - m (Fin.last k) := by
  intro k
  induction k with
  | zero => intro m _; simp [show Fin.last 0 = 0 from rfl]
  | succ k ih =>
    intro m hm
    have hrec : ∑ i : Fin k, (m i.castSucc.castSucc - m i.succ.castSucc)
        = m (0 : Fin (k + 1)).castSucc - m (Fin.last k).castSucc :=
      ih (fun j => m j.castSucc)
        (fun a b hab => hm (Fin.castSucc_le_castSucc_iff.mpr hab))
    have ha : m (Fin.last k).castSucc ≤ m 0 := hm (Fin.zero_le _)
    have hb : m (Fin.last (k + 1)) ≤ m (Fin.last k).castSucc := by
      rw [← Fin.succ_last]
      exact hm Fin.castSucc_lt_succ.le
    rw [Fin.sum_univ_castSucc]
    simp only [Fin.succ_castSucc, Fin.succ_last, Fin.castSucc_zero,
      Nat.succ_eq_add_one] at hrec ⊢
    rw [hrec]
    omega

/-- **A.e.-constant level dimensions.** For ergodic `T`, every Oseledets filtration has
a deterministic dimension profile: there is a strictly decreasing `m` with `m 0 = d` and
`m k = 0` such that a.e. `finrank ℝ (V i x) = m i`. The dimension is measurable via the
trace of the orthogonal projector, invariant via equivariance, hence a.e. constant by
ergodicity. -/
theorem IsOseledetsFiltration.exists_finrank_ae_eq
    [IsProbabilityMeasure μ] (hT : Ergodic T μ) (hA : ∀ x, (A x).det ≠ 0)
    (hV : IsOseledetsFiltration μ T A k lam V) :
    ∃ m : Fin (k + 1) → ℕ, StrictAnti m ∧ m 0 = d ∧ m (Fin.last k) = 0 ∧
      ∀ᵐ x ∂μ, ∀ i, Module.finrank ℝ (V i x) = m i := by
  -- the dimension of each level is a.e. `T`-invariant by equivariance
  have hinv : ∀ i : Fin (k + 1),
      (fun x => Module.finrank ℝ (V i x)) ∘ T =ᵐ[μ] fun x => Module.finrank ℝ (V i x) := by
    intro i
    filter_upwards [hV.2.2] with x hx
    have hmap := hx.2.2.2.1 i
    have hinj : Function.Injective
        ((Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap) := by
      have h1 : ((Matrix.toEuclideanCLM (𝕜 := ℝ) (A x)).toLinearMap :
          EuclideanSpace ℝ (Fin d) →ₗ[ℝ] EuclideanSpace ℝ (Fin d))
          = Matrix.toEuclideanLin (A x) :=
        Matrix.coe_toEuclideanCLM_eq_toEuclideanLin (A x)
      rw [h1]
      exact injective_toEuclideanLin (hA x)
    have heq := (Submodule.equivMapOfInjective _ hinj (V i x)).finrank_eq
    rw [Function.comp_apply, ← hmap]
    exact heq.symm
  -- ergodic constancy of the (measurable) dimension
  have hm : ∀ i : Fin (k + 1),
      ∃ c : ℕ, (fun x => Module.finrank ℝ (V i x)) =ᵐ[μ] fun _ => c := fun i =>
    hT.ae_eq_const_of_ae_eq_comp₀ (hV.2.1 i).measurable_finrank.nullMeasurable (hinv i)
  choose m hm using hm
  have hae : ∀ᵐ x ∂μ, ∀ i, Module.finrank ℝ (V i x) = m i := ae_all_iff.mpr hm
  -- read the profile structure off a single good point
  obtain ⟨x₀, hx₀, hc₀⟩ := (hV.2.2.and hae).exists
  obtain ⟨htop, hbot, hltx, -, -⟩ := hx₀
  refine ⟨m, ?_, ?_, ?_, hae⟩
  · refine Fin.strictAnti_iff_succ_lt.mpr fun i => ?_
    rw [← hc₀ i.succ, ← hc₀ i.castSucc]
    exact Submodule.finrank_lt_finrank_of_lt (hltx i)
  · rw [← hc₀ 0, htop, finrank_top, finrank_euclideanSpace_fin]
  · rw [← hc₀ (Fin.last k), hbot, finrank_bot]

/-- **Per-exponent multiplicities.** For ergodic `T`, each exponent `lam i` of an
Oseledets filtration carries a positive multiplicity `m i = dim (V i) - dim (V (i+1))`,
deterministic, with `∑ i, m i = d`. -/
theorem IsOseledetsFiltration.exists_multiplicity
    [IsProbabilityMeasure μ] (hT : Ergodic T μ) (hA : ∀ x, (A x).det ≠ 0)
    (hV : IsOseledetsFiltration μ T A k lam V) :
    ∃ m : Fin k → ℕ, (∀ i, 0 < m i) ∧ (∑ i, m i) = d ∧
      ∀ᵐ x ∂μ, ∀ i : Fin k,
        Module.finrank ℝ (V i.castSucc x) = Module.finrank ℝ (V i.succ x) + m i := by
  obtain ⟨m, hmA, hm0, hmL, hae⟩ := hV.exists_finrank_ae_eq hT hA
  have hstep : ∀ i : Fin k, m i.succ < m i.castSucc := fun _ =>
    hmA Fin.castSucc_lt_succ
  refine ⟨fun i => m i.castSucc - m i.succ, fun i => ?_, ?_, ?_⟩
  · exact Nat.sub_pos_of_lt (hstep i)
  · rw [sum_telescope_of_antitone m hmA.antitone, hm0, hmL, Nat.sub_zero]
  · filter_upwards [hae] with x hx i
    have h1 := hx i.castSucc
    have h2 := hx i.succ
    have h3 := hstep i
    omega

/-- **The Oseledets theorem with multiplicities**: the existence statement of
`oseledets_filtration` strengthened by the deterministic dimension profile of the
filtration levels. -/
theorem oseledets_filtration_with_multiplicities
    {μ : Measure X} [IsProbabilityMeasure μ] {T : X → X}
    (hT : Ergodic T μ)
    (A : X → Matrix (Fin d) (Fin d) ℝ)
    (hA : ∀ x, (A x).det ≠ 0)
    (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ)
    (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) :
    ∃ (k : ℕ) (lam : Fin k → ℝ)
      (V : Fin (k + 1) → X → Submodule ℝ (EuclideanSpace ℝ (Fin d)))
      (m : Fin (k + 1) → ℕ),
      IsOseledetsFiltration μ T A k lam V ∧
      StrictAnti m ∧ m 0 = d ∧ m (Fin.last k) = 0 ∧
      ∀ᵐ x ∂μ, ∀ i, Module.finrank ℝ (V i x) = m i := by
  obtain ⟨k, lam, V, hV⟩ := oseledets_filtration' hT A hA hAmeas hint hint'
  obtain ⟨m, h1, h2, h3, h4⟩ := hV.exists_finrank_ae_eq hT hA
  exact ⟨k, lam, V, m, hV, h1, h2, h3, h4⟩

end ErgodicTheory
