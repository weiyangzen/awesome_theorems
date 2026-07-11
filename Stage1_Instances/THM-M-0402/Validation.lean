import Statement

/-!
# THM-M-0402 independent validation probe

This module reconstructs the proof phase's normalization results without
importing or invoking `Proof.lean`. The unavailable S-unit finiteness theorem
and the exact Evertse root deliberately remain open.
-/

set_option autoImplicit false

noncomputable section

open scoped BigOperators
open scoped NumberField
open IsDedekindDomain

namespace Stage1Instances.THMM0402.Validation

universe u

variable {K : Type u} [Field K] [NumberField K]

def independentlyNormalize
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) {n : Nat}
    (x : SUnitTuple (K := K) S n) : SUnitTuple (K := K) S n :=
  fun i => (x 0)⁻¹ * x i

theorem independently_coordinateValue_ne_zero
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) {n : Nat}
    (x : SUnitTuple (K := K) S n) (i : Fin (n + 1)) :
    coordinateValue (K := K) S x i ≠ 0 := by
  exact Units.ne_zero (x i : Kˣ)

theorem independently_normalize_zero
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) {n : Nat}
    (x : SUnitTuple (K := K) S n) :
    coordinateValue (K := K) S (independentlyNormalize (K := K) S x) 0 = 1 := by
  simp [coordinateValue, independentlyNormalize]

theorem independently_coordinate_value
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) {n : Nat}
    (x : SUnitTuple (K := K) S n) (i : Fin (n + 1)) :
    coordinateValue (K := K) S (independentlyNormalize (K := K) S x) i =
      (coordinateValue (K := K) S x 0)⁻¹ * coordinateValue (K := K) S x i := by
  simp [coordinateValue, independentlyNormalize]

theorem independently_coordinate_sum
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) {n : Nat}
    (x : SUnitTuple (K := K) S n) (I : Finset (Fin (n + 1))) :
    coordinateSum (K := K) S (independentlyNormalize (K := K) S x) I =
      (coordinateValue (K := K) S x 0)⁻¹ * coordinateSum (K := K) S x I := by
  simp only [coordinateSum, independently_coordinate_value]
  rw [Finset.mul_sum]

theorem independently_coordinate_sum_eq_zero_iff
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) {n : Nat}
    (x : SUnitTuple (K := K) S n) (I : Finset (Fin (n + 1))) :
    coordinateSum (K := K) S (independentlyNormalize (K := K) S x) I = 0 ↔
      coordinateSum (K := K) S x I = 0 := by
  rw [independently_coordinate_sum]
  exact mul_eq_zero.trans
    (or_iff_right (inv_ne_zero (independently_coordinateValue_ne_zero S x 0)))

/-- Independent binder-level check of the conditional root composition. -/
theorem independently_root_of_finiteness
    (finiteness : ∀ (n : Nat), 0 < n ->
      ∀ S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K)), S.Finite ->
        (NormalizedNondegenerateSolutions (K := K) S n).Finite) :
    EvertseSUnitStatement (K := K) := by
  intro n hn S hS
  exact finiteness n hn S hS

end Stage1Instances.THMM0402.Validation

#print axioms Stage1Instances.THMM0402.Validation.independently_coordinateValue_ne_zero
#print axioms Stage1Instances.THMM0402.Validation.independently_normalize_zero
#print axioms Stage1Instances.THMM0402.Validation.independently_coordinate_value
#print axioms Stage1Instances.THMM0402.Validation.independently_coordinate_sum
#print axioms Stage1Instances.THMM0402.Validation.independently_coordinate_sum_eq_zero_iff
#print axioms Stage1Instances.THMM0402.Validation.independently_root_of_finiteness
