import Mathlib.Analysis.InnerProductSpace.JointEigenspace
import Mathlib.Analysis.Matrix.Spectrum
import ObligationTree

/-!
# THM-M-0043 proof execution

This module implements the frozen normal-matrix route locally. It constructs simultaneous
eigenvectors for the commuting Hermitian real and imaginary parts of a normal complex matrix,
packages the resulting orthonormal basis as a unitary matrix, and consumes the checked
child-to-root composition from `ObligationTree.lean`.
-/

namespace Stage1Instances.THM_M_0043.Proof

open scoped ComplexStarModule

open Complex LinearMap Matrix Module.End Submodule
open Stage1Instances.THM_M_0043
open Stage1Instances.THM_M_0043.ObligationTree

universe u

set_option maxHeartbeats 1600000 in
/-- Two commuting Hermitian complex matrices have a common orthonormal eigenbasis, which
diagonalizes their complex linear combination. -/
theorem commutingHermitianParts_conjugatedDiagonal
    {n : Type u} [Fintype n] [DecidableEq n]
    (H K : Matrix n n Complex) (hH : H.IsHermitian) (hK : K.IsHermitian)
    (hHK : H * K = K * H) :
    exists (P : Matrix n n Complex) (_ : P ∈ Matrix.unitaryGroup n Complex)
      (d : n -> Complex),
      star P * (H + Complex.I • K) * P = Matrix.diagonal d := by
  have hHs : (Matrix.toEuclideanLin H).IsSymmetric :=
    Matrix.isHermitian_iff_isSymmetric.mp hH
  have hKs : (Matrix.toEuclideanLin K).IsSymmetric :=
    Matrix.isHermitian_iff_isSymmetric.mp hK
  have hcomm : Commute (Matrix.toEuclideanLin H) (Matrix.toEuclideanLin K) := by
    show Matrix.toEuclideanLin H ∘ₗ Matrix.toEuclideanLin K =
      Matrix.toEuclideanLin K ∘ₗ Matrix.toEuclideanLin H
    ext v
    simp only [LinearMap.comp_apply, Matrix.toLpLin_apply, Matrix.mulVec_mulVec, hHK]

  have hInternal := hHs.directSum_isInternal_of_commute hKs hcomm
  have hOrthogonal := hHs.orthogonalFamily_eigenspace_inf_eigenspace hKs
  let W : Complex × Complex -> Submodule Complex (EuclideanSpace Complex n) :=
    fun p => eigenspace (Matrix.toEuclideanLin H) p.2 ⊓
      eigenspace (Matrix.toEuclideanLin K) p.1

  let Active := {p : Complex × Complex // W p ≠ ⊥}
  let eigenvalueEmbedding : Active ->
      Eigenvalues (Matrix.toEuclideanLin K) × Eigenvalues (Matrix.toEuclideanLin H) :=
    fun s =>
      (⟨s.1.1, hasEigenvalue_iff.mpr (ne_bot_of_le_ne_bot s.2 inf_le_right)⟩,
        ⟨s.1.2, hasEigenvalue_iff.mpr (ne_bot_of_le_ne_bot s.2 inf_le_left)⟩)
  have eigenvalueEmbedding_injective : Function.Injective eigenvalueEmbedding := by
    intro a b hab
    apply Subtype.ext
    exact Prod.ext (congrArg (fun z => z.1.1) hab) (congrArg (fun z => z.2.1) hab)
  letI : Finite Active := Finite.of_injective eigenvalueEmbedding eigenvalueEmbedding_injective
  letI : Fintype Active := Fintype.ofFinite Active

  have hActiveInternal : DirectSum.IsInternal (fun s : Active => W s.1) :=
    (hOrthogonal.comp Subtype.val_injective).isInternal_iff.mpr <| by
      rw [show (⨆ s : Active, W s.1) = ⨆ p, W p from iSup_ne_bot_subtype W]
      exact hOrthogonal.isInternal_iff.mp hInternal
  have hActiveOrthogonal :=
    hOrthogonal.comp (Subtype.val_injective (α := Complex × Complex) (p := fun p => W p ≠ ⊥))

  let b0 := hActiveInternal.subordinateOrthonormalBasis
    (finrank_euclideanSpace (ι := n)) hActiveOrthogonal
  let b := b0.reindex (Fintype.equivFin n).symm
  let eigenvalue : n -> Complex := fun j =>
    let jFin := Fintype.equivFin n j
    let component := hActiveInternal.subordinateOrthonormalBasisIndex
      (finrank_euclideanSpace (ι := n)) jFin hActiveOrthogonal
    component.1.2 + Complex.I * component.1.1
  let P := (EuclideanSpace.basisFun n Complex).toBasis.toMatrix b.toBasis
  have hP : P ∈ Matrix.unitaryGroup n Complex :=
    (EuclideanSpace.basisFun n Complex).toMatrix_orthonormalBasis_mem_unitary b
  refine ⟨P, hP, eigenvalue, ?_⟩

  have hEigenvector : forall j,
      Matrix.toEuclideanLin (H + Complex.I • K) (b j) = eigenvalue j • b j := by
    intro j
    let jFin := Fintype.equivFin n j
    let component := hActiveInternal.subordinateOrthonormalBasisIndex
      (finrank_euclideanSpace (ι := n)) jFin hActiveOrthogonal
    have hSubordinate := hActiveInternal.subordinateOrthonormalBasis_subordinate
      (finrank_euclideanSpace (ι := n)) jFin hActiveOrthogonal
    have hb : (b j : EuclideanSpace Complex n) = b0 jFin := by
      simp only [b, OrthonormalBasis.reindex_apply]
      congr 1
    have hbMem : (b0 jFin : EuclideanSpace Complex n) ∈ W component.1 := hSubordinate
    rw [Submodule.mem_inf] at hbMem
    have hHEigen := mem_eigenspace_iff.mp hbMem.1
    have hKEigen := mem_eigenspace_iff.mp hbMem.2
    rw [map_add, map_smul, LinearMap.add_apply, LinearMap.smul_apply, hb, hHEigen, hKEigen]
    simp only [eigenvalue, jFin, component, smul_smul, add_smul]

  have hMul : (H + Complex.I • K) * P = P * Matrix.diagonal eigenvalue := by
    apply Matrix.ext
    intro i j
    have hAtBasis := hEigenvector j
    rw [Matrix.toLpLin_apply] at hAtBasis
    have hEntry :
        ((H + Complex.I • K) *ᵥ (b j : EuclideanSpace Complex n).ofLp) i =
          eigenvalue j * (b j : EuclideanSpace Complex n).ofLp i := by
      have := congrFun (congrArg (fun x : EuclideanSpace Complex n => x.ofLp) hAtBasis) i
      simpa [Pi.smul_apply, smul_eq_mul] using this
    change ((H + Complex.I • K) *ᵥ (b j : EuclideanSpace Complex n).ofLp) i =
      ∑ x, (b x : EuclideanSpace Complex n).ofLp i *
        (if x = j then eigenvalue x else 0)
    rw [hEntry]
    simp [Finset.sum_ite_eq', Finset.mem_univ, mul_comm]
  calc
    star P * (H + Complex.I • K) * P = star P * ((H + Complex.I • K) * P) := by
      rw [Matrix.mul_assoc]
    _ = star P * (P * Matrix.diagonal eigenvalue) := by rw [hMul]
    _ = (star P * P) * Matrix.diagonal eigenvalue := by rw [← Matrix.mul_assoc]
    _ = 1 * Matrix.diagonal eigenvalue := by rw [Matrix.mem_unitaryGroup_iff'.mp hP]
    _ = Matrix.diagonal eigenvalue := Matrix.one_mul _

/-- Local placeholder-free implementation of the exact conjugated-diagonal anchor frozen by the
obligation registry. -/
theorem normalComplexConjugatedDiagonal : ExactConjugatedDiagonalAnchor.{u} := by
  intro n _ _ A hA
  let H : Matrix n n Complex := realPart A
  let K : Matrix n n Complex := imaginaryPart A
  have hH : H.IsHermitian := (realPart A).property
  have hK : K.IsHermitian := (imaginaryPart A).property
  have hDecomposition : A = H + Complex.I • K :=
    (realPart_add_I_smul_imaginaryPart A).symm
  have hCommute : H * K = K * H :=
    (isStarNormal_iff_commute_realPart_imaginaryPart.mp hA).eq
  obtain ⟨P, hP, d, hDiagonal⟩ :=
    commutingHermitianParts_conjugatedDiagonal H K hH hK hCommute
  exact ⟨P, hP, d, hDecomposition.symm ▸ hDiagonal⟩

/-- Exact frozen root, obtained from the locally implemented anchor through the previously checked
composition certificate. -/
theorem spectralTheorem_via_frozen_composition : SpectralTheoremTarget.{u} :=
  root_of_exactConjugatedDiagonalAnchor normalComplexConjugatedDiagonal

#print sorries commutingHermitianParts_conjugatedDiagonal
#print sorries normalComplexConjugatedDiagonal
#print sorries spectralTheorem_via_frozen_composition

#print axioms commutingHermitianParts_conjugatedDiagonal
#print axioms normalComplexConjugatedDiagonal
#print axioms spectralTheorem_via_frozen_composition

end Stage1Instances.THM_M_0043.Proof
