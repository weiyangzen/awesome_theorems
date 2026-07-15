/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.ForwardV
import ErgodicTheory.Lyapunov.LimitEigenbasis
import ErgodicTheory.Lyapunov.OseledetsLimit.Limit

/-!
# Forward spectral-rank / dimension formula (two-sided MET)

This module records the
*forward dimension formula* for the slow spectral filtration `vslow` of the sanitized
Oseledets limit operator: almost everywhere,

`finrank (vslow A T (exp t) x) = #{j < d | lam0 j ≤ t}`.

## Main results

* `cfc_apply_of_eigenvector` — per-point continuous functional calculus on an eigenvector:
  for a self-adjoint matrix `M` with `toEuclideanLin M v = c • v`, one has
  `toEuclideanLin (cfc f M) v = f c • v`.  No measurability content.
* `finrank_range_of_orthonormal_diag` — the rank of a self-adjoint idempotent matrix that
  is diagonal in an orthonormal basis with `0/1` eigenvalues equals the number of
  unit eigenvalues.
* `ae_finrank_vslow` — the validated a.e. dimension formula for `vslow`.

The eigenvector CFC lemma generalises the repo's `toEuclideanLin_cfc_fix_eigenvector`
(which only handles the unit-eigenvalue case); the rank lemma mirrors the
eigenbasis-span counting argument of `ExteriorNorm.finrank_spanP`.
-/

open MeasureTheory Filter Topology Matrix Module
open scoped Matrix

namespace ErgodicTheory

/-! ### Per-point CFC on an eigenvector -/

/-- **CFC acts as `f c` on an eigenvector.**  If `M` is Hermitian and `v` is an eigenvector of
`toEuclideanLin M` with eigenvalue `c`, then `toEuclideanLin (cfc f M) v = f c • v`.

Proof: expand `v` in the orthonormal eigenvector basis of `M`; the component `⟪b_j, v⟫` is nonzero
only for indices with `eigenvalues j = c` (eigenvectors at distinct eigenvalues are orthogonal
because `M` is self-adjoint), and the CFC acts diagonally there as `f (eigenvalues j) = f c`.  This
is pointwise, so it carries no measurability content. -/
theorem cfc_apply_of_eigenvector {d : ℕ} [NeZero d] (M : Matrix (Fin d) (Fin d) ℝ)
    (hM : M.IsHermitian) (f : ℝ → ℝ) (v : EuclideanSpace ℝ (Fin d)) {c : ℝ}
    (hev : Matrix.toEuclideanLin M v = c • v) :
    Matrix.toEuclideanLin (cfc f M) v = f c • v := by
  classical
  -- expand `v` in the eigenbasis: `v = ∑ i, ⟪b i, v⟫ • b i`
  have hexp : ∑ i, (inner ℝ (hM.eigenvectorBasis i) v : ℝ) • hM.eigenvectorBasis i = v :=
    hM.eigenvectorBasis.sum_repr' v
  -- componentwise: if `⟪b j, v⟫ ≠ 0` then `eigenvalues j = c`.
  have hcomp : ∀ j, (inner ℝ (hM.eigenvectorBasis j) v : ℝ) ≠ 0 → hM.eigenvalues j = c := by
    intro j hj
    have hMbj : Matrix.toEuclideanLin M (hM.eigenvectorBasis j)
        = hM.eigenvalues j • (hM.eigenvectorBasis j) := by
      rw [Matrix.toLpLin_apply, hM.mulVec_eigenvectorBasis j]; rfl
    have hsa : (Matrix.toEuclideanLin M).IsSymmetric :=
      Matrix.isHermitian_iff_isSymmetric.mp hM
    have e1 : (inner ℝ (hM.eigenvectorBasis j) (Matrix.toEuclideanLin M v) : ℝ)
        = c * (inner ℝ (hM.eigenvectorBasis j) v : ℝ) := by rw [hev, inner_smul_right]
    have e2 : (inner ℝ (Matrix.toEuclideanLin M (hM.eigenvectorBasis j)) v : ℝ)
        = hM.eigenvalues j * (inner ℝ (hM.eigenvectorBasis j) v : ℝ) := by
      rw [hMbj, inner_smul_left]; simp
    have e3 : (inner ℝ (hM.eigenvectorBasis j) (Matrix.toEuclideanLin M v) : ℝ)
        = (inner ℝ (Matrix.toEuclideanLin M (hM.eigenvectorBasis j)) v : ℝ) :=
      (hsa (hM.eigenvectorBasis j) v).symm
    have heq : c * (inner ℝ (hM.eigenvectorBasis j) v : ℝ)
        = hM.eigenvalues j * (inner ℝ (hM.eigenvectorBasis j) v : ℝ) := by rw [← e1, e3, e2]
    exact (mul_right_cancel₀ hj heq).symm
  -- compute `cfc f M` applied to `v`, diagonally in the eigenbasis.
  calc Matrix.toEuclideanLin (cfc f M) v
      = Matrix.toEuclideanLin (cfc f M)
          (∑ i, (inner ℝ (hM.eigenvectorBasis i) v : ℝ) • hM.eigenvectorBasis i) := by rw [hexp]
    _ = ∑ i, (inner ℝ (hM.eigenvectorBasis i) v : ℝ)
          • Matrix.toEuclideanLin (cfc f M) (hM.eigenvectorBasis i) := by
        rw [map_sum]; exact Finset.sum_congr rfl (fun i _ => by rw [map_smul])
    _ = ∑ i, (inner ℝ (hM.eigenvectorBasis i) v : ℝ) • (f c • hM.eigenvectorBasis i) := by
        apply Finset.sum_congr rfl
        intro j _
        rw [toEuclideanLin_cfc_eigenvectorBasis M hM f j]
        by_cases hj : (inner ℝ (hM.eigenvectorBasis j) v : ℝ) = 0
        · rw [hj, zero_smul, zero_smul]
        · rw [hcomp j hj]
    _ = f c • ∑ i, (inner ℝ (hM.eigenvectorBasis i) v : ℝ) • hM.eigenvectorBasis i := by
        rw [Finset.smul_sum]
        exact Finset.sum_congr rfl (fun i _ => by rw [smul_comm])
    _ = f c • v := by rw [hexp]

