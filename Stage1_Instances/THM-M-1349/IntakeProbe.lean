import Mathlib.Analysis.ODE.Basic
import Mathlib.Dynamics.Flow
import Mathlib.Dynamics.PeriodicPts.Defs
import Mathlib.MeasureTheory.Integral.DivergenceTheorem

/-! Discovery-only API checks for a later exact Bendixson-Dulac statement. -/

#check IsIntegralCurve
#check Flow
#check Function.IsPeriodicPt
#check HasFDerivAt
#check MeasureTheory.integral2_divergence_prod_of_hasFDerivAt
