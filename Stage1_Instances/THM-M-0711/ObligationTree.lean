import Statement

/-!
# THM-M-0711 conditional obligation composition

This file checks only the final existential assembly.  The construction of a
finite presentation with an undecidable identity predicate remains an explicit
premise, rather than a new primitive or a claimed Novikov-Boone proof.
-/

namespace Stage1.THM_M_0711

/-- The exact property that a proposed finite presentation must establish. -/
def FixedPresentationUndecidable (n : Nat)
    (rels : Finset (FreeGroup (Fin n))) : Prop :=
  ¬ComputablePred fun word : List (Fin n × Bool) =>
    PresentedGroup.mk (rels : Set (FreeGroup (Fin n))) (evalWord word) = 1

/-- Checked final composition from a constructed witness to the frozen root. -/
theorem novikovBooneTarget_of_witness
    {n : Nat} {rels : Finset (FreeGroup (Fin n))}
    (h : FixedPresentationUndecidable n rels) : NovikovBooneTarget := by
  exact ⟨n, rels, h⟩

#print axioms novikovBooneTarget_of_witness

end Stage1.THM_M_0711
