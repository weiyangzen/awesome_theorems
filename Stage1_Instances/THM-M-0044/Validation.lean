import Statement
import Mathlib.Analysis.InnerProductSpace.SingularValues
import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0044 differential validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It separately reconstructs
the exact frozen Real-and-Complex root from the pinned spectral and orthonormal-basis interfaces.
It is same-worker differential corroboration, not independent-runner or release evidence.
-/

noncomputable section

set_option autoImplicit false

namespace Stage1Instances.THM_M_0044.Validation

open Module InnerProductSpace
open scoped InnerProduct

open Stage1Instances.THM_M_0044

universe u

private theorem differentialSVDBasisTall {K : Type u} [RCLike K] {m n : Nat}
    (L : EuclideanSpace K (Fin n) →ₗ[K] EuclideanSpace K (Fin m)) (hnm : n <= m) :
    Exists fun b : OrthonormalBasis (Fin n) K (EuclideanSpace K (Fin n)) =>
      Exists fun c : OrthonormalBasis (Fin m) K (EuclideanSpace K (Fin m)) =>
        Exists fun sigma : Fin n -> Real =>
          (forall i, 0 <= sigma i) /\
          (forall i, L (b i) = (sigma i : K) • c (Fin.castLE hnm i)) := by
  classical
  let S := L.adjoint.comp L
  have hSsym : S.IsSymmetric := L.isSymmetric_adjoint_comp_self
  let b := hSsym.eigenvectorBasis finrank_euclideanSpace_fin
  let mu : Fin n -> Real := hSsym.eigenvalues finrank_euclideanSpace_fin
  have hmu : forall i, 0 <= mu i :=
    L.isPositive_adjoint_comp_self.nonneg_eigenvalues finrank_euclideanSpace_fin
  let sigma : Fin n -> Real := fun i => Real.sqrt (mu i)
  have hsigma : forall i, 0 <= sigma i := fun i => Real.sqrt_nonneg _
  have hmu_sigma : forall i, mu i = sigma i ^ 2 := by
    intro i
    simp [sigma, Real.sq_sqrt (hmu i)]
  have hinner : forall i j,
      inner K (L (b i)) (L (b j)) =
        (mu i : K) * (if i = j then (1 : K) else 0) := by
    intro i j
    calc
      inner K (L (b i)) (L (b j)) = inner K (S (b i)) (b j) := by
        simp [S, LinearMap.adjoint_inner_left]
      _ = inner K ((mu i : K) • b i) (b j) := by
        rw [show S (b i) = (mu i : K) • b i by
          exact hSsym.apply_eigenvectorBasis finrank_euclideanSpace_fin i]
      _ = (mu i : K) * (if i = j then (1 : K) else 0) := by
        rw [inner_smul_left]
        simp [orthonormal_iff_ite.mp b.orthonormal i j]
  have hzero : forall i, sigma i = 0 -> L (b i) = 0 := by
    intro i hi
    have hself : inner K (L (b i)) (L (b i)) = 0 := by
      rw [hinner i i, if_pos rfl, hmu_sigma i, hi]
      simp
    rwa [inner_self_eq_zero] at hself
  let e : Fin n -> Fin m := Fin.castLE hnm
  have he : Function.Injective e := Fin.castLE_injective hnm
  let active : Set (Fin m) := e '' {i | sigma i ≠ 0}
  let normalized : Fin n -> EuclideanSpace K (Fin m) :=
    fun i => (sigma i : K)⁻¹ • L (b i)
  let v : Fin m -> EuclideanSpace K (Fin m) := Function.extend e normalized 0
  have hv_e : forall i, v (e i) = normalized i := by
    intro i
    dsimp only [v]
    exact Function.Injective.extend_apply he normalized 0 i
  have hvon : Orthonormal K (active.restrict v) := by
    rw [orthonormal_iff_ite]
    rintro ⟨x, hx⟩ ⟨y, hy⟩
    obtain ⟨i, hi, rfl⟩ := hx
    obtain ⟨j, hj, rfl⟩ := hy
    simp only [Set.mem_setOf_eq] at hi hj
    simp only [Set.restrict_apply, hv_e, normalized]
    rw [inner_smul_left, inner_smul_right, hinner]
    rw [hmu_sigma]
    by_cases hij : i = j
    · subst j
      simp only [if_pos]
      have hiK : (sigma i : K) ≠ 0 := by exact_mod_cast hi
      have hstar : (starRingEnd K) (sigma i : K) = (sigma i : K) := by simp
      rw [map_inv₀, hstar]
      push_cast
      field_simp
    · have heij : e i ≠ e j := fun h => hij (he h)
      simp [hij, heij]
  obtain ⟨c, hc⟩ := hvon.exists_orthonormalBasis_extension_of_card_eq
    (by simp) (v := v)
  refine ⟨b, c, sigma, hsigma, ?_⟩
  intro i
  by_cases hi : sigma i = 0
  · simp [hi, hzero i hi]
  · have hci : c (e i) = v (e i) := hc (e i) (by exact ⟨i, hi, rfl⟩)
    rw [hci, hv_e]
    simp only [normalized]
    rw [smul_inv_smul₀]
    exact_mod_cast hi

