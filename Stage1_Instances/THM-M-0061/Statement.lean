import Mathlib.Algebra.Group.Subgroup.Finite

/-!
# THM-M-0061 canonical Lean statement

This module freezes Lagrange's divisibility theorem for finite multiplicative groups. It contains
one checked cardinality-interface transport and structural mutation fixtures, but no proof of the
canonical target and no import of the proof-bearing coset-cardinality module.
-/

noncomputable section

namespace Stage1Instances.THM_M_0061

universe u

/-- For every subgroup of every finite group, the subgroup order divides the ambient order. -/
def LagrangeDivisibilityTarget : Prop :=
  forall (G : Type u) [Group G] [Finite G] (H : Subgroup G),
    Nat.card H ∣ Nat.card G

/-- The same finite-group claim expressed through chosen `Fintype` cardinalities. -/
def LagrangeFintypeCardTarget : Prop :=
  forall (G : Type u) [Group G] [Fintype G] (H : Subgroup G),
    @Fintype.card H (Fintype.ofFinite H) ∣ Fintype.card G

/-- Checked transport between the canonical `Finite`/`Nat.card` encoding and `Fintype.card`. -/
theorem lagrangeDivisibilityTarget_iff_fintypeCardTarget :
    LagrangeDivisibilityTarget.{u} ↔ LagrangeFintypeCardTarget.{u} := by
  constructor
  · intro h G _ _ H
    letI := Fintype.ofFinite H
    simpa only [Nat.card_eq_fintype_card] using h G H
  · intro h G _ _ H
    letI := Fintype.ofFinite G
    letI := Fintype.ofFinite H
    simpa only [Nat.card_eq_fintype_card] using h G H

/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

/-- Domain-broadening mutation: the catalog's finite ambient-group premise is removed. -/
def mutationRemovedFiniteness : Prop :=
  forall (G : Type u) [Group G] (H : Subgroup G),
    Nat.card H ∣ Nat.card G

/-- Domain mutation: multiplicative groups and subgroups are replaced by their additive analogues. -/
def mutationChangedToAdditiveDomain : Prop :=
  forall (G : Type u) [AddGroup G] [Finite G] (H : AddSubgroup G),
    Nat.card H ∣ Nat.card G

/-- Binder-scope mutation: an arbitrary subgroup is replaced by existence of some subgroup. -/
def mutationExistentialSubgroup : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    exists H : Subgroup G, Nat.card H ∣ Nat.card G

/-- Boundary mutation: groups of order one are excluded from the claim. -/
def mutationExcludedTrivialGroup : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    Nat.card G ≠ 1 -> forall H : Subgroup G, Nat.card H ∣ Nat.card G

variable
  (hCanonical : LagrangeDivisibilityTarget.{u})
  (hAdditive : mutationChangedToAdditiveDomain.{u})
  (hExistential : mutationExistentialSubgroup.{u})
  (hNontrivial : mutationExcludedTrivialGroup.{u})

#guard_msgs (drop error) in
example : mutationRemovedFiniteness.{u} := hCanonical

#guard_msgs (drop error) in
example : LagrangeDivisibilityTarget.{u} := hAdditive

#guard_msgs (drop error) in
example : LagrangeDivisibilityTarget.{u} := hExistential

#guard_msgs (drop error) in
example : LagrangeDivisibilityTarget.{u} := hNontrivial

/-! These implications check that the canonical binders include the required boundary cases. -/

/-- A group of cardinality one remains inside the canonical target; no nontriviality premise is
added merely for an API boundary. -/
theorem target_includes_order_one_group
    (h : LagrangeDivisibilityTarget.{u})
    (G : Type u) [Group G] [Finite G]
    (_hcard : Nat.card G = 1) (H : Subgroup G) :
    Nat.card H ∣ Nat.card G :=
  h G H

/-- The canonical target includes the bottom subgroup of every finite group. -/
theorem target_includes_bottom_subgroup
    (h : LagrangeDivisibilityTarget.{u})
    (G : Type u) [Group G] [Finite G] :
    Nat.card (⊥ : Subgroup G) ∣ Nat.card G :=
  h G ⊥

/-- The canonical target includes the top subgroup of every finite group. -/
theorem target_includes_top_subgroup
    (h : LagrangeDivisibilityTarget.{u})
    (G : Type u) [Group G] [Finite G] :
    Nat.card (⊤ : Subgroup G) ∣ Nat.card G :=
  h G ⊤

#check lagrangeDivisibilityTarget_iff_fintypeCardTarget
#print axioms lagrangeDivisibilityTarget_iff_fintypeCardTarget
#print axioms target_includes_order_one_group
#print axioms target_includes_bottom_subgroup
#print axioms target_includes_top_subgroup

set_option pp.universes true in
set_option pp.explicit true in
#print LagrangeDivisibilityTarget

end Stage1Instances.THM_M_0061
