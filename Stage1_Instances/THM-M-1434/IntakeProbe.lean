import Mathlib.Analysis.Meromorphic.Basic
import Mathlib.Dynamics.PeriodicPts.Defs
import Mathlib.FieldTheory.RatFunc.AsPolynomial
import Mathlib.Topology.Compactification.OnePoint.ProjectiveLine
import Mathlib.Topology.Connected.LocallyConnected

/-! Bounded API checks only; this file states no no-wandering-domain theorem. -/

#check RatFunc
#check RatFunc.eval
#check Meromorphic
#check OnePoint
#check OnePoint.continuous_coe
#check connectedComponentIn
#check Function.iterate_succ_apply
#check Function.IsPeriodicPt
#check Function.periodicPts
