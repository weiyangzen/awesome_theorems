import Mathlib.LinearAlgebra.QuadraticForm.Radical
import Mathlib.LinearAlgebra.QuadraticForm.TensorProduct
import Mathlib.NumberTheory.NumberField.Completion.FinitePlace
import Mathlib.NumberTheory.NumberField.Completion.InfinitePlace

/-!
# Exact statement for THM-M-0423

The target is the Hasse-Minkowski local-global isotropy theorem.  Both finite
and infinite places occur explicitly.  This file freezes and elaborates only
the proposition; it does not assert or prove it.
-/

noncomputable section

namespace Stage1.THM_M_0423

universe u v

/-- A quadratic form has a nonzero isotropic vector. -/
def IsIsotropic {K : Type u} {V : Type v} [CommRing K] [AddCommGroup V] [Module K V]
    (Q : QuadraticForm K V) : Prop :=
  ∃ x : V, x ≠ 0 ∧ Q x = 0

/-- Isotropy after scalar extension from `K` to a commutative `K`-algebra `A`. -/
def IsIsotropicAfterBaseChange
    {K : Type u} {V : Type v} [Field K] [CharZero K] [AddCommGroup V] [Module K V]
    (Q : QuadraticForm K V) (A : Type*) [Field A] [Algebra K A] [CharZero A] : Prop :=
  letI : Invertible (2 : A) := invertibleOfNonzero (by norm_num)
  IsIsotropic (Q.baseChange A)

/-- Isotropy at every nonarchimedean completion of a number field. -/
def IsIsotropicAtEveryFinitePlace
    {K : Type u} {V : Type v} [Field K] [NumberField K]
    [AddCommGroup V] [Module K V] (Q : QuadraticForm K V) : Prop :=
  ∀ w : NumberField.FinitePlace K,
    letI : CharZero ((NumberField.FinitePlace.maximalIdeal w).adicCompletion K) :=
      charZero_of_injective_algebraMap (algebraMap K _).injective
    IsIsotropicAfterBaseChange Q
      ((NumberField.FinitePlace.maximalIdeal w).adicCompletion K)

/-- Isotropy at every archimedean completion of a number field. -/
def IsIsotropicAtEveryInfinitePlace
    {K : Type u} {V : Type v} [Field K] [NumberField K]
    [AddCommGroup V] [Module K V] (Q : QuadraticForm K V) : Prop :=
  ∀ w : NumberField.InfinitePlace K,
    letI : CharZero w.Completion :=
      charZero_of_injective_algebraMap (algebraMap K _).injective
    IsIsotropicAfterBaseChange Q w.Completion

/--
The exact coordinate-free Hasse-Minkowski target: a nondegenerate quadratic
form on a finite-dimensional vector space over a number field is isotropic
globally exactly when it is isotropic over every finite and infinite
completion.
-/
def HasseMinkowskiStatement : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K]
    (V : Type v) [AddCommGroup V] [Module K V] [FiniteDimensional K V]
    (Q : QuadraticForm K V),
    Q.Nondegenerate →
      (IsIsotropic Q ↔
        IsIsotropicAtEveryFinitePlace Q ∧ IsIsotropicAtEveryInfinitePlace Q)

#print HasseMinkowskiStatement

end Stage1.THM_M_0423
