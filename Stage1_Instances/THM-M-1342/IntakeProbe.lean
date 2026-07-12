import Mathlib.Analysis.ODE.Basic
import Mathlib.Dynamics.FixedPoints.Basic
import Mathlib.Topology.MetricSpace.Pseudo.Defs

/-!
# THM-M-1342 discovery-only intake probe

These checks authenticate adjacent pinned ODE, fixed-point, neighborhood, ball, and convergence
APIs. They do not choose or define a stability notion, select a proposition, or prove THM-M-1342.
-/

#check IsIntegralCurveOn
#check IsIntegralCurveAt
#check IsIntegralCurveAt.hasDerivAt
#check Function.IsFixedPt
#check Metric.ball
#check nhds
#check Filter.Tendsto
