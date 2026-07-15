import Statement
import ObligationTree

/-!
# THM-M-0729 proof blocker probe

This module rechecks the exact root and the only implemented composition
boundary.  It intentionally introduces no theorem: neither directional PCP
inclusion has a proof body in the pinned closure.
-/

namespace Stage1Instances.THM_M_0729

#check PCPTheorem
#check DirectionalPackage
#check pcpTheorem_iff_expandedTarget
#check expandedTarget_of_directionalPackage
#check root_of_directionalPackage

#print axioms pcpTheorem_iff_expandedTarget
#print axioms expandedTarget_of_directionalPackage
#print axioms root_of_directionalPackage

-- This theorem-shaped application does not resolve to an available
-- polynomial-time composition declaration in the pinned environment.
#check_failure Turing.TM2ComputableInPolyTime.comp (eα := id)

end Stage1Instances.THM_M_0729
