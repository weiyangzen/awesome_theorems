import Mathlib.Probability.Martingale.OptionalSampling
import Mathlib.Probability.Independence.Process.HasIndepIncrements
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Probability.Distributions.Gaussian.Real

/-!
# THM-M-1030 statement substrate probe

This file checks only the pinned mathlib types closest to a possible
Dambis-Dubins-Schwarz encoding. It is not the canonical theorem statement:
the dependency snapshot has no identified continuous-local-martingale,
quadratic-variation, or Brownian-motion API from which the source theorem can
be stated without introducing new mathematical definitions.
-/

open MeasureTheory ProbabilityTheory

#check Filtration
#check IsStoppingTime
#check stoppedProcess
#check Martingale
#check StronglyAdapted
#check IsPredictable
#check IsGaussianProcess
#check HasIndepIncrements
#check gaussianReal
