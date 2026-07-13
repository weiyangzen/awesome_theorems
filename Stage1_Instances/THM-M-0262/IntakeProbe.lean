import Mathlib.Analysis.Meromorphic.Basic
import Mathlib.Data.Complex.Basic
import Mathlib.Dynamics.PeriodicPts.Defs
import Mathlib.FieldTheory.RatFunc.AsPolynomial
import Mathlib.Topology.Compactification.OnePoint.ProjectiveLine
import Mathlib.Topology.Connected.LocallyConnected

/-!
# THM-M-0262 discovery-only intake probe

These checks authenticate adjacent pinned rational-function, complex, meromorphic, compactification,
component, iteration, and periodic-point APIs. They neither define a rational sphere dynamics
classification nor select or prove a Sullivan theorem.
-/

#check RatFunc
#check RatFunc.eval
#check Complex
#check OnePoint Complex
#check OnePoint.infty
#check MeromorphicAt
#check MeromorphicOn
#check connectedComponentIn
#check Function.iterate_succ_apply
#check Function.IsPeriodicPt
#check Function.periodicPts
