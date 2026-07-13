import Statement
import ObligationTree
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0914 proof execution

This module installs the audited pigeonhole declarations from the
manifest-pinned mathlib dependency at every open interface in the frozen proof
graph. It proves the exact canonical target both through the pinned finite-type
wrapper and through the fully expanded frozen finite-set route. The two roots
share the same finite-set terminal body and receive no duplicate proof credit.
-/

namespace Stage1Instances.THM_M_0914.Proof

open Stage1Instances.THM_M_0914
open Stage1Instances.THM_M_0914_ObligationTree

/-- Install pinned mathlib's finite-set cardinality bound at
`M0914-L-CARD-INJON-BOUND`. -/
theorem cardInjOnBound_pinned : FinsetCardInjOnBound := by
  intro alpha beta s t f hMaps hInj
  exact Finset.card_le_card_of_injOn f hMaps hInj

/-- Install pinned mathlib's substantive finite-set collision theorem at
`M0914-L-FINSET-COLLISION`. -/
theorem finsetCollision_pinned : FinsetCollisionPackage := by
  intro alpha beta s t hcard f hMaps
  exact Finset.exists_ne_map_eq_of_card_lt_of_maps_to hcard hMaps

/-- Reconstruct the same finite-set terminal through both frozen children. -/
theorem finsetCollision_from_frozen_children : FinsetCollisionPackage :=
  finsetCollisionPackage_of_cardBound_and_noCollision
    cardInjOnBound_pinned noCollisionImpliesInjOn_checked

/-- Install the audited finite-type wrapper at
`M0914-A-FINTYPE-WRAPPER`. -/
theorem fintypeWrapper_pinned : FintypeCollisionPackage := by
  intro alpha beta _ _ f hcard
  exact Fintype.exists_ne_map_eq_of_card_lt f hcard

/-- Reconstruct the finite-type interface through the expanded finite-set
route and its universe-membership normalization. -/
theorem fintypeWrapper_from_frozen_children : FintypeCollisionPackage :=
  fintypePackage_of_finsetPackage finsetCollision_from_frozen_children

/-- Exact frozen root through the pinned finite-type wrapper. -/
theorem root_via_pinned_wrapper : Root :=
  root_of_fintypePackage fintypeWrapper_pinned cardFinPackage

/-- Exact frozen root through every child of the selected proof graph. -/
theorem root_via_frozen_children : Root :=
  root_of_fintypePackage fintypeWrapper_from_frozen_children cardFinPackage

/-- Target-owned canonical proof of the literal `Fin (n + 1) -> Fin n`
pigeonhole statement. -/
theorem pigeonholeTarget_proof : PigeonholeTarget :=
  root_via_pinned_wrapper

/-- Exact-root cross-check through the expanded frozen route. -/
theorem pigeonholeTarget_via_frozen_children : PigeonholeTarget :=
  root_via_frozen_children

assert_no_sorry Finset.card_le_card_of_injOn
assert_no_sorry Finset.exists_ne_map_eq_of_card_lt_of_maps_to
assert_no_sorry Fintype.exists_ne_map_eq_of_card_lt
assert_no_sorry cardInjOnBound_pinned
assert_no_sorry finsetCollision_pinned
assert_no_sorry finsetCollision_from_frozen_children
assert_no_sorry fintypeWrapper_pinned
assert_no_sorry fintypeWrapper_from_frozen_children
assert_no_sorry root_via_pinned_wrapper
assert_no_sorry root_via_frozen_children
assert_no_sorry pigeonholeTarget_proof
assert_no_sorry pigeonholeTarget_via_frozen_children

#print sorries Finset.card_le_card_of_injOn
#print sorries Finset.exists_ne_map_eq_of_card_lt_of_maps_to
#print sorries Fintype.exists_ne_map_eq_of_card_lt
#print sorries cardInjOnBound_pinned
#print sorries finsetCollision_pinned
#print sorries finsetCollision_from_frozen_children
#print sorries fintypeWrapper_pinned
#print sorries fintypeWrapper_from_frozen_children
#print sorries root_via_pinned_wrapper
#print sorries root_via_frozen_children
#print sorries pigeonholeTarget_proof
#print sorries pigeonholeTarget_via_frozen_children

#print axioms Finset.card_le_card_of_injOn
#print axioms Finset.exists_ne_map_eq_of_card_lt_of_maps_to
#print axioms Fintype.exists_ne_map_eq_of_card_lt
#print axioms cardInjOnBound_pinned
#print axioms finsetCollision_pinned
#print axioms finsetCollision_from_frozen_children
#print axioms fintypeWrapper_pinned
#print axioms fintypeWrapper_from_frozen_children
#print axioms root_via_pinned_wrapper
#print axioms root_via_frozen_children
#print axioms pigeonholeTarget_proof
#print axioms pigeonholeTarget_via_frozen_children

end Stage1Instances.THM_M_0914.Proof
