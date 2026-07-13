import Mathlib.Analysis.InnerProductSpace.JointEigenspace
import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.LinearAlgebra.Complex.Module

/-!
# THM-M-0043 anchor-audit probes

This module checks the closest theorem and the principal composition anchors at the pinned mathlib
revision. The Hermitian adapter is deliberately a strict specialization of the frozen normal-matrix
target, not a proof of that target.
-/

namespace Stage1Instances.THM_M_0043_AnchorAudit

universe u

/-- The output shape of the root, restricted to the stronger Hermitian hypothesis. -/
def HermitianSpecializationTarget : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n] [Nonempty n]
      (A : Matrix n n Complex),
    A.IsHermitian ->
      exists (U : Matrix.unitaryGroup n Complex) (d : n -> Complex),
        A = (U : Matrix n n Complex) * Matrix.diagonal d * star (U : Matrix n n Complex)

/-- The stronger empty-index-inclusive statement shape supplied by the Atlas candidate. -/
def AtlasCandidateTarget : Prop :=
  forall (n : Type u) [Fintype n] [DecidableEq n] (A : Matrix n n Complex),
    IsStarNormal A ->
      exists (P : Matrix n n Complex) (_ : P ∈ Matrix.unitaryGroup n Complex)
        (d : n -> Complex),
        star P * A * P = Matrix.diagonal d

/-- The Atlas statement shape implies the exact frozen nonempty target equation. -/
theorem exactTarget_from_atlasCandidate (h : AtlasCandidateTarget.{u}) :
    forall (n : Type u) [Fintype n] [DecidableEq n] [Nonempty n]
        (A : Matrix n n Complex),
      IsStarNormal A ->
        exists (U : Matrix.unitaryGroup n Complex) (d : n -> Complex),
          A = (U : Matrix n n Complex) * Matrix.diagonal d * star (U : Matrix n n Complex) := by
  intro n _ _ _ A hA
  obtain ⟨P, hP, d, hDiagonal⟩ := h n A hA
  let U : Matrix.unitaryGroup n Complex := ⟨P, hP⟩
  refine ⟨U, d, ?_⟩
  calc
    A = (1 : Matrix n n Complex) * A * 1 := by simp
    _ = (P * star P) * A * (P * star P) := by rw [Matrix.mem_unitaryGroup_iff.mp hP]
    _ = P * (star P * A * P) * star P := by simp only [mul_assoc]
    _ = P * Matrix.diagonal d * star P := by rw [hDiagonal]

/-- Checked output-shape adapter from mathlib's Hermitian spectral theorem. -/
theorem hermitianSpecialization_from_mathlib : HermitianSpecializationTarget.{u} := by
  intro n _ _ _ A hA
  refine ⟨hA.eigenvectorUnitary, fun i => (hA.eigenvalues i : Complex), ?_⟩
  simpa only [Unitary.conjStarAlgAut_apply, Function.comp_apply] using hA.spectral_theorem

/-- A one-dimensional normal complex matrix need not be Hermitian. -/
theorem normal_not_implies_hermitian :
    exists A : Matrix Unit Unit Complex, IsStarNormal A /\ Not A.IsHermitian := by
  let A : Matrix Unit Unit Complex := fun _ _ => Complex.I
  refine ⟨A, ?_, ?_⟩
  · constructor
    ext
    simp [A, Matrix.mul_apply]
  · intro hA
    have hEntry := congr_fun (congr_fun hA Unit.unit) Unit.unit
    change star Complex.I = Complex.I at hEntry
    norm_num [Complex.ext_iff] at hEntry

#check Matrix.IsHermitian.spectral_theorem
#check Matrix.IsHermitian.eigenvectorUnitary
#check Unitary.conjStarAlgAut_apply
#check isStarNormal_iff_commute_realPart_imaginaryPart
#check LinearMap.IsSymmetric.directSum_isInternal_of_commute
#check LinearMap.IsSymmetric.iSup_iInf_eq_top_of_commute
#check DirectSum.IsInternal.subordinateOrthonormalBasis
#check OrthonormalBasis.toMatrix_orthonormalBasis_mem_unitary

#print Matrix.IsHermitian.spectral_theorem
#print axioms Matrix.IsHermitian.spectral_theorem
#print axioms exactTarget_from_atlasCandidate
#print axioms hermitianSpecialization_from_mathlib
#print axioms normal_not_implies_hermitian

end Stage1Instances.THM_M_0043_AnchorAudit
