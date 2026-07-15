/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.Measurable

/-!
# Measurability of the intersection subbundle

For the two-sided Oseledets splitting one forms, at each point, the intersection `K ⊓ L` of a
forward subspace `K` and a backward subspace `L`.  This module shows that the assignment
`x ↦ K x ⊓ L x` is a `MeasurableSubspace` whenever `K` and `L` are.

The route avoids any von Neumann alternating-projection theorem (absent from Mathlib).  Writing
`P_K`, `P_L` for the orthogonal projections, the self-adjoint contraction `S := P_K P_L P_K`
satisfies `S v = v ↔ v ∈ K ⊓ L`, its eigenvalues lie in `[0, 1]`, and `cⁿ → 0` for `c ∈ [0, 1)`.
Hence the operator powers `Sⁿ` converge to the orthogonal projection onto the intersection, and
the matrix powers `(orthProjMatrix K · orthProjMatrix L · orthProjMatrix K)ⁿ` converge entrywise to
`orthProjMatrix (K ⊓ L)`.  Entrywise measurability of the powers and
`measurable_of_tendsto_metrizable` then assemble the `MeasurableSubspace` statement, exactly as the
continuous-functional-calculus measurability arguments in `ErgodicTheory.Lyapunov.Measurable`.

## Main results

* `ErgodicTheory.inner_projComp_eq` — `⟪v, P_K (P_L (P_K v))⟫ = ‖P_L (P_K v)‖²`.
* `ErgodicTheory.one_eigenspace_projComp` — `P_K (P_L (P_K v)) = v ↔ v ∈ K ⊓ L`.
* `ErgodicTheory.tendsto_pow_orthProj_inf` — the matrix powers of `P_K P_L P_K` tend to
  the projection matrix onto `K ⊓ L`.
* `ErgodicTheory.MeasurableSubspace.inf` — `x ↦ K x ⊓ L x` is a `MeasurableSubspace`.
-/

open MeasureTheory Filter Topology Matrix
open scoped RealInnerProductSpace

namespace ErgodicTheory

variable {d : ℕ}

/-! ### The self-adjoint contraction `P_K P_L P_K` and its fixed points -/

/-- For an orthogonal projection `P_L`, `⟪P_L w, w⟫ = ‖P_L w‖²`: the orthogonal projection is a
symmetric idempotent. -/
private theorem inner_starProjection_self_eq
    (L : Submodule ℝ (EuclideanSpace ℝ (Fin d))) (w : EuclideanSpace ℝ (Fin d)) :
    ⟪L.starProjection w, w⟫ = ‖L.starProjection w‖ ^ 2 := by
  have hmem : L.starProjection w ∈ L := L.starProjection_apply_mem w
  have horth : w - L.starProjection w ∈ Lᗮ := L.sub_starProjection_mem_orthogonal w
  have hzero : ⟪L.starProjection w, w - L.starProjection w⟫ = 0 := horth _ hmem
  set p := L.starProjection w with hp
  have key : ⟪p, w⟫ = ⟪p, p⟫ + ⟪p, w - p⟫ := by
    rw [← inner_add_right, add_sub_cancel]
  rw [key, hzero, add_zero, real_inner_self_eq_norm_sq]

/-- **The key inner-product identity.** For orthogonal projections `P_K`, `P_L`,
`⟪v, P_K (P_L (P_K v))⟫ = ‖P_L (P_K v)‖²`.  This makes `S := P_K P_L P_K` positive semidefinite and
identifies its quadratic form. -/
theorem inner_projComp_eq (K L : Submodule ℝ (EuclideanSpace ℝ (Fin d)))
    (v : EuclideanSpace ℝ (Fin d)) :
    ⟪v, K.starProjection (L.starProjection (K.starProjection v))⟫
      = ‖L.starProjection (K.starProjection v)‖ ^ 2 := by
  rw [show ⟪v, K.starProjection (L.starProjection (K.starProjection v))⟫
        = ⟪K.starProjection v, L.starProjection (K.starProjection v)⟫ from
      (K.inner_starProjection_left_eq_right v (L.starProjection (K.starProjection v))).symm,
    real_inner_comm]
  exact inner_starProjection_self_eq L (K.starProjection v)

