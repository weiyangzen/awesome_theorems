import ObligationTree

/-!
# THM-M-0041 proof execution

This module installs the exact pinned matrix Cayley-Hamilton theorem at the frozen target. It also
replays the four visible stages of the upstream proof through the interfaces fixed by the
obligation tree, so the local root composition is checked rather than inferred from theorem names.
-/

namespace Stage1Instances.THM_M_0041.Proof

open Matrix Polynomial
open Stage1Instances.THM_M_0041
open Stage1Instances.THM_M_0041.ObligationTree

universe u v

noncomputable section

/-- The adjugate identity used by the pinned terminal proof body. -/
theorem adjugateIdentity : AdjugateIdentityEngine.{u, v} := by
  intro R _ n _ _ A
  exact (Matrix.adjugate_mul A.charmatrix).symm

/-- Move the adjugate identity from matrices of polynomials to polynomials of matrices. -/
theorem matrixPolynomialTransport : MatrixPolynomialTransportEngine.{u, v} := by
  intro R _ n _ _ A h
  exact congrArg matPolyEquiv h

/-- Evaluate the normalized identity and annihilate its right factor at `A`. -/
theorem rightFactorEvaluation : RightFactorEvaluationEngine.{u, v} := by
  intro R _ n _ _ A h
  change matPolyEquiv (A.charpoly • (1 : Matrix n n (Polynomial R))) =
    matPolyEquiv (Matrix.adjugate A.charmatrix * A.charmatrix) at h
  apply_fun fun p => p.eval A at h
  rw [map_mul, Matrix.matPolyEquiv_charmatrix, Polynomial.eval_mul_X_sub_C] at h
  exact h

/-- Convert the evaluated scalar-matrix polynomial back to ordinary algebra evaluation. -/
theorem scalarEvaluationTransport : ScalarEvaluationTransportEngine.{u, v} := by
  intro R _ n _ _ A h
  change Polynomial.eval A
    (matPolyEquiv (A.charpoly • (1 : Matrix n n (Polynomial R)))) = 0 at h
  rw [matPolyEquiv_smul_one, Polynomial.eval_map] at h
  exact h

/-- Local checked replay of the visible upstream proof architecture. -/
theorem matrixCayleyHamiltonExpanded : MatrixCayleyHamiltonEngine.{u, v} :=
  matrixCayleyHamilton_of_engines adjugateIdentity matrixPolynomialTransport
    rightFactorEvaluation scalarEvaluationTransport

/-- Exact checked wrapper around the terminal body at the pinned mathlib revision. -/
theorem pinnedMatrixCayleyHamilton : MatrixCayleyHamiltonEngine.{u, v} := by
  intro R _ n _ _ A
  exact Matrix.aeval_self_charpoly A

/-- The frozen target composed from its two required proof children. -/
theorem cayleyHamilton : CayleyHamiltonTarget.{u, v} :=
  root_of_characteristicPolynomialTransport_and_matrixCayleyHamilton
    characteristicPolynomialTransport pinnedMatrixCayleyHamilton

/-- Corroborating root closure through the locally expanded proof architecture. -/
theorem cayleyHamiltonExpanded : CayleyHamiltonTarget.{u, v} :=
  root_of_characteristicPolynomialTransport_and_matrixCayleyHamilton
    characteristicPolynomialTransport matrixCayleyHamiltonExpanded

#print axioms adjugateIdentity
#print axioms matrixPolynomialTransport
#print axioms rightFactorEvaluation
#print axioms scalarEvaluationTransport
#print axioms matrixCayleyHamiltonExpanded
#print axioms pinnedMatrixCayleyHamilton
#print axioms cayleyHamilton
#print axioms cayleyHamiltonExpanded
#print axioms Matrix.aeval_self_charpoly

end


end Stage1Instances.THM_M_0041.Proof
