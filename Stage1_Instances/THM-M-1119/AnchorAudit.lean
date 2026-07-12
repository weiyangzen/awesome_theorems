import Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected
import Mathlib.Probability.ProductMeasure
import Mathlib.Probability.ProbabilityMassFunction.Constructions

/-!
# THM-M-1119: pinned anchor probes

These checks cover the mathlib substrate used by the frozen statement. None is
the square-lattice critical-probability theorem.
-/

open MeasureTheory

#check SimpleGraph.Reachable
#check Measure.infinitePi
#check Measure.infinitePi_pi
#check Measure.infinitePi_map_eval
#check PMF.bernoulli
#check PMF.bernoulli_apply
#check PMF.toMeasure
#check sInf
