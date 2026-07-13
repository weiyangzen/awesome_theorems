import Mathlib.Analysis.Convex.Extrema
import Mathlib.Topology.Order.Compact

/-!
# THM-M-1490 discovery-only intake probe

These checks authenticate pinned interfaces for three different kinds of optimization result.
They do not choose one as the catalog target, declare a canonical statement, or supply proof credit
for THM-M-1490.
-/

#check IsMinOn
#check IsLocalMinOn
#check IsCompact.exists_isMinOn
#check ContinuousOn.exists_isMinOn'
#check IsMinOn.of_isLocalMinOn_of_convexOn
#check StrictConvexOn.eq_of_isMinOn

#print axioms IsCompact.exists_isMinOn
#print axioms IsMinOn.of_isLocalMinOn_of_convexOn
#print axioms StrictConvexOn.eq_of_isMinOn
