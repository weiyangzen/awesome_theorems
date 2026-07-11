import Statement

/-!
# THM-M-0402 proof execution

This module implements the projective-normalization leaves available from the
frozen S-unit representation and checks exact conditional composition into the
canonical root.  It does not postulate the missing S-unit finite-generation or
nondegenerate unit-equation theorem.
-/

set_option autoImplicit false

noncomputable section

open scoped BigOperators
open scoped NumberField
open IsDedekindDomain

namespace Stage1Instances.THMM0402

universe u

variable {K : Type u} [Field K] [NumberField K]

/-- Every coordinate of an S-unit tuple is nonzero in the ambient field. -/
theorem coordinateValue_ne_zero
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) {n : Nat}
    (x : SUnitTuple (K := K) S n) (i : Fin (n + 1)) :
    coordinateValue (K := K) S x i ≠ 0 := by
  exact Units.ne_zero (x i : Kˣ)

/-- Scale a tuple by the inverse of its coordinate zero. -/
def normalize
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) {n : Nat}
    (x : SUnitTuple (K := K) S n) : SUnitTuple (K := K) S n :=
  fun i => (x 0)⁻¹ * x i

/-- Normalization sets coordinate zero to one. -/
theorem coordinateValue_normalize_zero
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) {n : Nat}
    (x : SUnitTuple (K := K) S n) :
    coordinateValue (K := K) S (normalize (K := K) S x) 0 = 1 := by
  simp [coordinateValue, normalize]

/-- The ambient-field formula for every normalized coordinate. -/
theorem coordinateValue_normalize
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) {n : Nat}
    (x : SUnitTuple (K := K) S n) (i : Fin (n + 1)) :
    coordinateValue (K := K) S (normalize (K := K) S x) i =
      (coordinateValue (K := K) S x 0)⁻¹ *
        coordinateValue (K := K) S x i := by
  simp [coordinateValue, normalize]

/-- Normalization commutes with every finite coordinate sum by a nonzero
common scalar. -/
theorem coordinateSum_normalize
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) {n : Nat}
    (x : SUnitTuple (K := K) S n) (I : Finset (Fin (n + 1))) :
    coordinateSum (K := K) S (normalize (K := K) S x) I =
      (coordinateValue (K := K) S x 0)⁻¹ *
        coordinateSum (K := K) S x I := by
  simp only [coordinateSum, coordinateValue_normalize]
  rw [Finset.mul_sum]

/-- A coordinate sum vanishes before normalization exactly when it vanishes
after normalization. -/
theorem coordinateSum_normalize_eq_zero_iff
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) {n : Nat}
    (x : SUnitTuple (K := K) S n) (I : Finset (Fin (n + 1))) :
    coordinateSum (K := K) S (normalize (K := K) S x) I = 0 <->
      coordinateSum (K := K) S x I = 0 := by
  rw [coordinateSum_normalize]
  exact mul_eq_zero.trans (or_iff_right (inv_ne_zero (coordinateValue_ne_zero S x 0)))

/-- If a tuple already has coordinate zero equal to one, normalization leaves
it unchanged. -/
theorem normalize_eq_self
    (S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K))) {n : Nat}
    (x : SUnitTuple (K := K) S n)
    (hx : coordinateValue (K := K) S x 0 = 1) :
    normalize (K := K) S x = x := by
  funext i
  apply Subtype.ext
  apply Units.ext
  simpa [coordinateValue, normalize] using hx

/-- Exact binder-level composition for the frozen root.  The deep terminal
finiteness theorem remains an explicit premise rather than a local axiom. -/
theorem evertseSUnitStatement_of_finiteness
    (finiteness : ∀ (n : Nat), 0 < n ->
      ∀ S : Set (HeightOneSpectrum (NumberField.RingOfIntegers K)), S.Finite ->
        (NormalizedNondegenerateSolutions (K := K) S n).Finite) :
    EvertseSUnitStatement (K := K) := by
  intro n hn S hS
  exact finiteness n hn S hS

#print axioms coordinateValue_ne_zero
#print axioms coordinateValue_normalize_zero
#print axioms coordinateValue_normalize
#print axioms coordinateSum_normalize
#print axioms coordinateSum_normalize_eq_zero_iff
#print axioms normalize_eq_self
#print axioms evertseSUnitStatement_of_finiteness

end Stage1Instances.THMM0402
