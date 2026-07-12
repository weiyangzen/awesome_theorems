import Mathlib.Analysis.Distribution.Distribution

open Set TopologicalSpace
open scoped Distributions

-- This probe checks only the pinned substrate available for statement elaboration.
-- It is deliberately not a substitute statement for convolution of distributions.
#check TestFunction
#check Distribution
#check Distribution.mapCLM

section

variable (E : Type*) [NormedAddCommGroup E] [NormedSpace ℝ E] (Ω : Opens E)

#check (𝓓(Ω, ℝ))
#check (𝓓'(Ω, ℝ))

end
