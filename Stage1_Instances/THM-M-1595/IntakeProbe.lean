import Mathlib.Analysis.SpecialFunctions.BinaryEntropy
import Mathlib.Data.Matrix.Basic
import Mathlib.InformationTheory.Hamming
import Mathlib.LinearAlgebra.Matrix.Kronecker
import Mathlib.Probability.Kernel.Basic
import Mathlib.Probability.ProbabilityMassFunction.Constructions

/-!
# THM-M-1595 discovery-only intake probe

These checks authenticate generic pinned APIs adjacent to a possible finite polar-code encoding.
They do not define symmetric capacity, synthesized bit-channels, polar codes, successive-
cancellation decoding, a canonical target, or a proof of THM-M-1595.
-/

open ProbabilityTheory

#check PMF
#check PMF.bernoulli
#check Kernel
#check IsMarkovKernel
#check Kernel.deterministic
#check Real.binEntropy
#check hammingDist
#check Matrix
#check Matrix.kronecker
#check Matrix.kroneckerMap
