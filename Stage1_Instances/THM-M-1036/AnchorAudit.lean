import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Probability.Independence.Process.HasIndepIncrements
import Mathlib.Probability.Process.Adapted

open MeasureTheory

/-!
# THM-M-1036 anchor audit

This file checks the declarations actually available in the pinned local Lean
closure.  The mathlib declarations are substrate, while the historical Stage1
declarations are abstract statement/projection wrappers.  None has the exact
type of `Stage1Instances.THM_M_1036.SdeExistenceUniquenessTarget`.
-/

#check ProbabilityTheory.IsGaussianProcess
#check ProbabilityTheory.IsGaussianProcess.hasGaussianLaw_eval
#check ProbabilityTheory.HasIndepIncrements
#check ProbabilityTheory.HasIndepIncrements.indepFun_sub_sub
#check Adapted
