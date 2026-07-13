import Statement
import SchurPort
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-0045 differential validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It reconstructs the exact
frozen root directly from the current-pin Schur construction. This is a separately written root
adapter in the same worker, not distinct-runner or release-grade independent evidence.
-/

noncomputable section

namespace Stage1Instances.THM_M_0045.Validation

open Stage1Instances.THM_M_0045

/-- A separate derivation of the exact frozen root from the local Schur terminal body. -/
theorem differentialSchurTriangularization : SchurTriangularizationTarget := by
  intro n A
  let U : Matrix (Fin n) (Fin n) Complex := A.schurTriangulationUnitary
  let T : Matrix (Fin n) (Fin n) Complex := A.schurTriangulation
  refine ⟨U, A.schurTriangulationUnitary.property, ?_⟩
  have hleft : star U * U = 1 :=
    Matrix.mem_unitaryGroup_iff'.mp A.schurTriangulationUnitary.property
  have hA : A = U * T * star U := A.schur_triangulation
  convert A.schurTriangulation.property using 1
  calc
    star U * A * U = star U * (U * T * star U) * U :=
      congrArg (fun B => star U * B * U) hA
    _ = (star U * U) * T * (star U * U) := by
      noncomm_ring
    _ = T := by rw [hleft, one_mul, mul_one]

assert_no_sorry Matrix.schur_triangulation
assert_no_sorry differentialSchurTriangularization

#check differentialSchurTriangularization
#print sorries Matrix.schur_triangulation
#print sorries differentialSchurTriangularization
#print axioms Matrix.schur_triangulation
#print axioms differentialSchurTriangularization

end Stage1Instances.THM_M_0045.Validation
