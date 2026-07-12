import Mathlib.Analysis.ODE.Basic
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Dynamics.Flow
import Mathlib.Dynamics.PeriodicPts.Defs
import Mathlib.Topology.IsLocalHomeomorph
import Mathlib.Topology.Homeomorph.Defs
import Mathlib.Topology.OpenPartialHomeomorph.Basic

/-!
# THM-M-1345 discovery-only intake probe

These checks authenticate adjacent pinned APIs for ODE trajectories, flows, fixed points,
derivatives, local homeomorphisms, homeomorphisms, and conjugacy. They do not state or prove a
Hartman-Grobman theorem.
-/

#check IsIntegralCurveOn
#check IsIntegralCurveAt
#check Flow
#check Flow.toHomeomorph
#check Flow.IsSemiconjugacy
#check Function.IsFixedPt
#check HasFDerivAt
#check fderiv
#check IsLocalHomeomorphOn
#check Homeomorph
#check OpenPartialHomeomorph
#check Function.Semiconj
#check Function.Semiconj.iterate_right
