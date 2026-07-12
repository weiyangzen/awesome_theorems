import Mathlib.Order.RelClasses

/-!
# THM-M-0771: well-ordering theorem statement

This module freezes the relation-level formulation of the well-ordering theorem and checks its
equivalence with the bundled `LinearOrder` formulation. It does not prove the universal target.
-/

universe u

namespace Stage1Instances.THM_M_0771

/-- Every carrier admits a strict relation which is a well-order. -/
def WellOrderingTarget : Prop :=
  ∀ alpha : Type u, Nonempty { r : alpha → alpha → Prop // IsWellOrder alpha r }

/-- The equivalent bundled-order presentation used by mathlib's well-ordering theorem. -/
def BundledWellOrderingTarget : Prop :=
  ∀ alpha : Type u, ∃ _ : LinearOrder alpha, WellFoundedLT alpha

/-- A relation-level well-order induces the bundled linear-order presentation. -/
theorem relation_to_bundled (h : WellOrderingTarget.{u}) :
    BundledWellOrderingTarget.{u} := by
  intro alpha
  let ⟨r, hr⟩ := h alpha
  letI : IsWellOrder alpha r := hr
  let order : LinearOrder alpha := IsWellOrder.linearOrder r
  letI : LinearOrder alpha := order
  exact ⟨order, IsWellOrder.toIsWellFounded⟩

/-- A bundled well-order induces its underlying strict well-order relation. -/
theorem bundled_to_relation (h : BundledWellOrderingTarget.{u}) :
    WellOrderingTarget.{u} := by
  intro alpha
  let ⟨order, hwf⟩ := h alpha
  letI : LinearOrder alpha := order
  letI : WellFoundedLT alpha := hwf
  exact ⟨⟨(· < ·), inferInstance⟩⟩

/-- Checked transport between the two standard formulations. -/
theorem wellOrderingTarget_iff_bundled :
    WellOrderingTarget.{u} ↔ BundledWellOrderingTarget.{u} :=
  ⟨relation_to_bundled, bundled_to_relation⟩

-- Structural mutations are elaborated and distinguished by `check_statement.py`.
def mutationRemovedWellFoundedness : Prop :=
  ∀ alpha : Type u, Nonempty { r : alpha → alpha → Prop // IsStrictTotalOrder alpha r }

def mutationRemovedLinearity : Prop :=
  ∀ alpha : Type u, Nonempty { r : alpha → alpha → Prop // IsWellFounded alpha r }

def mutationRestrictedToInhabited : Prop :=
  ∀ (alpha : Type u) [Nonempty alpha],
    Nonempty { r : alpha → alpha → Prop // IsWellOrder alpha r }

def mutationFixedCarrier : Prop :=
  Nonempty { r : Nat → Nat → Prop // IsWellOrder Nat r }

/-- The empty carrier is included in the canonical domain. -/
theorem empty_boundary :
    Nonempty { r : Empty → Empty → Prop // IsWellOrder Empty r } :=
  ⟨⟨emptyRelation, inferInstance⟩⟩

/-- Singleton carriers are included in the canonical domain. -/
theorem singleton_boundary :
    Nonempty { r : PUnit → PUnit → Prop // IsWellOrder PUnit r } :=
  ⟨⟨emptyRelation, inferInstance⟩⟩

end Stage1Instances.THM_M_0771

#print axioms Stage1Instances.THM_M_0771.relation_to_bundled
#print axioms Stage1Instances.THM_M_0771.bundled_to_relation
#print axioms Stage1Instances.THM_M_0771.wellOrderingTarget_iff_bundled

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0771.WellOrderingTarget
