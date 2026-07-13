import Mathlib.GroupTheory.Solvable
import Mathlib.SetTheory.Cardinal.Finite

/-!
# THM-M-0070 anchor-audit probes

The pinned Lean inventory has statement interfaces and proper special cases, but no declaration
proving finite odd-order groups solvable. This module checks those interfaces against a literal
copy of the frozen target. None of the declarations below inhabits the root target.
-/

noncomputable section

namespace Stage1Instances.THM_M_0070_AnchorAudit

universe u

/-- Literal audit copy of the statement gate's exact target. -/
def ExactTarget : Prop :=
  forall (G : Type u) [Group G] [Finite G],
    Odd (Nat.card G) -> IsSolvable G

/-- The exact target exposes mathlib's derived-series definition of solvability. -/
theorem exactTarget_iff_derivedSeries :
    ExactTarget.{u} <->
      forall (G : Type u) [Group G] [Finite G],
        Odd (Nat.card G) -> exists n : Nat, derivedSeries G n = (⊥ : Subgroup G) := by
  simp only [ExactTarget, isSolvable_def]

/-- Pinned mathlib closes the commutative subdomain, not the unrestricted odd-order target. -/
theorem commutative_special_case
    (G : Type u) [CommGroup G] [Finite G]
    (_hodd : Odd (Nat.card G)) : IsSolvable G := by
  exact CommGroup.isSolvable

#check IsSolvable
#check isSolvable_def
#check derivedSeries
#check CommGroup.isSolvable
#check isSolvable_of_comm
#check solvable_of_ker_le_range
#check solvable_of_solvable_injective
#check solvable_of_surjective

#print axioms exactTarget_iff_derivedSeries
#print axioms CommGroup.isSolvable
#print axioms commutative_special_case

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0070_AnchorAudit