/-- **Fixed points of `S = P_K P_L P_K` are exactly `K ⊓ L`.**  `P_K (P_L (P_K v)) = v ↔ v ∈ K ⊓ L`.
The forward direction uses the norm chain `‖v‖² = ‖P_L (P_K v)‖² ≤ ‖P_K v‖² ≤ ‖v‖²` forced to be an
equality, hence each projection fixes `v`. -/
theorem one_eigenspace_projComp (K L : Submodule ℝ (EuclideanSpace ℝ (Fin d)))
    (v : EuclideanSpace ℝ (Fin d)) :
    K.starProjection (L.starProjection (K.starProjection v)) = v ↔ v ∈ K ⊓ L := by
  constructor
  · intro hS
    -- `‖v‖² = ⟪v, S v⟫ = ‖P_L (P_K v)‖²`.
    have hquad : ‖v‖ ^ 2 = ‖L.starProjection (K.starProjection v)‖ ^ 2 := by
      have := inner_projComp_eq K L v
      rw [hS, real_inner_self_eq_norm_sq] at this
      exact this
    -- The two contraction steps.
    have h1 : ‖L.starProjection (K.starProjection v)‖ ≤ ‖K.starProjection v‖ :=
      L.norm_starProjection_apply_le (K.starProjection v)
    have h2 : ‖K.starProjection v‖ ≤ ‖v‖ := K.norm_starProjection_apply_le v
    -- Both inequalities are equalities.
    have hnn1 : (0 : ℝ) ≤ ‖L.starProjection (K.starProjection v)‖ := norm_nonneg _
    have hnn2 : (0 : ℝ) ≤ ‖K.starProjection v‖ := norm_nonneg _
    have hnn3 : (0 : ℝ) ≤ ‖v‖ := norm_nonneg _
    have hsq : ‖L.starProjection (K.starProjection v)‖ ^ 2 ≤ ‖v‖ ^ 2 := by
      have := le_trans h1 h2
      nlinarith [this, hnn1, hnn3]
    have heqLK : ‖L.starProjection (K.starProjection v)‖ = ‖K.starProjection v‖ := by
      nlinarith [h1, h2, hquad, hnn1, hnn2, hnn3]
    have heqK : ‖K.starProjection v‖ = ‖v‖ := by
      nlinarith [h1, h2, hquad, hnn1, hnn2, hnn3]
    -- `‖P_K v‖ = ‖v‖ ⟹ v ∈ K`.
    have hvK : v ∈ K := (K.mem_iff_norm_starProjection v).2 heqK
    have hPKv : K.starProjection v = v := Submodule.starProjection_eq_self_iff.mpr hvK
    -- `‖P_L (P_K v)‖ = ‖P_K v‖`, and `P_K v = v`, so `‖P_L v‖ = ‖v‖ ⟹ v ∈ L`.
    have hvL : v ∈ L := by
      apply (L.mem_iff_norm_starProjection v).2
      rw [← hPKv]
      exact heqLK
    exact Submodule.mem_inf.2 ⟨hvK, hvL⟩
  · intro hv
    obtain ⟨hvK, hvL⟩ := Submodule.mem_inf.1 hv
    have hPKv : K.starProjection v = v := Submodule.starProjection_eq_self_iff.mpr hvK
    have hPLv : L.starProjection v = v := Submodule.starProjection_eq_self_iff.mpr hvL
    rw [hPKv, hPLv, hPKv]

/-! ### The operator `toEuclideanCLM (P_K P_L P_K)` -/

/-- The matrix `S = orthProjMatrix K · orthProjMatrix L · orthProjMatrix K`. -/
private noncomputable def projComp (K L : Submodule ℝ (EuclideanSpace ℝ (Fin d))) :
    Matrix (Fin d) (Fin d) ℝ :=
  orthProjMatrix K * orthProjMatrix L * orthProjMatrix K

