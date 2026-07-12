import Statement

/-!
# THM-M-0769 conditional obligation composition

This module checks the interfaces and child-to-parent composition selected by
the frozen obligation architecture. The fiber selector is deliberately an
explicit premise: supplying it belongs to the proof phase.
-/

universe u v

namespace Stage1Instances.THM_M_0769.ObligationTree

/-- The substantive choice step, separated from packaging its result as
`Nonempty`. -/
abbrev FiberSelector (ι : Sort u) (A : ι -> Sort v) :=
  (forall i, Nonempty (A i)) -> (forall i, A i)

/-- Checked child-to-parent composition. This proves no choice principle by
itself because `select` is the still-open substantive obligation. -/
theorem root_of_fiberSelector
    (select : forall (ι : Sort u) (A : ι -> Sort v), FiberSelector ι A) :
    AxiomOfChoiceTarget.{u, v} := by
  intro ι A h
  exact Nonempty.intro (select ι A h)

#check FiberSelector
#check root_of_fiberSelector
#print axioms root_of_fiberSelector

end Stage1Instances.THM_M_0769.ObligationTree
