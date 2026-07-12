import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.Analysis.Normed.Operator.FredholmAlternative

/-!
# THM-M-0590: pinned anchor probes

These declarations are infrastructure for the frozen BDF target. None states the
classification theorem, defines the Calkin algebra, or supplies a Fredholm index.
-/

#check IsCompactOperator
#check IsCompactOperator.add
#check IsCompactOperator.sub
#check IsCompactOperator.comp_clm
#check IsCompactOperator.clm_comp
#check ContinuousLinearMap.adjoint
#check ContinuousLinearMap.adjoint_adjoint
#check ContinuousLinearMap.adjoint_comp
#check spectrum
#check resolventSet
#check IsCompactOperator.hasEigenvalue_or_mem_resolventSet
#check IsCompactOperator.hasEigenvalue_iff_mem_spectrum
