import Statement

/-!
# THM-M-1269 independent local validation probe

This module intentionally does not import `Proof` or `ObligationTree`.  It
reconstructs the exact frozen root directly from the pinned mathlib theorem so
that validation is not merely a second invocation of the proof declaration.
-/

open Filter Set Topology

namespace Stage1Instances.THM_M_1269_Validation

universe u

theorem independentMinimizingSequence (X : Type u) (F : X -> Real) :
    THM_M_1269_statement X F := by
  intro _ hbounded
  rcases exists_seq_tendsto_sInf (Set.range_nonempty F) hbounded with
    ⟨values, _, hlimit, hvalues⟩
  let sequence : Nat -> X := fun n => Classical.choose (hvalues n)
  have hpointwise : forall n, F (sequence n) = values n := fun n =>
    Classical.choose_spec (hvalues n)
  refine ⟨sequence, ?_⟩
  simpa only [hpointwise] using hlimit

#print axioms independentMinimizingSequence

end Stage1Instances.THM_M_1269_Validation
