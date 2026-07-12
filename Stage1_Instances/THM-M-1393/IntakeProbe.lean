import Mathlib.Analysis.Normed.Operator.FredholmAlternative
import Mathlib.Analysis.ODE.Basic

/-! Bounded API checks only; this file states no boundary-value Fredholm alternative. -/

#check IsCompactOperator
#check IsCompactOperator.hasEigenvalue_or_mem_resolventSet
#check IsCompactOperator.hasEigenvalue_iff_mem_spectrum
#check spectrum
#check resolventSet
#check Module.End.HasEigenvalue
#check IsIntegralCurve
