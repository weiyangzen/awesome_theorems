import Mathlib.Analysis.InnerProductSpace.GramSchmidtOrtho
import Mathlib.Analysis.Matrix.Spectrum
import Mathlib.LinearAlgebra.Eigenspace.Triangularizable

/-!
# THM-M-0045 pinned anchor audit

The checked declarations below are the complete retained interface inventory at pinned mathlib
revision `8a178386ffc0f5fef0b77738bb5449d50efeea95`. None states Schur triangularization. The adapter
lemma records the exact bridge that an external `A = U * T * star U` candidate must satisfy; it
does not construct `U` or `T`.
-/

namespace Stage1Instances.THM_M_0045.AnchorAudit

#check Module.End.exists_eigenvalue
#check Module.End.iSup_maxGenEigenspace_eq_top
#check InnerProductSpace.gramSchmidtOrthonormalBasis_inv_blockTriangular
#check OrthonormalBasis.toMatrix_orthonormalBasis_mem_unitary
#check Matrix.IsHermitian.spectral_theorem
#check Matrix.BlockTriangular
#check Matrix.unitaryGroup

/-- Checked statement adapter for the equation form used by the immutable external candidate. -/
theorem equationCandidate_implies_targetAt {n : Nat} {A U T : Matrix (Fin n) (Fin n) Complex}
    (hU : U ∈ Matrix.unitaryGroup (Fin n) Complex)
    (hT : Matrix.BlockTriangular T id) (hA : A = U * T * star U) :
    Matrix.BlockTriangular (star U * A * U) id := by
  have hleft : star U * U = 1 := Matrix.mem_unitaryGroup_iff'.mp hU
  convert hT using 1
  calc
    star U * A * U = (star U * U) * T * (star U * U) := by
      rw [hA]
      noncomm_ring
    _ = T := by rw [hleft, one_mul, mul_one]

#print axioms Module.End.exists_eigenvalue
#print axioms Module.End.iSup_maxGenEigenspace_eq_top
#print axioms InnerProductSpace.gramSchmidtOrthonormalBasis_inv_blockTriangular
#print axioms OrthonormalBasis.toMatrix_orthonormalBasis_mem_unitary
#print axioms Matrix.IsHermitian.spectral_theorem
#print axioms equationCandidate_implies_targetAt

end Stage1Instances.THM_M_0045.AnchorAudit
