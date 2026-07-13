import Mathlib.Probability.Independence.Basic
import Mathlib.Probability.Moments.Basic
import Mathlib.Probability.ProbabilityMassFunction.Basic

/-!
# THM-M-0970 discovery-only intake probe

These checks authenticate pinned indexed-independence, finite product-law, probability-measure,
discrete-law, and expectation interfaces adjacent to a future Moser-Tardos encoding. They do not
define bad-event supports, a dependency graph, Algorithm 1.1, resampling semantics, a stopping time,
an expected bound, or a canonical THM-M-0970 target.
-/

#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.iIndepFun_iff_finset
#check ProbabilityTheory.iIndepFun_iff_map_fun_eq_pi_map
#check MeasureTheory.IsProbabilityMeasure
#check PMF
#check PMF.toMeasure
#check PMF.toMeasure.isProbabilityMeasure
#check ProbabilityTheory.moment
#check MeasureTheory.integral

#print axioms ProbabilityTheory.iIndepFun_iff_map_fun_eq_pi_map
#print axioms PMF.toMeasure.isProbabilityMeasure
#print axioms ProbabilityTheory.moment_one
