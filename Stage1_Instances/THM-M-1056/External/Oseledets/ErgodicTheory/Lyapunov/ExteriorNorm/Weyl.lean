/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.ExteriorNorm.Plucker

/-!
# Weyl eigenvalue-perturbation for symmetric operators / Hermitian matrices

The sorted eigenvalues of a self-adjoint operator are 1-Lipschitz in the operator norm of the
difference (the **Weyl perturbation inequality**, a consequence of the Courant–Fischer min-max
characterization). Mathlib's `Mathlib/Analysis/InnerProductSpace/Rayleigh.lean` provides only the
*extreme* eigenvalues as Rayleigh `iSup`/`iInf`; the per-index variational bound here — and the
resulting continuity of `Matrix.IsHermitian.eigenvalues₀` — are new, and are the analytic
ingredient that lets the eigenvalues pass to the Oseledets matrix limit.

## Main results

* `ErgodicTheory.Weyl.abs_eigenvalues₀_sub_le` — the Weyl perturbation inequality: sorted
  eigenvalues of Hermitian matrices are 1-Lipschitz in the `L²` operator norm.
* `ErgodicTheory.Weyl.tendsto_eigenvalues₀` — continuity of the sorted eigenvalues along limits.
-/

open Module InnerProductSpace
open scoped Matrix.Norms.L2Operator Matrix

noncomputable section

namespace ErgodicTheory.Weyl

open scoped RealInnerProductSpace
open Module Submodule Filter Topology

section Symmetric

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]

/-- Expansion of the quadratic form `⟪T v, v⟫` of a symmetric operator in its orthonormal
eigenbasis: `⟪T v, v⟫ = ∑ᵢ μᵢ ⟪bᵢ, v⟫²` where `μ` are the sorted eigenvalues and `b` the
eigenvector basis. -/
theorem quad_eq {n : ℕ} {T : E →ₗ[ℝ] E} (hT : T.IsSymmetric) (hn : finrank ℝ E = n) (v : E) :
    ⟪T v, v⟫ = ∑ i, hT.eigenvalues hn i * ⟪hT.eigenvectorBasis hn i, v⟫ ^ 2 := by
  rw [← (hT.eigenvectorBasis hn).sum_inner_mul_inner (T v) v]
  apply Finset.sum_congr rfl
  intro i _
  rw [hT v (hT.eigenvectorBasis hn i), hT.apply_eigenvectorBasis hn i, inner_smul_right,
    real_inner_comm v (hT.eigenvectorBasis hn i)]
  simp only [RCLike.ofReal_real_eq_id, id]
  ring

/-- Expansion of `‖v‖²` in an orthonormal eigenbasis: `‖v‖² = ∑ᵢ ⟪bᵢ, v⟫²`. -/
theorem normsq_eq {n : ℕ} {T : E →ₗ[ℝ] E} (hT : T.IsSymmetric) (hn : finrank ℝ E = n) (v : E) :
    ‖v‖ ^ 2 = ∑ i, ⟪hT.eigenvectorBasis hn i, v⟫ ^ 2 :=
  (OrthonormalBasis.sum_sq_inner_right _ v).symm

variable {n : ℕ} {T : E →ₗ[ℝ] E} (hT : T.IsSymmetric) (hn : finrank ℝ E = n)

/-- The subspace spanned by the eigenvectors whose (sorted) index satisfies the predicate `p`. -/
def spanP (p : Fin n → Prop) [DecidablePred p] : Submodule ℝ E :=
  span ℝ ((hT.eigenvectorBasis hn).toBasis '' {j | p j})

/-- Membership in `spanP p`: the inner products against the off-`p` eigenvectors vanish. -/
theorem mem_spanP {p : Fin n → Prop} [DecidablePred p] {v : E} :
    v ∈ spanP hT hn p ↔ ∀ j, ¬ p j → ⟪hT.eigenvectorBasis hn j, v⟫ = 0 := by
  rw [spanP, Basis.mem_span_image]
  constructor
  · intro h j hj
    by_contra hne
    have : j ∈ ((hT.eigenvectorBasis hn).toBasis.repr v).support := by
      simp only [Finsupp.mem_support_iff]
      rwa [OrthonormalBasis.coe_toBasis_repr_apply, OrthonormalBasis.repr_apply_apply]
    exact hj (h this)
  · intro h j hj
    simp only [Finset.mem_coe, Finsupp.mem_support_iff,
      OrthonormalBasis.coe_toBasis_repr_apply, OrthonormalBasis.repr_apply_apply,
      Set.mem_setOf_eq] at hj ⊢
    by_contra hp
    exact hj (h j hp)

