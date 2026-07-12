import Mathlib.Data.Finite.Card
import Mathlib.GroupTheory.Subgroup.Simple

/-!
# THM-M-0074 statement substrate probe

This file checks only the pinned interfaces needed to express finiteness, group simplicity, exact
cardinality, and identity up to multiplicative equivalence. It deliberately does not define the
Monster, the Griess algebra, or a canonical Griess theorem: the repository has not frozen the exact
source construction and conclusion.
-/

namespace Stage1Instances.THM_M_0074

#check Finite
#check Nat.card
#check Nat.card_congr
#check IsSimpleGroup
#check MulEquiv
#check MulEquiv.isSimpleGroup_congr

end Stage1Instances.THM_M_0074
