import Init

/-!
# THM-M-0388: canonical Pell-equation statement

This module freezes and elaborates the integer existence statement only. It does not prove it.
-/

namespace Stage1Instances.THMM0388

/-- `D` is not the square of an integer. This local spelling keeps the statement independent of
mathlib's proof modules while remaining the literal integer-square condition. -/
def IsNonsquareInteger (D : Int) : Prop :=
  ¬ ∃ k : Int, k * k = D

/-- The exact rev-5.6 target: every positive nonsquare integer parameter has a nontrivial
integer solution of the Pell equation. -/
def PellEquationStatement : Prop :=
  ∀ D : Int, 0 < D → IsNonsquareInteger D →
    ∃ x y : Int, x ^ 2 - D * y ^ 2 = 1 ∧ y ≠ 0

/-- A conjunction presentation of the same target, retained as a checked alternate encoding. -/
def ConjunctiveHypothesesStatement : Prop :=
  ∀ D : Int, 0 < D ∧ IsNonsquareInteger D →
    ∃ x y : Int, x ^ 2 - D * y ^ 2 = 1 ∧ y ≠ 0

/-- Statement-level transport only; this theorem supplies no Pell solution. -/
theorem pellEquationStatement_iff_conjunctiveHypothesesStatement :
    PellEquationStatement ↔ ConjunctiveHypothesesStatement := by
  constructor
  · intro h D hD
    exact h D hD.1 hD.2
  · intro h D hpos hnsq
    exact h D ⟨hpos, hnsq⟩

-- Separately elaborated mutation fixtures. The validator requires each expression to differ from
-- the canonical target; none receives equivalence or proof credit.
def MutationRemovedNonsquare : Prop :=
  ∀ D : Int, 0 < D →
    ∃ x y : Int, x ^ 2 - D * y ^ 2 = 1 ∧ y ≠ 0

def MutationChangedDomain : Prop :=
  ∀ D : Nat, 0 < D → (¬ ∃ k : Nat, k * k = D) →
    ∃ x y : Nat, x ^ 2 - D * y ^ 2 = 1 ∧ y ≠ 0

def MutationChangedBinderScope : Prop :=
  ∃ x y : Int, ∀ D : Int, 0 < D → IsNonsquareInteger D →
    x ^ 2 - D * y ^ 2 = 1 ∧ y ≠ 0

def MutationSquareBoundary : Prop :=
  ∀ D : Int, 0 < D → (∃ k : Int, k * k = D) →
    ∃ x y : Int, x ^ 2 - D * y ^ 2 = 1 ∧ y ≠ 0

end Stage1Instances.THMM0388

set_option pp.explicit true in
#print Stage1Instances.THMM0388.PellEquationStatement
