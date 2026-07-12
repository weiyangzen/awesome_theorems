import Mathlib.Topology.Covering.Basic

set_option autoImplicit false

namespace Stage1Instances.THM_M_0528

universe u v w

/-!
# THM-M-0528: immutable mathlib anchor probe

This adapter checks that the declaration at the pinned mathlib revision closes
every binder of the frozen target. It is anchor evidence only; the proof phase
owns the canonical wrapper and the validation phase owns the trust closure.
-/
theorem mathlibCandidateAdapter :
    ∀ (E : Type u) (X : Type v) (A : Type w),
      ∀ [TopologicalSpace E] [TopologicalSpace X] [TopologicalSpace A]
        [PreconnectedSpace A],
        ∀ (p : E → X), IsCoveringMap p →
          ∀ (g₁ g₂ : A → E), Continuous g₁ → Continuous g₂ →
            p ∘ g₁ = p ∘ g₂ → ∀ a : A, g₁ a = g₂ a → g₁ = g₂ := by
  intro E X A _ _ _ _ p hp g₁ g₂ hg₁ hg₂ hproj a ha
  exact hp.eq_of_comp_eq hg₁ hg₂ hproj a ha

#check IsCoveringMap.eq_of_comp_eq
#print axioms IsCoveringMap.eq_of_comp_eq
#print axioms mathlibCandidateAdapter

end Stage1Instances.THM_M_0528