/-- The dimension of `spanP p` equals the number of sorted indices satisfying `p`. -/
theorem finrank_spanP (p : Fin n → Prop) [DecidablePred p] :
    finrank ℝ (spanP hT hn p) = (Finset.univ.filter p).card := by
  classical
  rw [spanP, finrank_span_set_eq_card
      ((hT.eigenvectorBasis hn).toBasis.linearIndepOn _ |>.id_image)]
  rw [Set.toFinset_card, Set.card_image_of_injective _ (hT.eigenvectorBasis hn).toBasis.injective]
  rw [← Set.toFinset_card]
  congr 1
  ext j
  simp

/-- On the span of the top `i + 1` eigenvectors, the quadratic form is at least `μᵢ ‖v‖²`
(the `i`-th eigenvalue is the smallest of the top `i + 1`). -/
theorem quad_ge_on_top (i : Fin n) {v : E} (hv : v ∈ spanP hT hn (· ≤ i)) :
    hT.eigenvalues hn i * ‖v‖ ^ 2 ≤ ⟪T v, v⟫ := by
  classical
  rw [quad_eq hT hn, normsq_eq hT hn, Finset.mul_sum]
  apply Finset.sum_le_sum
  intro j _
  rcases le_or_gt j i with hji | hji
  · have : hT.eigenvalues hn i ≤ hT.eigenvalues hn j := hT.eigenvalues_antitone hn hji
    nlinarith [sq_nonneg (⟪hT.eigenvectorBasis hn j, v⟫)]
  · have hz : ⟪hT.eigenvectorBasis hn j, v⟫ = 0 :=
      (mem_spanP hT hn).mp hv j (by simp [not_le.mpr hji])
    rw [hz]; simp

/-- On the span of the bottom `n - i` eigenvectors, the quadratic form is at most `μᵢ ‖v‖²`
(the `i`-th eigenvalue is the largest of the bottom `n - i`). -/
theorem quad_le_on_bot (i : Fin n) {v : E} (hv : v ∈ spanP hT hn (i ≤ ·)) :
    ⟪T v, v⟫ ≤ hT.eigenvalues hn i * ‖v‖ ^ 2 := by
  classical
  rw [quad_eq hT hn, normsq_eq hT hn, Finset.mul_sum]
  apply Finset.sum_le_sum
  intro j _
  rcases le_or_gt i j with hij | hij
  · have : hT.eigenvalues hn j ≤ hT.eigenvalues hn i := hT.eigenvalues_antitone hn hij
    nlinarith [sq_nonneg (⟪hT.eigenvectorBasis hn j, v⟫)]
  · have hz : ⟪hT.eigenvectorBasis hn j, v⟫ = 0 :=
      (mem_spanP hT hn).mp hv j (by simp [not_le.mpr hij])
    rw [hz]; simp

