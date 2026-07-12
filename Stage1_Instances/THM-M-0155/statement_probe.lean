import Mathlib.MeasureTheory.Integral.CurveIntegral.Poincare

/-!
This file is a statement-surface probe, not the canonical statement of Green's theorem.

The pinned import exposes curve integrals and the rectangular divergence theorem used internally
by the Poincare lemma.  It does not expose a region class with an oriented boundary integration
operator from which the intake claim can be stated without restricting the theorem to rectangles
or assuming the desired boundary/area equality.
-/

#check curveIntegral
#check MeasureTheory.integral_divergence_prod_Icc_of_hasFDerivAt_of_le
#check MeasureTheory.integral2_divergence_prod_of_hasFDerivAt
#check ContinuousMap.Homotopy.curveIntegral_add_curveIntegral_eq_of_hasFDerivWithinAt

