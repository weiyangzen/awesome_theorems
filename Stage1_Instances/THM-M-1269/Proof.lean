import Statement

/-!
# THM-M-1269 proof execution

This module closes the frozen minimizing-sequence target using the pinned
mathlib infimum-approximation theorem and a checked choice of preimages.
-/

open Filter Set Topology

namespace Stage1Instances.THM_M_1269

universe u

/-- Every nonempty real-valued variational problem whose range is bounded
below admits a sequence whose functional values tend to the range infimum. -/
theorem minimizingSequence_proof (X : Type u) (F : X -> Real) :
    THM_M_1269_statement X F := by
  intro hX hbelow
  obtain ⟨values, _, hvalues, hmem⟩ :=
    exists_seq_tendsto_sInf (Set.range_nonempty F) hbelow
  choose sequence hsequence using hmem
  have heq : (fun n => F (sequence n)) = values := funext hsequence
  exact ⟨sequence, heq ▸ hvalues⟩

#check minimizingSequence_proof
#print axioms minimizingSequence_proof

end Stage1Instances.THM_M_1269
