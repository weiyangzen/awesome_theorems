import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.FieldTheory.IntermediateField.Adjoin.Basic

/-!
# THM-M-0401 independent validation probe

This module reconstructs the one proof-phase leaf without importing or
invoking `Proof.lean`.  It deliberately leaves the Schmidt/Subspace-Theorem
root open.
-/

set_option autoImplicit false

noncomputable section

open scoped BigOperators

namespace Stage1Instances.THMM0401.Validation

def IsNearestIntegerDistance (x d : Real) : Prop :=
  0 <= d ∧
    ∃ m : Int,
      d = |x - (m : Real)| ∧
        ∀ z : Int, d <= |x - (z : Real)|

def ProductTooGood
    (n : Nat) (alpha : Fin n -> Real) (epsilon : Real) (q : Nat) : Prop :=
  0 < q ∧
    ∃ d : Fin n -> Real,
      (∀ i, IsNearestIntegerDistance ((q : Real) * alpha i) (d i)) ∧
        (∏ i, d i) < Real.rpow (q : Real) (-1 - epsilon)

/-- Independent reconstruction of the integer-point normalization leaf. -/
theorem independently_has_integer_point
    {n : Nat} {alpha : Fin n -> Real} {epsilon : Real} {q : Nat}
    (hq : ProductTooGood n alpha epsilon q) :
    ∃ (d : Fin n -> Real) (p : Fin n -> Int),
      0 < q ∧
        (∀ i,
          0 <= d i ∧
            d i = |(q : Real) * alpha i - (p i : Real)| ∧
              ∀ z : Int, d i <= |(q : Real) * alpha i - (z : Real)|) ∧
        (∏ i, d i) < Real.rpow (q : Real) (-1 - epsilon) := by
  rcases hq with ⟨hqpos, d, hd, hproduct⟩
  let p : Fin n -> Int := fun i => Classical.choose (hd i).2
  have hp (i : Fin n) :
      d i = |(q : Real) * alpha i - (p i : Real)| ∧
        ∀ z : Int, d i <= |(q : Real) * alpha i - (z : Real)| :=
    Classical.choose_spec (hd i).2
  exact ⟨d, p, hqpos, fun i => ⟨(hd i).1, hp i⟩, hproduct⟩

end Stage1Instances.THMM0401.Validation

#print axioms Stage1Instances.THMM0401.Validation.independently_has_integer_point
