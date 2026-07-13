import Mathlib.Algebra.BigOperators.Group.Multiset.Basic
import Mathlib.Combinatorics.Additive.ErdosGinzburgZiv
import Mathlib.GroupTheory.FiniteAbelian.Basic
import Mathlib.GroupTheory.PGroup

/-!
# THM-M-0933 discovery-only intake probe

These checks authenticate adjacent pinned finite-abelian-group, p-group, multiset, sum, and
zero-sum APIs. They do not define a Davenport invariant, select an Olson theorem, declare the
canonical THM-M-0933 target, or grant proof credit.
-/

#check AddCommGroup.equiv_directSum_zmod_of_finite
#check IsPGroup
#check IsPGroup.iff_card
#check Multiset.card
#check Multiset.card_le_card
#check Multiset.sum
#check ZMod.erdos_ginzburg_ziv_multiset
