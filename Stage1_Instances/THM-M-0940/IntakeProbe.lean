import Mathlib.Combinatorics.Additive.CauchyDavenport
import Mathlib.Combinatorics.Additive.FreimanHom
import Mathlib.Combinatorics.Additive.PluenneckeRuzsa
import Mathlib.Combinatorics.Additive.RuzsaCovering

/-!
# THM-M-0940 discovery-only intake probe

These checks authenticate mutually distinct pinned additive-combinatorics APIs. The repository's
"fundamental theorem" label does not select any of them, so this file states no target theorem and
supplies no statement or proof credit.
-/

#check cauchy_davenport_minOrder_add
#check ZMod.cauchy_davenport
#check IsAddFreimanHom
#check isAddFreimanHom_two
#check Finset.ruzsa_covering_add
#check Finset.ruzsa_triangle_inequality_sub_sub_sub
#check Finset.pluennecke_ruzsa_inequality_nsmul_sub_nsmul_add
