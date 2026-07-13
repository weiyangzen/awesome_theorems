import Validation

/-!
# THM-M-1188 release probe

This module adds no proof content.  It checks, at the release snapshot, that
the exact canonical root and the frozen child-to-root route still have the
types reconciled by the validation phase.
-/

namespace Stage1Instances.THM_M_1188.ReleaseCheck

/-- Current-snapshot adapter for the exact canonical target. -/
theorem exactCanonicalRoot :
    Stage1Instances.THM_M_1188.HeatEquationWeakMaximumPrincipleTarget :=
  Stage1Instances.THM_M_1188.Validation.exactCanonicalRoot

/-- Current-snapshot adapter for the frozen composition route. -/
theorem exactComposedRoot :
    Stage1Instances.THM_M_1188.ObligationTree.Root :=
  Stage1Instances.THM_M_1188.Validation.exactComposedRoot

#check exactCanonicalRoot
#check exactComposedRoot
#print axioms exactCanonicalRoot
#print axioms exactComposedRoot

end Stage1Instances.THM_M_1188.ReleaseCheck
