import Mathlib.Data.Finite.Defs
import Mathlib.GroupTheory.Subgroup.Simple

/-!
# THM-M-0071 statement substrate probe

This file checks only the smallest pinned interfaces needed to begin expressing that a group is
finite and simple and that classification is up to multiplicative equivalence. It deliberately
does not define a classification predicate or declare the classification theorem: the repository
has not frozen the 18-family taxonomy or the 26 sporadic representatives.
-/

namespace Stage1Instances.THM_M_0071

#check Finite
#check IsSimpleGroup
#check MulEquiv
#check MulEquiv.isSimpleGroup_congr

end Stage1Instances.THM_M_0071
