import Mathlib.NumberTheory.Pell

/-!
# THM-M-0388 proof closure

This module pins the terminal proof body to `Pell.exists_of_not_isSquare` from the repository's
locked mathlib checkout and supplies the only transport needed by the frozen statement.
-/

namespace Stage1Instances.THMM0388.Proof

/-- Literal nonsquareness predicate used by the canonical statement. -/
def IsNonsquareInteger (D : Int) : Prop :=
  ¬ ∃ k : Int, k * k = D

/-- Exact canonical root repeated here so this proof artifact has a standalone elaboration gate. -/
def Root : Prop :=
  ∀ D : Int, 0 < D → IsNonsquareInteger D →
    ∃ x y : Int, x ^ 2 - D * y ^ 2 = 1 ∧ y ≠ 0

/-- The literal integer-square spelling implies mathlib's `¬ IsSquare D` spelling. -/
theorem not_isSquare_of_isNonsquareInteger {D : Int}
    (h : IsNonsquareInteger D) : ¬ IsSquare D := by
  rintro ⟨k, hk⟩
  exact h ⟨k, hk.symm⟩

/-- Kernel-checked closure of the exact THM-M-0388 root. -/
theorem pellEquationStatement : Root := by
  intro D hpos hnonsquare
  exact Pell.exists_of_not_isSquare hpos
    (not_isSquare_of_isNonsquareInteger hnonsquare)

/-- Definitional certificate that this artifact closes the frozen proposition. -/
theorem root_exact_type :
    Root =
      (∀ D : Int, 0 < D → (¬ ∃ k : Int, k * k = D) →
        ∃ x y : Int, x ^ 2 - D * y ^ 2 = 1 ∧ y ≠ 0) :=
  rfl

#check Pell.exists_of_not_isSquare
#print axioms Pell.exists_of_not_isSquare
#print axioms not_isSquare_of_isNonsquareInteger
#print axioms pellEquationStatement

end Stage1Instances.THMM0388.Proof
