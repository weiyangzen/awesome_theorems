import Mathlib.Analysis.Meromorphic.Divisor
import Mathlib.Analysis.SpecialFunctions.Complex.CircleMap
import Mathlib.Analysis.SpecialFunctions.Complex.LogDeriv

/-!
# THM-M-1357 discovery-only intake probe

These checks authenticate adjacent pinned meromorphic-order, divisor, logarithmic-derivative, and
circle-parameterization APIs. They do not define a feedback system or winding convention, select a
Nyquist stability proposition, or prove THM-M-1357.
-/

#check MeromorphicOn.divisor
#check MeromorphicOn.divisor_apply
#check meromorphicOrderAt
#check logDeriv
#check circleMap
#check periodic_circleMap
