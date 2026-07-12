import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Analysis.Convex.Basic

/-!
# THM-M-0318: exact Schauder fixed-point statement

This module freezes the compact-convex formulation selected by intake. It
contains statement checks only, not a proof of Schauder's theorem.
-/

namespace Stage1Instances.THM_M_0318

universe u

/-- A continuous self-map of a nonempty compact convex subset of a real
normed vector space has a fixed point in that subset. -/
def SchauderFixedPointTarget : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (K : Set E) (f : E → E),
      K.Nonempty → IsCompact K → Convex ℝ K →
        ContinuousOn f K → Set.MapsTo f K K →
          ∃ x : E, x ∈ K ∧ f x = x

/-- Direct expansion of the selected mathematical claim. -/
def ExpandedTarget : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (K : Set E) (f : E → E),
      (∃ x : E, x ∈ K) → IsCompact K → Convex ℝ K →
        ContinuousOn f K → (∀ x : E, x ∈ K → f x ∈ K) →
          ∃ x : E, x ∈ K ∧ f x = x

/-- Checked transport between the canonical API spelling and its direct
binder-level expansion. This proves statement identity only. -/
theorem target_iff_expanded :
    SchauderFixedPointTarget.{u} ↔ ExpandedTarget.{u} := by
  rfl

-- Separately elaborated, deliberately non-equivalent structural mutations.
def mutationRemovedCompactness : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (K : Set E) (f : E → E),
      K.Nonempty → Convex ℝ K → ContinuousOn f K →
        Set.MapsTo f K K → ∃ x : E, x ∈ K ∧ f x = x

def mutationChangedDomainToRealLine : Prop :=
  ∀ (K : Set ℝ) (f : ℝ → ℝ),
    K.Nonempty → IsCompact K → Convex ℝ K →
      ContinuousOn f K → Set.MapsTo f K K →
        ∃ x : ℝ, x ∈ K ∧ f x = x

def mutationChangedBinderScope : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (K : Set E),
      K.Nonempty → IsCompact K → Convex ℝ K →
        ∃ x : E, x ∈ K ∧ ∀ f : E → E,
          ContinuousOn f K → Set.MapsTo f K K → f x = x

def mutationRemovedSelfMap : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (K : Set E) (f : E → E),
      K.Nonempty → IsCompact K → Convex ℝ K →
        ContinuousOn f K → ∃ x : E, x ∈ K ∧ f x = x

/-- The empty-set boundary is excluded exactly by `K.Nonempty`. -/
theorem empty_boundary (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E] :
    ¬ (∅ : Set E).Nonempty := by
  simp

/-- On a singleton, preservation of the set already forces its sole point to
be fixed; this checks that the conclusion includes membership in `K`. -/
theorem singleton_boundary
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (a : E) (f : E → E) (hf : Set.MapsTo f ({a} : Set E) {a}) :
    ∃ x : E, x ∈ ({a} : Set E) ∧ f x = x := by
  refine ⟨a, by simp, ?_⟩
  simpa using hf (by simp)

end Stage1Instances.THM_M_0318

set_option pp.explicit true in
#print Stage1Instances.THM_M_0318.SchauderFixedPointTarget
