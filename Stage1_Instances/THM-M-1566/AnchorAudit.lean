import Mathlib.Analysis.Distribution.TemperedDistribution
import Mathlib.Probability.Distributions.Gaussian.Fernique
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Topology.MetricSpace.Holder

/-!
# THM-M-1566 pinned anchor probes

These checks establish the availability of relevant pinned mathlib
infrastructure. None is a proof of GIP Corollary 5.9. The exact statement is
checked separately because it is outside this Lake source tree, and the
historical nonterminal scaffold is audited directly from source.
-/

#check ProbabilityTheory.IsGaussianProcess
#check ProbabilityTheory.IsGaussian.exists_integrable_exp_sq
#check HolderOnWith
#check TemperedDistribution
#check MeasureTheory.TendstoInMeasure