/-- **Weyl one-sided inequality.** If `⟪(T - S) v, v⟫ ≤ C ‖v‖²` for all `v`, then the `i`-th
sorted eigenvalue of `T` exceeds that of `S` by at most `C`. The proof is the Courant–Fischer
dimension count: the top-`(i+1)` eigenspace of `T` (dim `i+1`) and the bottom-`(n-i)` eigenspace
of `S` (dim `n-i`) sum to dimension `n+1 > n`, hence meet in a nonzero vector. -/
theorem eigenvalues_sub_le {S : E →ₗ[ℝ] E} (hS : S.IsSymmetric) {C : ℝ}
    (hC : ∀ v : E, ⟪(T - S) v, v⟫ ≤ C * ‖v‖ ^ 2) (i : Fin n) :
    hT.eigenvalues hn i - hS.eigenvalues hn i ≤ C := by
  classical
  set V := spanP hT hn (· ≤ i) with hV
  set W := spanP hS hn (i ≤ ·) with hW
  have hdimV : finrank ℝ V = i + 1 := by
    rw [hV, finrank_spanP]
    rw [show (Finset.univ.filter (· ≤ i)) = Finset.Iic i from Finset.filter_ge_eq_Iic]
    exact Fin.card_Iic i
  have hdimW : finrank ℝ W = n - i := by
    rw [hW, finrank_spanP]
    rw [show (Finset.univ.filter (i ≤ ·)) = Finset.Ici i from Finset.filter_le_eq_Ici]
    exact Fin.card_Ici i
  have hsum : finrank ℝ (V ⊔ W : Submodule ℝ E) + finrank ℝ (V ⊓ W : Submodule ℝ E)
      = finrank ℝ V + finrank ℝ W := Submodule.finrank_sup_add_finrank_inf_eq V W
  have hle : finrank ℝ (V ⊔ W : Submodule ℝ E) ≤ n := by
    rw [← hn]; exact Submodule.finrank_le _
  have hipos : (i : ℕ) < n := i.isLt
  have hinf : 0 < finrank ℝ (V ⊓ W : Submodule ℝ E) := by omega
  have hne : (V ⊓ W : Submodule ℝ E) ≠ ⊥ := by
    intro h; rw [h, finrank_bot] at hinf; omega
  obtain ⟨v, hv, hv0⟩ := Submodule.exists_mem_ne_zero_of_ne_bot hne
  have hvV : v ∈ V := (Submodule.mem_inf.mp hv).1
  have hvW : v ∈ W := (Submodule.mem_inf.mp hv).2
  have hnormpos : 0 < ‖v‖ ^ 2 := by positivity
  have h1 : hT.eigenvalues hn i * ‖v‖ ^ 2 ≤ ⟪T v, v⟫ := quad_ge_on_top hT hn i hvV
  have h2 : ⟪S v, v⟫ ≤ hS.eigenvalues hn i * ‖v‖ ^ 2 := quad_le_on_bot hS hn i hvW
  have h3 : ⟪T v, v⟫ - ⟪S v, v⟫ ≤ C * ‖v‖ ^ 2 := by
    have := hC v
    simp only [LinearMap.sub_apply, inner_sub_left] at this
    linarith
  nlinarith [h1, h2, h3]

/-- **Weyl perturbation (two-sided).** If `|⟪(T - S) v, v⟫| ≤ C ‖v‖²` for all `v`, then the `i`-th
sorted eigenvalues of `T` and `S` differ by at most `C`. -/
theorem abs_eigenvalues_sub_le {S : E →ₗ[ℝ] E} (hS : S.IsSymmetric) {C : ℝ}
    (hC : ∀ v : E, |⟪(T - S) v, v⟫| ≤ C * ‖v‖ ^ 2) (i : Fin n) :
    |hT.eigenvalues hn i - hS.eigenvalues hn i| ≤ C := by
  rw [abs_le]
  refine ⟨?_, ?_⟩
  · have key := eigenvalues_sub_le hS hn (S := T) hT (C := C) (i := i) (fun v => ?_)
    · linarith
    · have h := abs_le.mp (hC v)
      have hsub : ⟪(T - S) v, v⟫ = -⟪(S - T) v, v⟫ := by
        simp only [LinearMap.sub_apply, inner_sub_left]; ring
      rw [hsub] at h; linarith [h.1]
  · exact eigenvalues_sub_le hT hn hS (C := C) (i := i) (fun v => (abs_le.mp (hC v)).2)

end Symmetric

section Matrix

variable {d : ℕ}

