import Mathlib.LinearAlgebra.ExteriorAlgebra.Grading
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.LinearAlgebra.CrossProduct

/-!
# THM-M-0051 discovery-only intake probe

These checks authenticate pinned exterior-algebra interfaces adjacent to the catalog's incomplete
"an identity about exterior algebra" gloss. They do not identify a singular Grassmann identity,
select a canonical target, or grant source, statement, provenance, or proof credit.
-/

#check ExteriorAlgebra
#check ExteriorAlgebra.ι
#check ExteriorAlgebra.ι_sq_zero
#check ExteriorAlgebra.ι_add_mul_swap
#check ExteriorAlgebra.lift
#check ExteriorAlgebra.lift_unique
#check ExteriorAlgebra.ιMulti
#check ExteriorAlgebra.ιMulti_mul_ιMulti
#check ExteriorAlgebra.map_apply_ιMulti
#check ExteriorAlgebra.gradedAlgebra
#check Submodule.finrank_sup_add_finrank_inf_eq
#check cross_cross
#check cross_cross_eq_smul_sub_smul
#check cross_cross_eq_smul_sub_smul'

#print axioms ExteriorAlgebra.ι_sq_zero
#print axioms ExteriorAlgebra.ι_add_mul_swap
#print axioms ExteriorAlgebra.ιMulti_mul_ιMulti
#print axioms Submodule.finrank_sup_add_finrank_inf_eq
#print axioms cross_cross_eq_smul_sub_smul
