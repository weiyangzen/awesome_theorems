import Mathlib.Analysis.SpecialFunctions.BinaryEntropy
import Mathlib.InformationTheory.Coding.UniquelyDecodable
import Mathlib.InformationTheory.Hamming
import Mathlib.InformationTheory.KullbackLeibler.ChainRule
import Mathlib.Probability.Kernel.Basic
import Mathlib.Probability.ProbabilityMassFunction.Basic

/-!
# THM-M-1580 discovery-only intake probe

These checks authenticate adjacent pinned probability, stochastic-kernel, divergence, elementary
entropy, and coding interfaces. They do not define Shannon's source entropy rate, channel capacity,
block codes, decoding error, or noisy-channel coding theorem. No target theorem or proof body is
declared here.
-/

open MeasureTheory ProbabilityTheory

#check PMF
#check PMF.toMeasure
#check Kernel
#check IsMarkovKernel
#check Kernel.deterministic
#check Real.binEntropy
#check InformationTheory.klDiv
#check InformationTheory.klDiv_compProd_eq_add
#check InformationTheory.UniquelyDecodable
#check hammingDist
