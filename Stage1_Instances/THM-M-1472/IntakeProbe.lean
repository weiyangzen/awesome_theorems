import Mathlib.Analysis.Normed.Operator.BanachSteinhaus
import Mathlib.Analysis.Normed.Operator.Completeness

/-!
# THM-M-1472 discovery-only intake probe

These checks authenticate adjacent pinned functional-analysis interfaces. They do not define a
finite-difference approximation, select a Lax-Richtmyer formulation, or supply target statement or
proof credit.
-/

#check ContinuousLinearMap.le_opNorm
#check banach_steinhaus
#check banach_steinhaus_iSup_nnnorm
#check ContinuousLinearMap.ofTendstoOfBoundedRange
#check ContinuousLinearMap.tendsto_of_tendsto_pointwise_of_cauchySeq
#check squeeze_zero

#print axioms banach_steinhaus
#print axioms ContinuousLinearMap.le_opNorm
