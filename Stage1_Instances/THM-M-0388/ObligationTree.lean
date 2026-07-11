import Init

/-!
# THM-M-0388 obligation composition

This file checks the shape of the root composition without asserting the imported Pell theorem.
`ImportedNotSquare` is an abstract stand-in for mathlib's `IsSquare` boundary.
-/

namespace Stage1Instances.THMM0388.ObligationTree

def IsNonsquareInteger (D : Int) : Prop :=
  ¬ ∃ k : Int, k * k = D

def Root : Prop :=
  ∀ D : Int, 0 < D → IsNonsquareInteger D →
    ∃ x y : Int, x ^ 2 - D * y ^ 2 = 1 ∧ y ≠ 0

/- Abstract predicate at the imported theorem boundary. -/
variable (ImportedNotSquare : Int → Prop)

def PredicateTransport : Prop :=
  ∀ D : Int, IsNonsquareInteger D → ImportedNotSquare D

def ImportedExistence : Prop :=
  ∀ D : Int, 0 < D → ImportedNotSquare D →
    ∃ x y : Int, x ^ 2 - D * y ^ 2 = 1 ∧ y ≠ 0

/-- Conditional composition certificate. Both root premises are consumed explicitly. -/
theorem root_compose
    (transport : PredicateTransport ImportedNotSquare)
    (pell : ImportedExistence ImportedNotSquare) : Root := by
  intro D hpos hnonsquare
  exact pell D hpos (transport D hnonsquare)

theorem root_exact_type :
    Root =
      (∀ D : Int, 0 < D → (¬ ∃ k : Int, k * k = D) →
        ∃ x y : Int, x ^ 2 - D * y ^ 2 = 1 ∧ y ≠ 0) :=
  rfl

#print root_compose
#print axioms root_compose

end Stage1Instances.THMM0388.ObligationTree
