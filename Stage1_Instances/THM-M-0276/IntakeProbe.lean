import Mathlib.Analysis.Normed.Operator.Banach

/-!
# THM-M-0276 discovery-only intake probe

These checks authenticate direct Banach open-mapping interfaces in the pinned mathlib snapshot.
They do not select a catalog-root formulation, establish source identity, or prove the target.
-/

#check ContinuousLinearMap.exists_approx_preimage_norm_le
#check ContinuousLinearMap.exists_preimage_norm_le
#check ContinuousLinearMap.isOpenMap
#check ContinuousLinearMap.isQuotientMap
#check LinearEquiv.continuous_symm
#check IsOpenMap

#print axioms ContinuousLinearMap.exists_preimage_norm_le
#print axioms ContinuousLinearMap.isOpenMap
#print axioms ContinuousLinearMap.isQuotientMap
