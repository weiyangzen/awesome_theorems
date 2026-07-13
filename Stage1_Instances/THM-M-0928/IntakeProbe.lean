import Mathlib.GroupTheory.GroupAction.Quotient
import Mathlib.GroupTheory.Perm.Cycle.Type

/-!
# THM-M-0928 discovery-only intake probe

These commands authenticate pinned orbit-counting, fixed-point, and permutation-cycle interfaces.
They do not define a coloring action or cycle index, select a source formulation, declare a
canonical THM-M-0928 target, or grant proof credit.
-/

#check MulAction.orbitRel
#check MulAction.fixedBy
#check MulAction.sigmaFixedByEquivOrbitsProdGroup
#check MulAction.sum_card_fixedBy_eq_card_orbits_mul_card_group
#check Equiv.Perm.cycleType
#check Equiv.Perm.card_fixedPoints

#print axioms MulAction.sigmaFixedByEquivOrbitsProdGroup
#print axioms MulAction.sum_card_fixedBy_eq_card_orbits_mul_card_group
#print axioms Equiv.Perm.card_fixedPoints
