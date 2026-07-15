/-
Copyright (c) 2026 Marcel Morgenstern. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Marcel Morgenstern
-/
import Mathlib.Analysis.InnerProductSpace.SingularValues
import Mathlib.Analysis.InnerProductSpace.PiL2
import Mathlib.Analysis.InnerProductSpace.LinearMap
import Mathlib.LinearAlgebra.ExteriorPower.Basis
import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Analysis.CStarAlgebra.Matrix
import Mathlib.LinearAlgebra.Trace
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Analysis.Matrix.PosDef
import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas

/-!
# Operator norm of the exterior power: trivializations and the compound matrix

For finite-dimensional real inner product spaces `E`, `F`, this module builds the operator-norm
theory of the `k`-th exterior power `⋀^k f` of a linear map `f : E →ₗ[ℝ] F`: the submultiplicativity
engine, the Hodge and orthonormal-basis trivializations, and the compound matrix with its
Cauchy–Binet multiplicativity. The Plücker eigenvalue ceilings and the Weyl perturbation theory
that build on this layer live in `ErgodicTheory.Lyapunov.ExteriorNorm.Plucker` and
`ErgodicTheory.Lyapunov.ExteriorNorm.Weyl`.

## Main definitions

* `ErgodicTheory.ExteriorNorm.compoundMatrix` — the `k`-th compound matrix, whose entries are the
  `k × k` minors.

## Main results

* `ErgodicTheory.ExteriorNorm.exteriorOpNorm_comp_le` — submultiplicativity of the exterior-power
  operator norm under composition.
* `ErgodicTheory.ExteriorNorm.exteriorOpNorm_hodge_eq_prod_singularValues` — the bridge
  identifying the
  exterior operator norm with the product of the top-`k` singular values `∏_{i<k} σᵢ(f)`.
* `ErgodicTheory.ExteriorNorm.compoundMatrix_mul`,
  `ErgodicTheory.ExteriorNorm.prod_singularValues_eq_l2_opNorm_compound` — Cauchy–Binet
  multiplicativity
  and the operator-norm identity of the compound matrix.

## Implementation notes

The type `⋀[ℝ]^k E` is definitionally `↥(Submodule …)` and already carries an `AddCommGroup`
instance coming from the ambient submodule. Asserting or installing a *fresh*
`NormedAddCommGroup (⋀[ℝ]^k E)` would create an `AddCommGroup`/topology **diamond** that breaks
even `IsTopologicalAddGroup` synthesis on `⋀^k E`.

To stay diamond-free we never put a normed structure on `⋀^k E`. Instead we carry an explicit
**linear trivialization** `ε : ⋀^k E ≃ₗ[ℝ] EuclideanSpace ℝ (Fin n)` as *data* and measure the
operator norm of the conjugated map in the genuine Euclidean target. Such a canonical
trivialization exists because `⋀^k E` is a finite free `ℝ`-module.

A small set of trivialization/ordering helper lemmas in this file are not `private` because the
`Plucker` layer downstream reuses them; they are internal infrastructure, not public API.
-/

open Module InnerProductSpace
open scoped Matrix.Norms.L2Operator Matrix

noncomputable section

namespace ErgodicTheory.ExteriorNorm

set_option maxHeartbeats 1000000

/-! ## The submultiplicativity engine

We carry explicit linear trivializations `ε : ⋀^k · ≃ₗ EuclideanSpace ℝ (Fin n)` as data and
take the operator norm of the conjugated exterior map in the genuine Euclidean target. -/

section Engine

variable {E F G : Type*}
  [NormedAddCommGroup E] [NormedSpace ℝ E] [FiniteDimensional ℝ E]
  [NormedAddCommGroup F] [NormedSpace ℝ F] [FiniteDimensional ℝ F]
  [NormedAddCommGroup G] [NormedSpace ℝ G] [FiniteDimensional ℝ G]
  {k nE nF nG : ℕ}

/-- The `k`-th exterior map `⋀^k f`, conjugated through trivializations of source and target
exterior powers into genuine Euclidean spaces. -/
def conjExteriorMap (k : ℕ)
    (εE : (⋀[ℝ]^k E) ≃ₗ[ℝ] EuclideanSpace ℝ (Fin nE))
    (εF : (⋀[ℝ]^k F) ≃ₗ[ℝ] EuclideanSpace ℝ (Fin nF)) (f : E →ₗ[ℝ] F) :
    EuclideanSpace ℝ (Fin nE) →ₗ[ℝ] EuclideanSpace ℝ (Fin nF) :=
  εF.toLinearMap ∘ₗ (exteriorPower.map k f) ∘ₗ εE.symm.toLinearMap

/-- The exterior-power operator norm of `f`, measured through the trivializations `εE`, `εF`.
When `εE`, `εF` are the orthonormal-wedge isometries for the Hodge inner product, this is the
genuine `‖⋀^k f‖`. -/
def exteriorOpNorm (k : ℕ)
    (εE : (⋀[ℝ]^k E) ≃ₗ[ℝ] EuclideanSpace ℝ (Fin nE))
    (εF : (⋀[ℝ]^k F) ≃ₗ[ℝ] EuclideanSpace ℝ (Fin nF)) (f : E →ₗ[ℝ] F) : ℝ :=
  ‖LinearMap.toContinuousLinearMap (conjExteriorMap k εE εF f)‖

omit [FiniteDimensional ℝ E] [FiniteDimensional ℝ F] in
@[simp]
lemma exteriorOpNorm_nonneg (k : ℕ)
    (εE : (⋀[ℝ]^k E) ≃ₗ[ℝ] EuclideanSpace ℝ (Fin nE))
    (εF : (⋀[ℝ]^k F) ≃ₗ[ℝ] EuclideanSpace ℝ (Fin nF)) (f : E →ₗ[ℝ] F) :
    0 ≤ exteriorOpNorm k εE εF f :=
  norm_nonneg _

omit [FiniteDimensional ℝ E] [FiniteDimensional ℝ F] [FiniteDimensional ℝ G] in
/-- **Submultiplicativity of the exterior-power operator norm.** Pure functoriality
(`exteriorPower.map_comp`, with the middle trivialization telescoping) together with the
submultiplicativity of the continuous-linear-map operator norm (`opNorm_comp_le`). -/
theorem exteriorOpNorm_comp_le (k : ℕ)
    (εE : (⋀[ℝ]^k E) ≃ₗ[ℝ] EuclideanSpace ℝ (Fin nE))
    (εF : (⋀[ℝ]^k F) ≃ₗ[ℝ] EuclideanSpace ℝ (Fin nF))
    (εG : (⋀[ℝ]^k G) ≃ₗ[ℝ] EuclideanSpace ℝ (Fin nG))
    (f : E →ₗ[ℝ] F) (g : F →ₗ[ℝ] G) :
    exteriorOpNorm k εE εG (g ∘ₗ f)
      ≤ exteriorOpNorm k εF εG g * exteriorOpNorm k εE εF f := by
  unfold exteriorOpNorm
  -- `⋀^k (g ∘ f)` conjugated telescopes: the inner `εF⁻¹ ∘ εF` cancels.
  have hcomp : conjExteriorMap k εE εG (g ∘ₗ f)
      = (conjExteriorMap k εF εG g) ∘ₗ (conjExteriorMap k εE εF f) := by
    unfold conjExteriorMap
    rw [exteriorPower.map_comp]
    ext x
    simp [LinearMap.comp_apply]
  have key : LinearMap.toContinuousLinearMap (conjExteriorMap k εE εG (g ∘ₗ f))
      = (LinearMap.toContinuousLinearMap (conjExteriorMap k εF εG g)).comp
          (LinearMap.toContinuousLinearMap (conjExteriorMap k εE εF f)) := by
    apply ContinuousLinearMap.coe_injective
    ext x
    simp only [LinearMap.coe_toContinuousLinearMap]
    rw [hcomp]; rfl
  rw [key]
  exact ContinuousLinearMap.opNorm_comp_le _ _

end Engine

/-! ## The Hodge trivialization

For an inner product space `E`, the **Hodge trivialization** of `⋀^k E` is the linear equiv to
`EuclideanSpace` that sends the orthonormal *wedge basis* — the `k`-fold wedges
`e_{i₁} ∧ ⋯ ∧ e_{i_k}` of the standard orthonormal basis `{eᵢ}` of `E` — to the standard
Euclidean basis. It is a concrete piece of `data` (no inner product is installed on `⋀^k E`,
avoiding the `AddCommGroup`/topology diamond). Measuring the exterior operator norm through this
trivialization gives the genuine `‖⋀^k f‖` for the Hodge inner product. -/

section Hodge

variable {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]

open scoped Classical in
/-- The wedge basis of `⋀^k E` induced by the standard orthonormal basis of `E`: its elements are
the `k`-fold wedge products of distinct standard basis vectors. As a `Basis` it is `data`, and
under the Hodge inner product it is orthonormal. -/
def wedgeBasis (k : ℕ) :
    Basis (Set.powersetCard (Fin (Module.finrank ℝ E)) k) ℝ (⋀[ℝ]^k E) :=
  (stdOrthonormalBasis ℝ E).toBasis.exteriorPower k

open scoped Classical in
/-- The reindexing equiv `powersetCard (Fin (finrank E)) k ≃ Fin (finrank (⋀^k E))` witnessing
that both index sets have the same cardinality `(finrank E).choose k`. -/
def wedgeIndexEquiv (k : ℕ) :
    Set.powersetCard (Fin (Module.finrank ℝ E)) k ≃ Fin (Module.finrank ℝ (⋀[ℝ]^k E)) :=
  Fintype.equivFinOfCardEq (by
    rw [exteriorPower.finrank_eq, ← Nat.card_eq_fintype_card, Set.powersetCard.card,
      Nat.card_eq_fintype_card, Fintype.card_fin])

open scoped Classical in
/-- The **Hodge trivialization** of `⋀^k E`: the linear equiv to a Euclidean space sending the
orthonormal wedge basis to the standard Euclidean basis. -/
def hodgeTrivialization (k : ℕ) :
    (⋀[ℝ]^k E) ≃ₗ[ℝ] EuclideanSpace ℝ (Fin (Module.finrank ℝ (⋀[ℝ]^k E))) :=
  ((wedgeBasis (E := E) k).reindex (wedgeIndexEquiv (E := E) k)).equivFun
    ≪≫ₗ (EuclideanSpace.equiv _ ℝ).symm.toLinearEquiv

end Hodge

/-! ## The bridge to singular values

`‖⋀^k f‖ = ∏_{i<k} σᵢ(f)`, measured through the Hodge trivializations of source and target.
Mathematically: an SVD of `f` diagonalizes `⋀^k f` on the orthonormal bases of `k`-fold wedges of
singular vectors; the operator norm is attained on the top wedge `u₀ ∧ ⋯ ∧ u_{k-1}`, whose image
has norm `∏_{i<k} σᵢ(f)` (the largest wedge product, since `σ` is antitone). This requires the
SVD-decomposition packaging, the orthonormality of the wedge basis for the Hodge inner product,
and a diagonal-operator-norm computation, none of which are currently in Mathlib. -/

section Bridge