/-- The operator associated to `projComp K L` is `P_K ∘ P_L ∘ P_K` applied to a vector. -/
private theorem toEuclideanCLM_projComp_apply (K L : Submodule ℝ (EuclideanSpace ℝ (Fin d)))
    (v : EuclideanSpace ℝ (Fin d)) :
    Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L) v
      = K.starProjection (L.starProjection (K.starProjection v)) := by
  have hK : Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix K) = K.starProjection := by
    rw [orthProjMatrix, StarAlgEquiv.apply_symm_apply]
  have hL : Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix L) = L.starProjection := by
    rw [orthProjMatrix, StarAlgEquiv.apply_symm_apply]
  rw [projComp, map_mul, map_mul, hK, hL]
  rfl

/-- `projComp K L` is a Hermitian matrix: its associated operator `P_K P_L P_K` is self-adjoint.
Proved by transporting through the injective star-algebra equivalence `toEuclideanCLM`, under which
`projComp K L` corresponds to the self-adjoint `P_K ∘ P_L ∘ P_K`. -/
private theorem isHermitian_projComp (K L : Submodule ℝ (EuclideanSpace ℝ (Fin d))) :
    (projComp K L).IsHermitian := by
  rw [Matrix.isHermitian_iff_isSelfAdjoint, IsSelfAdjoint]
  -- `toEuclideanCLM (projComp K L) = P_K ∘ P_L ∘ P_K`, which is self-adjoint.
  have hQ : Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L)
      = K.starProjection.comp (L.starProjection.comp K.starProjection) := by
    have hK : Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix K) = K.starProjection := by
      rw [orthProjMatrix, StarAlgEquiv.apply_symm_apply]
    have hL : Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix L) = L.starProjection := by
      rw [orthProjMatrix, StarAlgEquiv.apply_symm_apply]
    rw [projComp, map_mul, map_mul, hK, hL]
    rfl
  have hKsa : IsSelfAdjoint K.starProjection := K.starProjection_isSymmetric.isSelfAdjoint
  have hLsa : IsSelfAdjoint L.starProjection := L.starProjection_isSymmetric.isSelfAdjoint
  -- The operator `P_K ∘ P_L ∘ P_K` is self-adjoint.
  have hQsa : star (Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L))
      = Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L) := by
    rw [hQ, ContinuousLinearMap.star_eq_adjoint, ContinuousLinearMap.adjoint_comp,
      ContinuousLinearMap.adjoint_comp, ← ContinuousLinearMap.star_eq_adjoint,
      ← ContinuousLinearMap.star_eq_adjoint, hKsa, hLsa, ContinuousLinearMap.comp_assoc]
  -- Transport back: `toEuclideanCLM (star (projComp)) = star (toEuclideanCLM (projComp))`.
  have himg : Matrix.toEuclideanCLM (𝕜 := ℝ) (star (projComp K L))
      = Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L) := by
    calc
      Matrix.toEuclideanCLM (𝕜 := ℝ) (star (projComp K L))
          = star (Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L)) :=
              (Matrix.toEuclideanCLM (n := Fin d) (𝕜 := ℝ)).map_star' (projComp K L)
      _ = Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L) := hQsa
  exact (Matrix.toEuclideanCLM (𝕜 := ℝ) (n := Fin d)).injective himg

/-! ### Eigendata of `S = P_K P_L P_K` -/

/-- The eigenpair of `projComp K L` expressed on the operator side: for the eigenvector basis `b`
and eigenvalues `μ`, the operator `P_K P_L P_K` scales `b e` by `μ e`. -/
private theorem toEuclideanCLM_projComp_eigenvectorBasis
    (K L : Submodule ℝ (EuclideanSpace ℝ (Fin d))) (e : Fin d) :
    Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L)
        ((isHermitian_projComp K L).eigenvectorBasis e)
      = (isHermitian_projComp K L).eigenvalues e •
          (isHermitian_projComp K L).eigenvectorBasis e := by
  have h := (isHermitian_projComp K L).mulVec_eigenvectorBasis e
  apply WithLp.ofLp_injective 2
  rw [ofLp_toEuclideanCLM, WithLp.ofLp_smul]
  exact h

