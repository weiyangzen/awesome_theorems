import Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Basic
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Def

/-!
# THM-M-1085 anchor audit

This file checks the closest APIs found in pinned mathlib. None of these declarations states the
Slepian comparison inequality, so this is discovery evidence rather than a proof or wrapper.
-/

open ProbabilityTheory

#check HasGaussianLaw
#check IsGaussianProcess
#check HasGaussianLaw.charFunDual_map_eq
#check IsGaussianProcess.hasGaussianLaw

#print axioms HasGaussianLaw.charFunDual_map_eq
#print axioms IsGaussianProcess.hasGaussianLaw
