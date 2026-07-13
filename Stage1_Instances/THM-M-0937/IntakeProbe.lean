import Mathlib.Combinatorics.Additive.CauchyDavenport

/-!
# THM-M-0937 discovery-only intake probe

These checks authenticate the pinned finite-sumset and Cauchy-Davenport substrate relevant to a
future source-selected Vosper statement. The checked theorem is the forward cardinality lower
bound. This file does not state or prove Vosper's inverse classification, define arbitrary-length
arithmetic progressions, or supply a proof body for the target.
-/

open scoped Pointwise

#check Finset
#check Finset.Nonempty
#check Finset.range
#check Finset.image
#check ZMod
#check ZMod.cauchy_davenport
#check cauchy_davenport_minOrder_add
#check Finset.card_add_le
