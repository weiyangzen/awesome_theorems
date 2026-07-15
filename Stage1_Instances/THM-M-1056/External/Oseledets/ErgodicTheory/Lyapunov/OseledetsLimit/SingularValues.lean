/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import ErgodicTheory.Lyapunov.ExteriorNorm.Weyl
import ErgodicTheory.Lyapunov.Measurable
import ErgodicTheory.Cocycle.FurstenbergKesten
import ErgodicTheory.Ergodic.Kingman.Core
import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.LinearAlgebra.Matrix.PosDef
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.Analysis.Matrix.Order
import Mathlib.Analysis.Matrix.HermitianFunctionalCalculus
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Topology.UniformSpace.Cauchy
import Mathlib.Analysis.SpecialFunctions.Pow.Continuity
import Mathlib.MeasureTheory.Constructions.Polish.StronglyMeasurable

/-!
# The Oseledets singular-value (scalar) layer

This module builds the **scalar (singular-value) layer** of the Oseledets multiplicative
ergodic theorem: the genuine ergodic limits
`Γ_k = lim_n (1/n) log ∏_{i<k} σᵢ(A⁽ⁿ⁾)` and the per-exponent limits
`λᵢ = Γ_{i+1} − Γ_i` (the logarithms of the eigenvalues of the limiting matrix `Λ`),
*without ever constructing `Λ` as a matrix limit*.

The analytic input is the already-proved submultiplicativity of the product of the top-`k`
singular values (`ExteriorNorm.prod_singularValues_comp_le`), turned into a subadditive
cocycle and fed to Kingman's ergodic theorem (`tendsto_kingman_ergodic`).

## Main definitions

* `ErgodicTheory.gram` — the Gram matrix `Qₙ = (A⁽ⁿ⁾)ᵀ A⁽ⁿ⁾` of the cocycle iterate.
* `ErgodicTheory.sprod` — the product of the top-`k` singular values of `toEuclideanLin (A⁽ⁿ⁾)`.

## Main results

* `LinearMap.singularValues_le_opNorm` / `ErgodicTheory.sigma_le_opNorm` —
  `σᵢ(f) ≤ ‖f‖` and `σᵢ(toEuclideanLin M) ≤ ‖M‖`.
* `ErgodicTheory.sprod_submul`, `ErgodicTheory.logSprod_subadditive`,
  `ErgodicTheory.isSubadditiveCocycle_logSprod` — subadditivity of `log sprod`.
* `ErgodicTheory.integrable_logSprod`, `ErgodicTheory.bddBelow_logSprod` — integrability/lower
  bound.
* `ErgodicTheory.tendsto_gammaK` — the genuine ergodic `Γ_k` limit.
* `ErgodicTheory.lamSing`, `ErgodicTheory.tendsto_log_singularValue` — the per-singular-value
  exponents.
* `ErgodicTheory.sq_singularValues_eq_gram_eigenvalue` — squared singular values are Gram
  eigenvalues.
-/

open Module InnerProductSpace MeasureTheory Filter Topology
open scoped Matrix.Norms.L2Operator Matrix MatrixOrder RealInnerProductSpace

noncomputable section

/-! ## A singular value is bounded by the operator norm

`σᵢ(f) ≤ ‖f‖` for a linear map `f` between finite-dimensional inner product spaces.
This is genuinely missing from Mathlib (`SingularValues.lean` has no connection to the
operator norm); it is upstreamable. The proof: the right singular vectors `uᵢ` (an
orthonormal eigenvector basis of `adjoint f ∘ₗ f`) satisfy `‖f uᵢ‖ = σᵢ(f)`, and
`‖f uᵢ‖ ≤ ‖f‖ · ‖uᵢ‖ = ‖f‖`. -/

namespace LinearMap

