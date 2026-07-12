import Mathlib.MeasureTheory.Function.LpSeminorm.Basic
import Mathlib.MeasureTheory.Measure.Decomposition.RadonNikodym
import Mathlib.MeasureTheory.Measure.MutuallySingular
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Probability.Distributions.Gaussian.Real

/-!
# THM-M-1045 pinned anchor probes

These checks inventory the measure-theory and Gaussian interfaces available in
the pinned mathlib snapshot. None is a Cameron-Martin quasi-invariance result.
-/

noncomputable section

open MeasureTheory ProbabilityTheory

#check Measure.AbsolutelyContinuous
#check Measure.rnDeriv
#check Measure.rnDeriv_self
#check Measure.rnDeriv_withDensity
#check Measure.MutuallySingular
#check Measure.map
#check MemLp
#check gaussianReal
#check gaussianReal_map_add_const
#check ProbabilityTheory.HasGaussianLaw