variable {E F : Type*}
  [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
  [NormedAddCommGroup F] [InnerProductSpace ℝ F] [FiniteDimensional ℝ F]

/-- **SVD orthogonality core.** Let `u` be the orthonormal eigenvector basis of the symmetric,
positive map `adjoint f ∘ₗ f`. Then the images `{f (uᵢ)}` of these *right singular vectors* are
pairwise orthogonal, and `‖f (uᵢ)‖² = σᵢ(f)²`. Concretely, `⟪f uᵢ, f uⱼ⟫ = δᵢⱼ · σᵢ(f)²`.

This is the analytic heart of the singular value decomposition: rescaling the nonzero `f uᵢ` to
unit length yields the left singular vectors `wᵢ` with `f uᵢ = σᵢ · wᵢ`. -/
private lemma inner_apply_eigenvectorBasis_eq (f : E →ₗ[ℝ] F) {n : ℕ}
    (hn : Module.finrank ℝ E = n) (i j : Fin n) :
    (inner ℝ (f ((f.isSymmetric_adjoint_comp_self.eigenvectorBasis hn) i))
      (f ((f.isSymmetric_adjoint_comp_self.eigenvectorBasis hn) j)) : ℝ)
      = if i = j then (f.singularValues i) ^ 2 else 0 := by
  set hT := f.isSymmetric_adjoint_comp_self
  set u := hT.eigenvectorBasis hn
  have key : (inner ℝ (f (u i)) (f (u j)) : ℝ)
      = inner ℝ ((LinearMap.adjoint f ∘ₗ f) (u i)) (u j) := by
    rw [LinearMap.comp_apply, LinearMap.adjoint_inner_left]
  rw [key, show (LinearMap.adjoint f ∘ₗ f) (u i) = (hT.eigenvalues hn i : ℝ) • u i from
        hT.apply_eigenvectorBasis hn i, inner_smul_left, u.inner_eq_ite i j,
      f.sq_singularValues_fin hn i]
  simp only [RCLike.conj_to_real]
  split_ifs with h <;> simp

/-- The norm of the image of a right singular vector is the corresponding singular value:
`‖f uᵢ‖ = σᵢ(f)`. Immediate from the SVD orthogonality core. -/
private lemma norm_apply_eigenvectorBasis (f : E →ₗ[ℝ] F) {n : ℕ}
    (hn : Module.finrank ℝ E = n) (i : Fin n) :
    ‖f ((f.isSymmetric_adjoint_comp_self.eigenvectorBasis hn) i)‖ = f.singularValues i := by
  have h := inner_apply_eigenvectorBasis_eq f hn i i
  simp only [if_true] at h
  have hsq : ‖f ((f.isSymmetric_adjoint_comp_self.eigenvectorBasis hn) i)‖ ^ 2
      = f.singularValues i ^ 2 := by
    rw [real_inner_self_eq_norm_sq] at h; linarith
  nlinarith [norm_nonneg (f ((f.isSymmetric_adjoint_comp_self.eigenvectorBasis hn) i)),
    f.singularValues_nonneg i, hsq]

/-! ### The det-Gram (Hodge) bilinear form and orthonormal-wedge trivializations

We carry the Hodge inner product on `⋀^k E` as a plain bilinear *form* `hodgeForm` (never as a
typeclass instance, to avoid the `AddCommGroup`/topology diamond). It is defined by reusing the
exterior-power dual pairing composed with the inner-product-to-dual map `innerₗ`, so on `ιMulti`
families it is the determinant of the Gram matrix `det ⟪vᵢ, wⱼ⟫`. -/

/-- The det-Gram (Hodge) bilinear form on `⋀^k E`, defined via the exterior dual pairing and the
inner-product-to-dual map `innerₗ E`. -/
private def hodgeForm (k : ℕ) : (⋀[ℝ]^k E) →ₗ[ℝ] (⋀[ℝ]^k E) →ₗ[ℝ] ℝ where
  toFun ω := exteriorPower.pairingDual ℝ E k (exteriorPower.map k (innerₗ E) ω)
  map_add' x y := by simp [map_add]
  map_smul' c x := by simp [map_smul]

omit [FiniteDimensional ℝ E] in
private lemma hodgeForm_apply (k : ℕ) (ω η : ⋀[ℝ]^k E) :
    hodgeForm k ω η
      = exteriorPower.pairingDual ℝ E k (exteriorPower.map k (innerₗ E) ω) η := rfl

omit [FiniteDimensional ℝ E] in
/-- On `ιMulti` families, the Hodge form is the determinant of the Gram matrix `⟪vⱼ, wᵢ⟫`. -/
lemma hodgeForm_ιMulti (k : ℕ) (v w : Fin k → E) :
    hodgeForm k (exteriorPower.ιMulti ℝ k v) (exteriorPower.ιMulti ℝ k w)
      = (Matrix.of fun i j => (inner ℝ (v j) (w i) : ℝ)).det := by
  rw [hodgeForm_apply, exteriorPower.map_apply_ιMulti,
    exteriorPower.pairingDual_ιMulti_ιMulti]
  simp [innerₗ_apply_apply]

/-- The bilinear map `(ω, η) ↦ hodgeForm (⋀^k Q ω) (⋀^k Q η)`. -/
private def hodgeFormComp (k : ℕ) (Q : E →ₗ[ℝ] F) :
    (⋀[ℝ]^k E) →ₗ[ℝ] (⋀[ℝ]^k E) →ₗ[ℝ] ℝ :=
  (hodgeForm k).compl₁₂ (exteriorPower.map k Q) (exteriorPower.map k Q)

omit [FiniteDimensional ℝ E] [FiniteDimensional ℝ F] in
/-- **The compound of an orthogonal map is orthogonal.** `⋀^k Q` preserves the Hodge
form whenever `Q` is a linear isometry (`⟪Q x, Q y⟫ = ⟪x, y⟫`). On `ιMulti` families this is the
identity `det ⟪Q vⱼ, Q wᵢ⟫ = det ⟪vⱼ, wᵢ⟫`. -/
private lemma hodgeForm_map_isometry (k : ℕ) (Q : E →ₗ[ℝ] F)
    (hQ : ∀ x y : E, (inner ℝ (Q x) (Q y) : ℝ) = inner ℝ x y) :
    hodgeFormComp k Q = hodgeForm (E := E) k := by
  ext v w
  simp only [hodgeFormComp, LinearMap.compAlternatingMap_apply, LinearMap.compl₁₂_apply,
    exteriorPower.map_apply_ιMulti]
  rw [hodgeForm_ιMulti, hodgeForm_ιMulti]
  congr 1
  ext i j
  simp only [Matrix.of_apply]
  exact hQ _ _

omit [FiniteDimensional ℝ E] in
open scoped Classical in
/-- For an orthonormal basis `b`, the coordinate dual `b.toBasis.coord i` equals
`innerₗ E (b i) = ⟪b i, ·⟫`. -/
private lemma innerₗ_eq_coord {ι : Type*} [Fintype ι] (b : OrthonormalBasis ι ℝ E) (i : ι) :
    innerₗ E (b i) = b.toBasis.coord i := by
  ext x
  rw [innerₗ_apply_apply, Basis.coord_apply, b.coe_toBasis_repr_apply, b.repr_apply_apply]

omit [FiniteDimensional ℝ E] in
open scoped Classical in
/-- **The wedge basis of an orthonormal basis is orthonormal for the Hodge form.** This is the
det-Gram of the identity Gram matrix, packaged through the exterior dual pairing
`ιMultiDual_apply_diag`/`_apply_nondiag`. -/
private lemma hodgeForm_wedgeBasis {ι : Type*} [Fintype ι] [LinearOrder ι]
    (b : OrthonormalBasis ι ℝ E) (k : ℕ) (s t : Set.powersetCard ι k) :
    hodgeForm k (b.toBasis.exteriorPower k s) (b.toBasis.exteriorPower k t)
      = if s = t then 1 else 0 := by
  rw [exteriorPower.basis_apply, exteriorPower.basis_apply]
  have hcoord : (innerₗ E) ∘ (b.toBasis) = b.toBasis.coord := by
    ext i
    rw [Function.comp_apply, b.coe_toBasis, innerₗ_eq_coord]
  have key : hodgeForm k (exteriorPower.ιMulti_family ℝ k b.toBasis s)
      = exteriorPower.ιMultiDual ℝ k b.toBasis s := by
    change exteriorPower.pairingDual ℝ E k
        (exteriorPower.map k (innerₗ E) (exteriorPower.ιMulti_family ℝ k b.toBasis s))
      = exteriorPower.ιMultiDual ℝ k b.toBasis s
    rw [exteriorPower.map_apply_ιMulti_family, hcoord, exteriorPower.ιMultiDual]
  rw [LinearMap.congr_fun key]
  by_cases hst : s = t
  · subst hst
    rw [exteriorPower.ιMultiDual_apply_diag]; simp
  · rw [exteriorPower.ιMultiDual_apply_nondiag ℝ k b.toBasis s t hst]; simp [hst]

section OnbTriv

variable {ι : Type*} [Fintype ι] [LinearOrder ι]

open scoped Classical in
/-- Reindexing `powersetCard ι k ≃ Fin (finrank (⋀^k E))` for an o.n. basis `b` indexed by `ι`. -/
def wIndexEquiv (b : OrthonormalBasis ι ℝ E) (k : ℕ) :
    Set.powersetCard ι k ≃ Fin (Module.finrank ℝ (⋀[ℝ]^k E)) :=
  Fintype.equivFinOfCardEq (by
    rw [exteriorPower.finrank_eq, ← Nat.card_eq_fintype_card, Set.powersetCard.card,
      Nat.card_eq_fintype_card]
    congr 1
    exact (Module.finrank_eq_card_basis b.toBasis).symm)

open scoped Classical in
/-- The wedge trivialization attached to an arbitrary orthonormal basis `b` of `E`. -/
def onbTriv (b : OrthonormalBasis ι ℝ E) (k : ℕ) :
    (⋀[ℝ]^k E) ≃ₗ[ℝ] EuclideanSpace ℝ (Fin (Module.finrank ℝ (⋀[ℝ]^k E))) :=
  ((b.toBasis.exteriorPower k).reindex (wIndexEquiv b k)).equivFun
    ≪≫ₗ (EuclideanSpace.equiv _ ℝ).symm.toLinearEquiv

open scoped Classical in
private lemma onbTriv_apply (b : OrthonormalBasis ι ℝ E) (k : ℕ) (x : ⋀[ℝ]^k E)
    (i : Fin (Module.finrank ℝ (⋀[ℝ]^k E))) :
    onbTriv b k x i = ((b.toBasis.exteriorPower k).reindex (wIndexEquiv b k)).repr x i := by
  simp only [onbTriv, LinearEquiv.trans_apply, Basis.equivFun_apply]; rfl

omit [FiniteDimensional ℝ E] in
open scoped Classical in
/-- **Parseval for the Hodge form:** in the wedge basis of an o.n. basis it diagonalises. -/
private lemma hodgeForm_eq_sum_repr (b : OrthonormalBasis ι ℝ E) (k : ℕ) (x y : ⋀[ℝ]^k E) :
    hodgeForm k x y
      = ∑ s, (((b.toBasis.exteriorPower k).repr x) s)
          * (((b.toBasis.exteriorPower k).repr y) s) := by
  classical
  conv_lhs => rw [← (b.toBasis.exteriorPower k).sum_repr x,
    ← (b.toBasis.exteriorPower k).sum_repr y]
  rw [map_sum]
  simp only [LinearMap.coe_sum, Finset.sum_apply, map_sum, map_smul,
    LinearMap.smul_apply, smul_eq_mul]
  apply Finset.sum_congr rfl
  intro s _
  rw [Finset.sum_eq_single s]
  · rw [hodgeForm_wedgeBasis]; simp; ring
  · intro t _ hts; rw [hodgeForm_wedgeBasis]; simp [hts]
  · intro h; simp at h

open scoped Classical in
/-- **The trivialization is a Hodge isometry:** the L2 inner product of trivialized vectors equals
the Hodge form. -/
lemma inner_onbTriv (b : OrthonormalBasis ι ℝ E) (k : ℕ) (x y : ⋀[ℝ]^k E) :
    (inner ℝ (onbTriv b k x) (onbTriv b k y) : ℝ) = hodgeForm k x y := by
  classical
  rw [PiLp.inner_apply, hodgeForm_eq_sum_repr b k x y]
  simp only [onbTriv_apply]
  refine Fintype.sum_equiv (wIndexEquiv b k).symm _ _ (fun i => ?_)
  rw [Basis.repr_reindex_apply, Basis.repr_reindex_apply]
  apply RCLike.inner_apply'

end OnbTriv

section OnbChange

variable {ιE ιE' ιF ιF' : Type*}
  [Fintype ιE] [LinearOrder ιE] [Fintype ιE'] [LinearOrder ιE']
  [Fintype ιF] [LinearOrder ιF] [Fintype ιF'] [LinearOrder ιF']

open scoped Classical in
/-- **Change of coordinates between two o.n.-basis wedge trivializations of the *same* space is
an L2 isometry** (the compound `⋀^k Q` of the orthogonal change of basis). The two bases may be
indexed differently; only the space `E` (hence `finrank (⋀^k E)`) matters. -/
def onbChange (b : OrthonormalBasis ιE ℝ E) (b' : OrthonormalBasis ιE' ℝ E) (k : ℕ) :
    EuclideanSpace ℝ (Fin (Module.finrank ℝ (⋀[ℝ]^k E)))
      ≃ₗᵢ[ℝ] EuclideanSpace ℝ (Fin (Module.finrank ℝ (⋀[ℝ]^k E))) :=
  LinearEquiv.isometryOfInner
    ((onbTriv b k).symm ≪≫ₗ (onbTriv b' k)) (fun p q => by
      simp only [LinearEquiv.trans_apply]
      rw [inner_onbTriv b' k, ← inner_onbTriv b k, LinearEquiv.apply_symm_apply,
        LinearEquiv.apply_symm_apply])

open scoped Classical in
lemma onbChange_apply (b : OrthonormalBasis ιE ℝ E) (b' : OrthonormalBasis ιE' ℝ E) (k : ℕ)
    (p : EuclideanSpace ℝ (Fin (Module.finrank ℝ (⋀[ℝ]^k E)))) :
    onbChange b b' k p = onbTriv b' k ((onbTriv b k).symm p) := rfl

open scoped Classical in
/-- **Operator-norm invariance under change of orthonormal-wedge trivialization.** Replacing the
source/target o.n.-basis trivializations (possibly indexed differently) conjugates
`conjExteriorMap` by the L2 isometries `onbChange`, leaving the operator norm unchanged. -/
private lemma exteriorOpNorm_onbTriv_eq (bE : OrthonormalBasis ιE ℝ E)
    (bE' : OrthonormalBasis ιE' ℝ E)
    (bF : OrthonormalBasis ιF ℝ F) (bF' : OrthonormalBasis ιF' ℝ F) (k : ℕ) (f : E →ₗ[ℝ] F) :
    exteriorOpNorm k (onbTriv bE k) (onbTriv bF k) f
      = exteriorOpNorm k (onbTriv bE' k) (onbTriv bF' k) f := by
  set g := conjExteriorMap k (onbTriv bE k) (onbTriv bF k) f with hg
  set g' := conjExteriorMap k (onbTriv bE' k) (onbTriv bF' k) f with hg'
  have hrel : LinearMap.toContinuousLinearMap g'
      = (onbChange bF bF' k).toLinearIsometry.toContinuousLinearMap.comp
          ((LinearMap.toContinuousLinearMap g).comp
            (onbChange bE' bE k).toLinearIsometry.toContinuousLinearMap) := by
    refine ContinuousLinearMap.ext (fun p => ?_)
    simp only [ContinuousLinearMap.coe_comp', Function.comp_apply,
      LinearMap.coe_toContinuousLinearMap', LinearIsometry.coe_toContinuousLinearMap,
      LinearIsometryEquiv.coe_toLinearIsometry]
    simp only [hg, hg', conjExteriorMap, LinearMap.comp_apply, LinearEquiv.coe_coe,
      onbChange_apply, LinearEquiv.symm_apply_apply]
  rw [exteriorOpNorm, exteriorOpNorm, hrel,
    LinearIsometry.norm_toContinuousLinearMap_comp,
    ContinuousLinearMap.opNorm_comp_linearIsometryEquiv]

end OnbChange

/-! ### Operator norm of a map with orthogonal images of an orthonormal basis -/

/-- `‖g p‖² = ∑ i, (p i)² · c i` for a Euclidean map `g` whose images of the standard basis are
pairwise orthogonal with `⟪g eᵢ, g eⱼ⟫ = if i = j then c i else 0`. -/
private lemma normSq_apply_of_ortho {W : Type*} [NormedAddCommGroup W] [InnerProductSpace ℝ W]
    {N : ℕ} (g : EuclideanSpace ℝ (Fin N) →ₗ[ℝ] W) (c : Fin N → ℝ)
    (hortho : ∀ i j, (inner ℝ (g (EuclideanSpace.basisFun (Fin N) ℝ i))
      (g (EuclideanSpace.basisFun (Fin N) ℝ j)) : ℝ) = if i = j then c i else 0)
    (p : EuclideanSpace ℝ (Fin N)) :
    ‖g p‖ ^ 2 = ∑ i, (p i) ^ 2 * c i := by
  have hp : p = ∑ i, (p i) • EuclideanSpace.basisFun (Fin N) ℝ i := by
    conv_lhs => rw [← (EuclideanSpace.basisFun (Fin N) ℝ).sum_repr p]
    simp only [EuclideanSpace.basisFun_repr]
  rw [← real_inner_self_eq_norm_sq]
  conv_lhs => rw [hp]
  rw [map_sum, sum_inner]
  apply Finset.sum_congr rfl
  intro i _
  rw [map_smul, inner_smul_left, RCLike.conj_to_real, inner_sum]
  rw [Finset.sum_eq_single i]
  · rw [map_smul, inner_smul_right, hortho i i, if_pos rfl]; ring
  · intro j _ hji; rw [map_smul, inner_smul_right, hortho i j, if_neg (Ne.symm hji)]; ring
  · intro h; simp at h

/-- **Operator norm of a map with orthogonal basis images.** If `g` sends the standard orthonormal
basis to a pairwise-orthogonal family with `⟪g eᵢ, g eⱼ⟫ = if i = j then c i else 0`, `c ≥ 0`, and
`i₀` attains `max c`, then `‖g‖ = √(c i₀)`. -/
private lemma opNorm_eq_of_ortho {W : Type*} [NormedAddCommGroup W] [InnerProductSpace ℝ W]
    {N : ℕ} (g : EuclideanSpace ℝ (Fin N) →ₗ[ℝ] W) (c : Fin N → ℝ)
    (hortho : ∀ i j, (inner ℝ (g (EuclideanSpace.basisFun (Fin N) ℝ i))
      (g (EuclideanSpace.basisFun (Fin N) ℝ j)) : ℝ) = if i = j then c i else 0)
    (hc : ∀ i, 0 ≤ c i) (i₀ : Fin N) (hi₀ : ∀ i, c i ≤ c i₀) :
    ‖LinearMap.toContinuousLinearMap g‖ = Real.sqrt (c i₀) := by
  apply le_antisymm
  · apply ContinuousLinearMap.opNorm_le_bound _ (Real.sqrt_nonneg _)
    intro p
    rw [LinearMap.coe_toContinuousLinearMap']
    rw [← Real.sqrt_sq (norm_nonneg (g p)), normSq_apply_of_ortho g c hortho p, Real.sqrt_le_iff]
    refine ⟨by positivity, ?_⟩
    rw [mul_pow, Real.sq_sqrt (hc i₀), ← real_inner_self_eq_norm_sq, PiLp.inner_apply]
    rw [Finset.mul_sum]
    apply Finset.sum_le_sum
    intro i _
    change (p i) ^ 2 * c i ≤ c i₀ * (p i * p i)
    have hpow : p i * p i = (p i) ^ 2 := by ring
    rw [hpow, mul_comm (c i₀) ((p i) ^ 2)]
    exact mul_le_mul_of_nonneg_left (hi₀ i) (sq_nonneg _)
  · have hb : ‖EuclideanSpace.basisFun (Fin N) ℝ i₀‖ = 1 :=
      (EuclideanSpace.basisFun (Fin N) ℝ).orthonormal.1 i₀
    have hnorm : ‖g (EuclideanSpace.basisFun (Fin N) ℝ i₀)‖ = Real.sqrt (c i₀) := by
      rw [← Real.sqrt_sq (norm_nonneg _), normSq_apply_of_ortho g c hortho]
      congr 1
      rw [Finset.sum_eq_single i₀]
      · simp [EuclideanSpace.basisFun_apply]
      · intro j _ hj; simp [EuclideanSpace.basisFun_apply, hj]
      · intro h; simp at h
    have hle := (LinearMap.toContinuousLinearMap g).le_opNorm
      (EuclideanSpace.basisFun (Fin N) ℝ i₀)
    rw [LinearMap.coe_toContinuousLinearMap', hnorm, hb, mul_one] at hle
    exact hle

/-! ### The Gram determinant and the top-`k` product maximization -/

open Set.powersetCard in
/-- **Gram determinant with a diagonal weight.** If a Gram-type matrix has `(i, j)`-entry
`d (σ_S j)` when `σ_S j = σ_T i` and `0` otherwise (with `σ_S`, `σ_T` the ordered enumerations of
two `k`-subsets `S`, `T`), then its determinant is `∏_{a ∈ S} d a` when `S = T` and `0` otherwise.
The off-diagonal case has a zero column (an element of `S ∖ T`); the diagonal case is a literal
diagonal matrix. -/
private lemma gram_det {ι : Type*} [LinearOrder ι] {k : ℕ}
    (d : ι → ℝ) (S T : Set.powersetCard ι k) :
    (Matrix.of fun i j : Fin k =>
      if (ofFinEmbEquiv.symm S j : ι) = (ofFinEmbEquiv.symm T i : ι)
        then d (ofFinEmbEquiv.symm S j) else 0).det
      = if S = T then ∏ a ∈ (S : Finset ι), d a else 0 := by
  by_cases hST : S = T
  · subst hST
    rw [if_pos rfl]
    have hdiag : (Matrix.of fun i j : Fin k =>
        if (ofFinEmbEquiv.symm S j : ι) = (ofFinEmbEquiv.symm S i : ι)
          then d (ofFinEmbEquiv.symm S j) else 0)
        = Matrix.diagonal (fun i => d (ofFinEmbEquiv.symm S i)) := by
      ext i j
      simp only [Matrix.of_apply, Matrix.diagonal_apply]
      by_cases hij : i = j
      · subst hij; simp
      · rw [if_neg hij, if_neg]
        intro h
        exact hij (((ofFinEmbEquiv.symm S).injective h).symm)
    rw [hdiag, Matrix.det_diagonal, ← Finset.prod_image]
    · congr 1
      ext a
      simp only [Finset.mem_image, Finset.mem_univ, true_and]
      constructor
      · rintro ⟨i, rfl⟩
        rw [ofFinEmbEquiv_symm_apply]
        exact Finset.orderEmbOfFin_mem S.val S.prop i
      · intro ha
        obtain ⟨i, rfl⟩ := (mem_range_ofFinEmbEquiv_symm_iff_mem S a).mpr ha
        exact ⟨i, rfl⟩
    · intro i _ j _ h
      exact (ofFinEmbEquiv.symm S).injective h
  · rw [if_neg hST]
    obtain ⟨a, haS, haT⟩ := (Set.powersetCard.exists_mem_notMem_iff_ne S T).mp hST
    obtain ⟨j₀, hj₀⟩ := (mem_range_ofFinEmbEquiv_symm_iff_mem S a).mpr haS
    apply Matrix.det_eq_zero_of_column_eq_zero j₀
    intro i
    simp only [Matrix.of_apply, hj₀]
    rw [if_neg]
    intro h
    exact haT ((mem_range_ofFinEmbEquiv_symm_iff_mem T a).mp ⟨i, h.symm⟩)

/-- A strictly monotone `Fin k → Fin n` satisfies `i ≤ g i`. -/
private lemma le_orderEmb {k n : ℕ} (g : Fin k ↪o Fin n) (i : Fin k) :
    (i : ℕ) ≤ (g i : ℕ) := by
  have hmono : StrictMono (fun j : Fin k => (g j : ℕ)) := fun a b hab =>
    (Fin.lt_def).mp (g.strictMono hab)
  obtain ⟨iv, hiv⟩ := i
  induction iv using Nat.strong_induction_on with
  | _ iv ih =>
    cases iv with
    | zero => exact Nat.zero_le _
    | succ m =>
      have hm : m < k := Nat.lt_of_succ_lt hiv
      have ihm := ih m (Nat.lt_succ_self m) hm
      have hstep : (g ⟨m, hm⟩ : ℕ) < (g ⟨m + 1, hiv⟩ : ℕ) :=
        hmono (by simp [Fin.lt_def])
      have hv : ((⟨m, hm⟩ : Fin k) : ℕ) = m := rfl
      have hv2 : ((⟨m + 1, hiv⟩ : Fin k) : ℕ) = m + 1 := rfl
      rw [hv] at ihm
      rw [hv2]
      omega

/-- **Top-`k` prefix maximizes the product of antitone nonnegative weights.** For antitone
nonnegative `σ : Fin n → ℝ`, the product over any `k`-subset is at most the product over the
top-`k` prefix indices (any `top` with `(top i : ℕ) = i`). -/
lemma prod_le_prod_top {n k : ℕ} (σ : Fin n → ℝ) (hσ : Antitone σ)
    (hpos : ∀ i, 0 ≤ σ i) (S : Set.powersetCard (Fin n) k)
    (top : Fin k → Fin n) (htop : ∀ i, (top i : ℕ) = i) :
    ∏ a ∈ (S : Finset (Fin n)), σ a ≤ ∏ i, σ (top i) := by
  rw [← Finset.image_orderEmbOfFin_univ (S : Finset (Fin n)) S.prop,
    Finset.prod_image (fun i _ j _ h => (Finset.orderEmbOfFin S.val S.prop).injective h)]
  apply Finset.prod_le_prod
  · intro i _; exact hpos _
  · intro i _
    apply hσ
    rw [Fin.le_iff_val_le_val, htop]
    exact le_orderEmb (Finset.orderEmbOfFin S.val S.prop) i

/-- **The top element of a non-top `k`-subset is `≥ k`.** If the ordered enumeration `e` of a
`k`-subset `S` of `Fin n` does not enumerate the top prefix `{0,…,k-1}`, then its largest element
`e ⟨k-1⟩` has value `≥ k`. (Otherwise all of `S` lies in `{0,…,k-1}`, forcing `S` = top prefix.) -/
lemma top_elem_ge {n k : ℕ} (hk1 : 1 ≤ k) (hkn : k ≤ n) (e : Fin k ↪o Fin n)
    (htop : ((Finset.univ.image (fun j : Fin k => (e j))) : Finset (Fin n))
      ≠ Finset.univ.image (fun i : Fin k => (⟨i, lt_of_lt_of_le i.2 hkn⟩ : Fin n))) :
    k ≤ (e ⟨k-1, by omega⟩ : ℕ) := by
  by_contra hlt
  rw [not_le] at hlt
  apply htop
  apply Finset.eq_of_subset_of_card_le
  · intro x hx
    simp only [Finset.mem_image, Finset.mem_univ, true_and] at hx ⊢
    obtain ⟨j, rfl⟩ := hx
    have hjlt := j.2
    have hle : (e j : ℕ) ≤ (e ⟨k-1, by omega⟩ : ℕ) := by
      have hj : j ≤ (⟨k-1, by omega⟩ : Fin k) := by rw [Fin.le_def]; simp only; omega
      exact_mod_cast (e.monotone hj)
    have hjk : (e j : ℕ) < k := lt_of_le_of_lt hle hlt
    exact ⟨⟨(e j : ℕ), hjk⟩, Fin.ext rfl⟩
  · rw [Finset.card_image_of_injective _ (fun a b h => e.injective h),
        Finset.card_image_of_injective _ (fun a b h => Fin.ext (by simpa using congrArg Fin.val h))]

/-- **The second-largest `k`-subset product bound.** For antitone nonnegative `lam`, the product of
`lam` over the ordered enumeration `e` of a `k`-subset whose top element is `≥ k` (i.e. a non-top
subset) is at most the second-largest product `(∏_{i<k-1} lam i)·lam k`. The top factor drops from
`lam (k-1)` to `lam k`; the remaining `k-1` factors are bounded by the prefix `{0,…,k-2}`. -/
lemma prod_le_second_aux {n : ℕ} (m : ℕ) (lam : ℕ → ℝ)
    (hanti : Antitone lam) (hpos : ∀ i, 0 ≤ lam i) (e : Fin (m + 1) ↪o Fin n)
    (htopge : m + 1 ≤ (e ⟨m, by omega⟩ : ℕ)) :
    ∏ j : Fin (m + 1), lam (e j : ℕ) ≤ (∏ i ∈ Finset.range m, lam i) * lam (m + 1) := by
  rw [Fin.prod_univ_castSucc]
  have hlast : lam (e (Fin.last m) : ℕ) ≤ lam (m + 1) := by
    apply hanti
    rw [show (Fin.last m : Fin (m + 1)) = ⟨m, by omega⟩ from rfl]; exact htopge
  have hcast : ∏ j : Fin m, lam (e j.castSucc : ℕ) ≤ ∏ i ∈ Finset.range m, lam i := by
    rw [Finset.prod_range fun i => lam i]
    apply Finset.prod_le_prod (fun i _ => hpos _)
    intro i _
    apply hanti
    have := le_orderEmb e i.castSucc
    simpa using this
  calc (∏ j : Fin m, lam (e j.castSucc : ℕ)) * lam (e (Fin.last m) : ℕ)
      ≤ (∏ i ∈ Finset.range m, lam i) * lam (e (Fin.last m) : ℕ) :=
        mul_le_mul_of_nonneg_right hcast (hpos _)
    _ ≤ (∏ i ∈ Finset.range m, lam i) * lam (m + 1) :=
        mul_le_mul_of_nonneg_left hlast (Finset.prod_nonneg (fun _ _ => hpos _))

/-- **The bridge.** Through the Hodge trivializations of source and target, the exterior operator
norm equals the product of the top-`k` singular values:
`exteriorOpNorm k (hodgeTrivialization k) (hodgeTrivialization k) f = ∏_{i<k} σᵢ(f)`. -/
theorem exteriorOpNorm_hodge_eq_prod_singularValues (k : ℕ) (f : E →ₗ[ℝ] F) :
    exteriorOpNorm k (hodgeTrivialization k) (hodgeTrivialization k) f
      = ∏ i ∈ Finset.range k, f.singularValues i := by
  classical
  set nE := Module.finrank ℝ E with hnE
  set hT := f.isSymmetric_adjoint_comp_self with hThT
  set u := hT.eigenvectorBasis (hnE.symm : Module.finrank ℝ E = nE) with hu
  set wF := stdOrthonormalBasis ℝ F with hwF
  -- Step A: the Hodge trivialization is the o.n.-basis trivialization of the standard basis.
  have hStdE : hodgeTrivialization (E := E) k = onbTriv (stdOrthonormalBasis ℝ E) k := by
    unfold hodgeTrivialization onbTriv wedgeBasis wedgeIndexEquiv wIndexEquiv
    rfl
  have hStdF : hodgeTrivialization (E := F) k = onbTriv wF k := by
    unfold hodgeTrivialization onbTriv wedgeBasis wedgeIndexEquiv wIndexEquiv
    rfl
  -- Step B: change source o.n. basis to the SVD basis `u`.
  rw [hStdE, hStdF, exteriorOpNorm_onbTriv_eq (stdOrthonormalBasis ℝ E) u wF wF k f]
  -- Abbreviations.
  set σ : Fin nE → ℝ := fun a => f.singularValues (a : ℕ) with hσdef
  -- the Gram orthogonality of `f uᵢ`.
  have hGram : ∀ a b : Fin nE, (inner ℝ (f (u a)) (f (u b)) : ℝ)
      = if a = b then σ a ^ 2 else 0 := by
    intro a b
    rw [hσdef, hu]
    exact inner_apply_eigenvectorBasis_eq f (hnE.symm : Module.finrank ℝ E = nE) a b
  unfold exteriorOpNorm
  set N := Module.finrank ℝ (⋀[ℝ]^k E) with hN
  -- the diagonal weight for the op-norm lemma.
  set c : Fin N → ℝ := fun i =>
    ∏ a ∈ ((wIndexEquiv u k).symm i : Set.powersetCard (Fin nE) k).val, σ a ^ 2 with hcdef
  -- `g (basisFun i) = onbTriv wF (⋀^k f (u-wedge basis at (wIndexEquiv u).symm i))`.
  have hgbasis : ∀ i : Fin N,
      conjExteriorMap k (onbTriv u k) (onbTriv wF k) f (EuclideanSpace.basisFun (Fin N) ℝ i)
      = onbTriv wF k (exteriorPower.map k f
          (u.toBasis.exteriorPower k ((wIndexEquiv u k).symm i))) := by
    intro i
    rw [conjExteriorMap]
    simp only [LinearMap.comp_apply, LinearEquiv.coe_coe]
    congr 2
    rw [LinearEquiv.symm_apply_eq]
    ext1 j
    rw [onbTriv_apply, EuclideanSpace.basisFun_apply, PiLp.ofLp_single,
      Basis.repr_reindex_apply, Basis.repr_self, Pi.single_apply, Finsupp.single_apply]
    simp only [eq_comm]
    by_cases hij : i = j <;> simp [hij]
  -- orthogonality of the basis images, with weights `c`.
  have hortho : ∀ i j : Fin N,
      (inner ℝ
        (conjExteriorMap k (onbTriv u k) (onbTriv wF k) f (EuclideanSpace.basisFun (Fin N) ℝ i))
        (conjExteriorMap k (onbTriv u k) (onbTriv wF k) f (EuclideanSpace.basisFun (Fin N) ℝ j))
        : ℝ) = if i = j then c i else 0 := by
    intro i j
    rw [hgbasis i, hgbasis j, inner_onbTriv]
    -- map f (wedge_S) = ιMulti_family (f ∘ u.toBasis) S
    rw [exteriorPower.basis_apply, exteriorPower.basis_apply,
      exteriorPower.map_apply_ιMulti_family, exteriorPower.map_apply_ιMulti_family,
      exteriorPower.ιMulti_family, exteriorPower.ιMulti_family, hodgeForm_ιMulti]
    -- the Gram matrix matches `gram_det` with weight `σ²`.
    have hfu : (f ∘ ⇑u.toBasis) = fun a => f (u a) := by funext a; simp [u.coe_toBasis]
    rw [hfu]
    simp only [Function.comp_apply]
    have hmat : (Matrix.of fun i' j' : Fin k =>
        (inner ℝ (f (u (Set.powersetCard.ofFinEmbEquiv.symm ((wIndexEquiv u k).symm i) j')))
          (f (u (Set.powersetCard.ofFinEmbEquiv.symm ((wIndexEquiv u k).symm j) i'))) : ℝ))
        = Matrix.of fun i' j' : Fin k =>
          if (Set.powersetCard.ofFinEmbEquiv.symm ((wIndexEquiv u k).symm i) j' : Fin nE)
              = (Set.powersetCard.ofFinEmbEquiv.symm ((wIndexEquiv u k).symm j) i' : Fin nE)
            then σ (Set.powersetCard.ofFinEmbEquiv.symm ((wIndexEquiv u k).symm i) j') ^ 2
            else 0 := by
      ext i' j'
      simp only [Matrix.of_apply]
      exact hGram _ _
    rw [hmat, gram_det (fun a => σ a ^ 2)]
    -- `Si = Sj ↔ i = j`, and the diagonal product is `c i`.
    have hiff : (((wIndexEquiv u k).symm i) = ((wIndexEquiv u k).symm j)) ↔ (i = j) :=
      (wIndexEquiv u k).symm.injective.eq_iff
    by_cases hij : i = j
    · rw [if_pos hij, if_pos (hiff.mpr hij), hcdef]
    · rw [if_neg hij, if_neg (fun h => hij (hiff.mp h))]
  -- nonnegativity of the weights.
  have hcnonneg : ∀ i, 0 ≤ c i := fun i => Finset.prod_nonneg (fun a _ => sq_nonneg _)
  -- σ is antitone and nonnegative.
  have hσanti : Antitone σ := fun a b hab => by
    simp only [hσdef]
    exact f.singularValues_antitone (by exact_mod_cast hab)
  have hσpos : ∀ a, 0 ≤ σ a := fun a => f.singularValues_nonneg _
  by_cases hkn : k ≤ nE
  · -- main case: the maximum is attained at the top-`k` prefix set.
    -- the order embedding `i ↦ ⟨i⟩ : Fin k ↪o Fin nE` and its `powersetCard` image.
    set topEmb : Fin k ↪o Fin nE :=
      { toFun := fun i => ⟨i, lt_of_lt_of_le i.2 hkn⟩
        inj' := fun i j h => by
          apply Fin.ext
          have := congrArg Fin.val h
          simpa using this
        map_rel_iff' := Iff.rfl } with htopEmb
    set topSet : Set.powersetCard (Fin nE) k := Set.powersetCard.ofFinEmbEquiv topEmb with htopSet
    have htopenum : Set.powersetCard.ofFinEmbEquiv.symm topSet = topEmb := by
      rw [htopSet, Equiv.symm_apply_apply]
    have htopval : ∀ i : Fin k, (topEmb i : Fin nE).val = (i : ℕ) := fun i => rfl
    set i₀ : Fin N := wIndexEquiv u k topSet with hi₀def
    have hS₀ : (wIndexEquiv u k).symm i₀ = topSet := by rw [hi₀def, Equiv.symm_apply_apply]
    -- `∏_{a ∈ topSet} g a = ∏_{i} g (topEmb i)` for any `g`.
    have htopprod : ∀ g : Fin nE → ℝ,
        ∏ a ∈ topSet.val, g a = ∏ j, g (topEmb j) := by
      intro g
      have hval : topSet.val = Finset.univ.image (topEmb) := by
        ext x
        rw [Finset.mem_image]
        rw [show x ∈ topSet.val ↔ x ∈ topSet from Iff.rfl, htopSet,
          Set.powersetCard.mem_ofFinEmbEquiv_iff_mem_range, Set.mem_range]
        constructor
        · rintro ⟨j, hj⟩; exact ⟨j, Finset.mem_univ _, hj⟩
        · rintro ⟨j, _, hj⟩; exact ⟨j, hj⟩
      rw [hval, Finset.prod_image (fun x _ y _ h => topEmb.injective h)]
    -- maximality of `c i₀`.
    have hmax : ∀ i, c i ≤ c i₀ := by
      intro i
      rw [hcdef]
      simp only
      rw [hS₀, htopprod (fun a => σ a ^ 2)]
      exact prod_le_prod_top (fun a => σ a ^ 2)
        (fun a b hab => pow_le_pow_left₀ (hσpos b) (hσanti hab) 2)
        (fun a => sq_nonneg _) ((wIndexEquiv u k).symm i) topEmb htopval
    rw [opNorm_eq_of_ortho _ c hortho hcnonneg i₀ hmax]
    -- compute `√(c i₀) = ∏_{i<k} σ ⟨i⟩ = ∏_{i<k} singularValues i`.
    rw [hcdef]
    simp only
    rw [hS₀, htopprod (fun a => σ a ^ 2), Finset.prod_pow,
      Real.sqrt_sq (Finset.prod_nonneg (fun j _ => hσpos _)),
      Finset.prod_range fun i => f.singularValues i]
    apply Finset.prod_congr rfl
    intro j _
    rw [hσdef]
    rfl
  · -- edge case: `k > nE`, so `⋀^k E = 0` and both sides vanish.
    have hNzero : N = 0 := by
      have heq : N = (Module.finrank ℝ E).choose k := by
        rw [hN, exteriorPower.finrank_eq]
      rw [heq]
      exact Nat.choose_eq_zero_of_lt (Nat.lt_of_not_le hkn)
    have hopzero : ‖LinearMap.toContinuousLinearMap
        (conjExteriorMap k (onbTriv u k) (onbTriv wF k) f)‖ = 0 := by
      rw [norm_eq_zero]
      apply ContinuousLinearMap.ext
      intro p
      have hsub : Subsingleton (EuclideanSpace ℝ (Fin N)) := by
        rw [hNzero]; infer_instance
      rw [Subsingleton.elim p 0]
      simp
    rw [hopzero]
    symm
    apply Finset.prod_eq_zero (Finset.mem_range.mpr (Nat.lt_of_not_le hkn))
    exact f.singularValues_of_finrank_le hnE.symm.le

/-! ### The Plücker bridge: eigen-diagonalization of the compound

For a symmetric map `f` with orthonormal eigenbasis `u` and eigenvalues `lam`, the compound
`⋀^k f` is diagonal in the wedge basis of `u`: it scales the wedge `u_S` by `∏_{a ∈ S} lam a`.
This is the abstract spectral core behind the Plücker top eigenpair and the second-eigenvalue
ceiling established below. -/

/-- **Product reindexing.** A product of `lam` over the ordered enumeration of a `k`-subset `S`
equals the product of `lam` over `S`. -/
lemma prod_ofFinEmbEquiv_symm {ι : Type*} [LinearOrder ι] {k : ℕ} (lam : ι → ℝ)
    (S : Set.powersetCard ι k) :
    ∏ i, lam ((Set.powersetCard.ofFinEmbEquiv.symm S) i) = ∏ a ∈ (S : Finset ι), lam a := by
  have himg : (S : Finset ι) = Finset.univ.image (Set.powersetCard.ofFinEmbEquiv.symm S) := by
    rw [Set.powersetCard.ofFinEmbEquiv_symm_apply, Finset.image_orderEmbOfFin_univ]
  rw [himg, Finset.prod_image
    (fun i _ j _ h => (Set.powersetCard.ofFinEmbEquiv.symm S).injective h)]

omit [FiniteDimensional ℝ E] in
/-- **`ιMulti_family` scalar pull-out.** A family rescaled entrywise by `lam` factors a product
of scalars out of the wedge:
`ιMulti_family (fun j ↦ lam j • g j) S = (∏_{a ∈ S} lam a) • ιMulti_family g S`.
Multilinearity of the alternating map `ιMulti` (`AlternatingMap.map_smul_univ`). -/
private lemma ιMulti_family_smul {ι : Type*} [LinearOrder ι] {k : ℕ} (lam : ι → ℝ) (g : ι → E)
    (S : Set.powersetCard ι k) :
    exteriorPower.ιMulti_family ℝ k (fun j => lam j • g j) S
      = (∏ a ∈ (S : Finset ι), lam a) • exteriorPower.ιMulti_family ℝ k g S := by
  classical
  rw [exteriorPower.ιMulti_family, exteriorPower.ιMulti_family]
  have hcomp : (fun j => lam j • g j) ∘ (Set.powersetCard.ofFinEmbEquiv.symm S)
      = fun i => lam ((Set.powersetCard.ofFinEmbEquiv.symm S) i) •
          (g ∘ (Set.powersetCard.ofFinEmbEquiv.symm S)) i := by
    funext i; simp
  rw [hcomp]
  change (exteriorPower.ιMulti ℝ k).toMultilinearMap
      (fun i => lam ((Set.powersetCard.ofFinEmbEquiv.symm S) i) •
        (g ∘ (Set.powersetCard.ofFinEmbEquiv.symm S)) i) = _
  rw [MultilinearMap.map_smul_univ, prod_ofFinEmbEquiv_symm]
  rfl

omit [FiniteDimensional ℝ E] in
open scoped Classical in
/-- **Eigen-diagonalization of the compound (abstract).** For a linear map `f` with an orthonormal
eigenbasis `u` (`f (u i) = lam i • u i`), the compound `⋀^k f` scales each wedge basis vector
`u_S` by the subset product `∏_{a ∈ S} lam a`. -/
lemma map_exteriorPower_wedgeBasis_eq {ι : Type*} [Fintype ι] [LinearOrder ι]
    (f : E →ₗ[ℝ] E) (u : OrthonormalBasis ι ℝ E) (lam : ι → ℝ)
    (hf : ∀ i, f (u i) = lam i • u i) (k : ℕ) (S : Set.powersetCard ι k) :
    exteriorPower.map k f (u.toBasis.exteriorPower k S)
      = (∏ a ∈ (S : Finset ι), lam a) • (u.toBasis.exteriorPower k S) := by
  classical
  rw [exteriorPower.basis_apply, exteriorPower.map_apply_ιMulti_family]
  have hfun : (⇑f ∘ ⇑u.toBasis) = fun j => lam j • (⇑u.toBasis j) := by
    funext j; simp only [Function.comp_apply, u.coe_toBasis]; exact hf j
  rw [hfun]
  exact ιMulti_family_smul lam (⇑u.toBasis) S

/-! ### The compound matrix and the operator-norm/compound bridge

For a square matrix `M`, the conjugated exterior map `⋀^k (toEuclideanLin M)` through the
orthonormal-wedge trivialization of the *standard* basis `EuclideanSpace.basisFun` is itself
`toEuclideanLin` of an explicit **compound matrix** `compoundMatrix k M`, whose entries are the
`k × k` minors of `M`. This converts the (analytically delicate) exterior operator norm into the
L2 operator norm of a concrete matrix of determinants — the form needed for measurability. -/

section Compound

variable {d : ℕ}

open scoped Classical in
/-- `onbTriv` sends the `i`-th wedge basis vector (under `(wIndexEquiv b k).symm`) to the `i`-th
standard Euclidean basis vector. -/
lemma onbTriv_wedge_eq_basisFun {ι : Type*} [Fintype ι] [LinearOrder ι]
    {E : Type*} [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    (b : OrthonormalBasis ι ℝ E) (k : ℕ)
    (i : Fin (Module.finrank ℝ (⋀[ℝ]^k E))) :
    onbTriv b k ((b.toBasis.exteriorPower k) ((wIndexEquiv b k).symm i))
      = EuclideanSpace.basisFun (Fin (Module.finrank ℝ (⋀[ℝ]^k E))) ℝ i := by
  ext1 j
  rw [onbTriv_apply, EuclideanSpace.basisFun_apply, PiLp.ofLp_single,
    Basis.repr_reindex_apply, Basis.repr_self, Pi.single_apply, Finsupp.single_apply]
  simp only [eq_comm]
  by_cases hij : i = j <;> simp [hij]

open scoped Classical in
/-- The `t`-th coordinate of `conjExteriorMap k (onbTriv b)(onbTriv b) f` applied to the
`s`-th standard basis vector equals the Hodge form of the corresponding wedge basis vectors. -/
private lemma conjExteriorMap_basisFun_coord {ι : Type*} [Fintype ι] [LinearOrder ι]
    {E F : Type*}
    [NormedAddCommGroup E] [InnerProductSpace ℝ E] [FiniteDimensional ℝ E]
    [NormedAddCommGroup F] [InnerProductSpace ℝ F] [FiniteDimensional ℝ F]
    (bE : OrthonormalBasis ι ℝ E) {κ : Type*} [Fintype κ] [LinearOrder κ]
    (bF : OrthonormalBasis κ ℝ F) (k : ℕ) (f : E →ₗ[ℝ] F)
    (s : Fin (Module.finrank ℝ (⋀[ℝ]^k E))) (t : Fin (Module.finrank ℝ (⋀[ℝ]^k F))) :
    conjExteriorMap k (onbTriv bE k) (onbTriv bF k) f
        (EuclideanSpace.basisFun (Fin (Module.finrank ℝ (⋀[ℝ]^k E))) ℝ s) t
      = hodgeForm k ((bF.toBasis.exteriorPower k) ((wIndexEquiv bF k).symm t))
          (exteriorPower.map k f ((bE.toBasis.exteriorPower k) ((wIndexEquiv bE k).symm s))) := by
  -- Reduce the standard basis vector to the wedge basis through `onbTriv`.
  have hsource : (EuclideanSpace.basisFun (Fin (Module.finrank ℝ (⋀[ℝ]^k E))) ℝ s)
      = onbTriv bE k ((bE.toBasis.exteriorPower k) ((wIndexEquiv bE k).symm s)) :=
    (onbTriv_wedge_eq_basisFun bE k s).symm
  rw [hsource, conjExteriorMap]
  simp only [LinearMap.comp_apply, LinearEquiv.coe_coe, LinearEquiv.symm_apply_apply]
  -- The `t`-coordinate is an inner product with the `t`-th standard basis vector.
  have hcoord : ∀ Y : ⋀[ℝ]^k F, (onbTriv bF k Y) t
      = (inner ℝ (EuclideanSpace.basisFun (Fin (Module.finrank ℝ (⋀[ℝ]^k F))) ℝ t)
          (onbTriv bF k Y) : ℝ) := by
    intro Y
    rw [EuclideanSpace.basisFun_apply]
    change (onbTriv bF k Y) t =
      inner ℝ (EuclideanSpace.single t (1 : ℝ)) (onbTriv bF k Y)
    simpa only [map_one, one_mul] using
      (EuclideanSpace.inner_single_left t (1 : ℝ) (onbTriv bF k Y)).symm
  rw [hcoord, ← onbTriv_wedge_eq_basisFun bF k t, inner_onbTriv]

open Set.powersetCard in
/-- The **compound matrix** `C_k(M)`: its `(t, s)` entry is the `k × k` minor of `M` obtained by
selecting the rows enumerated by the `t`-th `k`-subset and the columns enumerated by the `s`-th
`k`-subset (under the standard orthonormal-wedge index equivalence). -/
noncomputable def compoundMatrix (k : ℕ) (M : Matrix (Fin d) (Fin d) ℝ) :
    Matrix (Fin (Module.finrank ℝ (⋀[ℝ]^k (EuclideanSpace ℝ (Fin d)))))
      (Fin (Module.finrank ℝ (⋀[ℝ]^k (EuclideanSpace ℝ (Fin d))))) ℝ :=
  Matrix.of fun t s =>
    (M.submatrix
      (fun i : Fin k =>
        (ofFinEmbEquiv.symm ((wIndexEquiv (EuclideanSpace.basisFun (Fin d) ℝ) k).symm t)) i)
      (fun j : Fin k =>
        (ofFinEmbEquiv.symm ((wIndexEquiv (EuclideanSpace.basisFun (Fin d) ℝ) k).symm s)) j)).det

/-- The coordinate of `toEuclideanLin M` on a standard basis vector recovers a matrix entry:
`(toEuclideanLin M (eq)) p = M p q`. -/
private lemma toEuclideanLin_single_apply {m : ℕ} (M : Matrix (Fin m) (Fin m) ℝ) (p q : Fin m) :
    (Matrix.toEuclideanLin M (EuclideanSpace.single q (1 : ℝ))) p = M p q := by
  have hofLp : (Matrix.toEuclideanLin M (EuclideanSpace.single q (1 : ℝ))) p
      = (M.mulVec (WithLp.ofLp (EuclideanSpace.single q (1 : ℝ)))) p := rfl
  rw [hofLp,
    show WithLp.ofLp (EuclideanSpace.single q (1 : ℝ)) = Pi.single q (1 : ℝ) from rfl,
    Matrix.mulVec_single_one]
  simp [Matrix.col_apply]

/-- The Gram entry of the standard basis under `toEuclideanLin M` recovers the matrix entry:
`⟪eₚ, (toEuclideanLin M) e_q⟫ = M p q`. -/
private lemma inner_basisFun_toEuclideanLin (M : Matrix (Fin d) (Fin d) ℝ) (p q : Fin d) :
    (inner ℝ ((EuclideanSpace.basisFun (Fin d) ℝ) p)
      (Matrix.toEuclideanLin M ((EuclideanSpace.basisFun (Fin d) ℝ) q)) : ℝ) = M p q := by
  rw [EuclideanSpace.basisFun_apply, EuclideanSpace.basisFun_apply]
  change inner ℝ (EuclideanSpace.single p (1 : ℝ))
      (Matrix.toEuclideanLin M (EuclideanSpace.single q (1 : ℝ))) = M p q
  calc
    _ = (Matrix.toEuclideanLin M (EuclideanSpace.single q (1 : ℝ))) p := by
      simpa only [map_one, one_mul] using
        EuclideanSpace.inner_single_left p (1 : ℝ)
          (Matrix.toEuclideanLin M (EuclideanSpace.single q (1 : ℝ)))
    _ = M p q := toEuclideanLin_single_apply M p q

open scoped Classical in
open Set.powersetCard in
/-- **The compound bridge.** Through the orthonormal-wedge trivializations of the standard basis,
`⋀^k (toEuclideanLin M)` is `toEuclideanLin` of the compound matrix `C_k(M)`. -/
theorem conjExteriorMap_eq_toEuclideanLin_compound (k : ℕ) (M : Matrix (Fin d) (Fin d) ℝ) :
    conjExteriorMap k (onbTriv (EuclideanSpace.basisFun (Fin d) ℝ) k)
        (onbTriv (EuclideanSpace.basisFun (Fin d) ℝ) k) (Matrix.toEuclideanLin M)
      = Matrix.toEuclideanLin (compoundMatrix k M) := by
  -- It suffices to agree on each standard basis vector, coordinatewise.
  refine Basis.ext (EuclideanSpace.basisFun _ ℝ).toBasis (fun s => ?_)
  rw [OrthonormalBasis.coe_toBasis]
  ext t
  -- LHS coordinate is the Hodge form of the wedge basis vectors.
  rw [conjExteriorMap_basisFun_coord (EuclideanSpace.basisFun (Fin d) ℝ)
    (EuclideanSpace.basisFun (Fin d) ℝ) k (Matrix.toEuclideanLin M)]
  -- RHS coordinate is the compound entry `compoundMatrix k M t s`.
  have hRHS : (Matrix.toEuclideanLin (compoundMatrix k M)
      (EuclideanSpace.basisFun (Fin (Module.finrank ℝ (⋀[ℝ]^k (EuclideanSpace ℝ (Fin d))))) ℝ s)) t
      = compoundMatrix k M t s := by
    rw [EuclideanSpace.basisFun_apply, toEuclideanLin_single_apply]
  rw [hRHS, compoundMatrix]
  simp only [Matrix.of_apply]
  -- Expand the Hodge form to a determinant of inner products, then identify with the minor.
  rw [exteriorPower.basis_apply, exteriorPower.basis_apply,
    exteriorPower.map_apply_ιMulti_family, exteriorPower.ιMulti_family,
    exteriorPower.ιMulti_family, hodgeForm_ιMulti]
  -- The Gram entry is `M (row) (col)`; det is invariant under transpose.
  rw [← Matrix.det_transpose]
  congr 1
  ext i j
  rw [Matrix.transpose_apply, Matrix.of_apply, Matrix.submatrix_apply]
  -- Both sides reduce to `M (rowEnum i) (colEnum j)` via `inner_basisFun_toEuclideanLin`.
  simp only [Function.comp_apply, OrthonormalBasis.coe_toBasis]
  exact inner_basisFun_toEuclideanLin M _ _

/-- `toEuclideanLin` of a matrix product is the composition of the linear maps. -/
private lemma toEuclideanLin_mul (B M : Matrix (Fin d) (Fin d) ℝ) :
    Matrix.toEuclideanLin (B * M)
      = (Matrix.toEuclideanLin B) ∘ₗ (Matrix.toEuclideanLin M) := by
  ext v i
  simp only [Matrix.toLpLin_apply, LinearMap.comp_apply, Matrix.mulVec_mulVec]

open scoped Classical in
/-- **Matrix-level Cauchy–Binet.** The `k`-th compound of a matrix product is the
product of the compounds: `C_k(B * M) = C_k(B) * C_k(M)`. This is the multiplicativity of the
compound matrix, proved via the functoriality `⋀^k(B ∘ M) = ⋀^k B ∘ ⋀^k M`
(`exteriorPower.map_comp`) transported through the standard orthonormal-wedge trivialization by
the compound bridge `conjExteriorMap_eq_toEuclideanLin_compound`. -/
theorem compoundMatrix_mul (k : ℕ) (B M : Matrix (Fin d) (Fin d) ℝ) :
    compoundMatrix k (B * M) = compoundMatrix k B * compoundMatrix k M := by
  -- Work through the injective `toEuclideanLin` linear equiv.
  apply (Matrix.toEuclideanLin (n := Fin _) (m := Fin _)).injective
  rw [toEuclideanLin_mul, ← conjExteriorMap_eq_toEuclideanLin_compound,
    ← conjExteriorMap_eq_toEuclideanLin_compound, ← conjExteriorMap_eq_toEuclideanLin_compound]
  -- `toEuclideanLin (B * M) = toEuclideanLin B ∘ₗ toEuclideanLin M`,
  -- then telescope the trivializations.
  rw [toEuclideanLin_mul]
  unfold conjExteriorMap
  rw [exteriorPower.map_comp]
  ext x
  simp [LinearMap.comp_apply]

open scoped Classical in
open Set.powersetCard in
/-- **Compound of a transpose.** The `k`-th compound matrix of `Mᵀ` is the transpose of the `k`-th
compound of `M`: `C_k(Mᵀ) = C_k(M)ᵀ`. Entrywise this is `det(Mᵀ.minor) = det(M.minorᵀ)`
(`Matrix.det_transpose`), since the row/column enumerators at index `t`, `s` coincide. -/
theorem compoundMatrix_transpose (k : ℕ) (M : Matrix (Fin d) (Fin d) ℝ) :
    compoundMatrix k Mᵀ = (compoundMatrix k M)ᵀ := by
  ext t s
  rw [compoundMatrix, Matrix.transpose_apply, compoundMatrix, Matrix.of_apply, Matrix.of_apply,
    ← Matrix.det_transpose, Matrix.transpose_submatrix, Matrix.transpose_transpose]

open scoped Classical in
/-- The `k`-th compound of the Gram matrix `Mᵀ M` is `(C_k M)ᵀ (C_k M)`, i.e. the Gram matrix of the
compound. Combines `compoundMatrix_mul` with `compoundMatrix_transpose`. -/
theorem compoundMatrix_gram (k : ℕ) (M : Matrix (Fin d) (Fin d) ℝ) :
    compoundMatrix k (Mᵀ * M) = (compoundMatrix k M)ᵀ * compoundMatrix k M := by
  rw [compoundMatrix_mul, compoundMatrix_transpose]

open scoped Classical in
/-- **Cauchy–Binet, linear-map form.** `toEuclideanLin` of the `k`-th compound of a product is
the composition of the compounds. This is the form consumed by the rank-1 exterior
Rayleigh-deficit chain below, where the right-hand factor is post-composed with the inverse
compound. -/
theorem toEuclideanLin_compoundMatrix_mul (k : ℕ) (B M : Matrix (Fin d) (Fin d) ℝ) :
    Matrix.toEuclideanLin (compoundMatrix k (B * M))
      = Matrix.toEuclideanLin (compoundMatrix k B)
        ∘ₗ Matrix.toEuclideanLin (compoundMatrix k M) := by
  rw [compoundMatrix_mul, toEuclideanLin_mul]

/-! ### Top singular value vs. the sum of squared singular values (Frobenius)

The Frobenius back-transport below needs `‖M‖_op ≤ ‖M‖_F`. Stated through the
singular-value bridge (`toEuclideanLin`) to avoid the L2-operator vs. Frobenius
`NormedAddCommGroup`-instance diamond on `Matrix`. The core inequality is that the top squared
singular value is at most the sum of all squared singular values; the sum equals
`tr(MᵀM) = ‖M‖_F²`. -/

/-- **The L2 operator-norm/Frobenius bridge.** The squared L2 operator norm `‖M‖²` of a
matrix is at most the sum of the squared singular values of `toEuclideanLin M` (the squared
Frobenius norm). The L2 matrix norm `‖M‖` is by definition the operator norm of `toEuclideanLin M`
on `EuclideanSpace`; expanding any vector in the singular-value eigenbasis `u` of
`adjoint f ∘ₗ f` (with `f = toEuclideanLin M`), the images `f uⱼ` are pairwise orthogonal with
`‖f uⱼ‖ = σⱼ`, so `‖f v‖² = ∑ⱼ ⟪uⱼ, v⟫² σⱼ² ≤ (∑ σᵢ²) ‖v‖²`. -/
theorem l2_opNorm_sq_le_sum_singularValues (M : Matrix (Fin d) (Fin d) ℝ) :
    ‖M‖ ^ 2 ≤ ∑ i : Fin d, (Matrix.toEuclideanLin M).singularValues i ^ 2 := by
  set f := Matrix.toEuclideanLin M with hf
  set S := ∑ i : Fin d, f.singularValues i ^ 2 with hS
  have hSnn : 0 ≤ S := Finset.sum_nonneg (fun i _ => sq_nonneg _)
  have hfin : Module.finrank ℝ (EuclideanSpace ℝ (Fin d)) = d := finrank_euclideanSpace_fin
  set hT := f.isSymmetric_adjoint_comp_self with hhT
  set u := hT.eigenvectorBasis hfin with hu
  -- pointwise bound `‖f v‖² ≤ S ‖v‖²`
  have hpt : ∀ v : EuclideanSpace ℝ (Fin d), ‖f v‖ ^ 2 ≤ S * ‖v‖ ^ 2 := by
    intro v
    have hexp : f v = ∑ j, (inner ℝ (u j) v : ℝ) • f (u j) := by
      conv_lhs => rw [← u.sum_repr' v]
      rw [map_sum]; simp_rw [map_smul]
    have horth : ∀ i j, i ≠ j → (inner ℝ (f (u i)) (f (u j)) : ℝ) = 0 := by
      intro i j hij
      have h1 : (inner ℝ (f (u i)) (f (u j)) : ℝ)
          = inner ℝ ((LinearMap.adjoint f ∘ₗ f) (u j)) (u i) := by
        rw [LinearMap.comp_apply, LinearMap.adjoint_inner_left, real_inner_comm]
      rw [h1, show (LinearMap.adjoint f ∘ₗ f) (u j) = (hT.eigenvalues hfin j : ℝ) • u j from
            hT.apply_eigenvectorBasis hfin j, inner_smul_left, u.inner_eq_ite j i]
      simp [Ne.symm hij]
    have hnormfu : ∀ j, ‖f (u j)‖ ^ 2 = f.singularValues j ^ 2 := by
      intro j
      have key : (inner ℝ (f (u j)) (f (u j)) : ℝ) = f.singularValues j ^ 2 := by
        have h1 : (inner ℝ (f (u j)) (f (u j)) : ℝ)
            = inner ℝ ((LinearMap.adjoint f ∘ₗ f) (u j)) (u j) := by
          rw [LinearMap.comp_apply, LinearMap.adjoint_inner_left]
        rw [h1, show (LinearMap.adjoint f ∘ₗ f) (u j) = (hT.eigenvalues hfin j : ℝ) • u j from
              hT.apply_eigenvectorBasis hfin j, inner_smul_left, u.inner_eq_ite j j,
            f.sq_singularValues_fin hfin j]
        simp
      rw [← real_inner_self_eq_norm_sq]; exact key
    have hsq : ‖f v‖ ^ 2 = ∑ j, (inner ℝ (u j) v : ℝ) ^ 2 * ‖f (u j)‖ ^ 2 := by
      rw [← real_inner_self_eq_norm_sq, hexp, inner_sum]
      simp_rw [sum_inner, inner_smul_left, inner_smul_right]
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro j _
      rw [Finset.sum_eq_single j]
      · rw [real_inner_self_eq_norm_sq]
        simp only [starRingEnd_apply, star_trivial]; ring
      · intro i _ hij
        rw [horth j i (Ne.symm hij)]; ring
      · intro h; exact absurd (Finset.mem_univ j) h
    rw [hsq]
    have hpars : ∑ j, (inner ℝ (u j) v : ℝ) ^ 2 = ‖v‖ ^ 2 := by
      have := u.sum_sq_norm_inner_right v
      simp only [Real.norm_eq_abs, sq_abs] at this
      exact this
    calc ∑ j, (inner ℝ (u j) v : ℝ) ^ 2 * ‖f (u j)‖ ^ 2
        = ∑ j, (inner ℝ (u j) v : ℝ) ^ 2 * f.singularValues j ^ 2 := by
          apply Finset.sum_congr rfl; intro j _; rw [hnormfu]
      _ ≤ ∑ j, (inner ℝ (u j) v : ℝ) ^ 2 * S := by
          apply Finset.sum_le_sum; intro j _
          apply mul_le_mul_of_nonneg_left _ (sq_nonneg _)
          rw [hS]
          exact Finset.single_le_sum
            (f := fun i : Fin d => f.singularValues i ^ 2)
            (fun i _ => sq_nonneg _) (Finset.mem_univ j)
      _ = S * ‖v‖ ^ 2 := by rw [← Finset.sum_mul, hpars]; ring
  -- bound the operator norm by `√S`
  have hnorm_le : ‖M‖ ≤ Real.sqrt S := by
    rw [Matrix.l2_opNorm_def]
    apply ContinuousLinearMap.opNorm_le_bound _ (Real.sqrt_nonneg S)
    intro v
    change ‖_‖ ≤ Real.sqrt S * ‖v‖
    rw [LinearEquiv.trans_apply, LinearMap.coe_toContinuousLinearMap', ← hf]
    have h2 := hpt v
    have hrhs : 0 ≤ Real.sqrt S * ‖v‖ := mul_nonneg (Real.sqrt_nonneg S) (norm_nonneg v)
    nlinarith [norm_nonneg (f v), Real.sq_sqrt hSnn, h2, hrhs]
  nlinarith [hnorm_le, norm_nonneg M, Real.sq_sqrt hSnn, Real.sqrt_nonneg S]

/-- The sum of the squared singular values of `toEuclideanLin N` equals the trace of the Gram
matrix `tr(Nᵀ N)` (the squared Frobenius norm). Both sides are the trace of the self-adjoint
operator `adjoint f ∘ₗ f = toEuclideanLin (Nᵀ N)`: in the singular-value eigenbasis its diagonal
entries are the eigenvalues `σᵢ²`, while as a matrix its trace is `tr(Nᵀ N)`. -/
theorem sum_sq_singularValues_eq_trace (N : Matrix (Fin d) (Fin d) ℝ) :
    ∑ i : Fin d, (Matrix.toEuclideanLin N).singularValues i ^ 2 = (Nᵀ * N).trace := by
  set f := Matrix.toEuclideanLin N with hf
  have hfin : Module.finrank ℝ (EuclideanSpace ℝ (Fin d)) = d := finrank_euclideanSpace_fin
  set hT := f.isSymmetric_adjoint_comp_self with hhT
  set u := hT.eigenvectorBasis hfin with hu
  -- `∑ σᵢ² = trace (adjoint f ∘ₗ f)`, computed in the eigenbasis `u`.
  have h1 : ∑ i : Fin d, f.singularValues i ^ 2
      = LinearMap.trace ℝ _ (LinearMap.adjoint f ∘ₗ f) := by
    rw [LinearMap.trace_eq_matrix_trace ℝ u.toBasis (LinearMap.adjoint f ∘ₗ f), Matrix.trace]
    apply Finset.sum_congr rfl
    intro i _
    rw [Matrix.diag_apply, LinearMap.toMatrix_apply, OrthonormalBasis.coe_toBasis,
      show (LinearMap.adjoint f ∘ₗ f) (u i) = (hT.eigenvalues hfin i : ℝ) • u i from
        hT.apply_eigenvectorBasis hfin i, map_smul, Finsupp.smul_apply, smul_eq_mul,
      OrthonormalBasis.coe_toBasis_repr_apply, u.repr_self, f.sq_singularValues_fin hfin i]
    simp
  -- `adjoint f ∘ₗ f = toEuclideanLin (Nᵀ N)`.
  have h2 : LinearMap.adjoint f ∘ₗ f = Matrix.toEuclideanLin (Nᵀ * N) := by
    subst f
    rw [toEuclideanLin_mul]
    have hadj := Matrix.toEuclideanLin_conjTranspose_eq_adjoint N
    rw [Matrix.conjTranspose_eq_transpose_of_trivial] at hadj
    rw [hadj]
    rfl
  -- `trace (toEuclideanLin G) = tr G`.
  rw [h1, h2, Matrix.toEuclideanLin_eq_toLin_orthonormal, Matrix.trace_toLin_eq]

/-- `toEuclideanLin` of a (rectangular) matrix product is the composition of the linear maps. -/
private lemma toEuclideanLin_mul_rect {a b c : ℕ} (B : Matrix (Fin a) (Fin b) ℝ)
    (M : Matrix (Fin b) (Fin c) ℝ) :
    Matrix.toEuclideanLin (B * M)
      = (Matrix.toEuclideanLin B) ∘ₗ (Matrix.toEuclideanLin M) := by
  ext v i
  simp only [Matrix.toLpLin_apply, LinearMap.comp_apply, Matrix.mulVec_mulVec]

/-- A matrix `U` with orthonormal columns (`Uᵀ U = 1`) is an isometry, so its L2 operator norm is
at most `1`. -/
theorem norm_le_one_of_cols_orthonormal {k : ℕ} (U : Matrix (Fin d) (Fin k) ℝ)
    (hU : Uᵀ * U = 1) : ‖U‖ ≤ 1 := by
  rw [Matrix.l2_opNorm_def]
  apply ContinuousLinearMap.opNorm_le_bound _ zero_le_one
  intro x
  rw [one_mul]
  change ‖Matrix.toEuclideanLin U x‖ ≤ ‖x‖
  have hsq : ‖Matrix.toEuclideanLin U x‖ ^ 2 = ‖x‖ ^ 2 := by
    rw [← real_inner_self_eq_norm_sq, ← real_inner_self_eq_norm_sq]
    have hadj : (inner ℝ (Matrix.toEuclideanLin U x) (Matrix.toEuclideanLin U x) : ℝ)
        = inner ℝ
            ((LinearMap.adjoint (Matrix.toEuclideanLin U) ∘ₗ Matrix.toEuclideanLin U) x) x := by
      rw [LinearMap.comp_apply, LinearMap.adjoint_inner_left]
    rw [hadj]
    congr 1
    have hadj' := Matrix.toEuclideanLin_conjTranspose_eq_adjoint U
    rw [Matrix.conjTranspose_eq_transpose_of_trivial] at hadj'
    have hcomp : LinearMap.adjoint (Matrix.toEuclideanLin U) ∘ₗ Matrix.toEuclideanLin U
        = Matrix.toEuclideanLin (Uᵀ * U) := by
      calc
        LinearMap.adjoint (Matrix.toEuclideanLin U) ∘ₗ Matrix.toEuclideanLin U
            = Matrix.toEuclideanLin Uᵀ ∘ₗ Matrix.toEuclideanLin U := by
              rw [hadj']
              rfl
        _ = Matrix.toEuclideanLin (Uᵀ * U) := (toEuclideanLin_mul_rect Uᵀ U).symm
    rw [hcomp, hU]
    simp
  nlinarith [norm_nonneg (Matrix.toEuclideanLin U x), norm_nonneg x, hsq]

/-- The eigenvalues of the Gram matrix `Wᵀ W` are bounded by the squared L2 operator norm `‖W‖²`.
Each eigenvalue `μᵢ` of the Hermitian matrix `G = Wᵀ W`, with unit eigenvector `bᵢ`, equals
`‖toEuclideanLin W (bᵢ)‖² ≤ ‖W‖²`. -/
theorem gram_eigenvalues_le_opNorm_sq {k : ℕ} (W : Matrix (Fin k) (Fin k) ℝ)
    (hGherm : (Wᵀ * W).IsHermitian) (i : Fin k) : hGherm.eigenvalues i ≤ ‖W‖ ^ 2 := by
  set G := Wᵀ * W with hG
  set b := hGherm.eigenvectorBasis with hb
  set W' := Matrix.toEuclideanLin W with hW'
  have hGlin : Matrix.toEuclideanLin G = LinearMap.adjoint W' ∘ₗ W' := by
    subst W'
    rw [hG, toEuclideanLin_mul]
    have hadj := Matrix.toEuclideanLin_conjTranspose_eq_adjoint W
    rw [Matrix.conjTranspose_eq_transpose_of_trivial] at hadj
    rw [hadj]
    rfl
  have hmuleq : hGherm.eigenvalues i = ‖W' (b i)‖ ^ 2 := by
    have hmv : G *ᵥ ⇑(b i) = hGherm.eigenvalues i • ⇑(b i) := hGherm.mulVec_eigenvectorBasis i
    have hinner : (inner ℝ (Matrix.toEuclideanLin G (b i)) (b i) : ℝ)
        = hGherm.eigenvalues i := by
      have hsmul : Matrix.toEuclideanLin G (b i) = hGherm.eigenvalues i • (b i) := by
        rw [Matrix.toLpLin_apply, hmv]; rfl
      rw [hsmul, inner_smul_left, real_inner_self_eq_norm_sq, b.orthonormal.1 i]
      simp
    rw [← hinner, hGlin, LinearMap.comp_apply, LinearMap.adjoint_inner_left,
      real_inner_self_eq_norm_sq]
  rw [hmuleq]
  have hbnd : ‖W' (b i)‖ ≤ ‖W‖ * ‖b i‖ := by
    have hle := (LinearMap.toContinuousLinearMap W').le_opNorm (b i)
    rwa [LinearMap.coe_toContinuousLinearMap',
      show ‖LinearMap.toContinuousLinearMap W'‖ = ‖W‖ from rfl] at hle
  rw [b.orthonormal.1 i, mul_one] at hbnd
  nlinarith [norm_nonneg (W' (b i)), norm_nonneg W, hbnd]

/-- **The Frobenius back-transport.** For matrices `U, V` with orthonormal columns
(`Uᵀ U = 1`, `Vᵀ V = 1`), the squared L2 operator norm of the difference of the orthogonal
projectors `U Uᵀ` and `V Vᵀ` is bounded by `2 k (1 - det(Uᵀ V)²)`. Chain: self-adjoint idempotents
of trace `k`; `‖P − P'‖²_op ≤ ∑σᵢ² = tr((P−P')²) = 2k − 2 tr(P P')`; `tr(P P') = ‖Uᵀ V‖_F² = tr(G)`
for the Gram `G = (Uᵀ V)ᵀ (Uᵀ V)`; then the elementary AM-GM `k ∏ tᵢ ≤ ∑ tᵢ` over the eigenvalues
`tᵢ ∈ [0, 1]` of `G`, with `∏ tᵢ = det G = det(Uᵀ V)²`. -/
theorem norm_proj_sub_le_wedge {k : ℕ} (U V : Matrix (Fin d) (Fin k) ℝ)
    (hU : Uᵀ * U = 1) (hV : Vᵀ * V = 1) :
    ‖U * Uᵀ - V * Vᵀ‖ ^ 2 ≤ 2 * k * (1 - (Uᵀ * V).det ^ 2) := by
  set P := U * Uᵀ with hP
  set P' := V * Vᵀ with hP'
  -- self-adjoint idempotents of trace `k`
  have hPidem : P * P = P := by
    rw [hP, show U * Uᵀ * (U * Uᵀ) = U * (Uᵀ * U) * Uᵀ by simp only [Matrix.mul_assoc], hU,
      Matrix.mul_one]
  have hP'idem : P' * P' = P' := by
    rw [hP', show V * Vᵀ * (V * Vᵀ) = V * (Vᵀ * V) * Vᵀ by simp only [Matrix.mul_assoc], hV,
      Matrix.mul_one]
  have hPsymm : Pᵀ = P := by rw [hP, Matrix.transpose_mul, Matrix.transpose_transpose]
  have hP'symm : P'ᵀ = P' := by rw [hP', Matrix.transpose_mul, Matrix.transpose_transpose]
  have hPtrace : P.trace = (k : ℝ) := by
    rw [hP, Matrix.trace_mul_comm, hU, Matrix.trace_one, Fintype.card_fin]
  have hP'trace : P'.trace = (k : ℝ) := by
    rw [hP', Matrix.trace_mul_comm, hV, Matrix.trace_one, Fintype.card_fin]
  -- `‖P − P'‖²_op ≤ ∑σᵢ(P−P')² = tr((P−P')ᵀ(P−P')) = tr((P−P')²)`
  have hsymm : (P - P')ᵀ = P - P' := by rw [Matrix.transpose_sub, hPsymm, hP'symm]
  have hnorm : ‖P - P'‖ ^ 2 ≤ ((P - P')ᵀ * (P - P')).trace :=
    le_trans (l2_opNorm_sq_le_sum_singularValues _) (le_of_eq (sum_sq_singularValues_eq_trace _))
  rw [hsymm] at hnorm
  -- `tr((P−P')²) = 2k − 2 tr(P P')`
  have htrid : ((P - P') * (P - P')).trace = 2 * (k : ℝ) - 2 * (P * P').trace := by
    have hexp : (P - P') * (P - P') = P * P - P * P' - P' * P + P' * P' := by
      rw [sub_mul, mul_sub, mul_sub]; abel
    rw [hexp, hPidem, hP'idem, Matrix.trace_add, Matrix.trace_sub, Matrix.trace_sub,
      hPtrace, hP'trace, Matrix.trace_mul_comm P' P]
    ring
  rw [htrid] at hnorm
  -- `tr(P P') = tr((Uᵀ V)ᵀ (Uᵀ V))`
  have htrPP' : (P * P').trace = ((Uᵀ * V)ᵀ * (Uᵀ * V)).trace := by
    have step1 : (P * P').trace = ((Uᵀ * V) * (Uᵀ * V)ᵀ).trace := by
      rw [hP, hP', show U * Uᵀ * (V * Vᵀ) = U * (Uᵀ * V * Vᵀ) by simp only [Matrix.mul_assoc],
        Matrix.trace_mul_comm U (Uᵀ * V * Vᵀ)]
      congr 1
      simp only [Matrix.transpose_mul, Matrix.transpose_transpose, Matrix.mul_assoc]
    rw [step1, Matrix.trace_mul_comm]
  -- the Gram `G = (Uᵀ V)ᵀ (Uᵀ V)`: PosSemidef Hermitian, eigenvalues in `[0, 1]`
  set W := Uᵀ * V with hW
  have hWconj : Wᴴ = Wᵀ := Matrix.conjTranspose_eq_transpose_of_trivial _
  have hPSD : (Wᵀ * W).PosSemidef := by
    have hps := Matrix.posSemidef_conjTranspose_mul_self W
    rwa [hWconj] at hps
  set G := Wᵀ * W with hG
  set hGherm := hPSD.isHermitian with hGhermdef
  set t : Fin k → ℝ := hGherm.eigenvalues with ht
  have htnn : ∀ i, 0 ≤ t i := fun i => hPSD.eigenvalues_nonneg i
  have hWnorm : ‖W‖ ≤ 1 := by
    have hUtnorm : ‖(Uᵀ : Matrix (Fin k) (Fin d) ℝ)‖ ≤ 1 := by
      rw [show (Uᵀ : Matrix (Fin k) (Fin d) ℝ) = Uᴴ from
        (Matrix.conjTranspose_eq_transpose_of_trivial U).symm, Matrix.l2_opNorm_conjTranspose]
      exact norm_le_one_of_cols_orthonormal U hU
    calc ‖W‖ = ‖Uᵀ * V‖ := by rw [hW]
      _ ≤ ‖Uᵀ‖ * ‖V‖ := Matrix.l2_opNorm_mul _ _
      _ ≤ 1 * 1 :=
          mul_le_mul hUtnorm (norm_le_one_of_cols_orthonormal V hV) (norm_nonneg _) zero_le_one
      _ = 1 := one_mul 1
  have ht1 : ∀ i, t i ≤ 1 := by
    intro i
    calc t i ≤ ‖W‖ ^ 2 := gram_eigenvalues_le_opNorm_sq W hGherm i
      _ ≤ 1 ^ 2 := by gcongr
      _ = 1 := one_pow 2
  have htrG : G.trace = ∑ i, t i := by
    rw [ht, hGhermdef, hGherm.trace_eq_sum_eigenvalues]; simp
  have hdetG : G.det = ∏ i, t i := by
    rw [ht, hGhermdef, hGherm.det_eq_prod_eigenvalues]; simp
  have hdetGW : G.det = W.det ^ 2 := by rw [hG, Matrix.det_mul, Matrix.det_transpose]; ring
  -- AM-GM: `k ∏ tᵢ ≤ ∑ tᵢ` (each `tᵢ ∈ [0, 1]`)
  have hAMGM : (k : ℝ) * ∏ i, t i ≤ ∑ i, t i := by
    have hprod_le : ∀ j : Fin k, ∏ i, t i ≤ t j := by
      intro j
      calc ∏ i, t i = t j * ∏ i ∈ Finset.univ.erase j, t i :=
            (Finset.mul_prod_erase Finset.univ t (Finset.mem_univ j)).symm
        _ ≤ t j * 1 := by
            apply mul_le_mul_of_nonneg_left _ (htnn j)
            exact Finset.prod_le_one (fun i _ => htnn i) (fun i _ => ht1 i)
        _ = t j := mul_one _
    calc (k : ℝ) * ∏ i, t i
        = ∑ _j : Fin k, ∏ i, t i := by
          rw [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
      _ ≤ ∑ j, t j := Finset.sum_le_sum (fun j _ => hprod_le j)
  -- assemble
  have hPP'trace : (P * P').trace = ∑ i, t i := htrPP'.trans htrG
  rw [hPP'trace] at hnorm
  have hprodeq : ∏ i, t i = (Uᵀ * V).det ^ 2 := by rw [← hdetG, hdetGW, hW]
  have hfinal : 2 * (k : ℝ) - 2 * ∑ i, t i ≤ 2 * (k : ℝ) * (1 - (Uᵀ * V).det ^ 2) := by
    rw [← hprodeq]; nlinarith [hAMGM]
  exact le_trans hnorm hfinal

set_option maxHeartbeats 800000 in -- heavy elaboration; exceeds the default budget
-- The `⋀^k`-finrank-indexed `EuclideanSpace` statement is expensive to elaborate.
/-- **The product of singular values is the L2 operator norm of the compound matrix.** Combining
the singular-value bridge with the compound identity: `∏_{i<k} σᵢ(toEuclideanLin M) = ‖C_k(M)‖`. -/
theorem prod_singularValues_eq_l2_opNorm_compound (k : ℕ) (M : Matrix (Fin d) (Fin d) ℝ) :
    ∏ i ∈ Finset.range k, (Matrix.toEuclideanLin M).singularValues i
      = ‖compoundMatrix k M‖ := by
  classical
  -- The Hodge trivialization on `EuclideanSpace ℝ (Fin d)` is the standard-basis wedge
  -- trivialization, so the singular-value bridge is the standard-basis exterior operator norm.
  have hStd : hodgeTrivialization (E := EuclideanSpace ℝ (Fin d)) k
      = onbTriv (stdOrthonormalBasis ℝ (EuclideanSpace ℝ (Fin d))) k := by
    unfold hodgeTrivialization onbTriv wedgeBasis wedgeIndexEquiv wIndexEquiv
    rfl
  -- Pass from the Hodge trivialization to the standard-basis (`basisFun`) trivialization.
  rw [← exteriorOpNorm_hodge_eq_prod_singularValues k (Matrix.toEuclideanLin M)]
  rw [show exteriorOpNorm k (hodgeTrivialization (E := EuclideanSpace ℝ (Fin d)) k)
        (hodgeTrivialization (E := EuclideanSpace ℝ (Fin d)) k) (Matrix.toEuclideanLin M)
      = exteriorOpNorm k (onbTriv (EuclideanSpace.basisFun (Fin d) ℝ) k)
          (onbTriv (EuclideanSpace.basisFun (Fin d) ℝ) k) (Matrix.toEuclideanLin M) by
    rw [hStd]
    exact exteriorOpNorm_onbTriv_eq (stdOrthonormalBasis ℝ (EuclideanSpace ℝ (Fin d)))
      (EuclideanSpace.basisFun (Fin d) ℝ) (stdOrthonormalBasis ℝ (EuclideanSpace ℝ (Fin d)))
      (EuclideanSpace.basisFun (Fin d) ℝ) k (Matrix.toEuclideanLin M)]
  -- Now identify the conjugated exterior map with `toEuclideanLin` of the compound matrix.
  rw [exteriorOpNorm, conjExteriorMap_eq_toEuclideanLin_compound k M]
  rw [Matrix.l2_opNorm_def]
  rfl

end Compound

end Bridge

end ErgodicTheory.ExteriorNorm

end