private theorem differentialFullSVDTall {K : Type u} [RCLike K] {m n : Nat}
    (hmn : n <= m) (A : Matrix (Fin m) (Fin n) K) : IsFullSVD A := by
  classical
  let L : EuclideanSpace K (Fin n) →ₗ[K] EuclideanSpace K (Fin m) :=
    Matrix.toEuclideanLin A
  obtain ⟨b, c, sigma, hsigma, hLb⟩ := differentialSVDBasisTall L hmn
  let e : Fin n -> Fin m := Fin.castLE hmn
  let stdN := EuclideanSpace.basisFun (Fin n) K
  let stdM := EuclideanSpace.basisFun (Fin m) K
  let U : Matrix (Fin m) (Fin m) K := stdM.toBasis.toMatrix c.toBasis
  let V : Matrix (Fin n) (Fin n) K := stdN.toBasis.toMatrix b.toBasis
  have hmin : Nat.min m n = n := Nat.min_eq_right hmn
  let sigmaMin : Fin (Nat.min m n) -> Real := fun i => sigma (Fin.cast hmin i)
  refine ⟨U, V, sigmaMin, ?_, ?_, ?_, ?_⟩
  · exact stdM.toMatrix_orthonormalBasis_mem_unitary c
  · exact stdN.toMatrix_orthonormalBasis_mem_unitary b
  · intro i
    exact hsigma (Fin.cast hmin i)
  · dsimp only
    constructor
    · intro i j hij
      simp only
      rw [dif_neg]
      simpa only [bne_iff_ne] using hij
    · let Sigma : Matrix (Fin m) (Fin n) K := fun i j => if h : i.val = j.val then
          (sigmaMin ⟨i.val, lt_min i.isLt (h ▸ j.isLt)⟩ : K) else 0
      have hAV : A * V = U * Sigma := by
        ext i j
        simp only [V, U, Sigma, Matrix.mul_apply, Basis.toMatrix_apply]
        have hcoord := congrFun (congrArg (WithLp.ofLp :
          EuclideanSpace K (Fin m) -> (Fin m -> K)) (hLb j)) i
        change (∑ x, A i x * (b j) x) = _
        rw [show (∑ x, A i x * (b j) x) = (L (b j)) i by rfl]
        rw [hcoord]
        rw [Finset.sum_eq_single (e j)]
        · simp only [e, sigmaMin, PiLp.smul_apply, smul_eq_mul,
            OrthonormalBasis.coe_toBasis, Fin.cast_mk]
          have heval : (Fin.castLE hmn j).val = j.val := rfl
          rw [dif_pos heval]
          change (sigma j : K) * (c (Fin.castLE hmn j)) i =
            (c (Fin.castLE hmn j)) i * (sigma j : K)
          exact mul_comm _ _
        · intro k _ hkj
          rw [dif_neg]
          · simp
          · intro hval
            apply hkj
            exact Fin.ext hval
        · simp
      calc
        A = (A * V) * star V := by
          rw [Matrix.mul_assoc]
          change A = A * (V * star V)
          rw [Matrix.mem_unitaryGroup_iff.mp
            (show V ∈ Matrix.unitaryGroup (Fin n) K from
              stdN.toMatrix_orthonormalBasis_mem_unitary b), Matrix.mul_one]
        _ = U * Sigma * star V := by rw [hAV]

