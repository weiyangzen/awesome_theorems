import Mathlib.Combinatorics.Additive.PluenneckeRuzsa

/-!
# THM-M-0943 discovery-only intake probe

These checks authenticate a close pinned Plunnecke-Ruzsa declaration, its Petridis bridge, and
nearby variants. They do not select the catalog root, establish source identity, or prove a new
theorem.
-/

#check Finset.pluennecke_petridis_inequality_add
#check Finset.pluennecke_ruzsa_inequality_nsmul_sub_nsmul_add
#check Finset.pluennecke_ruzsa_inequality_nsmul_sub_nsmul_sub
#check Finset.pluennecke_ruzsa_inequality_nsmul_add
#check Finset.pluennecke_ruzsa_inequality_nsmul_sub

#print axioms Finset.pluennecke_ruzsa_inequality_nsmul_sub_nsmul_add
#print axioms Finset.pluennecke_ruzsa_inequality_nsmul_sub_nsmul_sub
