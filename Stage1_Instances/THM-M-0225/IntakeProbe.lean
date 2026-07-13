import Mathlib.Analysis.Complex.AbsMax

/-!
# THM-M-0225 discovery-only intake probe

These checks authenticate representative maximum-modulus interfaces in the pinned mathlib
snapshot. They do not select a variant as the catalog root, repair the catalog's missing constant
exception, establish statement identity, or credit a proof body.
-/

#check Complex.norm_eventually_eq_of_isLocalMax
#check Complex.eventually_eq_of_isLocalMax_norm
#check Complex.norm_eqOn_of_isPreconnected_of_isMaxOn
#check Complex.eqOn_of_isPreconnected_of_isMaxOn_norm
#check Complex.exists_mem_frontier_isMaxOn_norm
#check Complex.norm_le_of_forall_mem_frontier_norm_le

#print axioms Complex.norm_eventually_eq_of_isLocalMax
#print axioms Complex.eventually_eq_of_isLocalMax_norm
#print axioms Complex.eqOn_of_isPreconnected_of_isMaxOn_norm
#print axioms Complex.exists_mem_frontier_isMaxOn_norm
