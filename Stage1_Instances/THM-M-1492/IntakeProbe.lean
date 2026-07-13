import Mathlib.Analysis.Convex.Cone.Dual
import Mathlib.Tactic.Linarith.Oracle.SimplexAlgorithm.PositiveVector

/-!
# THM-M-1492 discovery-only intake probe

These checks authenticate pinned proper-cone, separation, and meta simplex-certificate APIs near
the linear-programming topic. They do not define a linear program, select a canonical proposition,
or prove THM-M-1492. The simplex declarations are meta-level tactic infrastructure, not credited
kernel theorems for the catalog target.
-/

#check ProperCone
#check ProperCone.positive
#check ProperCone.dual
#check ProperCone.hyperplane_separation
#check ProperCone.hyperplane_separation_point
#check Mathlib.Tactic.Linarith.SimplexAlgorithm.stateLP
#check Mathlib.Tactic.Linarith.SimplexAlgorithm.findPositiveVector