/-- The eigenvalues of `S = P_K P_L P_K` lie in `[0, 1]`: `S` is positive semidefinite (its
quadratic form is `‖P_L (P_K v)‖² ≥ 0`) and a contraction (`‖S v‖ ≤ ‖v‖`). -/
private theorem eigenvalues_projComp_mem_Icc
    (K L : Submodule ℝ (EuclideanSpace ℝ (Fin d))) (e : Fin d) :
    (isHermitian_projComp K L).eigenvalues e ∈ Set.Icc (0 : ℝ) 1 := by
  set b := (isHermitian_projComp K L).eigenvectorBasis with hb
  set μ := (isHermitian_projComp K L).eigenvalues with hμ
  -- `μ e = ⟪b e, S (b e)⟫ = ‖P_L (P_K (b e))‖²`.
  have hnorm1 : ‖b e‖ = 1 := b.orthonormal.1 e
  have heig : Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L) (b e) = μ e • b e :=
    toEuclideanCLM_projComp_eigenvectorBasis K L e
  have hquad : μ e = ‖L.starProjection (K.starProjection (b e))‖ ^ 2 := by
    have hinner : ⟪b e, Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L) (b e)⟫
        = ‖L.starProjection (K.starProjection (b e))‖ ^ 2 := by
      rw [toEuclideanCLM_projComp_apply]
      exact inner_projComp_eq K L (b e)
    rw [heig, inner_smul_right, real_inner_self_eq_norm_sq, hnorm1] at hinner
    simpa using hinner
  refine ⟨?_, ?_⟩
  · rw [hquad]; positivity
  · -- `‖P_L (P_K (b e))‖ ≤ ‖P_K (b e)‖ ≤ ‖b e‖ = 1`.
    have h1 : ‖L.starProjection (K.starProjection (b e))‖ ≤ ‖K.starProjection (b e)‖ :=
      L.norm_starProjection_apply_le (K.starProjection (b e))
    have h2 : ‖K.starProjection (b e)‖ ≤ ‖b e‖ := K.norm_starProjection_apply_le (b e)
    rw [hquad, ← hnorm1]
    nlinarith [norm_nonneg (L.starProjection (K.starProjection (b e))),
      norm_nonneg (K.starProjection (b e)), norm_nonneg (b e), h1, h2]

/-- `μ e = 1` exactly when the eigenvector `b e` lies in `K ⊓ L`. -/
private theorem eigenvalue_eq_one_iff
    (K L : Submodule ℝ (EuclideanSpace ℝ (Fin d))) (e : Fin d) :
    (isHermitian_projComp K L).eigenvalues e = 1 ↔
      (isHermitian_projComp K L).eigenvectorBasis e ∈ K ⊓ L := by
  set b := (isHermitian_projComp K L).eigenvectorBasis with hb
  set μ := (isHermitian_projComp K L).eigenvalues with hμ
  have hne : b e ≠ 0 := by
    have : ‖b e‖ = 1 := b.orthonormal.1 e
    intro h; rw [h, norm_zero] at this; exact one_ne_zero this.symm
  have heig : Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L) (b e) = μ e • b e :=
    toEuclideanCLM_projComp_eigenvectorBasis K L e
  -- `S (b e) = b e ↔ μ e = 1`, and `S (b e) = b e ↔ b e ∈ K ⊓ L`.
  rw [← one_eigenspace_projComp K L (b e), ← toEuclideanCLM_projComp_apply, heig]
  constructor
  · intro h; rw [h, one_smul]
  · intro h
    have : (μ e - 1) • b e = 0 := by rw [sub_smul, one_smul, h, sub_self]
    rcases smul_eq_zero.1 this with h0 | h0
    · linarith [sub_eq_zero.1 h0]
    · exact absurd h0 hne

/-! ### Convergence of the operator powers -/

