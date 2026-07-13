import Mathlib.Analysis.SpecialFunctions.BinaryEntropy
import Mathlib.InformationTheory.Coding.KraftMcMillan
import Mathlib.Probability.ProbabilityMassFunction.Basic

/-!
# THM-M-1581 discovery-only intake probe

These checks authenticate nearby pinned probability, entropy-function, uniquely-decodable-code,
and Kraft-McMillan interfaces. They do not define a source entropy rate, expected code length,
constrained noiseless channel, source encoder, or Shannon source-coding theorem. No target theorem
or proof body is declared here.
-/

#check PMF
#check PMF.tsum_coe
#check Real.binEntropy
#check Real.qaryEntropy
#check InformationTheory.UniquelyDecodable
#check InformationTheory.UniquelyDecodable.epsilon_not_mem
#check InformationTheory.UniquelyDecodable.flatten_injective
#check InformationTheory.kraft_mcmillan_inequality
