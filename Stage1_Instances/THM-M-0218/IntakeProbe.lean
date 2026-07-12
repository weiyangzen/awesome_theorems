import Mathlib.Analysis.Complex.Conformal
import Mathlib.Analysis.Complex.UnitDisc.Basic
import Mathlib.Analysis.Complex.UpperHalfPlane.Metric

/-!
# THM-M-0218 discovery-only intake probe

These checks authenticate adjacent pinned APIs. `Complex.UnitDisc` has only its inherited Euclidean
structure here, while `UpperHalfPlane.dist_eq` belongs to a different model. This file neither
defines a disk hyperbolic metric nor states or proves a Poincare-disk model theorem.
-/

#check Complex.UnitDisc
#check Complex.UnitDisc.mk
#check Complex.UnitDisc.norm_lt_one
#check Metric.ball
#check ConformalAt
#check DifferentiableAt.conformalAt
#check UpperHalfPlane
#check UpperHalfPlane.dist_eq
#check UpperHalfPlane.isometry_vertical_line
