import Mathlib.Algebra.Polynomial.AlgebraMap
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-!
# THM-M-0041 canonical Lean statement

This module freezes the finite square-matrix Cayley-Hamilton statement selected at intake. The
characteristic polynomial is written out as `det (X I - A)`, so the statement does not import the
mathlib module that contains `Matrix.aeval_self_charpoly` and its proof.
-/

namespace Stage1Instances.THM_M_0041

universe u v

noncomputable section

/-- The characteristic polynomial, expanded as the determinant of `X I - A`. -/
def characteristicPolynomial {R : Type u} [CommRing R]
    {n : Type v} [DecidableEq n] [Fintype n] (A : Matrix n n R) : Polynomial R :=
  Matrix.det (Matrix.scalar n Polynomial.X - A.map Polynomial.C)

/-- Every finite square matrix over a commutative ring is annihilated by `det (X I - A)`. -/
def CayleyHamiltonTarget : Prop :=
  forall {R : Type u} [CommRing R] {n : Type v} [DecidableEq n] [Fintype n]
      (A : Matrix n n R),
    Polynomial.aeval A (characteristicPolynomial A) = 0

/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

/-- Specialize the coefficient domain from arbitrary commutative rings to fields. -/
def mutationChangedDomainToField : Prop :=
  forall {K : Type u} [Field K] {n : Type v} [DecidableEq n] [Fintype n]
      (A : Matrix n n K),
    Polynomial.aeval A (characteristicPolynomial A) = 0

/-- Change the matrix binder from universal to existential. -/
def mutationChangedMatrixBinderScope : Prop :=
  forall {R : Type u} [CommRing R] {n : Type v} [DecidableEq n] [Fintype n],
    exists A : Matrix n n R,
      Polynomial.aeval A (characteristicPolynomial A) = 0

/-- Exclude both intake-selected boundary classes: empty index types and zero rings. -/
def mutationExcludedBoundaries : Prop :=
  forall {R : Type u} [CommRing R] [Nontrivial R]
      {n : Type v} [DecidableEq n] [Fintype n] [Nonempty n]
      (A : Matrix n n R),
    Polynomial.aeval A (characteristicPolynomial A) = 0

#check_failure (rfl : CayleyHamiltonTarget.{u, v} = mutationChangedDomainToField.{u, v})
#check_failure (rfl : CayleyHamiltonTarget.{u, v} = mutationChangedMatrixBinderScope.{u, v})
#check_failure (rfl : CayleyHamiltonTarget.{u, v} = mutationExcludedBoundaries.{u, v})

#check_failure Matrix.charpoly
#check_failure Matrix.aeval_self_charpoly

end

end Stage1Instances.THM_M_0041

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0041.CayleyHamiltonTarget
