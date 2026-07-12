import Mathlib.RingTheory.Ideal.Operations
import Mathlib.RingTheory.LocalRing.Defs
import Mathlib.RingTheory.Noetherian.Defs

/-!
# THM-M-0030 canonical Lean statement

This module freezes the proper-ideal form of the Krull intersection theorem selected at intake.
It checks a membership-level alternate encoding and statement mutations, but does not import or
invoke a proof of the Krull intersection theorem.
-/

namespace Stage1Instances.THM_M_0030

universe u

/-- The intersection of all natural powers of a proper ideal in a commutative Noetherian local
ring is the zero ideal. -/
def KrullIntersectionTarget : Prop :=
  forall {R : Type u} [CommRing R] [IsNoetherianRing R] [IsLocalRing R]
    (I : Ideal R), I ≠ ⊤ -> (iInf fun n : Nat => I ^ n) = ⊥

/-- Membership-level expansion of the same ideal equality. -/
def MembershipTarget : Prop :=
  forall {R : Type u} [CommRing R] [IsNoetherianRing R] [IsLocalRing R]
    (I : Ideal R), I ≠ ⊤ -> forall x : R, (forall n : Nat, x ∈ I ^ n) -> x = 0

/-- Checked transport between ideal equality and elementwise intersection formulations. -/
theorem krullIntersectionTarget_iff_membershipTarget :
    KrullIntersectionTarget.{u} <-> MembershipTarget.{u} := by
  constructor
  · intro h R _ _ _ I hI x hx
    have hxBot : x ∈ (⊥ : Ideal R) := by
      rw [<- h I hI]
      exact Ideal.mem_iInf.mpr hx
    exact hxBot
  · intro h R _ _ _ I hI
    apply le_antisymm
    · intro x hx
      exact h I hI x (Ideal.mem_iInf.mp hx)
    · exact bot_le

/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

def mutationRemovedPropernessHypothesis : Prop :=
  forall {R : Type u} [CommRing R] [IsNoetherianRing R] [IsLocalRing R]
    (I : Ideal R), (iInf fun n : Nat => I ^ n) = ⊥

def mutationChangedDomainToField : Prop :=
  forall {K : Type u} [Field K] (I : Ideal K),
    I ≠ ⊤ -> (iInf fun n : Nat => I ^ n) = ⊥

def mutationChangedBinderScope : Prop :=
  forall {R : Type u} [CommRing R] [IsNoetherianRing R] [IsLocalRing R],
    exists I : Ideal R, I ≠ ⊤ /\ (iInf fun n : Nat => I ^ n) = ⊥

def mutationExcludedBottomIdeal : Prop :=
  forall {R : Type u} [CommRing R] [IsNoetherianRing R] [IsLocalRing R]
    (I : Ideal R), I ≠ ⊥ -> I ≠ ⊤ -> (iInf fun n : Nat => I ^ n) = ⊥

variable
  (hRemoved : mutationRemovedPropernessHypothesis.{u})
  (hDomain : mutationChangedDomainToField.{u})
  (hScope : mutationChangedBinderScope.{u})
  (hBoundary : mutationExcludedBottomIdeal.{u})

#check_failure (show KrullIntersectionTarget.{u} from hRemoved)
#check_failure (show KrullIntersectionTarget.{u} from hDomain)
#check_failure (show KrullIntersectionTarget.{u} from hScope)
#check_failure (show KrullIntersectionTarget.{u} from hBoundary)

/-- The excluded `I = top` boundary makes the conclusion false in every local ring. -/
theorem topIdeal_is_counterboundary
    (R : Type u) [CommRing R] [IsLocalRing R] :
    (iInf fun n : Nat => (⊤ : Ideal R) ^ n) ≠ ⊥ := by
  have htop : (iInf fun n : Nat => (⊤ : Ideal R) ^ n) = ⊤ := by
    apply top_unique
    exact le_iInf fun n => by simp
  rw [htop]
  exact top_ne_bot

/-- The bottom ideal is proper and remains in the canonical target's scope. -/
theorem bottomIdeal_is_in_scope
    (R : Type u) [CommRing R] [IsLocalRing R] :
    (⊥ : Ideal R) ≠ ⊤ /\ (iInf fun n : Nat => (⊥ : Ideal R) ^ n) = ⊥ := by
  constructor
  · exact bot_ne_top
  · apply le_antisymm
    · exact (iInf_le _ 1).trans (by simp)
    · exact bot_le

#check krullIntersectionTarget_iff_membershipTarget
#print axioms krullIntersectionTarget_iff_membershipTarget
#print axioms topIdeal_is_counterboundary
#print axioms bottomIdeal_is_in_scope

set_option pp.all true in
#print KrullIntersectionTarget

end Stage1Instances.THM_M_0030
