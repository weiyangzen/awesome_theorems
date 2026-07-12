import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Probability.Process.Kolmogorov

/-!
Pinned-mathlib probes for the THM-M-1028 anchor audit.  These declarations
check useful infrastructure only; none has the frozen Wiener path-regularity
target as its type.
-/

#check ProbabilityTheory.IsGaussianProcess.congr
#check ProbabilityTheory.IsGaussianProcess.hasGaussianLaw_increments
#check ProbabilityTheory.IsKolmogorovProcess
#check ProbabilityTheory.IsAEKolmogorovProcess
#check ProbabilityTheory.IsKolmogorovProcess.IsAEKolmogorovProcess
#check ProbabilityTheory.IsAEKolmogorovProcess.mk
#check ProbabilityTheory.IsAEKolmogorovProcess.ae_eq_mk
#check ProbabilityTheory.IsAEKolmogorovProcess.kolmogorovCondition

#print axioms ProbabilityTheory.IsGaussianProcess.congr
#print axioms ProbabilityTheory.IsGaussianProcess.hasGaussianLaw_increments
#print axioms ProbabilityTheory.IsKolmogorovProcess.IsAEKolmogorovProcess
#print axioms ProbabilityTheory.IsAEKolmogorovProcess.ae_eq_mk
#print axioms ProbabilityTheory.IsAEKolmogorovProcess.kolmogorovCondition
