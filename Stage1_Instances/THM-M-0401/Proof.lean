import Mathlib.Analysis.SpecialFunctions.Pow.Real
import Mathlib.FieldTheory.IntermediateField.Adjoin.Basic

/-!
# THM-M-0401 proof work

This file implements the normalization leaf that extracts the integer
coordinates hidden in `ProductTooGood`.  It deliberately does not postulate
the missing Subspace Theorem bridge.
-/

set_option autoImplicit false

noncomputable section

open scoped BigOperators

namespace Stage1Instances.THMM0401

/- These definitions mirror the checked definitions in `Statement.lean`.
`check_proof.sh` elaborates both files independently because Lean refuses to
emit an `.olean` for a source outside the Lake package root. -/
def AlgebraicVector (n : Nat) (alpha : Fin n -> Real) : Prop :=
  forall i, IsAlgebraic Rat (alpha i)

def RationalIndependenceWithOne (n : Nat) (alpha : Fin n -> Real) : Prop :=
  LinearIndependent Rat (fun j : Option (Fin n) =>
    match j with
    | none => (1 : Real)
    | some i => alpha i)

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

/-- An exceptional denominator supplies one nearest integer in every coordinate. -/
theorem productTooGood_has_integer_point
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
  choose p hp using fun i => (hd i).2
  exact ⟨d, p, hqpos, fun i => ⟨(hd i).1, hp i⟩, hproduct⟩

end Stage1Instances.THMM0401

#print axioms Stage1Instances.THMM0401.productTooGood_has_integer_point
