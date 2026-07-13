import Mathlib.Analysis.Complex.HasPrimitives
import Mathlib.MeasureTheory.Integral.CurveIntegral.Poincare

/-! Discovery-only API checks for a later source-frozen Cauchy-integral statement. -/

#check Complex.integral_boundary_rect_eq_zero_of_differentiableOn
#check Complex.circleIntegral_eq_zero_of_differentiable_on_off_countable
#check DiffContOnCl.circleIntegral_eq_zero
#check Complex.IsExactOn
#check DifferentiableOn.isExactOn_ball
#check Differentiable.isExactOn_univ
#check curveIntegral
#check ContinuousMap.Homotopy.curveIntegral_add_curveIntegral_eq_of_diffContOnCl
#check circleIntegral.integral_sub_center_inv

#print axioms Complex.integral_boundary_rect_eq_zero_of_differentiableOn
#print axioms DiffContOnCl.circleIntegral_eq_zero
#print axioms ContinuousMap.Homotopy.curveIntegral_add_curveIntegral_eq_of_diffContOnCl
#print axioms circleIntegral.integral_sub_center_inv
