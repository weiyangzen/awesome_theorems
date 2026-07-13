import Mathlib.Combinatorics.SimpleGraph.Clique
import Mathlib.Combinatorics.SimpleGraph.Finite
import Mathlib.Probability.Independence.Basic

/-!
# THM-M-0971 discovery-only intake probe

These checks authenticate pinned event-independence, finite-intersection, finite-graph,
independent-set, neighborhood, and degree APIs. They do not define Shearer's polynomial, select a
canonical target, or prove any form of the Shearer bound.
-/

#check ProbabilityTheory.iIndepSet
#check ProbabilityTheory.iIndepSet.meas_biInter
#check ProbabilityTheory.iIndepSet_iff_meas_biInter
#check MeasureTheory.measure_compl
#check SimpleGraph.IsIndepSet
#check SimpleGraph.indepSetFinset
#check SimpleGraph.neighborFinset
#check SimpleGraph.maxDegree
