import Statement

/-!
# THM-M-1005 obligation-tree composition boundary

This module checks the exact final interface that the proof phase must supply.  It intentionally
contains no proof of Doob's inequality: `StrongDoobTerminal` is the terminal estimate package, and
the theorem below only certifies that its output composes to the frozen public target.
-/

noncomputable section

namespace Stage1Instances.THM_M_1005.ObligationTree

universe u

/-- Exact output required from the analytic weak-to-strong proof subtree. -/
abbrev StrongDoobTerminal : Prop :=
  Stage1Instances.THM_M_1005.DoobLpMomentEstimate.{u}

/-- Checked terminal transport into the canonical root. -/
theorem root_of_strongDoobTerminal
    (h : StrongDoobTerminal.{u}) : Stage1Instances.THM_M_1005.Statement.{u} := h

#check root_of_strongDoobTerminal
#print axioms root_of_strongDoobTerminal

end Stage1Instances.THM_M_1005.ObligationTree