/-- The operator `Q = P_K P_L P_K` is self-adjoint, so its inner product is symmetric. -/
private theorem inner_projComp_symm (K L : Submodule ℝ (EuclideanSpace ℝ (Fin d)))
    (x y : EuclideanSpace ℝ (Fin d)) :
    ⟪x, Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L) y⟫
      = ⟪Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L) x, y⟫ := by
  have hsa : ContinuousLinearMap.adjoint (Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L))
      = Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L) := by
    have hQ : Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L)
        = K.starProjection.comp (L.starProjection.comp K.starProjection) := by
      have hK : Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix K) = K.starProjection := by
        rw [orthProjMatrix, StarAlgEquiv.apply_symm_apply]
      have hL : Matrix.toEuclideanCLM (𝕜 := ℝ) (orthProjMatrix L) = L.starProjection := by
        rw [orthProjMatrix, StarAlgEquiv.apply_symm_apply]
      rw [projComp, map_mul, map_mul, hK, hL]; rfl
    have hKsa : IsSelfAdjoint K.starProjection := K.starProjection_isSymmetric.isSelfAdjoint
    have hLsa : IsSelfAdjoint L.starProjection := L.starProjection_isSymmetric.isSelfAdjoint
    rw [hQ, ContinuousLinearMap.adjoint_comp, ContinuousLinearMap.adjoint_comp,
      ← ContinuousLinearMap.star_eq_adjoint, ← ContinuousLinearMap.star_eq_adjoint,
      hKsa, hLsa, ContinuousLinearMap.comp_assoc]
  conv_lhs => rw [← hsa]
  rw [ContinuousLinearMap.adjoint_inner_right]

