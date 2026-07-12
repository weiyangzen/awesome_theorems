import Statement

/-!
# THM-M-0161 conditional obligation composition

This file checks only the final conjunction boundary selected by the frozen
architecture. Existence and uniqueness remain explicit proof obligations.
-/

namespace Stage1Instances.THM_M_0161

/-- The exact existence half of the canonical target. -/
def ExistencePackage : Prop :=
  forall (a b : Real), a < b -> forall (kappa tau : Real -> Real),
    DifferentiableOn Real kappa (Set.Ioo a b) ->
    DifferentiableOn Real tau (Set.Ioo a b) ->
    (∀ s ∈ Set.Ioo a b, 0 < kappa s) ->
    exists c : Real -> E3, RealizesInvariants a b kappa tau c

/-- The exact uniqueness half, with all canonical hypotheses repeated. -/
def UniquenessPackage : Prop :=
  forall (a b : Real), a < b -> forall (kappa tau : Real -> Real),
    DifferentiableOn Real kappa (Set.Ioo a b) ->
    DifferentiableOn Real tau (Set.Ioo a b) ->
    (∀ s ∈ Set.Ioo a b, 0 < kappa s) ->
    forall c1 c2 : Real -> E3,
      RealizesInvariants a b kappa tau c1 ->
      RealizesInvariants a b kappa tau c2 ->
      RelatedByProperRigidMotion a b c1 c2

/-- Checked composition of the two open packages into the exact root. -/
theorem root_of_existence_and_uniqueness
    (existence : ExistencePackage) (uniqueness : UniquenessPackage) :
    FundamentalTheoremOfSpaceCurvesTarget := by
  intro a b hab kappa tau hkappa htau hpositive
  exact ⟨existence a b hab kappa tau hkappa htau hpositive,
    uniqueness a b hab kappa tau hkappa htau hpositive⟩

#print axioms root_of_existence_and_uniqueness

end Stage1Instances.THM_M_0161