/-- The quadratic-form / operator-norm bound for a matrix difference in `EuclideanSpace`:
`|⟪(A - B) v, v⟫| ≤ ‖A - B‖ ‖v‖²` (with `‖·‖` the L² operator norm). -/
theorem matrix_quad_le_opNorm (A B : Matrix (Fin d) (Fin d) ℝ) (v : EuclideanSpace ℝ (Fin d)) :
    |⟪(Matrix.toEuclideanLin A - Matrix.toEuclideanLin B) v, v⟫| ≤ ‖A - B‖ * ‖v‖ ^ 2 := by
  have hlin : (Matrix.toEuclideanLin A - Matrix.toEuclideanLin B) v
      = Matrix.toEuclideanLin (A - B) v := by
    simp only [LinearMap.sub_apply, map_sub]
  rw [hlin]
  calc |⟪Matrix.toEuclideanLin (A - B) v, v⟫|
      ≤ ‖Matrix.toEuclideanLin (A - B) v‖ * ‖v‖ := abs_real_inner_le_norm _ _
    _ ≤ ‖A - B‖ * ‖v‖ * ‖v‖ := by
        gcongr; exact ExteriorNorm.norm_toEuclideanLin_apply_le (A - B) v
    _ = ‖A - B‖ * ‖v‖ ^ 2 := by ring

/-- **Weyl eigenvalue perturbation for Hermitian matrices.** The sorted eigenvalues `eigenvalues₀`
of real symmetric (Hermitian) `d × d` matrices are 1-Lipschitz in the `L²` operator norm of the
difference: `|eigenvalues₀ A i − eigenvalues₀ B i| ≤ ‖A − B‖`. -/
theorem abs_eigenvalues₀_sub_le {A B : Matrix (Fin d) (Fin d) ℝ}
    (hA : A.IsHermitian) (hB : B.IsHermitian) (i : Fin (Fintype.card (Fin d))) :
    |hA.eigenvalues₀ i - hB.eigenvalues₀ i| ≤ ‖A - B‖ := by
  have hTA : (Matrix.toEuclideanLin A).IsSymmetric := Matrix.isHermitian_iff_isSymmetric.mp hA
  have hTB : (Matrix.toEuclideanLin B).IsSymmetric := Matrix.isHermitian_iff_isSymmetric.mp hB
  have key := abs_eigenvalues_sub_le (T := Matrix.toEuclideanLin A) (S := Matrix.toEuclideanLin B)
    hTA finrank_euclideanSpace hTB (C := ‖A - B‖) (i := i)
    (fun v => by simpa using matrix_quad_le_opNorm A B v)
  -- `eigenvalues₀` is *by definition* the symmetric-map `eigenvalues` at `finrank_euclideanSpace`
  have eA : hTA.eigenvalues finrank_euclideanSpace i = hA.eigenvalues₀ i := rfl
  have eB : hTB.eigenvalues finrank_euclideanSpace i = hB.eigenvalues₀ i := rfl
  rwa [eA, eB] at key

/-- **Continuity of the sorted eigenvalues.** If `M_·` converges to `M₀` (in the matrix topology)
and every term and the limit are Hermitian, then the `i`-th sorted eigenvalue converges. -/
theorem tendsto_eigenvalues₀ {ι : Type*} {l : Filter ι} {M : ι → Matrix (Fin d) (Fin d) ℝ}
    {M₀ : Matrix (Fin d) (Fin d) ℝ} (hM : ∀ k, (M k).IsHermitian) (hM₀ : M₀.IsHermitian)
    (hconv : Tendsto M l (𝓝 M₀)) (i : Fin (Fintype.card (Fin d))) :
    Tendsto (fun k => (hM k).eigenvalues₀ i) l (𝓝 (hM₀.eigenvalues₀ i)) := by
  rw [tendsto_iff_dist_tendsto_zero]
  have hbd : Tendsto (fun k => ‖M k - M₀‖) l (𝓝 0) := by
    have hc : Tendsto (fun k => M k - M₀) l (𝓝 0) := by
      have := hconv.sub (tendsto_const_nhds (x := M₀)); simpa using this
    have := (continuous_norm.tendsto (0 : Matrix (Fin d) (Fin d) ℝ)).comp hc
    simpa using this
  refine squeeze_zero (fun k => dist_nonneg) (fun k => ?_) hbd
  rw [Real.dist_eq]
  exact abs_eigenvalues₀_sub_le (hM k) hM₀ i

end Matrix

end ErgodicTheory.Weyl
end
