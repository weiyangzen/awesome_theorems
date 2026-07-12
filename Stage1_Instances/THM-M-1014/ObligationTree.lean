import Statement

/-!
# THM-M-1014 obligation-tree composition boundary

This module checks the exact final interface between the pinned terminal bridge and the frozen
public target. The bridge premise is deliberately explicit: accepting its proof body belongs to
the dependent proof node, while this node freezes and checks only the composition architecture.
-/

noncomputable section

namespace Stage1Instances.THM_M_1014.ObligationTree

universe u v w

/-- Exact output required from the pinned continuous-mapping bridge. -/
abbrev ContinuousMappingTerminal : Prop :=
  Stage1Instances.THM_M_1014.StatementShape.{u, v, w}

/-- Checked child-to-parent composition without changing a binder or conclusion. -/
theorem root_of_continuousMappingTerminal
    (h : ContinuousMappingTerminal.{u, v, w}) :
    Stage1Instances.THM_M_1014.StatementShape.{u, v, w} := h

#check root_of_continuousMappingTerminal
#print axioms root_of_continuousMappingTerminal

end Stage1Instances.THM_M_1014.ObligationTree