/-! ### Rank of a diagonalised projection -/

/-- **Rank of a self-adjoint idempotent that is diagonal in an orthonormal basis.**  If a matrix
`Q` is idempotent (`Q * Q = Q`) and acts diagonally on an orthonormal basis `b` with eigenvalues
`ε e ∈ {0, 1}`, then the rank of its range equals the number of unit eigenvalues.

Proof: membership in `range (toEuclideanCLM Q)` is `toEuclideanLin Q v = v`, which — expanded in the
basis — is exactly the vanishing of all components against the zero-eigenvalue vectors.  This is the
same membership predicate as the span of the unit-eigenvalue vectors, so the range equals that span,
whose dimension is the cardinality of the unit-eigenvalue set (orthonormal vectors are linearly
independent). -/
theorem finrank_range_of_orthonormal_diag {d : ℕ}
    (b : OrthonormalBasis (Fin d) ℝ (EuclideanSpace ℝ (Fin d)))
    (Q : Matrix (Fin d) (Fin d) ℝ) (hidem : Q * Q = Q) (ε : Fin d → ℝ)
    (hdiag : ∀ e, Matrix.toEuclideanLin Q (b e) = ε e • b e)
    (h01 : ∀ e, ε e = 0 ∨ ε e = 1) :
    Module.finrank ℝ (LinearMap.range (Matrix.toEuclideanCLM (𝕜 := ℝ) Q).toLinearMap)
      = (Finset.univ.filter (fun e => ε e = 1)).card := by
  classical
  -- Action of `Q` on a vector, expanded in the basis: `Q v = ∑ e, ε e * ⟪b e, v⟫ • b e`.
  have hQv : ∀ v : EuclideanSpace ℝ (Fin d),
      Matrix.toEuclideanLin Q v = ∑ e, (ε e * (inner ℝ (b e) v : ℝ)) • b e := by
    intro v
    conv_lhs => rw [← b.sum_repr' v]
    rw [map_sum]
    refine Finset.sum_congr rfl fun e _ => ?_
    rw [map_smul, hdiag e, smul_smul, mul_comm]
  -- Membership in the range, expressed via the basis components.
  have hmemrange : ∀ v : EuclideanSpace ℝ (Fin d),
      v ∈ LinearMap.range (Matrix.toEuclideanCLM (𝕜 := ℝ) Q).toLinearMap
        ↔ ∀ e, ¬ (ε e = 1) → (inner ℝ (b e) v : ℝ) = 0 := by
    intro v
    rw [mem_range_toEuclideanCLM_iff hidem]
    -- Compare the `b`-coordinates of `Q v` and `v` via the orthonormal repr.
    have hcoordQ : ∀ e, (inner ℝ (b e) (Matrix.toEuclideanLin Q v) : ℝ)
        = ε e * (inner ℝ (b e) v : ℝ) := by
      intro e
      rw [hQv v, inner_sum]
      rw [Finset.sum_eq_single e]
      · rw [inner_smul_right]
        have hbe : (inner ℝ (b e) (b e) : ℝ) = 1 := by
          rw [real_inner_self_eq_norm_sq, b.orthonormal.1 e, one_pow]
        rw [hbe]; ring
      · intro f _ hfe
        rw [inner_smul_right, b.orthonormal.2 hfe.symm, mul_zero]
      · intro h; exact absurd (Finset.mem_univ e) h
    constructor
    · intro hQ e he
      have hcomp : ε e * (inner ℝ (b e) v : ℝ) = (inner ℝ (b e) v : ℝ) := by
        rw [← hcoordQ e, hQ]
      rcases h01 e with h0 | h1
      · rw [h0, zero_mul] at hcomp; exact hcomp.symm
      · exact absurd h1 he
    · intro hv
      -- two vectors with equal `b`-coordinates are equal.
      apply b.toBasis.ext_elem
      intro e
      rw [OrthonormalBasis.coe_toBasis_repr_apply, OrthonormalBasis.coe_toBasis_repr_apply,
        b.repr_apply_apply, b.repr_apply_apply, hcoordQ e]
      rcases h01 e with h0 | h1
      · rw [h0, zero_mul, (hv e (by rw [h0]; norm_num))]
      · rw [h1, one_mul]
  -- Identify the range with the span of the unit-eigenvalue basis vectors.
  have hrange_eq : LinearMap.range (Matrix.toEuclideanCLM (𝕜 := ℝ) Q).toLinearMap
      = Submodule.span ℝ (b.toBasis '' {e | ε e = 1}) := by
    apply Submodule.ext
    intro v
    rw [hmemrange v, Basis.mem_span_image]
    constructor
    · intro hv j hj
      simp only [Finset.mem_coe, Finsupp.mem_support_iff,
        OrthonormalBasis.coe_toBasis_repr_apply, b.repr_apply_apply, Set.mem_setOf_eq] at hj ⊢
      by_contra hp
      exact hj (hv j hp)
    · intro hv j hj
      by_contra hne
      have : j ∈ (b.toBasis.repr v).support := by
        simp only [Finsupp.mem_support_iff]
        rwa [OrthonormalBasis.coe_toBasis_repr_apply, b.repr_apply_apply]
      have := hv this
      simp only [Set.mem_setOf_eq] at this
      exact hj this
  rw [hrange_eq, finrank_span_set_eq_card (b.toBasis.linearIndepOn _ |>.id_image)]
  rw [Set.toFinset_card, Set.card_image_of_injective _ b.toBasis.injective, ← Set.toFinset_card]
  congr 1
  ext j
  simp

/-! ### The a.e. dimension formula for `vslow` -/

/-- **A.e. forward dimension formula.**  Almost everywhere, the dimension of the slow spectral
filtration `vslow A T (exp t) x` at threshold `t` is the number of indices `j < d` whose
deterministic exponent `lam0 j` does not exceed `t`. -/
theorem ae_finrank_vslow {X : Type*} [MeasurableSpace X] {μ : Measure X}
    [IsProbabilityMeasure μ] {T : X → X} {d : ℕ} [NeZero d] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    (lam0 : ℕ → ℝ)
    (hlam0 : ∀ i : ℕ, i < d → ∀ᵐ x ∂μ, Filter.Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
      Filter.atTop (𝓝 (lam0 i))) :
    ∀ᵐ x ∂μ, ∀ t : ℝ,
      Module.finrank ℝ (vslow A T (Real.exp t) x)
        = ((Finset.range d).filter (fun j => lam0 j ≤ t)).card := by
  classical
  filter_upwards [limitEigenbasis_eigenpair_exp hT hA hAmeas hint hint',
    ae_lamSing_eq_lam0 lam0 hlam0] with x hpair hlameq
  intro t
  set b := limitEigenbasis A T x with hb
  set Q := slowProjector A T (Real.exp t) x with hQ
  set f : ℝ → ℝ := Set.indicator (Set.Iic (Real.exp t)) (1 : ℝ → ℝ) with hf
  -- The slow projector acts diagonally on the limit eigenbasis with `0/1` eigenvalues.
  set ε : Fin d → ℝ := fun e => f (Real.exp (lamSing A T x (e : ℕ))) with hε
  have hdiag : ∀ e : Fin d, Matrix.toEuclideanLin Q (b e) = ε e • b e := by
    intro e
    have hev : Matrix.toEuclideanLin (lambdaHat A T x) (b e)
        = Real.exp (lamSing A T x (e : ℕ)) • b e := hpair e
    rw [hQ, slowProjector, hε]
    exact cfc_apply_of_eigenvector (lambdaHat A T x)
      (lambdaHat_isSelfAdjoint A T x).isHermitian f (b e) hev
  -- The eigenvalue `ε e` is the indicator value at `exp (lamSing e)`.
  have hεval : ∀ e : Fin d, ε e
      = Set.indicator (Set.Iic (Real.exp t)) (1 : ℝ → ℝ)
          (Real.exp (lamSing A T x (e : ℕ))) := by
    intro e; rw [hε, hf]
  have h01 : ∀ e : Fin d, ε e = 0 ∨ ε e = 1 := by
    intro e
    rw [hεval e]
    by_cases hm : Real.exp (lamSing A T x (e : ℕ)) ∈ Set.Iic (Real.exp t)
    · right; rw [Set.indicator_of_mem hm]; rfl
    · left; rw [Set.indicator_of_notMem hm]
  -- The unit-eigenvalue indices are exactly `{e | lam0 e ≤ t}`.
  have hunit : ∀ e : Fin d, ε e = 1 ↔ lam0 (e : ℕ) ≤ t := by
    intro e
    rw [hεval e, ← hlameq e]
    constructor
    · intro h
      by_contra hgt
      rw [not_le] at hgt
      have hnot : Real.exp (lamSing A T x (e : ℕ)) ∉ Set.Iic (Real.exp t) := by
        simp only [Set.mem_Iic, not_le]; exact Real.exp_lt_exp.mpr hgt
      rw [Set.indicator_of_notMem hnot] at h
      exact zero_ne_one h
    · intro h
      have hmem : Real.exp (lamSing A T x (e : ℕ)) ∈ Set.Iic (Real.exp t) := by
        simp only [Set.mem_Iic]; exact Real.exp_le_exp.mpr h
      rw [Set.indicator_of_mem hmem]; rfl
  rw [vslow, ← hQ,
    finrank_range_of_orthonormal_diag b Q (slowProjector_mul_self A T (Real.exp t) x) ε hdiag h01]
  -- Convert the `Fin d` count to a `range d` count.
  rw [← Finset.card_image_of_injective _ (Fin.val_injective)]
  congr 1
  ext j
  simp only [Finset.mem_image, Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_range]
  constructor
  · rintro ⟨e, he, rfl⟩
    exact ⟨e.isLt, (hunit e).mp he⟩
  · rintro ⟨hjd, hjt⟩
    exact ⟨⟨j, hjd⟩, (hunit ⟨j, hjd⟩).mpr hjt, rfl⟩

end ErgodicTheory
