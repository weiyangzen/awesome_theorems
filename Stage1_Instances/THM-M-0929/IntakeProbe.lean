import Mathlib.GroupTheory.GroupAction.Quotient

/-!
# THM-M-0929 discovery-only intake probe

These checks authenticate the pinned group-action, fixed-point, orbit-quotient, and direct
Burnside-lemma interfaces. They do not select a source-identical canonical statement, audit the
terminal proof body, or grant statement or proof credit.
-/

#check MulAction.fixedBy
#check MulAction.orbitRel
#check MulAction.orbitRel.Quotient
#check MulAction.sigmaFixedByEquivOrbitsProdGroup
#check MulAction.sum_card_fixedBy_eq_card_orbits_mul_card_group
#check AddAction.sigmaFixedByEquivOrbitsProdAddGroup
#check AddAction.sum_card_fixedBy_eq_card_orbits_mul_card_addGroup

#print axioms MulAction.sigmaFixedByEquivOrbitsProdGroup
#print axioms MulAction.sum_card_fixedBy_eq_card_orbits_mul_card_group
#print axioms AddAction.sum_card_fixedBy_eq_card_orbits_mul_card_addGroup
