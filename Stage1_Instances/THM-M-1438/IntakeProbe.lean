import Mathlib.Analysis.Analytic.Basic
import Mathlib.Analysis.Normed.Operator.FredholmAlternative
import Mathlib.Analysis.Normed.Operator.ContinuousLinearMap
import Mathlib.Dynamics.FixedPoints.Basic

/-!
# THM-M-1438 discovery-only intake probe

These checks authenticate adjacent pinned analytic, fixed-point, linear-operator, compactness, and
spectral APIs. They neither encode Lanford's renormalization operator nor select or prove any of the
numbered results in the 1982 source.
-/

#check AnalyticAt
#check AnalyticOnNhd
#check Function.IsFixedPt
#check ContinuousLinearMap
#check IsCompactOperator
#check IsCompactOperator.hasEigenvalue_iff_mem_spectrum
#check spectrum
#check spectrum.mem_resolventSet_iff
