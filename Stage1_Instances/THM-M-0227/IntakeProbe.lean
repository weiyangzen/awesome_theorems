import Mathlib.AlgebraicTopology.FundamentalGroupoid.SimplyConnected
import Mathlib.Analysis.Complex.Conformal
import Mathlib.Analysis.Complex.UnitDisc.Basic
import Mathlib.Analysis.Analytic.Basic

/-! Discovery-only API checks for a later source-frozen Riemann-mapping statement. -/

#check Complex.UnitDisc
#check Complex.UnitDisc.norm_lt_one
#check IsOpen
#check IsSimplyConnected
#check IsSimplyConnected.nonempty
#check AnalyticAt
#check AnalyticOnNhd
#check Homeomorph
#check ConformalAt
#check DifferentiableAt.conformalAt
