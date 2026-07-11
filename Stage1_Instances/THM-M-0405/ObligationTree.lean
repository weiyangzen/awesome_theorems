import Statement

/-!
# THM-M-0405 checked obligation interfaces

This file checks the conjunction-composition boundary and names the two exact
branches of the frozen target. It deliberately assumes both branches; it does
not prove Bilu-Hanrot-Voutier or provide proof credit for either assumption.
-/

namespace Stage1.THM_M_0405

/-- Exact Lucas branch of the canonical conjunction. -/
def LucasBranch : Prop :=
  ∀ (L : LucasPair) (n : Nat), 30 < n →
    ∃ p : Nat, L.IsPrimitiveDivisor p n

/-- Exact Lehmer branch of the canonical conjunction. -/
def LehmerBranch : Prop :=
  ∀ (L : LehmerPair) (n : Nat), 30 < n →
    ∃ p : Nat, L.IsPrimitiveDivisor p n

/-- Checked child-to-root composition interface; both premises remain open. -/
theorem statement_of_branches
    (hLucas : LucasBranch) (hLehmer : LehmerBranch) : Statement := by
  exact ⟨hLucas, hLehmer⟩

/-- The canonical root exposes exactly the Lucas branch. -/
theorem lucasBranch_of_statement (h : Statement) : LucasBranch := h.1

/-- The canonical root exposes exactly the Lehmer branch. -/
theorem lehmerBranch_of_statement (h : Statement) : LehmerBranch := h.2

#print axioms statement_of_branches
#print axioms lucasBranch_of_statement
#print axioms lehmerBranch_of_statement

end Stage1.THM_M_0405
