import Mathlib.Analysis.Meromorphic.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Dynamics.PeriodicPts.Defs
import Mathlib.Topology.Closure
import Mathlib.Topology.Compactification.OnePoint.Basic

/-!
# THM-M-1435 discovery-only intake probe

These checks authenticate adjacent pinned complex, meromorphic, iteration, periodic-point, and
topological APIs. They neither define a rational sphere map or Julia set nor select or prove a
McMullen theorem.
-/

#check ℂ
#check OnePoint ℂ
#check OnePoint.infty
#check MeromorphicAt
#check MeromorphicOn
#check Function.iterate_succ_apply
#check Function.IsPeriodicPt
#check Function.periodicPts
#check closure
#check frontier