variable {E F : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [NormedAddCommGroup F] [InnerProductSpace ℝ F] [FiniteDimensional ℝ F]

/-- The norm of the image of a right singular vector is the corresponding singular value:
`‖f uᵢ‖ = σᵢ(f)`, where `u` is the orthonormal eigenvector basis of `adjoint f ∘ₗ f`. This is
the analytic heart of the singular value decomposition. -/
theorem norm_apply_eigenvectorBasis_eq_singularValues (f : E →ₗ[ℝ] F) {n : ℕ}
    (hn : Module.finrank ℝ E = n) (i : Fin n) :
    ‖f ((f.isSymmetric_adjoint_comp_self.eigenvectorBasis hn) i)‖ = f.singularValues i := by
  set hT := f.isSymmetric_adjoint_comp_self with hThT
  set u := hT.eigenvectorBasis hn with hu
  -- `⟪f uᵢ, f uᵢ⟫ = ⟪(adjoint f ∘ₗ f) uᵢ, uᵢ⟫ = eigenvalue · ⟪uᵢ, uᵢ⟫ = σᵢ²`.
  have key : (inner ℝ (f (u i)) (f (u i)) : ℝ) = f.singularValues i ^ 2 := by
    have h1 : (inner ℝ (f (u i)) (f (u i)) : ℝ)
        = inner ℝ ((LinearMap.adjoint f ∘ₗ f) (u i)) (u i) := by
      rw [LinearMap.comp_apply, LinearMap.adjoint_inner_left]
    rw [h1, show (LinearMap.adjoint f ∘ₗ f) (u i) = (hT.eigenvalues hn i : ℝ) • u i from
          hT.apply_eigenvectorBasis hn i, inner_smul_left, u.inner_eq_ite i i,
        f.sq_singularValues_fin hn i]
    simp
  have hsq : ‖f (u i)‖ ^ 2 = f.singularValues i ^ 2 := by
    rw [← real_inner_self_eq_norm_sq]; exact key
  nlinarith [norm_nonneg (f (u i)), f.singularValues_nonneg i, hsq]

/-- Every singular value of a linear map between finite-dimensional inner
product spaces is bounded by its operator norm: `σᵢ(f) ≤ ‖f‖`. -/
theorem singularValues_le_opNorm (f : E →ₗ[ℝ] F) (i : ℕ) :
    f.singularValues i ≤ ‖LinearMap.toContinuousLinearMap f‖ := by
  set n := Module.finrank ℝ E with hn
  by_cases hi : i < n
  · -- `σᵢ = ‖f uᵢ‖ ≤ ‖f‖ · ‖uᵢ‖ = ‖f‖`.
    set u := f.isSymmetric_adjoint_comp_self.eigenvectorBasis hn.symm with hu
    have heq : f.singularValues i = ‖f (u ⟨i, hi⟩)‖ :=
      (f.norm_apply_eigenvectorBasis_eq_singularValues hn.symm ⟨i, hi⟩).symm
    have hbound : ‖f (u ⟨i, hi⟩)‖ ≤ ‖LinearMap.toContinuousLinearMap f‖ * ‖u ⟨i, hi⟩‖ := by
      have := (LinearMap.toContinuousLinearMap f).le_opNorm (u ⟨i, hi⟩)
      rwa [LinearMap.coe_toContinuousLinearMap'] at this
    have hu1 : ‖u ⟨i, hi⟩‖ = 1 := u.orthonormal.1 _
    rw [hu1, mul_one] at hbound
    rw [heq]; exact hbound
  · -- `σᵢ = 0` for `i ≥ n`.
    rw [f.singularValues_of_finrank_le (not_lt.mp hi)]
    exact norm_nonneg _

end LinearMap

namespace ErgodicTheory

variable {X : Type*} [MeasurableSpace X] {d : ℕ}

/-! ## The Gram matrix and the singular-value product -/

/-- The **Gram matrix** `Qₙ = (A⁽ⁿ⁾)ᵀ · A⁽ⁿ⁾` of the cocycle iterate. Its eigenvalues are the
squared singular values of `A⁽ⁿ⁾` (see `sq_singularValues_eq_gram_eigenvalue`). -/
def gram (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ) (x : X) :
    Matrix (Fin d) (Fin d) ℝ :=
  (cocycle A T n x)ᵀ * cocycle A T n x

/-- The **top-`k` singular value product** of the cocycle iterate, as a Euclidean linear map. -/
def sprod (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (k n : ℕ) (x : X) : ℝ :=
  ∏ i ∈ Finset.range k,
    (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i

/-- `toEuclideanLin` turns a matrix product into a composition of linear maps. -/
private theorem toEuclideanLin_mul (M N : Matrix (Fin d) (Fin d) ℝ) :
    Matrix.toEuclideanLin (M * N)
      = (Matrix.toEuclideanLin M) ∘ₗ (Matrix.toEuclideanLin N) := by
  ext v i
  simp only [Matrix.toLpLin_apply, LinearMap.comp_apply, Matrix.mulVec_mulVec]

/-! ## Subadditivity of `log sprod` -/

set_option linter.unusedSectionVars false in
/-- **Submultiplicativity of `sprod`.** `∏σ(A⁽ᵐ⁺ⁿ⁾) ≤ ∏σ(A⁽ᵐ⁾∘Tⁿ) · ∏σ(A⁽ⁿ⁾)`. -/
theorem sprod_submul (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (k m n : ℕ) (x : X) :
    sprod A T k (m + n) x ≤ sprod A T k m (T^[n] x) * sprod A T k n x := by
  unfold sprod
  rw [cocycle_add, toEuclideanLin_mul]
  exact ExteriorNorm.prod_singularValues_comp_le k (Matrix.toEuclideanLin (cocycle A T n x))
    (Matrix.toEuclideanLin (cocycle A T m (T^[n] x)))

/-- **Subadditivity of `log sprod`** in the plain (`T^[n]`-shifted) split, provided each
`sprod` is positive (true for an invertible cocycle and `k ≤ d`). -/
theorem logSprod_subadditive (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (k m n : ℕ) (x : X)
    (hpos : ∀ (j : ℕ) (y : X), 0 < sprod A T k j y) :
    Real.log (sprod A T k (m + n) x)
      ≤ Real.log (sprod A T k m (T^[n] x)) + Real.log (sprod A T k n x) := by
  have hsub := sprod_submul A T k m n x
  calc Real.log (sprod A T k (m + n) x)
      ≤ Real.log (sprod A T k m (T^[n] x) * sprod A T k n x) :=
        Real.log_le_log (hpos (m + n) x) hsub
    _ = Real.log (sprod A T k m (T^[n] x)) + Real.log (sprod A T k n x) :=
        Real.log_mul (ne_of_gt (hpos m (T^[n] x))) (ne_of_gt (hpos n x))

set_option linter.unusedSectionVars false in
/-- **Kingman index convention.** `log sprod` is a subadditive cocycle in Kingman's sense
`g(m+n,x) ≤ g(m,x) + g(n,T^[m]x)`, obtained from the symmetric cocycle split. -/
theorem isSubadditiveCocycle_logSprod {T : X → X} (A : X → Matrix (Fin d) (Fin d) ℝ) (k : ℕ)
    (hpos : ∀ (j : ℕ) (y : X), 0 < sprod A T k j y) :
    IsSubadditiveCocycle T (fun n x => Real.log (sprod A T k n x)) := by
  refine ⟨fun m n x => ?_⟩
  -- Use the symmetric split `cocycle (m+n) x = cocycle n (T^[m] x) * cocycle m x`.
  have hcoc : cocycle A T (m + n) x = cocycle A T n (T^[m] x) * cocycle A T m x := by
    rw [show m + n = n + m by ring, cocycle_add]
  have hsub : sprod A T k (m + n) x ≤ sprod A T k n (T^[m] x) * sprod A T k m x := by
    unfold sprod; rw [hcoc, toEuclideanLin_mul]
    exact ExteriorNorm.prod_singularValues_comp_le k (Matrix.toEuclideanLin (cocycle A T m x))
      (Matrix.toEuclideanLin (cocycle A T n (T^[m] x)))
  calc Real.log (sprod A T k (m + n) x)
      ≤ Real.log (sprod A T k n (T^[m] x) * sprod A T k m x) :=
        Real.log_le_log (hpos (m + n) x) hsub
    _ = Real.log (sprod A T k m x) + Real.log (sprod A T k n (T^[m] x)) := by
        rw [Real.log_mul (ne_of_gt (hpos n (T^[m] x))) (ne_of_gt (hpos m x))]; ring

/-! ## Singular-value/operator-norm bound (matrix form) and sandwich bounds -/

/-- **Matrix form of the singular-value bound.** Each singular value of `toEuclideanLin M` is at
most the L2 operator norm `‖M‖`: `σᵢ(toEuclideanLin M) ≤ ‖M‖`. -/
theorem sigma_le_opNorm (M : Matrix (Fin d) (Fin d) ℝ) (i : ℕ) :
    (Matrix.toEuclideanLin M).singularValues i ≤ ‖M‖ :=
  (Matrix.toEuclideanLin M).singularValues_le_opNorm i

/-- A lower bound on every singular value of an invertible matrix: `(‖M⁻¹‖)⁻¹ ≤ σᵢ`, for
`i < d`. (`uᵢ = M⁻¹(M uᵢ)`, so `1 = ‖uᵢ‖ ≤ ‖M⁻¹‖ · ‖M uᵢ‖ = ‖M⁻¹‖ · σᵢ`.) -/
theorem inv_opNorm_inv_le_sigma {M : Matrix (Fin d) (Fin d) ℝ} (hM : M.det ≠ 0) {i : ℕ}
    (hi : i < d) : (‖M⁻¹‖)⁻¹ ≤ (Matrix.toEuclideanLin M).singularValues i := by
  set f := Matrix.toEuclideanLin M with hf
  have hfin : Module.finrank ℝ (EuclideanSpace ℝ (Fin d)) = d := finrank_euclideanSpace_fin
  set u := f.isSymmetric_adjoint_comp_self.eigenvectorBasis hfin with hu
  -- `σᵢ = ‖f uᵢ‖`.
  have hσ : f.singularValues i = ‖f (u ⟨i, hi⟩)‖ :=
    (f.norm_apply_eigenvectorBasis_eq_singularValues hfin ⟨i, hi⟩).symm
  -- `M⁻¹ * M = 1`, so `toEuclideanLin M⁻¹ (f uᵢ) = uᵢ`.
  have hinv : M⁻¹ * M = 1 := Matrix.nonsing_inv_mul _ (Ne.isUnit hM)
  have hround : Matrix.toEuclideanLin M⁻¹ (f (u ⟨i, hi⟩)) = u ⟨i, hi⟩ := by
    rw [hf, ← LinearMap.comp_apply, ← toEuclideanLin_mul, hinv]
    simp
  -- `‖uᵢ‖ ≤ ‖M⁻¹‖ · ‖f uᵢ‖`.
  have hbound : ‖u ⟨i, hi⟩‖ ≤ ‖M⁻¹‖ * ‖f (u ⟨i, hi⟩)‖ := by
    have hle := (Matrix.toEuclideanLin M⁻¹).singularValues_le_opNorm 0
    have hople : ‖(Matrix.toEuclideanLin M⁻¹) (f (u ⟨i, hi⟩))‖
        ≤ ‖LinearMap.toContinuousLinearMap (Matrix.toEuclideanLin M⁻¹)‖ * ‖f (u ⟨i, hi⟩)‖ := by
      have := (LinearMap.toContinuousLinearMap (Matrix.toEuclideanLin M⁻¹)).le_opNorm
        (f (u ⟨i, hi⟩))
      rwa [LinearMap.coe_toContinuousLinearMap'] at this
    rw [hround] at hople
    have hnorm : ‖LinearMap.toContinuousLinearMap (Matrix.toEuclideanLin M⁻¹)‖ = ‖M⁻¹‖ := rfl
    rw [hnorm] at hople
    exact hople
  have hu1 : ‖u ⟨i, hi⟩‖ = 1 := u.orthonormal.1 _
  rw [hu1] at hbound
  have hinvpos : 0 < ‖M⁻¹‖ := by
    rw [norm_pos_iff]
    intro hz
    have hdet : (M⁻¹).det ≠ 0 := by
      rw [Matrix.det_nonsing_inv, Ring.inverse_eq_inv']; exact inv_ne_zero hM
    exact hdet (by rw [hz, Matrix.det_zero]; exact ⟨⟨i, hi⟩⟩)
  rw [hσ, inv_le_iff_one_le_mul₀ hinvpos]
  linarith [hbound]

/-! ## Positivity of `sprod` (the Kingman `hpos` proviso, for `k ≤ d`) -/

/-- `toEuclideanLin M` is injective when `M` is invertible (`det M ≠ 0`). -/
theorem injective_toEuclideanLin {M : Matrix (Fin d) (Fin d) ℝ} (hM : M.det ≠ 0) :
    Function.Injective (Matrix.toEuclideanLin M) := by
  have hinv : M⁻¹ * M = 1 := Matrix.nonsing_inv_mul _ (Ne.isUnit hM)
  have hid : (Matrix.toEuclideanLin M⁻¹) ∘ₗ (Matrix.toEuclideanLin M) = LinearMap.id := by
    rw [← toEuclideanLin_mul, hinv]
    ext v i
    simp
  exact Function.LeftInverse.injective (g := Matrix.toEuclideanLin M⁻¹)
    (fun a => by rw [← LinearMap.comp_apply, hid, LinearMap.id_apply])

set_option linter.unusedSectionVars false in
/-- Each of the top-`d` singular values of an invertible cocycle iterate is strictly positive. -/
theorem singularValues_cocycle_pos {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X}
    (hA : ∀ x, (A x).det ≠ 0) (n : ℕ) (x : X) {i : ℕ} (hi : i < d) :
    0 < (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i := by
  have hdet : (cocycle A T n x).det ≠ 0 := det_cocycle_ne_zero hA n x
  have hinj : Function.Injective (Matrix.toEuclideanLin (cocycle A T n x)) :=
    injective_toEuclideanLin hdet
  have hfin : Module.finrank ℝ (EuclideanSpace ℝ (Fin d)) = d := finrank_euclideanSpace_fin
  have hpos := (Matrix.toEuclideanLin
    (cocycle A T n x)).injective_iff_forall_lt_finrank_singularValues_pos.mp hinj
  exact hpos i (by rw [hfin]; exact hi)

/-- **`hpos` for `k ≤ d`.** `sprod A T k n x > 0` for an invertible cocycle and `k ≤ d`. -/
theorem sprod_pos {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X}
    (hA : ∀ x, (A x).det ≠ 0) {k : ℕ} (hk : k ≤ d) (n : ℕ) (x : X) :
    0 < sprod A T k n x :=
  Finset.prod_pos fun _i hi =>
    singularValues_cocycle_pos hA n x (lt_of_lt_of_le (Finset.mem_range.mp hi) hk)

/-! ## Integrability and bounded-below of `log sprod`

The sandwich `−k·log‖(A⁽ⁿ⁾)⁻¹‖ ≤ log sprod ≤ k·log‖A⁽ⁿ⁾‖` (from the singular-value/operator-norm
bound and its inverse companion) dominates `log sprod` by integrable functions, reusing the
Furstenberg–Kesten integrability plumbing. -/

variable [NeZero d]

set_option linter.unusedSectionVars false in
/-- **Upper Fekete bound.** `log sprod_k ≤ k · log‖A⁽ⁿ⁾‖`. -/
theorem logSprod_le {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X}
    (hA : ∀ x, (A x).det ≠ 0) {k : ℕ} (hk : k ≤ d) (n : ℕ) (x : X) :
    Real.log (sprod A T k n x) ≤ (k : ℝ) * Real.log ‖cocycle A T n x‖ := by
  rw [sprod, Real.log_prod (fun i hi =>
    ne_of_gt (singularValues_cocycle_pos hA n x (lt_of_lt_of_le (Finset.mem_range.mp hi) hk)))]
  have hbnd : ∀ i ∈ Finset.range k,
      Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i)
        ≤ Real.log ‖cocycle A T n x‖ := by
    intro i hi
    have hpos := singularValues_cocycle_pos (T := T) hA n x
      (lt_of_lt_of_le (Finset.mem_range.mp hi) hk)
    exact Real.log_le_log hpos (sigma_le_opNorm _ i)
  calc ∑ i ∈ Finset.range k,
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i)
      ≤ ∑ _i ∈ Finset.range k, Real.log ‖cocycle A T n x‖ := Finset.sum_le_sum hbnd
    _ = (k : ℝ) * Real.log ‖cocycle A T n x‖ := by
        rw [Finset.sum_const, Finset.card_range, nsmul_eq_mul]

/-- **Lower Fekete bound.** `−k · log‖(A⁽ⁿ⁾)⁻¹‖ ≤ log sprod_k`. -/
theorem neg_le_logSprod {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X}
    (hA : ∀ x, (A x).det ≠ 0) {k : ℕ} (hk : k ≤ d) (n : ℕ) (x : X) :
    - ((k : ℝ) * Real.log ‖(cocycle A T n x)⁻¹‖) ≤ Real.log (sprod A T k n x) := by
  rw [sprod, Real.log_prod (fun i hi =>
    ne_of_gt (singularValues_cocycle_pos hA n x (lt_of_lt_of_le (Finset.mem_range.mp hi) hk)))]
  have hdet : (cocycle A T n x).det ≠ 0 := det_cocycle_ne_zero hA n x
  have hbnd : ∀ i ∈ Finset.range k,
      - Real.log ‖(cocycle A T n x)⁻¹‖
        ≤ Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i) := by
    intro i hi
    have hik := lt_of_lt_of_le (Finset.mem_range.mp hi) hk
    have hlb := inv_opNorm_inv_le_sigma hdet hik
    have hinvpos : 0 < ‖(cocycle A T n x)⁻¹‖ := norm_inv_cocycle_pos hA n x
    -- `-log‖M⁻¹‖ = log (‖M⁻¹‖)⁻¹ ≤ log σᵢ`.
    rw [← Real.log_inv]
    exact Real.log_le_log (by positivity) hlb
  calc - ((k : ℝ) * Real.log ‖(cocycle A T n x)⁻¹‖)
      = ∑ _i ∈ Finset.range k, (- Real.log ‖(cocycle A T n x)⁻¹‖) := by
        rw [Finset.sum_const, Finset.card_range, nsmul_eq_mul]; ring
    _ ≤ ∑ i ∈ Finset.range k,
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i) :=
        Finset.sum_le_sum hbnd

variable {μ : Measure X} {T : X → X}

/-- Measurability of the determinant of a measurable square-matrix-valued function (entrywise a
polynomial in the measurable entries). Used to read off measurability of the compound-matrix
entries, which are minors of the cocycle iterate. -/
theorem measurable_det_comp {k : ℕ} {N : X → Matrix (Fin k) (Fin k) ℝ}
    (hN : Measurable N) : Measurable (fun x => (N x).det) := by
  have hentry : ∀ i j : Fin k, Measurable fun x => N x i j := fun i j =>
    (measurable_pi_apply j).comp ((measurable_pi_apply i).comp hN)
  simp only [Matrix.det_apply]
  refine Finset.measurable_sum _ fun σ _ => ?_
  refine Measurable.const_smul ?_ _
  exact Finset.measurable_prod _ fun i _ => hentry _ _

set_option linter.unusedSectionVars false in
/-- Measurability of `x ↦ sprod A T k n x`. By the **compound-matrix bridge**
`ExteriorNorm.prod_singularValues_eq_l2_opNorm_compound`, the product of the top-`k` singular
values equals the L2 operator norm of the `k`-th **compound matrix** `C_k(A⁽ⁿ⁾ x)`, whose entries
are the `k × k` minors of `A⁽ⁿ⁾ x`. Each minor is the determinant of a submatrix of the
(measurable) cocycle iterate, hence measurable; the matrix-valued map is then measurable
entrywise, and the (continuous) L2 operator norm preserves measurability. No exterior-power /
linear-map continuity is needed. -/
theorem measurable_sprod {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X}
    (hAmeas : Measurable A) (hTmeas : Measurable T) (k n : ℕ) :
    Measurable (fun x => sprod A T k n x) := by
  -- `sprod = ‖compoundMatrix k (cocycle A T n x)‖`.
  have heq : (fun x => sprod A T k n x)
      = fun x => ‖ExteriorNorm.compoundMatrix k (cocycle A T n x)‖ := by
    funext x
    rw [sprod, ExteriorNorm.prod_singularValues_eq_l2_opNorm_compound]
  rw [heq]
  -- The L2 operator norm is measurable on the entrywise σ-algebra; reduce to the compound matrix.
  refine measurable_l2_opNorm.comp ?_
  have hcoc : Measurable fun x => cocycle A T n x := measurable_cocycle hAmeas hTmeas n
  -- A matrix-valued map is measurable iff each entry is; each entry is a minor (a determinant).
  refine measurable_pi_iff.2 fun t => measurable_pi_iff.2 fun s => ?_
  simp only [ExteriorNorm.compoundMatrix, Matrix.of_apply]
  -- The submatrix entries are measurable (entries of the measurable cocycle), so its det is too.
  refine measurable_det_comp ?_
  refine measurable_pi_iff.2 fun i => measurable_pi_iff.2 fun j => ?_
  simp only [Matrix.submatrix_apply]
  exact (measurable_pi_apply _).comp ((measurable_pi_apply _).comp hcoc)

/-- **Integrability of `log sprod`.** Each level `gₙ = log sprod_k` is integrable, dominated
by the two (integrable) Furstenberg–Kesten log-norm cocycles. -/
theorem integrable_logSprod (hT : MeasurePreserving T μ μ) [IsFiniteMeasure μ]
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hTmeas : Measurable T) (hint : IntegrableLogNorm A μ)
    (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) {k : ℕ} (hk : k ≤ d) (n : ℕ) :
    Integrable (fun x => Real.log (sprod A T k n x)) μ := by
  -- The dominating bounds (FK integrability), scaled by `k`.
  have hU : Integrable (fun x => (k : ℝ) * Real.log ‖cocycle A T n x‖) μ :=
    (integrable_logNorm_cocycle hT hA hAmeas hTmeas hint hint' n).const_mul _
  have hL : Integrable (fun x => - ((k : ℝ) * Real.log ‖(cocycle A T n x)⁻¹‖)) μ :=
    ((integrable_logNorm_inv_cocycle hT hA hAmeas hTmeas hint hint' n).const_mul _).neg
  -- Measurability of `log sprod` (from measurability of `sprod`).
  have hmeas : AEStronglyMeasurable (fun x => Real.log (sprod A T k n x)) μ :=
    (Real.measurable_log.comp (measurable_sprod hAmeas hTmeas k n)).aestronglyMeasurable
  exact integrable_of_le_of_le hmeas
    (Filter.Eventually.of_forall fun x => neg_le_logSprod hA hk n x)
    (Filter.Eventually.of_forall fun x => logSprod_le hA hk n x) hL hU

/-- **Bounded-below proviso (Fekete lower bound).** The normalized integrals of `log sprod`
are bounded below by `−k · ∫ log⁺‖A⁻¹‖`, keeping the Kingman limit finite. -/
theorem bddBelow_logSprod (hT : MeasurePreserving T μ μ) [IsFiniteMeasure μ]
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hTmeas : Measurable T) (hint : IntegrableLogNorm A μ)
    (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ) {k : ℕ} (hk : k ≤ d) :
    BddBelow (Set.range fun n : ℕ =>
      (∫ x, Real.log (sprod A T k (n + 1) x) ∂μ) / (n + 1)) := by
  refine ⟨- ((k : ℝ) * ∫ x, Real.posLog ‖(A x)⁻¹‖ ∂μ), ?_⟩
  rintro _ ⟨n, rfl⟩
  have hpos : (0 : ℝ) < (n : ℝ) + 1 := by positivity
  rw [le_div_iff₀ hpos]
  -- lower bound on the integral of `log sprod`.
  have hlb : ∀ x, - ((k : ℝ) * birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) (n + 1) x)
      ≤ Real.log (sprod A T k (n + 1) x) := by
    intro x
    refine le_trans ?_ (neg_le_logSprod hA hk (n + 1) x)
    have hub := logNorm_inv_cocycle_le_birkhoffSum (T := T) hA (n + 1) x
    have hknn : (0 : ℝ) ≤ (k : ℝ) := Nat.cast_nonneg k
    nlinarith [hub, hknn]
  have hmono : - ((k : ℝ) * ∫ x, birkhoffSum T (fun y => Real.posLog ‖(A y)⁻¹‖) (n + 1) x ∂μ)
      ≤ ∫ x, Real.log (sprod A T k (n + 1) x) ∂μ := by
    rw [← integral_const_mul, ← integral_neg]
    exact integral_mono (((integrable_birkhoffSum hT hint' (n + 1)).const_mul _).neg)
      (integrable_logSprod hT hA hAmeas hTmeas hint hint' hk (n + 1)) hlb
  rw [integral_birkhoffSum hT hint' (n + 1), nsmul_eq_mul] at hmono
  push_cast at hmono ⊢
  nlinarith [hmono]

/-! ## Squared singular values are the Gram eigenvalues -/

set_option linter.unusedSectionVars false in
/-- The adjoint of `toEuclideanLin M` composed with `toEuclideanLin M` equals `toEuclideanLin`
of the Gram matrix `Mᵀ M` (over `ℝ`). -/
theorem adjoint_comp_self_eq_gram (M : Matrix (Fin d) (Fin d) ℝ) :
    (Matrix.toEuclideanLin M).adjoint ∘ₗ (Matrix.toEuclideanLin M)
      = Matrix.toEuclideanLin (Mᵀ * M) := by
  have hadj := Matrix.toEuclideanLin_conjTranspose_eq_adjoint M
  rw [Matrix.conjTranspose_eq_transpose_of_trivial] at hadj
  calc
    (Matrix.toEuclideanLin M).adjoint ∘ₗ Matrix.toEuclideanLin M
        = Matrix.toEuclideanLin Mᵀ ∘ₗ Matrix.toEuclideanLin M := by
          exact congrArg (fun f => f ∘ₗ Matrix.toEuclideanLin M) hadj.symm
    _ = Matrix.toEuclideanLin (Mᵀ * M) := by
      ext v i
      simp only [LinearMap.comp_apply, Matrix.toLpLin_apply, Matrix.mulVec_mulVec]

set_option linter.unusedSectionVars false in
/-- **The eigenvalue bridge.** The squared singular values of `toEuclideanLin M` are the
eigenvalues of the symmetric operator `adjoint ∘ self = toEuclideanLin (Mᵀ M)`, i.e. the
eigenvalues of the Gram matrix `Qₙ = (A⁽ⁿ⁾)ᵀ A⁽ⁿ⁾`. This delivers the eigenvalues of the
Oseledets limit `Λ` as genuine ergodic limits (via `tendsto_gammaK`) without constructing `Λ`. -/
theorem sq_singularValues_eq_gram_eigenvalue {n : ℕ} (M : Matrix (Fin d) (Fin d) ℝ)
    (hn : Module.finrank ℝ (EuclideanSpace ℝ (Fin d)) = n) (i : Fin n) :
    (Matrix.toEuclideanLin M).singularValues i ^ 2
      = (Matrix.toEuclideanLin M).isSymmetric_adjoint_comp_self.eigenvalues hn i :=
  (Matrix.toEuclideanLin M).sq_singularValues_fin hn i

/-! ## The genuine ergodic `Γ_k` limit -/

set_option linter.unusedSectionVars false in
/-- **The genuine ergodic `Γ_k` limit** (spike form). Under ergodicity, with the
Furstenberg–Kesten-style integrability (`hint`) and bounded-below (`hbdd`) provisos and the
positivity proviso (`hpos`, valid for `k ≤ d` on an invertible cocycle), the normalized
`log sprod_k` converges `μ`-a.e. to a constant `Γ_k`. -/
theorem tendsto_gammaK [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    (A : X → Matrix (Fin d) (Fin d) ℝ) (k : ℕ)
    (hpos : ∀ (j : ℕ) (y : X), 0 < sprod A T k j y)
    (hint : ∀ n, Integrable (fun x => Real.log (sprod A T k n x)) μ)
    (hbdd : BddBelow (Set.range fun n : ℕ =>
      (∫ x, Real.log (sprod A T k (n + 1) x) ∂μ) / (n + 1))) :
    ∃ Γk : ℝ, ∀ᵐ x ∂μ,
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (sprod A T k n x)) atTop (𝓝 Γk) :=
  tendsto_kingman_ergodic hT (g := fun n x => Real.log (sprod A T k n x))
    (isSubadditiveCocycle_logSprod A k hpos) hint hbdd

/-- **The genuine ergodic `Γ_k` limit** (with the integrability/lower-bound provisos discharged).
For an ergodic
measure-preserving `T`, an everywhere-invertible measurable cocycle generator with
`log⁺‖A‖, log⁺‖A⁻¹‖ ∈ L¹`, and `k ≤ d`, the normalized `log sprod_k` converges `μ`-a.e. to a
constant `Γ_k`. -/
theorem tendsto_gammaK_of_integrableLogNorm [IsProbabilityMeasure μ] (hT : Ergodic T μ)
    {A : X → Matrix (Fin d) (Fin d) ℝ} (hA : ∀ x, (A x).det ≠ 0) (hAmeas : Measurable A)
    (hint : IntegrableLogNorm A μ) (hint' : IntegrableLogNorm (fun x => (A x)⁻¹) μ)
    {k : ℕ} (hk : k ≤ d) :
    ∃ Γk : ℝ, ∀ᵐ x ∂μ,
      Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (sprod A T k n x)) atTop (𝓝 Γk) := by
  have hmp : MeasurePreserving T μ μ := hT.toMeasurePreserving
  have hTmeas : Measurable T := hmp.measurable
  exact tendsto_gammaK hT A k (fun j y => sprod_pos hA hk j y)
    (fun n => integrable_logSprod hmp hA hAmeas hTmeas hint hint' hk n)
    (bddBelow_logSprod hmp hA hAmeas hTmeas hint hint' hk)

/-! ## The per-singular-value exponents -/

set_option linter.unusedSectionVars false in
/-- **Per-`σ` exponent.** Differencing the `Γ_k` limits: if `(1/n) log sprod_{i+1} → a` and
`(1/n) log sprod_i → b` for `μ`-a.e. `x` and the singular values are positive (`k ≤ d`), then the
normalized log of the `i`-th singular value converges to `a − b` (the `i`-th Lyapunov exponent
`λᵢ = Γ_{i+1} − Γ_i`). -/
theorem tendsto_log_singularValue {A : X → Matrix (Fin d) (Fin d) ℝ}
    (hA : ∀ x, (A x).det ≠ 0) {i : ℕ} (hi : i < d) {a b : ℝ} {x : X}
    (ha : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (sprod A T (i + 1) n x)) atTop (𝓝 a))
    (hb : Tendsto (fun n : ℕ => (n : ℝ)⁻¹ * Real.log (sprod A T i n x)) atTop (𝓝 b)) :
    Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
      atTop (𝓝 (a - b)) := by
  -- `log sprod_{i+1} − log sprod_i = log σᵢ` (the telescoping factor at index `i`).
  have hsplit : ∀ n : ℕ,
      (n : ℝ)⁻¹ * Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i)
        = (n : ℝ)⁻¹ * Real.log (sprod A T (i + 1) n x)
          - (n : ℝ)⁻¹ * Real.log (sprod A T i n x) := by
    intro n
    have hSi1 : sprod A T (i + 1) n x
        = sprod A T i n x
          * (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i := by
      rw [sprod, sprod, Finset.prod_range_succ]
    have hSi_pos : 0 < sprod A T i n x := sprod_pos hA (le_of_lt hi) n x
    have hσ_pos : 0 < (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i :=
      singularValues_cocycle_pos hA n x hi
    rw [hSi1, Real.log_mul (ne_of_gt hSi_pos) (ne_of_gt hσ_pos)]
    ring
  refine (ha.sub hb).congr (fun n => (hsplit n).symm)

set_option linter.unusedSectionVars false in
/-- **Antitonicity of the per-`σ` exponents.** For each fixed `n` and `x`, the normalized
logs of the singular values are antitone in the index (since the singular values themselves are
antitone). -/
theorem antitone_log_singularValue (A : X → Matrix (Fin d) (Fin d) ℝ) (n : ℕ) (x : X) :
    Antitone fun i : ℕ =>
      (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i :=
  (Matrix.toEuclideanLin (cocycle A T n x)).singularValues_antitone

/-- **The per-point singular-value Lyapunov exponent.** The `i`-th Lyapunov exponent at the
point `x`, defined as the (junk-on-divergence) limit of the normalized log of the `i`-th singular
value of `A⁽ⁿ⁾`. Where the singular-value limit exists (`μ`-a.e., by `tendsto_log_singularValue`)
this equals the deterministic exponent `λᵢ`; `lamSing` packages it as a concrete per-point datum so
that the spectrum of the Oseledets limit `Λ` can be labelled by `e^{lamSing}`. -/
noncomputable def lamSing (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (x : X) (i : ℕ) : ℝ :=
  limUnder atTop (fun n : ℕ => (n : ℝ)⁻¹ *
    Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))

set_option linter.unusedSectionVars false in
/-- If, at `x`, the normalized log of the `i`-th singular value converges to `lam` (true `μ`-a.e. by
`tendsto_log_singularValue`), then `lamSing A T x i = lam`. -/
theorem lamSing_eq_of_tendsto {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X} {x : X} {i : ℕ}
    {lam : ℝ} (h : Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
      atTop (𝓝 lam)) :
    lamSing A T x i = lam :=
  h.limUnder_eq

/-! ## The Gram matrix is PosSemidef / self-adjoint, and the matrix root `qpow`

The Gram matrix `Qₙ = (A⁽ⁿ⁾)ᵀ A⁽ⁿ⁾` is positive semidefinite and self-adjoint, so the
continuous functional calculus applies to it. The candidate Oseledets limit at level `n` is the
matrix `(Qₙ)^{1/(2n)} = cfc (·^{1/(2n)}) Qₙ`, whose eigenvalues are the `1/n`-th powers of the
singular values of `A⁽ⁿ⁾`. -/

set_option linter.unusedSectionVars false in
/-- The Gram matrix `Qₙ = (A⁽ⁿ⁾)ᵀ A⁽ⁿ⁾` is positive semidefinite. -/
theorem gram_posSemidef (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ) (x : X) :
    (gram A T n x).PosSemidef := by
  unfold gram
  have h : (cocycle A T n x)ᴴ * cocycle A T n x = (cocycle A T n x)ᵀ * cocycle A T n x := by
    rw [Matrix.conjTranspose_eq_transpose_of_trivial]
  rw [← h]
  exact Matrix.posSemidef_conjTranspose_mul_self _

/-- The Gram matrix `Qₙ = (A⁽ⁿ⁾)ᵀ A⁽ⁿ⁾` is self-adjoint, hence the continuous
functional calculus applies to it. -/
theorem gram_isSelfAdjoint (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ) (x : X) :
    IsSelfAdjoint (gram A T n x) :=
  (gram_posSemidef A T n x).isHermitian.isSelfAdjoint

/-- The candidate Oseledets limit at level `n`: the matrix `1/(2n)`-th power
`(Qₙ)^{1/(2n)} = cfc (·^{1/(2n)}) Qₙ` of the Gram matrix, defined via the continuous functional
calculus on the (self-adjoint, positive semidefinite) Gram matrix `Qₙ`. Its eigenvalues are the
`1/n`-th powers of the singular values of `A⁽ⁿ⁾`, which converge to `e^{λᵢ}`
(see `eigenvalues_qpow_tendsto`). -/
def qpow (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ) (x : X) :
    Matrix (Fin d) (Fin d) ℝ :=
  cfc (fun t : ℝ => t ^ ((2 * (n : ℝ))⁻¹)) (gram A T n x)

set_option linter.unusedSectionVars false in
/-- `qpow A T n x` is self-adjoint (a CFC of a real-valued function is always self-adjoint). -/
theorem qpow_isSelfAdjoint (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ) (x : X) :
    IsSelfAdjoint (qpow A T n x) :=
  cfc_predicate _ _

/-- `qpow A T n x = (Qₙ)^{1/(2n)}` is positive semidefinite: `cfc` of the nonnegative function
`t ↦ t^{1/(2n)}` on the PosSemidef (hence nonnegative-spectrum) Gram matrix `Qₙ` yields a
nonnegative (hence PosSemidef) matrix. -/
theorem qpow_posSemidef (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ) (x : X) :
    (qpow A T n x).PosSemidef := by
  have hspec : _root_.spectrum ℝ (gram A T n x) ⊆ {a : ℝ | 0 ≤ a} :=
    (Matrix.posSemidef_iff_isHermitian_and_spectrum_nonneg.mp (gram_posSemidef A T n x)).2
  have hnonneg : (0 : Matrix (Fin d) (Fin d) ℝ) ≤ qpow A T n x := by
    refine cfc_nonneg (fun t ht => ?_)
    exact Real.rpow_nonneg (hspec ht) _
  exact Matrix.nonneg_iff_posSemidef.mp hnonneg

/-! ## The eigenvalues of `qpow` converge to `e^{λᵢ}`

The eigenvalues of `qpow A T n x = (Qₙ)^{1/(2n)}` are the `1/n`-th powers of the singular values
of `A⁽ⁿ⁾`. Since `(1/n) log σᵢ → λᵢ` a.e. (`tendsto_log_singularValue`), these converge to
`e^{λᵢ}`. The CFC of a monotone function applied to a Hermitian matrix has, as its sorted
eigenvalues, that function applied to the sorted eigenvalues of the matrix; we package this as a
helper and then chain it with the singular-value layer. -/

/-- The roots of the characteristic polynomial of `cfc f A` (for Hermitian `A`) are `f` applied to
the eigenvalues of `A` (cast into `𝕜`). The matrix analogue of
`Matrix.IsHermitian.roots_charpoly_eq_eigenvalues`. -/
theorem roots_charpoly_cfc_eq {n : Type*} [Fintype n] [DecidableEq n] {𝕜 : Type*} [RCLike 𝕜]
    {A : Matrix n n 𝕜} (hA : A.IsHermitian) (f : ℝ → ℝ) :
    (cfc f A).charpoly.roots
      = Multiset.map (RCLike.ofReal ∘ (f ∘ hA.eigenvalues)) Finset.univ.val := by
  rw [Matrix.IsHermitian.charpoly_cfc_eq hA f, Polynomial.roots_prod]
  · simp [Function.comp_def]
  · simp [Finset.prod_ne_zero_iff, Polynomial.X_sub_C_ne_zero]

/-- For a Hermitian matrix `A` with nonnegative eigenvalues and a function `f` that is monotone on
`[0, ∞)` (hence preserves the descending order of the eigenvalues), the sorted eigenvalues
`eigenvalues₀` of `cfc f A` are `f` applied to the sorted eigenvalues of `A`. The matrix analogue
(with a monotonicity-on-the-spectrum hypothesis) of
`Matrix.IsHermitian.sort_roots_charpoly_eq_eigenvalues₀`. The `MonotoneOn` form is needed because
the relevant function `t ↦ t^{1/(2n)}` is `Real.rpow`, which is monotone only on `[0, ∞)`. -/
theorem eigenvalues₀_cfc_of_monotoneOn {n : Type*} [Fintype n] [DecidableEq n] {𝕜 : Type*}
    [RCLike 𝕜] {A : Matrix n n 𝕜} (hA : A.IsHermitian) {f : ℝ → ℝ}
    (hf : MonotoneOn f (Set.Ici 0)) (hpos : ∀ i, 0 ≤ hA.eigenvalues₀ i) :
    ((cfc_predicate f A : IsSelfAdjoint (cfc f A)).isHermitian).eigenvalues₀
      = f ∘ hA.eigenvalues₀ := by
  -- `f ∘ eigenvalues₀` is antitone, because `eigenvalues₀` is antitone into `[0, ∞)` and `f` is
  -- monotone there.
  have hanti : Antitone (f ∘ hA.eigenvalues₀) := by
    intro i j hij
    exact hf (hpos j) (hpos i) (Matrix.IsHermitian.eigenvalues₀_antitone hA hij)
  -- Both sides, sorted descending, agree as lists.
  rw [← List.ofFn_inj,
    ← Matrix.IsHermitian.sort_roots_charpoly_eq_eigenvalues₀]
  -- The real parts of the roots of `(cfc f A).charpoly` are `f ∘ eigenvalues₀` over `univ`.
  have hroots : (cfc f A).charpoly.roots.map RCLike.re
      = Multiset.map (f ∘ hA.eigenvalues₀) Finset.univ.val := by
    rw [roots_charpoly_cfc_eq hA f, Multiset.map_map]
    simp only [Matrix.IsHermitian.eigenvalues, Function.comp_def, RCLike.ofReal_re]
    -- Reindex `univ` by the bijection `(equivOfCardEq).symm`.
    have hmap : Multiset.map
        (fun i => f (hA.eigenvalues₀ ((Fintype.equivOfCardEq (Fintype.card_fin _)).symm i)))
        Finset.univ.val
        = Multiset.map (fun j => f (hA.eigenvalues₀ j))
          (Finset.univ.map (Fintype.equivOfCardEq (Fintype.card_fin _)).symm.toEmbedding).val := by
      rw [Finset.map_val, Multiset.map_map]; rfl
    rw [hmap, Finset.map_univ_equiv]
  rw [hroots]
  -- Sorting an already-antitone tuple is the identity.
  simp only [Fin.univ_val_map, Function.comp_def, Multiset.coe_sort]
  refine List.mergeSort_of_pairwise ?_
  simp_rw [decide_eq_true_eq, ← List.sortedGE_iff_pairwise]
  exact hanti.sortedGE_ofFn

/-- The sorted eigenvalues `eigenvalues₀` of the Gram matrix `Qₙ = (A⁽ⁿ⁾)ᵀ A⁽ⁿ⁾` are the squared
singular values of `A⁽ⁿ⁾`: `eigenvalues₀ (Qₙ) i = σᵢ(A⁽ⁿ⁾)²`. This bridges the matrix-eigenvalue
layer (`Matrix.IsHermitian.eigenvalues₀`) to the singular-value layer
(`sq_singularValues_eq_gram_eigenvalue`). -/
theorem gram_eigenvalues₀_eq_sq_singularValues (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X)
    (n : ℕ) (x : X) (i : Fin (Fintype.card (Fin d))) :
    (gram_posSemidef A T n x).isHermitian.eigenvalues₀ i
      = (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i ^ 2 := by
  set M := cocycle A T n x with hM
  -- `eigenvalues₀` of the Gram matrix = eigenvalues of `toEuclideanLin (gram)` (linear-map layer).
  have hsym₁ : (Matrix.toEuclideanLin (gram A T n x)).IsSymmetric :=
    Matrix.isHermitian_iff_isSymmetric.mp (gram_posSemidef A T n x).isHermitian
  -- The `adjoint ∘ self` operator equals `toEuclideanLin (gram)`.
  have hop : (Matrix.toEuclideanLin M).adjoint ∘ₗ (Matrix.toEuclideanLin M)
      = Matrix.toEuclideanLin (gram A T n x) := by
    rw [gram, ← hM]; exact adjoint_comp_self_eq_gram M
  have hsym₂ : ((Matrix.toEuclideanLin M).adjoint ∘ₗ (Matrix.toEuclideanLin M)).IsSymmetric :=
    (Matrix.toEuclideanLin M).isSymmetric_adjoint_comp_self
  have hfr : Module.finrank ℝ (EuclideanSpace ℝ (Fin d)) = Fintype.card (Fin d) :=
    finrank_euclideanSpace
  -- The two symmetric operators are equal, hence have equal eigenvalue functions.
  -- `eigenvalues₀` of the Gram matrix is by definition the linear-map eigenvalues.
  have hdef : (gram_posSemidef A T n x).isHermitian.eigenvalues₀ i = hsym₁.eigenvalues hfr i := by
    rfl
  rw [hdef]
  have heig : hsym₁.eigenvalues hfr i = hsym₂.eigenvalues hfr i := by
    congr 2
    exact hop.symm
  rw [heig]
  -- The bridge: `σᵢ² = eigenvalues (adjoint ∘ self)`.
  exact (sq_singularValues_eq_gram_eigenvalue M hfr i).symm

/-- **The eigenvalues of `qpow` are the `1/n`-th powers of the singular values.** The sorted
eigenvalues of `qpow A T n x = (Qₙ)^{1/(2n)}` are `σᵢ(A⁽ⁿ⁾)^{1/n}`. -/
theorem eigenvalues₀_qpow_eq (A : X → Matrix (Fin d) (Fin d) ℝ) (T : X → X) (n : ℕ) (x : X)
    (i : Fin (Fintype.card (Fin d))) :
    (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ i
      = (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i ^ ((n : ℝ)⁻¹) := by
  -- The function `t ↦ t^{1/(2n)}` is monotone on `[0, ∞)` and the Gram eigenvalues are nonneg.
  have hmono : MonotoneOn (fun t : ℝ => t ^ ((2 * (n : ℝ))⁻¹)) (Set.Ici 0) :=
    Real.monotoneOn_rpow_Ici_of_exponent_nonneg (by positivity)
  have hpos : ∀ j, 0 ≤ (gram_posSemidef A T n x).isHermitian.eigenvalues₀ j := by
    intro j
    rw [gram_eigenvalues₀_eq_sq_singularValues]; positivity
  -- The eigenvalues of `qpow = cfc (·^{1/(2n)}) (gram)` are `(·^{1/(2n)})` of the Gram eigenvalues.
  have hcfc := eigenvalues₀_cfc_of_monotoneOn (gram_posSemidef A T n x).isHermitian hmono hpos
  -- `qpow_isSelfAdjoint` is definitionally `cfc_predicate (·^{1/(2n)}) (gram)`.
  have hi : (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ i
      = (fun t : ℝ => t ^ ((2 * (n : ℝ))⁻¹))
          ((gram_posSemidef A T n x).isHermitian.eigenvalues₀ i) := by
    rw [show (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ i
        = ((cfc_predicate (fun t : ℝ => t ^ ((2 * (n : ℝ))⁻¹))
            (gram A T n x) : IsSelfAdjoint _).isHermitian).eigenvalues₀ i from rfl, hcfc]
    rfl
  rw [hi, gram_eigenvalues₀_eq_sq_singularValues]
  -- `(σᵢ²)^{1/(2n)} = σᵢ^{1/n}` via `rpow` rules (`σᵢ ≥ 0`).
  set σ := (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i with hσ
  have hσnn : 0 ≤ σ := (Matrix.toEuclideanLin (cocycle A T n x)).singularValues_nonneg i
  simp only
  rw [← Real.rpow_natCast σ 2, ← Real.rpow_mul hσnn]
  congr 1
  push_cast
  field_simp

/-- **The eigenvalues of `qpow` converge to `e^{λᵢ}`.** If, at a point `x`, the normalized log
of the `i`-th singular value of `A⁽ⁿ⁾` converges to `λᵢ` (which holds `μ`-a.e. by
`tendsto_log_singularValue`), then the `i`-th sorted eigenvalue of `qpow A T n x = (Qₙ)^{1/(2n)}`
converges to `e^{λᵢ}`. This is the eigenvalue layer of the Oseledets limit: the eigenvalues of the
candidate matrix limit are the exponentials of the Lyapunov exponents. Stated per eigenvalue-index
`i` (eigenvalues may repeat across distinct exponents — that is harmless here; the
per-distinct-exponent constraint only bites for the band spectral projectors below). -/
theorem eigenvalues_qpow_tendsto {A : X → Matrix (Fin d) (Fin d) ℝ} {T : X → X}
    (hA : ∀ x, (A x).det ≠ 0) {x : X} (i : Fin (Fintype.card (Fin d))) {lam : ℝ}
    (hlam : Tendsto
      (fun n : ℕ => (n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i))
      atTop (𝓝 lam)) :
    Tendsto (fun n : ℕ => (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ i)
      atTop (𝓝 (Real.exp lam)) := by
  have hid : (i : ℕ) < d := lt_of_lt_of_eq i.isLt (Fintype.card_fin d)
  -- For each `n ≥ 1`, the eigenvalue `σᵢ^{1/n} = exp((1/n) log σᵢ)` (using `σᵢ > 0`).
  have hev : ∀ n : ℕ, 1 ≤ n →
      (qpow_isSelfAdjoint A T n x).isHermitian.eigenvalues₀ i
        = Real.exp ((n : ℝ)⁻¹ *
            Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i)) := by
    intro n hn
    have hσpos : 0 < (Matrix.toEuclideanLin (cocycle A T n x)).singularValues i :=
      singularValues_cocycle_pos hA n x hid
    rw [eigenvalues₀_qpow_eq, Real.rpow_def_of_pos hσpos]
    ring_nf
  -- The exponent sequence converges to `lam`, so its exponential converges to `e^{lam}`.
  have hexp : Tendsto
      (fun n : ℕ => Real.exp ((n : ℝ)⁻¹ *
        Real.log ((Matrix.toEuclideanLin (cocycle A T n x)).singularValues i)))
      atTop (𝓝 (Real.exp lam)) :=
    (Real.continuous_exp.tendsto lam).comp hlam
  -- The eigenvalue sequence agrees with the exponential sequence eventually (for `n ≥ 1`).
  refine hexp.congr' ?_
  filter_upwards [eventually_ge_atTop 1] with n hn using (hev n hn).symm

/-! ## The Oseledets-limit existence statement (`oseledetsLimit`)

The Prop that the band-projector machinery below discharges: a.e., the matrix sequence
`(Qₙ)^{1/(2n)} = qpow A T n x` converges, in the (complete, finite-dimensional) matrix metric, to
a single matrix `Λ x`. -/

/-- **The Oseledets-limit existence statement.** A.e. the `1/(2n)`-th matrix power of the Gram
matrix converges (in the finite-dimensional matrix metric) to a single matrix `Λ x`. This is the
existence statement of the Oseledets limit; it is proved jointly with its eigen-data conclusions
below (the gapped band-projector-Cauchy estimate). -/
def oseledetsLimitExists (μ : Measure X) (T : X → X) (A : X → Matrix (Fin d) (Fin d) ℝ) : Prop :=
  ∃ Λ : X → Matrix (Fin d) (Fin d) ℝ,
    ∀ᵐ x ∂μ, Tendsto (fun n : ℕ => qpow A T n x) atTop (𝓝 (Λ x))

end ErgodicTheory

end
