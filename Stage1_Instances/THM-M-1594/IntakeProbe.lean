import Mathlib.Computability.DFA
import Mathlib.InformationTheory.Hamming
import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.Probability.Kernel.Basic
import Mathlib.Probability.ProbabilityMassFunction.Basic

/-!
# THM-M-1594 discovery-only intake probe

These checks authenticate generic pinned APIs adjacent to possible word, state-machine, channel,
discrete-probability, and Gaussian-noise models. They do not define a turbo encoder, interleaver,
trellis, iterative decoder, error metric, Shannon limit, or canonical target. No target theorem or
proof body is declared here.
-/

open MeasureTheory ProbabilityTheory

#check hammingDist
#check hammingDist_triangle
#check Hamming
#check DFA
#check DFA.eval
#check PMF
#check PMF.toMeasure
#check Kernel
#check IsMarkovKernel
#check Kernel.deterministic
#check gaussianReal
#check instIsProbabilityMeasureGaussianReal
