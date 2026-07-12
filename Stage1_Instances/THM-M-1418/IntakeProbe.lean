import Mathlib.Logic.Function.Iterate
import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Order.LiminfLimsup

/-! Discovery-only API checks for a later source-corrected Lyapunov-exponent statement. -/

#check Function.comp_def
#check Function.Semiconj.iterate_right
#check dist
#check fderiv
#check HasFDerivAt
#check norm_nonneg
#check Real.log
#check Filter.limsup
#check Filter.liminf
