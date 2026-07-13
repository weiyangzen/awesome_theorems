import Mathlib.Combinatorics.Additive.ErdosGinzburgZiv

/-!
# THM-M-0932 discovery-only intake probe

These checks authenticate generic finite-sequence sum interfaces and the pinned EGZ declarations
owned by neighboring target THM-M-0931. They do not define a zero-sum-sequence predicate, select a
canonical theorem, compile a source transport, or supply proof credit to THM-M-0932.
-/

#check Multiset
#check Multiset.card
#check Multiset.sum
#check Multiset.map
#check Multiset.le_iff_exists_add
#check Int.erdos_ginzburg_ziv
#check ZMod.erdos_ginzburg_ziv
#check Int.erdos_ginzburg_ziv_multiset
#check ZMod.erdos_ginzburg_ziv_multiset

#print axioms Int.erdos_ginzburg_ziv
#print axioms ZMod.erdos_ginzburg_ziv_multiset
