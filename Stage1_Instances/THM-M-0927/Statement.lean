import Mathlib.Data.Nat.Fib.Basic
import Mathlib.Data.Real.Sqrt

/-!
# THM-M-0927 canonical Lean statement

This module freezes the zero-based, natural-index radical formula printed by
NIST DLMF 26.11.7. It contains checked statement transports, mutation
fixtures, and boundary checks, but no proof of the canonical target.
-/

noncomputable section

namespace Stage1Instances.THM_M_0927

/-- The exact DLMF 26.11.7 source spelling of Binet's formula. -/
def BinetFormulaTarget : Prop :=
  forall n : Nat,
    (Nat.fib n : Real) =
      ((1 + Real.sqrt 5) ^ n - (1 - Real.sqrt 5) ^ n) /
        ((2 : Real) ^ n * Real.sqrt 5)

/-- The positive characteristic root `(1 + sqrt 5) / 2`. -/
def positiveRoot : Real :=
  (1 + Real.sqrt 5) / 2

/-- The conjugate characteristic root `(1 - sqrt 5) / 2`. -/
def conjugateRoot : Real :=
  (1 - Real.sqrt 5) / 2

/-- The usual named-root spelling of the same natural-index formula. -/
def CharacteristicRootTarget : Prop :=
  forall n : Nat,
    (Nat.fib n : Real) =
      (positiveRoot ^ n - conjugateRoot ^ n) / Real.sqrt 5

/-- The same source formula represented as an equality of functions. -/
def FunctionEqualityTarget : Prop :=
  (fun n : Nat => (Nat.fib n : Real)) =
    fun n : Nat =>
      ((1 + Real.sqrt 5) ^ n - (1 - Real.sqrt 5) ^ n) /
        ((2 : Real) ^ n * Real.sqrt 5)

/-- Checked transport between the pointwise and function-equality forms. -/
theorem binetFormulaTarget_iff_functionEqualityTarget :
    BinetFormulaTarget <-> FunctionEqualityTarget := by
  constructor
  · exact fun h => funext h
  · exact fun h n => congrFun h n

/-- Checked algebraic transport from the source radical spelling to the
characteristic-root spelling. -/
theorem binetFormulaTarget_iff_characteristicRootTarget :
    BinetFormulaTarget <-> CharacteristicRootTarget := by
  have normalized (n : Nat) :
      ((positiveRoot ^ n - conjugateRoot ^ n) / Real.sqrt 5) =
        ((1 + Real.sqrt 5) ^ n - (1 - Real.sqrt 5) ^ n) /
          ((2 : Real) ^ n * Real.sqrt 5) := by
    simp only [positiveRoot, conjugateRoot, div_pow]
    ring
  constructor <;> intro h n
  · rw [h n, normalized n]
  · rw [h n, normalized n]

/-! Structural mutations elaborate but receive no statement-identity credit. -/

/-- Removed-contract mutation: omit the conjugate-root contribution. The
source proposition has no standalone hypothesis, so this tests deletion of a
required conclusion term rather than removal of an antecedent. -/
def mutationRemovedConjugateContribution : Prop :=
  forall n : Nat,
    (Nat.fib n : Real) =
      (1 + Real.sqrt 5) ^ n / ((2 : Real) ^ n * Real.sqrt 5)

/-- Changed-domain mutation: quantify only over the first ten indices. -/
def mutationChangedDomainToFinTen : Prop :=
  forall n : Fin 10,
    (Nat.fib n : Real) =
      ((1 + Real.sqrt 5) ^ (n : Nat) -
          (1 - Real.sqrt 5) ^ (n : Nat)) /
        ((2 : Real) ^ (n : Nat) * Real.sqrt 5)

/-- Changed-binder-scope mutation: assert the formula at some index rather
than at every nonnegative index. -/
def mutationChangedBinderScope : Prop :=
  exists n : Nat,
    (Nat.fib n : Real) =
      ((1 + Real.sqrt 5) ^ n - (1 - Real.sqrt 5) ^ n) /
        ((2 : Real) ^ n * Real.sqrt 5)

/-- Boundary mutation: exclude the source-admitted index zero. -/
def mutationExcludesZeroIndex : Prop :=
  forall n : Nat, 1 <= n ->
    (Nat.fib n : Real) =
      ((1 + Real.sqrt 5) ^ n - (1 - Real.sqrt 5) ^ n) /
        ((2 : Real) ^ n * Real.sqrt 5)

variable
  (hRemoved : mutationRemovedConjugateContribution)
  (hDomain : mutationChangedDomainToFinTen)
  (hScope : mutationChangedBinderScope)
  (hBoundary : mutationExcludesZeroIndex)

#check_failure (show BinetFormulaTarget from hRemoved)
#check_failure (show BinetFormulaTarget from hDomain)
#check_failure (show BinetFormulaTarget from hScope)
#check_failure (show BinetFormulaTarget from hBoundary)

/-! Boundary witnesses inspect the encoding without proving the root target. -/

/-- Index zero is included and the displayed equality reduces to `0 = 0`. -/
theorem zero_index_formula :
    (Nat.fib 0 : Real) =
      ((1 + Real.sqrt 5) ^ 0 - (1 - Real.sqrt 5) ^ 0) /
        ((2 : Real) ^ 0 * Real.sqrt 5) := by
  simp

/-- Deleting the conjugate contribution makes the proposed universal formula
false at the included index zero. -/
theorem removed_conjugate_mutation_is_false :
    Not mutationRemovedConjugateContribution := by
  intro h
  have h0 := h 0
  norm_num at h0
  have hp : (0 : Real) < Real.sqrt 5 :=
    Real.sqrt_pos.2 (by norm_num)
  linarith

/-- The denominator's square-root factor is nonzero. -/
theorem sqrt_five_ne_zero : Real.sqrt 5 ≠ 0 := by
  exact (Real.sqrt_pos.2 (show (0 : Real) < 5 by norm_num)).ne'

/-- Index one is included and satisfies the displayed boundary equation. -/
theorem one_index_formula :
    (Nat.fib 1 : Real) =
      ((1 + Real.sqrt 5) ^ 1 - (1 - Real.sqrt 5) ^ 1) /
        ((2 : Real) ^ 1 * Real.sqrt 5) := by
  norm_num [Nat.fib]
  field_simp [sqrt_five_ne_zero]
  ring

/-- The finite-domain mutation omits the canonical index ten. -/
theorem ten_has_no_fin_ten_representation :
    Not (Exists fun n : Fin 10 => (n : Nat) = 10) := by
  rintro ⟨n, hn⟩
  exact (Nat.ne_of_lt n.isLt) hn

#print axioms binetFormulaTarget_iff_functionEqualityTarget
#print axioms binetFormulaTarget_iff_characteristicRootTarget
#print axioms zero_index_formula
#print axioms removed_conjugate_mutation_is_false
#print axioms sqrt_five_ne_zero
#print axioms one_index_formula
#print axioms ten_has_no_fin_ten_representation

set_option pp.universes true in
set_option pp.explicit true in
#print BinetFormulaTarget

end Stage1Instances.THM_M_0927
