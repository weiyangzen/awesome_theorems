import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Block
import Mathlib.LinearAlgebra.UnitaryGroup

/-!
# THM-M-0045 canonical Lean statement

This module freezes the finite complex square-matrix form of Schur triangularization selected from
Axler's upper-triangular operator/orthonormal-basis statement. It defines the target and statement
mutations, but contains no proof of Schur triangularization.
-/

namespace Stage1Instances.THM_M_0045

/-- Every finite complex square matrix is unitarily similar to an upper triangular matrix. -/
def SchurTriangularizationTarget : Prop :=
  forall (n : Nat) (A : Matrix (Fin n) (Fin n) Complex),
    exists U : Matrix (Fin n) (Fin n) Complex,
      U ∈ Matrix.unitaryGroup (Fin n) Complex ∧
        Matrix.BlockTriangular (star U * A * U) id

/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

/-- Remove the unitary requirement on the change-of-basis matrix. -/
def mutationRemovedUnitarity : Prop :=
  forall (n : Nat) (A : Matrix (Fin n) (Fin n) Complex),
    exists U : Matrix (Fin n) (Fin n) Complex,
      Matrix.BlockTriangular (star U * A * U) id

/-- Change the scalar domain from complex to rational matrices. -/
def mutationChangedDomainToRational : Prop :=
  forall (n : Nat) (A : Matrix (Fin n) (Fin n) Rat),
    exists U : Matrix (Fin n) (Fin n) Rat,
      U ∈ Matrix.unitaryGroup (Fin n) Rat ∧
        Matrix.BlockTriangular (star U * A * U) id

/-- Change the matrix binder from universal to existential. -/
def mutationChangedMatrixBinderScope : Prop :=
  forall (n : Nat),
    exists A U : Matrix (Fin n) (Fin n) Complex,
      U ∈ Matrix.unitaryGroup (Fin n) Complex ∧
        Matrix.BlockTriangular (star U * A * U) id

/-- Exclude the zero-dimensional boundary case. -/
def mutationExcludedZeroDimension : Prop :=
  forall (n : Nat), 0 < n → forall (A : Matrix (Fin n) (Fin n) Complex),
    exists U : Matrix (Fin n) (Fin n) Complex,
      U ∈ Matrix.unitaryGroup (Fin n) Complex ∧
        Matrix.BlockTriangular (star U * A * U) id

variable (hRemoved : mutationRemovedUnitarity)
#check_failure (show SchurTriangularizationTarget from hRemoved)

variable (hDomain : mutationChangedDomainToRational)
#check_failure (show SchurTriangularizationTarget from hDomain)

variable (hScope : mutationChangedMatrixBinderScope)
#check_failure (show SchurTriangularizationTarget from hScope)

variable (hBoundary : mutationExcludedZeroDimension)
#check_failure (show SchurTriangularizationTarget from hBoundary)

set_option pp.universes true in
set_option pp.explicit true in
#print SchurTriangularizationTarget

end Stage1Instances.THM_M_0045
