import Mathlib.GroupTheory.Solvable
import Mathlib.SetTheory.Cardinal.Finite

/-!
# THM-M-0070 canonical Lean statement

This module freezes the finite odd-order solvability claim. It contains checked statement
transports and structural mutation fixtures, but no proof of the canonical target.
-/

noncomputable section

namespace Stage1Instances.THM_M_0070

universe u

/-- Every finite multiplicative group of odd cardinality is solvable. -/
def OddOrderSolvabilityTarget : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    Odd (Nat.card G) -> IsSolvable G

/-- The same finite-group claim expressed through a chosen `Fintype` cardinality. -/
def OddOrderFintypeCardTarget : Prop :=
  forall (G : Type u) [Group G] [Fintype G],
    Odd (Fintype.card G) -> IsSolvable G

/-- The same odd-order hypothesis expressed as a congruence modulo two. -/
def OddOrderModTwoTarget : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    Nat.card G % 2 = 1 -> IsSolvable G

/-- The solvability conclusion expanded to the eventual-triviality derived-series witness. -/
def OddOrderDerivedSeriesTarget : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    Odd (Nat.card G) -> exists n : Nat, derivedSeries G n = (⊥ : Subgroup G)

/-- Checked transport between the canonical `Finite`/`Nat.card` encoding and `Fintype.card`. -/
theorem oddOrderSolvabilityTarget_iff_fintypeCardTarget :
    OddOrderSolvabilityTarget.{u} <-> OddOrderFintypeCardTarget.{u} := by
  constructor
  · intro h G _ _ hodd
    exact h G (Nat.card_eq_fintype_card (α := G) ▸ hodd)
  · intro h G _ _ hodd
    letI := Fintype.ofFinite G
    exact h G (Nat.card_eq_fintype_card (α := G) ▸ hodd)

/-- Checked transport between factorization oddness and congruence modulo two. -/
theorem oddOrderSolvabilityTarget_iff_modTwoTarget :
    OddOrderSolvabilityTarget.{u} <-> OddOrderModTwoTarget.{u} := by
  simp only [OddOrderSolvabilityTarget, OddOrderModTwoTarget, Nat.odd_iff]

/-- Checked transport to mathlib's explicit definition of group solvability. -/
theorem oddOrderSolvabilityTarget_iff_derivedSeriesTarget :
    OddOrderSolvabilityTarget.{u} <-> OddOrderDerivedSeriesTarget.{u} := by
  simp only [OddOrderSolvabilityTarget, OddOrderDerivedSeriesTarget, isSolvable_def]

/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

/-- Removed-hypothesis mutation: all finite groups are asserted to be solvable. -/
def mutationRemovedOddness : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    IsSolvable G

/-- Domain mutation: arbitrary groups are restricted to commutative groups. -/
def mutationChangedToCommutativeDomain : Prop :=
  forall (G : Type u) [CommGroup G] [Finite G],
    Odd (Nat.card G) -> IsSolvable G

/-- Binder-scope mutation: oddness is asserted together with solvability instead of assumed. -/
def mutationChangedOddnessScope : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    Odd (Nat.card G) /\ IsSolvable G

/-- Boundary mutation: even cardinality is substituted for the source's odd-cardinality boundary. -/
def mutationChangedToEvenOrder : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    Even (Nat.card G) -> IsSolvable G

variable
  (hCanonical : OddOrderSolvabilityTarget.{u})
  (hCommutative : mutationChangedToCommutativeDomain.{u})
  (hBoundary : mutationChangedToEvenOrder.{u})

#check_failure (show mutationRemovedOddness.{u} from hCanonical)

#check_failure (show OddOrderSolvabilityTarget.{u} from hCommutative)

#check_failure (show mutationChangedOddnessScope.{u} from hCanonical)

#check_failure (show OddOrderSolvabilityTarget.{u} from hBoundary)

/-! These implications confirm that the canonical binders retain required boundary classes. -/

/-- Groups of cardinality one remain in scope; no nontriviality premise is added. -/
theorem target_includes_order_one_group
    (h : OddOrderSolvabilityTarget.{u})
    (G : Type u) [Group G] [Finite G]
    (hcard : Nat.card G = 1) : IsSolvable G := by
  apply h G
  rw [hcard]
  exact odd_one

/-- Finite commutative odd-order groups remain instances of the unrestricted group target. -/
theorem target_includes_commutative_groups
    (h : OddOrderSolvabilityTarget.{u})
    (G : Type u) [CommGroup G] [Finite G]
    (hodd : Odd (Nat.card G)) : IsSolvable G :=
  h G hodd

#check oddOrderSolvabilityTarget_iff_fintypeCardTarget
#check oddOrderSolvabilityTarget_iff_modTwoTarget
#check oddOrderSolvabilityTarget_iff_derivedSeriesTarget
#print axioms oddOrderSolvabilityTarget_iff_fintypeCardTarget
#print axioms oddOrderSolvabilityTarget_iff_modTwoTarget
#print axioms oddOrderSolvabilityTarget_iff_derivedSeriesTarget
#print axioms target_includes_order_one_group
#print axioms target_includes_commutative_groups

set_option pp.universes true in
set_option pp.explicit true in
#print OddOrderSolvabilityTarget

end Stage1Instances.THM_M_0070
