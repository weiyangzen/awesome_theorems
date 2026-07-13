import Mathlib.Analysis.Convex.Extrema

/-!
# THM-M-1491 discovery-only intake probe

These checks authenticate pinned local-to-global extrema APIs adjacent to one possible convex-
optimization theorem. They do not select the catalog's canonical claim, define a general convex
optimization problem, prove minimizer existence or uniqueness, establish KKT or duality, or verify
an optimization algorithm.
-/

#check ConvexOn
#check IsLocalMinOn
#check IsMinOn
#check IsMinOn.of_isLocalMinOn_of_convexOn
#check IsMinOn.of_isLocalMin_of_convex_univ

#print axioms IsMinOn.of_isLocalMinOn_of_convexOn
#print axioms IsMinOn.of_isLocalMin_of_convex_univ
