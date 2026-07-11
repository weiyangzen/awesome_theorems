import Mathlib.NumberTheory.Pell

/-!
# THM-M-0388 anchor adapter

This is the narrow adapter from the frozen rev-5.6 statement to mathlib's Pell theorem. The audit
records this as an eligible candidate, not as checked closure: the pinned worker cache currently
lacks `Mathlib.NumberTheory.Pell.olean`, so this module cannot yet be elaborated without building a
dependency artifact.
-/

namespace Stage1Instances.THMM0388

/-- Audit-local spelling of the predicate frozen in `Statement.lean`. -/
def AuditIsNonsquareInteger (D : Int) : Prop :=
  ¬ ∃ k : Int, k * k = D

/-- The local literal square predicate is equivalent to mathlib's `IsSquare` predicate. -/
theorem isNonsquareInteger_iff_not_isSquare (D : Int) :
    AuditIsNonsquareInteger D ↔ ¬ IsSquare D := by
  constructor
  · intro h hs
    obtain ⟨k, hk⟩ := hs
    exact h ⟨k, hk.symm⟩
  · intro h hs
    obtain ⟨k, hk⟩ := hs
    exact h ⟨k, hk.symm⟩

/-- Exact candidate wrapper for the canonical statement, with no strengthened conclusion. -/
theorem pellEquationStatement_mathlib_candidate :
    ∀ D : Int, 0 < D → AuditIsNonsquareInteger D →
      ∃ x y : Int, x ^ 2 - D * y ^ 2 = 1 ∧ y ≠ 0 := by
  intro D hpos hnsq
  exact Pell.exists_of_not_isSquare hpos
    ((isNonsquareInteger_iff_not_isSquare D).mp hnsq)

#check Pell.exists_of_not_isSquare
#print axioms Pell.exists_of_not_isSquare
#print axioms pellEquationStatement_mathlib_candidate

end Stage1Instances.THMM0388
