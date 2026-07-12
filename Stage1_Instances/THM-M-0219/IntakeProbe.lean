import Mathlib.Analysis.Complex.UpperHalfPlane.Metric
import Mathlib.Analysis.Complex.UnitDisc.Basic

/-!
# THM-M-0219 discovery-only intake probe

These checks authenticate adjacent pinned upper-half-plane, Poincare-metric, real fractional-linear
symmetry, and unit-disk interfaces. They do not select a meaning of "model", declare the target
proposition, establish a disk/half-plane transport, or supply proof credit.
-/

open scoped MatrixGroups

#check UpperHalfPlane
#check UpperHalfPlane.dist_eq
#check UpperHalfPlane.isometry_vertical_line
#check UpperHalfPlane.coe_specialLinearGroup_apply
#check Complex.UnitDisc
#check Complex.UnitDisc.norm_lt_one
#synth MetricSpace UpperHalfPlane
#synth ProperSpace UpperHalfPlane
#synth IsIsometricSMul SL(2, ℝ) UpperHalfPlane
