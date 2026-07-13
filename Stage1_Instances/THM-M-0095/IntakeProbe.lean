import Mathlib.Algebra.Lie.Weights.Killing

/-!
# THM-M-0095 discovery-only intake probe

These checks authenticate pinned ordinary and generalized weight/root-space infrastructure. They
do not select or prove the catalog's semisimple root-space decomposition.
-/

#check LieModule.weightSpace
#check LieModule.genWeightSpace
#check LieAlgebra.rootSpace
#check LieModule.iSupIndep_genWeightSpace'
#check LieModule.iSup_genWeightSpace_eq_top'
#check LieAlgebra.rootSpace_zero_eq
#check LieAlgebra.cartan_sup_iSup_rootSpace_eq_top
#check LieAlgebra.lie_mem_genWeightSpace_of_mem_genWeightSpace
#check LieAlgebra.IsKilling.lie_eq_smul_of_mem_rootSpace
