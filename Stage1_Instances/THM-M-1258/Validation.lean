import Statement
import Mathlib.LinearAlgebra.StdBasis

/-!
# THM-M-1258 independent local reconstruction

This module reconstructs the concrete coordinate-field witness without importing `Proof`. It is a
differential check in the same worker environment, not the distinct-runner independent evidence
required for release.
-/

noncomputable section

namespace Stage1Instances.THM_M_1258_Validation

open Stage1Instances.THM_M_1258

def validationZeroDrift (n : Nat) : Coefficients n := fun _ _ => 0

def validationCoordinateFields (n : Nat) : Fin n -> Coefficients n :=
  fun j i _ => if i = j then 1 else 0

theorem validationCoordinateFields_value (n : Nat) (j : Fin n) (x : Euclidean n) :
    asVectorField (validationCoordinateFields n j) x = Pi.basisFun Real (Fin n) j := by
  funext i
  simp [asVectorField, validationCoordinateFields, Pi.basisFun_apply, Pi.single_apply]

theorem independentlyReconstructed_coordinateCondition (n : Nat)
    (Omega : TopologicalSpace.Opens (Euclidean n)) :
    hormanderCondition Omega (validationZeroDrift n) (validationCoordinateFields n) := by
  intro x _hx
  apply (Submodule.eq_top_iff_forall_basis_mem (Pi.basisFun Real (Fin n))).mpr
  intro j
  apply Submodule.subset_span
  refine ⟨asVectorField (validationCoordinateFields n j), ?_,
    validationCoordinateFields_value n j x⟩
  exact GeneratedBracket.square j

#print axioms independentlyReconstructed_coordinateCondition

end Stage1Instances.THM_M_1258_Validation
