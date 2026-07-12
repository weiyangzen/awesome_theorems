import Mathlib.Probability.Distributions.Gaussian.Fernique
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Independence

/-!
# THM-M-1088 anchor audit

This file checks the nearest pinned mathlib Gaussian APIs found by the anchor audit. The exact local
target is checked separately by `Statement.lean`; these declarations are infrastructure, not proofs
of Borell--TIS.
-/

#check ProbabilityTheory.IsGaussianProcess
#check ProbabilityTheory.IsGaussianProcess.hasGaussianLaw_eval
#check ProbabilityTheory.IsGaussianProcess.indepFun_of_covariance_eq_zero
#check ProbabilityTheory.IsGaussian.exists_integrable_exp_sq
