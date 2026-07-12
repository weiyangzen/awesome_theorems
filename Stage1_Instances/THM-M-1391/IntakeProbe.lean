import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.SpecialFunctions.PolarCoord

/-!
# THM-M-1391 discovery-only intake probe

These checks authenticate adjacent pinned ODE, polar-coordinate, phase, and derivative APIs. They
do not select a Pruefer convention, construct a continuous lifted phase, state transformed
Sturm-Liouville equations, or prove THM-M-1391.
-/

#check IsIntegralCurve
#check IsIntegralCurveOn
#check IsIntegralCurveAt.hasDerivAt
#check HasDerivAt
#check Real.hasDerivAt_sin
#check Real.hasDerivAt_cos
#check HasDerivAt.sin
#check HasDerivAt.cos
#check polarCoord
#check polarCoord_symm_apply
#check hasFDerivAt_polarCoord_symm
#check Complex.polarCoord
#check Complex.polarCoord_apply
#check Complex.polarCoord_symm_apply
#check Complex.continuousAt_arg
#check Complex.continuousAt_arg_coe_angle
#check Real.Angle
#check Real.Angle.continuous_coe
