import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Probability.Independence.Process.HasIndepIncrements
import Mathlib.Probability.Process.Predictable

/-!
# THM-M-1034 statement substrate probe

This module checks the pinned mathlib types closest to an Ito-integral
construction. It is not a canonical statement or a proof of that construction.
-/

open MeasureTheory ProbabilityTheory

#check Filtration
#check IsPredictable
#check IsGaussianProcess
#check HasIndepIncrements
#check MeasureTheory.Lp
#check MemLp

