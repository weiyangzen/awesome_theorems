import Mathlib.NumberTheory.Pell

/-!
# THM-M-0388 independent validation probe

This module deliberately does not import the local proof wrapper. It reconstructs the frozen root
from the pinned terminal declaration so validation catches a wrapper whose type or transport has
drifted while still permitting a direct comparison with `Proof.lean`.
-/

namespace Stage1Instances.THMM0388.Validation

def IsNonsquareInteger (D : Int) : Prop :=
  ¬ ∃ k : Int, k * k = D

def Root : Prop :=
  ∀ D : Int, 0 < D → IsNonsquareInteger D →
    ∃ x y : Int, x ^ 2 - D * y ^ 2 = 1 ∧ y ≠ 0

theorem independentPredicateTransport {D : Int}
    (h : IsNonsquareInteger D) : ¬ IsSquare D := by
  rintro ⟨k, hk⟩
  exact h ⟨k, hk.symm⟩

theorem independentRoot : Root := by
  intro D hpos hnonsquare
  exact Pell.exists_of_not_isSquare hpos
    (independentPredicateTransport hnonsquare)

theorem root_exact_type :
    Root =
      (∀ D : Int, 0 < D → (¬ ∃ k : Int, k * k = D) →
        ∃ x y : Int, x ^ 2 - D * y ^ 2 = 1 ∧ y ≠ 0) :=
  rfl

#check Pell.exists_of_not_isSquare
#print axioms independentPredicateTransport
#print axioms Pell.exists_of_not_isSquare
#print axioms independentRoot

end Stage1Instances.THMM0388.Validation
