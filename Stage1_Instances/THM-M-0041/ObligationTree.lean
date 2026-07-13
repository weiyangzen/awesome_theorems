import Statement
import Mathlib.LinearAlgebra.Matrix.Charpoly.Basic

/-!
# THM-M-0041 conditional obligation composition

This module checks the child-to-parent interfaces frozen by the obligation registry. The central
matrix identity, polynomial-matrix transport, evaluation, and scalar-evaluation steps remain
explicit premises. Consequently, these declarations validate composition but do not install the
audited mathlib candidate as the canonical proof.
-/

namespace Stage1Instances.THM_M_0041.ObligationTree

open Matrix Polynomial

universe u v

noncomputable section

/-- The exact definitional bridge from the expanded determinant to mathlib's characteristic
polynomial. -/
def CharacteristicPolynomialTransport : Prop :=
  forall {R : Type u} [CommRing R] {n : Type v} [DecidableEq n] [Fintype n]
      (A : Matrix n n R),
    Stage1Instances.THM_M_0041.characteristicPolynomial A = Matrix.charpoly A

/-- The frozen expanded definition and mathlib definition agree by reduction. -/
theorem characteristicPolynomialTransport : CharacteristicPolynomialTransport.{u, v} := by
  intro R _ n _ _ A
  rfl

/-- Output of the adjugate construction in the pinned proof architecture. -/
def AdjugateIdentityOutput {R : Type u} [CommRing R]
    {n : Type v} [DecidableEq n] [Fintype n] (A : Matrix n n R) : Prop :=
  A.charpoly • (1 : Matrix n n (Polynomial R)) =
    Matrix.adjugate A.charmatrix * A.charmatrix

/-- The adjugate identity child, kept as an explicit imported-theorem boundary. -/
def AdjugateIdentityEngine : Prop :=
  forall {R : Type u} [CommRing R] {n : Type v} [DecidableEq n] [Fintype n]
      (A : Matrix n n R),
    AdjugateIdentityOutput A

/-- Output after moving the adjugate identity into polynomials of matrices. -/
def MatrixPolynomialIdentityOutput {R : Type u} [CommRing R]
    {n : Type v} [DecidableEq n] [Fintype n] (A : Matrix n n R) : Prop :=
  matPolyEquiv (A.charpoly • (1 : Matrix n n (Polynomial R))) =
    matPolyEquiv (Matrix.adjugate A.charmatrix * A.charmatrix)

/-- Representation-normalization interface supplied by `matPolyEquiv` and its charmatrix lemma. -/
def MatrixPolynomialTransportEngine : Prop :=
  forall {R : Type u} [CommRing R] {n : Type v} [DecidableEq n] [Fintype n]
      (A : Matrix n n R),
    AdjugateIdentityOutput A -> MatrixPolynomialIdentityOutput A

/-- Output after evaluating the polynomial identity at the matrix and killing the right factor. -/
def EvaluatedIdentityOutput {R : Type u} [CommRing R]
    {n : Type v} [DecidableEq n] [Fintype n] (A : Matrix n n R) : Prop :=
  Polynomial.eval A
      (matPolyEquiv (A.charpoly • (1 : Matrix n n (Polynomial R)))) = 0

/-- Evaluation interface whose central imported lemma is `Polynomial.eval_mul_X_sub_C`. -/
def RightFactorEvaluationEngine : Prop :=
  forall {R : Type u} [CommRing R] {n : Type v} [DecidableEq n] [Fintype n]
      (A : Matrix n n R),
    MatrixPolynomialIdentityOutput A -> EvaluatedIdentityOutput A

/-- Final scalar/evaluation transport back to the ordinary matrix characteristic polynomial. -/
def ScalarEvaluationTransportEngine : Prop :=
  forall {R : Type u} [CommRing R] {n : Type v} [DecidableEq n] [Fintype n]
      (A : Matrix n n R),
    EvaluatedIdentityOutput A -> Polynomial.aeval A A.charpoly = 0

/-- Exact matrix-level Cayley-Hamilton interface exported by the audited candidate route. -/
def MatrixCayleyHamiltonEngine : Prop :=
  forall {R : Type u} [CommRing R] {n : Type v} [DecidableEq n] [Fintype n]
      (A : Matrix n n R),
    Polynomial.aeval A A.charpoly = 0

/-- Checked composition of the four visible proof-body stages. Every child is consumed. -/
theorem matrixCayleyHamilton_of_engines
    (adjugateIdentity : AdjugateIdentityEngine.{u, v})
    (matrixPolynomialTransport : MatrixPolynomialTransportEngine.{u, v})
    (rightFactorEvaluation : RightFactorEvaluationEngine.{u, v})
    (scalarEvaluationTransport : ScalarEvaluationTransportEngine.{u, v}) :
    MatrixCayleyHamiltonEngine.{u, v} := by
  intro R _ n _ _ A
  exact scalarEvaluationTransport A
    (rightFactorEvaluation A
      (matrixPolynomialTransport A (adjugateIdentity A)))

/-- Checked final composition into the exact frozen target. Both children are consumed. -/
theorem root_of_characteristicPolynomialTransport_and_matrixCayleyHamilton
    (characteristicPolynomialTransport : CharacteristicPolynomialTransport.{u, v})
    (matrixCayleyHamilton : MatrixCayleyHamiltonEngine.{u, v}) :
    Stage1Instances.THM_M_0041.CayleyHamiltonTarget.{u, v} := by
  intro R _ n _ _ A
  rw [characteristicPolynomialTransport A]
  exact matrixCayleyHamilton A

#check Matrix.adjugate_mul
#check matPolyEquiv
#check Matrix.matPolyEquiv_charmatrix
#check Polynomial.eval_mul_X_sub_C
#check matPolyEquiv_smul_one
#check Polynomial.eval_map

#print axioms matrixCayleyHamilton_of_engines
#print axioms characteristicPolynomialTransport
#print axioms root_of_characteristicPolynomialTransport_and_matrixCayleyHamilton

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0041.CayleyHamiltonTarget

end

end Stage1Instances.THM_M_0041.ObligationTree