/-- **Projection onto `K ⊓ L` as the sum over the `1`-eigenvectors.**  The orthogonal projection of
`v` onto `K ⊓ L` is `∑_{e : μ e = 1} ⟪b e, v⟫ • b e`, where `b`, `μ` are the eigenbasis and
eigenvalues of `S = P_K P_L P_K`. -/
private theorem starProjection_inf_eq_sum
    (K L : Submodule ℝ (EuclideanSpace ℝ (Fin d))) (v : EuclideanSpace ℝ (Fin d)) :
    (K ⊓ L).starProjection v
      = ∑ e ∈ Finset.univ.filter
            (fun e => (isHermitian_projComp K L).eigenvalues e = 1),
          ⟪(isHermitian_projComp K L).eigenvectorBasis e, v⟫ •
            (isHermitian_projComp K L).eigenvectorBasis e := by
  set b := (isHermitian_projComp K L).eigenvectorBasis with hb
  set μ := (isHermitian_projComp K L).eigenvalues with hμ
  set s := Finset.univ.filter (fun e => μ e = 1) with hs
  set w := ∑ e ∈ s, ⟪b e, v⟫ • b e with hw
  -- `w ∈ K ⊓ L`.
  have hwmem : w ∈ K ⊓ L := by
    rw [hw]
    refine Submodule.sum_mem _ fun e he => Submodule.smul_mem _ _ ?_
    rw [hs, Finset.mem_filter] at he
    exact (eigenvalue_eq_one_iff K L e).1 he.2
  refine Submodule.eq_starProjection_of_mem_of_inner_eq_zero hwmem fun u hu => ?_
  -- For `u ∈ K ⊓ L`: `Q u = u`, hence `⟪b e, u⟫ = 0` whenever `μ e ≠ 1`.
  have hQu : Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L) u = u := by
    rw [toEuclideanCLM_projComp_apply]
    exact (one_eigenspace_projComp K L u).2 hu
  have hzero : ∀ e, μ e ≠ 1 → ⟪b e, u⟫ = 0 := by
    intro e he
    have key : μ e * ⟪b e, u⟫ = ⟪b e, u⟫ := by
      have h1 : ⟪b e, Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L) u⟫
          = ⟪Matrix.toEuclideanCLM (𝕜 := ℝ) (projComp K L) (b e), u⟫ :=
        inner_projComp_symm K L (b e) u
      rw [hQu] at h1
      rw [toEuclideanCLM_projComp_eigenvectorBasis, inner_smul_left] at h1
      simpa using h1.symm
    by_contra hcontra
    apply hcontra
    have : (μ e - 1) * ⟪b e, u⟫ = 0 := by ring_nf; linarith [key]
    rcases mul_eq_zero.1 this with h0 | h0
    · exact absurd (by linarith [sub_eq_zero.1 h0] : μ e = 1) he
    · exact h0
  -- Expand `⟪v, u⟫` and `⟪w, u⟫` over the orthonormal basis; only `e ∈ s` survive.
  have hvu : ⟪v, u⟫ = ∑ e ∈ s, ⟪b e, u⟫ * ⟪b e, v⟫ := by
    conv_lhs => rw [← b.sum_repr' u, inner_sum]
    rw [← Finset.sum_filter_add_sum_filter_not Finset.univ (fun e => μ e = 1)]
    have hrest : ∑ e ∈ Finset.univ.filter (fun e => ¬ μ e = 1),
        ⟪v, ⟪b e, u⟫ • b e⟫ = 0 := by
      refine Finset.sum_eq_zero fun e he => ?_
      rw [Finset.mem_filter] at he
      rw [hzero e he.2, zero_smul, inner_zero_right]
    have hrest' : ∑ x with ¬ μ x = 1, ⟪v, ⟪b x, u⟫ • b x⟫ = 0 := hrest
    have hsplit :
        (∑ x with μ x = 1, ⟪v, ⟪b x, u⟫ • b x⟫) +
            ∑ x with ¬ μ x = 1, ⟪v, ⟪b x, u⟫ • b x⟫
          = ∑ x with μ x = 1, ⟪v, ⟪b x, u⟫ • b x⟫ := by
      rw [hrest', add_zero]
    calc
      (∑ x with μ x = 1, ⟪v, ⟪b x, u⟫ • b x⟫) +
            ∑ x with ¬ μ x = 1, ⟪v, ⟪b x, u⟫ • b x⟫
          = ∑ x with μ x = 1, ⟪v, ⟪b x, u⟫ • b x⟫ := hsplit
      _ = ∑ e ∈ s, ⟪b e, u⟫ * ⟪b e, v⟫ := by
        refine Finset.sum_congr (by rw [hs]) fun e _ => ?_
        rw [inner_smul_right, real_inner_comm v (b e)]
  have hwu : ⟪w, u⟫ = ∑ e ∈ s, ⟪b e, v⟫ * ⟪b e, u⟫ := by
    rw [hw, sum_inner]
    refine Finset.sum_congr rfl fun e _ => ?_
    rw [inner_smul_left]; simp
  rw [inner_sub_left, hwu, hvu, sub_eq_zero]
  refine Finset.sum_congr rfl fun e _ => ?_
  ring

/-- The `n`-th power `Sⁿ`, as an operator, scales the eigenvector `b e` by `(μ e)ⁿ`. -/
private theorem toEuclideanCLM_projComp_pow_eigenvectorBasis
    (K L : Submodule ℝ (EuclideanSpace ℝ (Fin d))) (n : ℕ) (e : Fin d) :
    Matrix.toEuclideanCLM (𝕜 := ℝ) ((projComp K L) ^ n)
        ((isHermitian_projComp K L).eigenvectorBasis e)
      = ((isHermitian_projComp K L).eigenvalues e) ^ n •
          (isHermitian_projComp K L).eigenvectorBasis e := by
  set b := (isHermitian_projComp K L).eigenvectorBasis
  set μ := (isHermitian_projComp K L).eigenvalues
  rw [map_pow]
  induction n with
  | zero => simp
  | succ k ih =>
      rw [pow_succ, ContinuousLinearMap.mul_apply, toEuclideanCLM_projComp_eigenvectorBasis,
        ContinuousLinearMap.map_smul, ih, smul_smul, pow_succ, mul_comm]

/-- **Operator powers converge to the projection onto `K ⊓ L`.** For every vector `v`,
`Sⁿ v → P_{K ⊓ L} v` where `S = P_K P_L P_K`. -/
private theorem tendsto_pow_projComp_apply
    (K L : Submodule ℝ (EuclideanSpace ℝ (Fin d))) (v : EuclideanSpace ℝ (Fin d)) :
    Tendsto (fun n : ℕ => Matrix.toEuclideanCLM (𝕜 := ℝ) ((projComp K L) ^ n) v)
      atTop (𝓝 ((K ⊓ L).starProjection v)) := by
  set b := (isHermitian_projComp K L).eigenvectorBasis with hb
  set μ := (isHermitian_projComp K L).eigenvalues with hμ
  -- `Sⁿ v = ∑ e, ⟪b e, v⟫ • (μ e)ⁿ • b e`.
  have hexpand : ∀ n : ℕ, Matrix.toEuclideanCLM (𝕜 := ℝ) ((projComp K L) ^ n) v
      = ∑ e, ⟪b e, v⟫ • (μ e ^ n • b e) := by
    intro n
    conv_lhs => rw [← b.sum_repr' v]
    rw [map_sum]
    refine Finset.sum_congr rfl fun e _ => ?_
    rw [ContinuousLinearMap.map_smul, toEuclideanCLM_projComp_pow_eigenvectorBasis, hb, hμ]
    rfl
  simp only [hexpand]
  -- The projection equals `∑ e, ⟪b e, v⟫ • (if μ e = 1 then 1 else 0) • b e`.
  have hlim : (K ⊓ L).starProjection v
      = ∑ e, ⟪b e, v⟫ • ((if μ e = 1 then (1 : ℝ) else 0) • b e) := by
    rw [starProjection_inf_eq_sum K L v, ← hb, ← hμ]
    rw [← Finset.sum_filter_add_sum_filter_not Finset.univ (fun e => μ e = 1)]
    have hsecond : ∑ e ∈ Finset.univ.filter (fun e => ¬ μ e = 1),
        ⟪b e, v⟫ • ((if μ e = 1 then (1 : ℝ) else 0) • b e) = 0 := by
      refine Finset.sum_eq_zero fun e he => ?_
      rw [Finset.mem_filter] at he
      rw [if_neg he.2, zero_smul, smul_zero]
    rw [hsecond, add_zero]
    refine Finset.sum_congr rfl fun e he => ?_
    rw [Finset.mem_filter] at he
    rw [if_pos he.2, one_smul]
  rw [hlim]
  -- Termwise convergence and finite sum.
  refine tendsto_finset_sum _ fun e _ => ?_
  -- `(μ e)ⁿ → if μ e = 1 then 1 else 0`.
  have hsc : Tendsto (fun n : ℕ => μ e ^ n) atTop
      (𝓝 (if μ e = 1 then (1 : ℝ) else 0)) := by
    obtain ⟨h0, h1⟩ := eigenvalues_projComp_mem_Icc K L e
    by_cases hμe : μ e = 1
    · rw [if_pos hμe]
      simpa only [hμe, one_pow] using tendsto_const_nhds (x := (1 : ℝ))
    · rw [if_neg hμe]
      exact tendsto_pow_atTop_nhds_zero_of_abs_lt_one
        (by rw [abs_of_nonneg h0]; exact lt_of_le_of_ne h1 hμe)
  exact ((hsc.smul_const (b e)).const_smul ⟪b e, v⟫)

/-! ### Matrix-power convergence and the measurable intersection -/

/-- **The matrix powers of `P_K P_L P_K` converge to the projection onto `K ⊓ L`.**
`(orthProjMatrix K · orthProjMatrix L · orthProjMatrix K)ⁿ → orthProjMatrix (K ⊓ L)` (entrywise).
This is the von Neumann alternating-projection limit, obtained from the operator-power convergence
`tendsto_pow_projComp_apply` by reading off coordinates of the standard basis vectors. -/
theorem tendsto_pow_orthProj_inf (K L : Submodule ℝ (EuclideanSpace ℝ (Fin d))) :
    Tendsto (fun n : ℕ => (orthProjMatrix K * orthProjMatrix L * orthProjMatrix K) ^ n)
      atTop (𝓝 (orthProjMatrix (K ⊓ L))) := by
  -- It suffices to prove entrywise convergence.
  refine tendsto_pi_nhds.2 fun i => tendsto_pi_nhds.2 fun j => ?_
  -- Entry `(i, j)` of `Sⁿ` is the `i`-th coordinate of `toEuclideanCLM (Sⁿ) (single j 1)`.
  have hentry : ∀ n : ℕ,
      ((orthProjMatrix K * orthProjMatrix L * orthProjMatrix K) ^ n) i j
      = Matrix.toEuclideanCLM (𝕜 := ℝ) ((projComp K L) ^ n)
          (EuclideanSpace.single j (1 : ℝ)) i := by
    intro n
    rw [ofLp_toEuclideanCLM,
      show WithLp.ofLp (EuclideanSpace.single j (1 : ℝ)) = Pi.single j (1 : ℝ) from rfl,
      Matrix.mulVec_single_one]
    simp [projComp, Matrix.col_apply]
  -- The limit entry is `((K ⊓ L).starProjection (single j 1)) i = orthProjMatrix (K ⊓ L) i j`.
  have hlimit : orthProjMatrix (K ⊓ L) i j
      = (K ⊓ L).starProjection (EuclideanSpace.single j (1 : ℝ)) i := orthProjMatrix_apply _ i j
  rw [hlimit]
  simp only [hentry]
  -- Take the `i`-th coordinate of the operator-power convergence.
  have hcoord : Continuous fun w : EuclideanSpace ℝ (Fin d) => w i :=
    PiLp.continuous_apply (β := fun _ : Fin d => ℝ) 2 i
  exact (hcoord.tendsto _).comp (tendsto_pow_projComp_apply K L (EuclideanSpace.single j (1 : ℝ)))

variable {X : Type*} [MeasurableSpace X]

/-- **The intersection of two measurable subspace families is measurable.**  If `K` and `L` are
`MeasurableSubspace`s, then so is `x ↦ K x ⊓ L x`.  The projection matrix onto `K x ⊓ L x` is the
entrywise limit of the measurable matrix powers
`(orthProjMatrix (K x) · orthProjMatrix (L x) · orthProjMatrix (K x))ⁿ`, so
`measurable_of_tendsto_metrizable` applies entrywise. -/
theorem MeasurableSubspace.inf
    {K L : X → Submodule ℝ (EuclideanSpace ℝ (Fin d))}
    (hK : MeasurableSubspace K) (hL : MeasurableSubspace L) :
    MeasurableSubspace fun x => K x ⊓ L x := by
  -- The `n`-th power `x ↦ Sⁿ` is measurable.
  have hpow : ∀ n : ℕ, Measurable fun x =>
      (orthProjMatrix (K x) * orthProjMatrix (L x) * orthProjMatrix (K x)) ^ n := by
    intro n
    have hbase : Measurable fun x =>
        orthProjMatrix (K x) * orthProjMatrix (L x) * orthProjMatrix (K x) :=
      (hK.mul hL).mul hK
    exact (measurable_matrix_pow n).comp hbase
  -- Entrywise: pointwise limit of measurable functions is measurable.
  refine measurable_pi_iff.2 fun i => measurable_pi_iff.2 fun j => ?_
  have hentry : ∀ n : ℕ, Measurable fun x =>
      ((orthProjMatrix (K x) * orthProjMatrix (L x) * orthProjMatrix (K x)) ^ n) i j :=
    fun n => ((measurable_pi_apply j).comp ((measurable_pi_apply i).comp (hpow n)))
  refine measurable_of_tendsto_metrizable hentry ?_
  refine tendsto_pi_nhds.2 fun x => ?_
  have := tendsto_pow_orthProj_inf (K x) (L x)
  exact (tendsto_pi_nhds.1 (tendsto_pi_nhds.1 this i) j)

end ErgodicTheory