private theorem differentialFullSVDWide {K : Type u} [RCLike K] {m n : Nat}
    (hmn : m <= n) (A : Matrix (Fin m) (Fin n) K) : IsFullSVD A := by
  classical
  obtain ⟨U0, V0, sigma, hU0, hV0, hsigma, hSigma0, hfac⟩ :=
    differentialFullSVDTall hmn A.conjTranspose
  let U : Matrix (Fin m) (Fin m) K := V0
  let V : Matrix (Fin n) (Fin n) K := U0
  have hmin : Nat.min m n = m := Nat.min_eq_left hmn
  have hmin0 : Nat.min n m = m := Nat.min_eq_right hmn
  let sigmaMin : Fin (Nat.min m n) -> Real := fun i => sigma (Fin.cast hmin0.symm (Fin.cast hmin i))
  refine ⟨U, V, sigmaMin, hV0, hU0, ?_, ?_⟩
  · intro i
    exact hsigma (Fin.cast hmin0.symm (Fin.cast hmin i))
  dsimp only
  constructor
  · intro i j hij
    simp only
    rw [dif_neg]
    simpa only [bne_iff_ne] using hij
  · let Sigma : Matrix (Fin m) (Fin n) K := fun i j => if h : i.val = j.val then
        (sigmaMin ⟨i.val, lt_min i.isLt (h ▸ j.isLt)⟩ : K) else 0
    let Sigma0 : Matrix (Fin n) (Fin m) K := fun i j => if h : i.val = j.val then
        (sigma ⟨i.val, lt_min i.isLt (h ▸ j.isLt)⟩ : K) else 0
    have hstarSigma : Sigma0.conjTranspose = Sigma := by
      ext i j
      simp only [Matrix.conjTranspose_apply, Sigma0, Sigma]
      by_cases h : i.val = j.val
      · have h' : j.val = i.val := h.symm
        rw [dif_pos h', dif_pos h]
        simp [sigmaMin, h]
      · have h' : j.val ≠ i.val := Ne.symm h
        simp [h, h']
    have hfac' : A.conjTranspose = U0 * Sigma0 * star V0 := hfac
    have := congrArg Matrix.conjTranspose hfac'
    simpa only [Matrix.conjTranspose_mul, Matrix.conjTranspose_conjTranspose,
      Matrix.star_eq_conjTranspose, hstarSigma, U, V, Matrix.mul_assoc] using this

private theorem differentialFullSVDOver (K : Type u) [RCLike K] : FullSVDOver K := by
  intro m n A
  by_cases hmn : n <= m
  · exact differentialFullSVDTall hmn A
  · exact differentialFullSVDWide (Nat.le_of_lt (Nat.lt_of_not_ge hmn)) A

/-- Separately written exact root for same-worker differential validation. -/
theorem differentialSingularValueDecomposition : SingularValueDecompositionTarget :=
  ⟨differentialFullSVDOver Real, differentialFullSVDOver Complex⟩

assert_no_sorry differentialSingularValueDecomposition
#print sorries differentialSingularValueDecomposition
#print axioms differentialSingularValueDecomposition

end Stage1Instances.THM_M_0044.Validation
