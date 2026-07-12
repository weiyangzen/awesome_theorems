import Statement

/-!
# THM-M-0773 differential validation probe

This probe reconstructs the exact root directly from the pinned mathlib theorem.
It deliberately imports neither `Proof` nor `ObligationTree`.
-/

open Set

universe u

namespace Stage1Instances.THM_M_0773

/-- Same-worker differential reconstruction of the exact frozen root. -/
theorem independentlyReconstructedRoot : TeichmullerTukeyTarget.{u} := by
  intro alpha F hfinite hnonempty
  rcases hnonempty with ⟨seed, hseed⟩
  rcases Order.IsOfFiniteCharacter.exists_maximal hfinite hseed with ⟨m, _hseedm, hm⟩
  exact ⟨m, hm⟩

#check independentlyReconstructedRoot
#print axioms independentlyReconstructedRoot

end Stage1Instances.THM_M_0773
