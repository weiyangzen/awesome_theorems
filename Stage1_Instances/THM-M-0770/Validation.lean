import Statement

/-!
# THM-M-0770 independent validation probe

This reconstructs the frozen root through `zorn_le`, handling the empty-chain
case locally, rather than invoking the proof phase's `zorn_le_nonempty` wrapper.
-/

namespace Stage1Instances.THM_M_0770.Validation

open Stage1Instances.THM_M_0770

universe u

theorem independentlyReconstructedRoot : ZornsLemmaTarget.{u} := by
  intro alpha _ _ chains_bounded
  apply zorn_le
  intro c hc
  rcases c.eq_empty_or_nonempty with rfl | hne
  · exact ⟨Classical.arbitrary alpha, by simp⟩
  · exact chains_bounded c hc hne

#print axioms independentlyReconstructedRoot

end Stage1Instances.THM_M_0770.Validation
