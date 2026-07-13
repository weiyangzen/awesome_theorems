import Mathlib.Algebra.MvPolynomial.Eval
import Mathlib.Algebra.MvPolynomial.PDeriv
import Mathlib.Probability.Distributions.SetBernoulli
import Mathlib.Probability.Independence.Basic

/-!
# THM-M-0973 discovery-only intake probe

These checks authenticate pinned multivariate-polynomial, partial-derivative, independent-function,
and Bernoulli-product APIs adjacent to a possible future Kim-Vu statement. They do not select the
catalog's exact inequality, define its derivative expectation parameters, state its hypotheses or
tail bound, or prove any Kim-Vu theorem.
-/

#check MvPolynomial
#check MvPolynomial.eval
#check MvPolynomial.eval₂
#check MvPolynomial.pderiv
#check ProbabilityTheory.iIndepFun
#check ProbabilityTheory.setBernoulli
#check ProbabilityTheory.IsSetBernoulli
#check ProbabilityTheory.setBernoulli_singleton
