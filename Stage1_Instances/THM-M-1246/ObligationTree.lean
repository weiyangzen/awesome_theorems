import Statement

/-!
# THM-M-1246 obligation-tree composition boundary

The analytic proof remains an explicit premise.  This module checks only that
the terminal package has exactly the canonical target and composes without a
weakened statement or an extra assumption.
-/

namespace Stage1Instances.THM_M_1246.ObligationTree

/-- Exact output required from the analytic proof subtree. -/
abbrev HardyTerminal : Prop :=
  Stage1Instances.THM_M_1246.HardyInequalityTarget

/-- Checked transport from the terminal package to the public root. -/
theorem root_of_hardyTerminal
    (h : HardyTerminal) : Stage1Instances.THM_M_1246.HardyInequalityTarget := h

#check root_of_hardyTerminal
#print axioms root_of_hardyTerminal

end Stage1Instances.THM_M_1246.ObligationTree
