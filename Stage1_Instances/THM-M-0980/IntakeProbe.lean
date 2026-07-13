import Mathlib.Probability.Moments.Basic
import Mathlib.Probability.Moments.Variance

/-!
# THM-M-0980 discovery-only intake probe

These checks authenticate pinned moment-generating-function, Chernoff, independence, and variance
interfaces adjacent to the conventional Bennett inequality family. They do not select a canonical
statement, perform the downstream anchor audit, or install any proof credit.
-/

#check ProbabilityTheory.mgf
#check ProbabilityTheory.cgf
#check ProbabilityTheory.measure_ge_le_exp_mul_mgf
#check ProbabilityTheory.measure_ge_le_exp_cgf
#check ProbabilityTheory.iIndepFun.mgf_sum
#check ProbabilityTheory.IndepFun.variance_sum

#print axioms ProbabilityTheory.measure_ge_le_exp_mul_mgf
#print axioms ProbabilityTheory.measure_ge_le_exp_cgf
#print axioms ProbabilityTheory.iIndepFun.mgf_sum
#print axioms ProbabilityTheory.IndepFun.variance_sum
