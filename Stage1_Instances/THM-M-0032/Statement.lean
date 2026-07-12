import Mathlib.RingTheory.RegularLocalRing.Defs

/-!
# THM-M-0032 canonical Lean statement

This module freezes the unrestricted commutative-ring formulation of the Auslander-Buchsbaum
unique-factorization theorem selected at intake. It contains a checked statement transport and
mutation fixtures, but no proof of the canonical target.
-/

namespace Stage1Instances.THM_M_0032

universe u

/-- Every regular local ring is a unique factorization domain. -/
def AuslanderBuchsbaumUFDTarget : Prop :=
  forall (R : Type u) [CommRing R] [IsRegularLocalRing R],
    UniqueFactorizationMonoid R

/-- The same claim with regularity passed as an explicit proposition rather than an instance. -/
def ExplicitRegularityTarget : Prop :=
  forall (R : Type u) [CommRing R],
    IsRegularLocalRing R -> UniqueFactorizationMonoid R

/-- Checked transport between instance-binder and explicit-hypothesis formulations. -/
theorem auslanderBuchsbaumUFDTarget_iff_explicitRegularityTarget :
    AuslanderBuchsbaumUFDTarget.{u} <-> ExplicitRegularityTarget.{u} := by
  constructor
  · intro h R _ hregular
    letI : IsRegularLocalRing R := hregular
    exact h R
  · intro h R _ _
    exact h R inferInstance

/-! Structural mutations elaborate as propositions but receive no statement-identity credit. -/

def mutationRemovedRegularityHypothesis : Prop :=
  forall (R : Type u) [CommRing R],
    UniqueFactorizationMonoid R

def mutationChangedDomainToField : Prop :=
  forall (K : Type u) [Field K] [IsRegularLocalRing K],
    UniqueFactorizationMonoid K

def mutationChangedBinderScope : Prop :=
  exists R : Type u,
    forall [CommRing R] [IsRegularLocalRing R], UniqueFactorizationMonoid R

def mutationExcludedFieldBoundary : Prop :=
  forall (R : Type u) [CommRing R] [IsRegularLocalRing R],
    Not (IsField R) -> UniqueFactorizationMonoid R

variable
  (hCanonical : AuslanderBuchsbaumUFDTarget.{u})
  (hDomain : mutationChangedDomainToField.{u})
  (hScope : mutationChangedBinderScope.{u})
  (hBoundary : mutationExcludedFieldBoundary.{u})

#check_failure (show mutationRemovedRegularityHypothesis.{u} from hCanonical)
#check_failure (show AuslanderBuchsbaumUFDTarget.{u} from hDomain)
#check_failure (show AuslanderBuchsbaumUFDTarget.{u} from hScope)
#check_failure (show AuslanderBuchsbaumUFDTarget.{u} from hBoundary)

/-! Boundary witnesses authenticate which rings satisfy the target's antecedent only. -/

/-- The rational field is a zero-dimensional regular local ring and is not excluded. -/
example : IsRegularLocalRing Rat := inferInstance
example : IsField Rat := Field.toIsField Rat

#check auslanderBuchsbaumUFDTarget_iff_explicitRegularityTarget
#print axioms auslanderBuchsbaumUFDTarget_iff_explicitRegularityTarget

set_option pp.universes true in
set_option pp.explicit true in
#print AuslanderBuchsbaumUFDTarget

end Stage1Instances.THM_M_0032
