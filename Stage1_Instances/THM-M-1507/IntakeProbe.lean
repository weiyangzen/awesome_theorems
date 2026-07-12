import Mathlib.Analysis.Convex.Cone.Dual

/-!
Discovery-only checks for APIs adjacent to the THM-M-1507 topic family.

These declarations concern proper dual cones and separation. They do not define a primal or dual
optimization problem, state Lagrangian weak or strong duality, or prove THM-M-1507. Mathlib's
`Analysis.Convex.Cone.Basic` module documentation lists cone-program duality as future work.
-/

#check ProperCone
#check ProperCone.dual
#check ProperCone.subset_dual_dual
#check ProperCone.hyperplane_separation
#check ProperCone.hyperplane_separation_point
