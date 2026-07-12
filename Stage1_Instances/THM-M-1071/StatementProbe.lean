import Mathlib.Probability.Distributions.Gaussian.Multivariate
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def
import Mathlib.Probability.Distributions.Poisson.Basic
import Mathlib.Probability.Independence.Process.HasIndepIncrements
import Mathlib.MeasureTheory.Integral.Lebesgue.Basic

/-!
# THM-M-1071 statement substrate probe

This is not the canonical Levy-Ito statement.  It checks only the closest
interfaces exposed by the pinned mathlib snapshot while the exact source
statement and the required stochastic-calculus interfaces remain unresolved.
-/

open MeasureTheory ProbabilityTheory

#check HasIndepIncrements
#check IsGaussianProcess
#check multivariateGaussian
#check poissonMeasure
#check MeasureTheory.integral
