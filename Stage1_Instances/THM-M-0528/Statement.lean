import Mathlib.Topology.Covering.Basic

set_option autoImplicit false

namespace Stage1Instances.THM_M_0528

universe u v w

/-- Uniqueness of two lifts through a covering map after agreement at one point. -/
def CoveringLiftUniquenessTarget : Prop :=
  ∀ (E : Type u) (X : Type v) (A : Type w),
    ∀ [TopologicalSpace E] [TopologicalSpace X] [TopologicalSpace A]
      [PreconnectedSpace A],
      ∀ (p : E → X), IsCoveringMap p →
        ∀ (g₁ g₂ : A → E), Continuous g₁ → Continuous g₂ →
          p ∘ g₁ = p ∘ g₂ → ∀ a : A, g₁ a = g₂ a → g₁ = g₂

/-- The same target with the projection equation written pointwise. -/
def PointwiseProjectionEncoding : Prop :=
  ∀ (E : Type u) (X : Type v) (A : Type w),
    ∀ [TopologicalSpace E] [TopologicalSpace X] [TopologicalSpace A]
      [PreconnectedSpace A],
      ∀ (p : E → X), IsCoveringMap p →
        ∀ (g₁ g₂ : A → E), Continuous g₁ → Continuous g₂ →
          (∀ x : A, p (g₁ x) = p (g₂ x)) → ∀ a : A, g₁ a = g₂ a → g₁ = g₂

theorem coveringLiftUniquenessTarget_iff_pointwiseProjectionEncoding :
    CoveringLiftUniquenessTarget.{u, v, w} ↔
      PointwiseProjectionEncoding.{u, v, w} := by
  constructor
  · intro h E X A _ _ _ _ p hp g₁ g₂ hg₁ hg₂ hproj a ha
    exact h E X A p hp g₁ g₂ hg₁ hg₂ (funext hproj) a ha
  · intro h E X A _ _ _ _ p hp g₁ g₂ hg₁ hg₂ hproj a ha
    exact h E X A p hp g₁ g₂ hg₁ hg₂ (congrFun hproj) a ha

def mutationRemovedPreconnectedness : Prop :=
  ∀ (E : Type u) (X : Type v) (A : Type w),
    ∀ [TopologicalSpace E] [TopologicalSpace X] [TopologicalSpace A],
      ∀ (p : E → X), IsCoveringMap p →
        ∀ (g₁ g₂ : A → E), Continuous g₁ → Continuous g₂ →
          p ∘ g₁ = p ∘ g₂ → ∀ a : A, g₁ a = g₂ a → g₁ = g₂

def mutationRemovedContinuityOfSecondLift : Prop :=
  ∀ (E : Type u) (X : Type v) (A : Type w),
    ∀ [TopologicalSpace E] [TopologicalSpace X] [TopologicalSpace A]
      [PreconnectedSpace A],
      ∀ (p : E → X), IsCoveringMap p →
        ∀ (g₁ g₂ : A → E), Continuous g₁ →
          p ∘ g₁ = p ∘ g₂ → ∀ a : A, g₁ a = g₂ a → g₁ = g₂

def mutationRemovedInitialAgreement : Prop :=
  ∀ (E : Type u) (X : Type v) (A : Type w),
    ∀ [TopologicalSpace E] [TopologicalSpace X] [TopologicalSpace A]
      [PreconnectedSpace A],
      ∀ (p : E → X), IsCoveringMap p →
        ∀ (g₁ g₂ : A → E), Continuous g₁ → Continuous g₂ →
          p ∘ g₁ = p ∘ g₂ → g₁ = g₂

def mutationChangedConclusionToAgreementAtWitness : Prop :=
  ∀ (E : Type u) (X : Type v) (A : Type w),
    ∀ [TopologicalSpace E] [TopologicalSpace X] [TopologicalSpace A]
      [PreconnectedSpace A],
      ∀ (p : E → X), IsCoveringMap p →
        ∀ (g₁ g₂ : A → E), Continuous g₁ → Continuous g₂ →
          p ∘ g₁ = p ∘ g₂ → ∀ a : A, g₁ a = g₂ a → g₁ a = g₂ a

#check IsCoveringMap.eq_of_comp_eq
#print Stage1Instances.THM_M_0528.CoveringLiftUniquenessTarget

end Stage1Instances.THM_M_0528
