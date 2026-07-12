import Mathlib.Algebra.Group.Pointwise.Finset.Basic

/-!
# THM-M-0385 statement-infrastructure probe

The catalogue does not identify one exact Bourgain sum-product proposition, so
this module deliberately declares no canonical target. It checks only that a
single pinned import provides concrete finite sumset, product-set, and
cardinality expressions that any finite-cardinality reading would need.
-/

namespace Stage1Instances.THM_M_0385.StatementInfrastructureProbe

open scoped Pointwise

variable (A : Finset Nat)

#check A + A
#check A * A
#check (A + A).card
#check (A * A).card

end Stage1Instances.THM_M_0385.StatementInfrastructureProbe
