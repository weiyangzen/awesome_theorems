import Mathlib.MeasureTheory.OuterMeasure.Basic
import Mathlib.Probability.Combinatorics.BinomialRandomGraph.Defs
import Mathlib.Probability.Independence.Basic
import Mathlib.Probability.Moments.Basic

/-!
# THM-M-0972 discovery-only intake probe

These checks authenticate adjacent pinned APIs for independent random sets, event independence,
finite unions, lower-tail Chernoff bounds, and binomial random graphs. They neither choose among
the inequivalent statements called Janson's inequality nor prove THM-M-0972.
-/

#check ProbabilityTheory.setBernoulli
#check ProbabilityTheory.setBernoulli_apply
#check ProbabilityTheory.iIndepSet
#check ProbabilityTheory.iIndepSet.meas_biInter
#check ProbabilityTheory.iIndepSet.iIndepFun_indicator
#check ProbabilityTheory.mgf
#check ProbabilityTheory.measure_le_le_exp_mul_mgf
#check ProbabilityTheory.measure_le_le_exp_cgf
#check MeasureTheory.measure_biUnion_finset_le
#check MeasureTheory.measure_iUnion_fintype_le
#check SimpleGraph.binomialRandom
