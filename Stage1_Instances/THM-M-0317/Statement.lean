import Mathlib.Topology.Algebra.Module.LocallyConvex
import Mathlib.Dynamics.FixedPoints.Basic

/-!
The exact target is Tychonoff's 1935 real, Hausdorff formulation.  The source's
"bikompakt" is represented by `IsCompact`; nonemptiness is explicit because it
is required for the conclusion and is not part of mathlib's `IsCompact`.
-/

universe u

namespace AwesomeTheorems.THM_M_0317

def TychonoffFixedPointTarget {E : Type u} [AddCommGroup E] [Module ℝ E]
    [TopologicalSpace E] [IsTopologicalAddGroup E] [ContinuousSMul ℝ E]
    [T2Space E] [LocallyConvexSpace ℝ E] (K : Set E) (f : E → E) : Prop :=
  K.Nonempty →
    IsCompact K →
      Convex ℝ K →
        Continuous f →
          Set.MapsTo f K K →
            ∃ x ∈ K, Function.IsFixedPt f x

def subtypeSelfMap {E : Type u} (K : Set E) (f : E → E) (hfK : Set.MapsTo f K K) : K → K :=
  fun x ↦ ⟨f x, hfK x.property⟩

theorem ambient_subtype_fixed_point_iff {E : Type u} (K : Set E) (f : E → E)
    (hfK : Set.MapsTo f K K) :
    (∃ x ∈ K, Function.IsFixedPt f x) ↔
      ∃ x : K, Function.IsFixedPt (subtypeSelfMap K f hfK) x := by
  constructor
  · rintro ⟨x, hxK, hx⟩
    exact ⟨⟨x, hxK⟩, Subtype.ext hx⟩
  · rintro ⟨x, hx⟩
    exact ⟨x, x.property, congrArg Subtype.val hx⟩

-- Boundary mutation: compactness and convexity do not make the empty set admissible.
theorem empty_boundary_rejects_removed_nonempty :
    ¬ (IsCompact (∅ : Set ℝ) → Convex ℝ (∅ : Set ℝ) →
      Continuous (id : ℝ → ℝ) → Set.MapsTo id (∅ : Set ℝ) ∅ →
        ∃ x ∈ (∅ : Set ℝ), Function.IsFixedPt id x) := by
  intro h
  rcases h isCompact_empty convex_empty continuous_id (by simp) with ⟨x, hx, _⟩
  exact hx

-- Domain mutation: an ambient fixed point cannot replace membership in the compact convex set.
theorem ambient_domain_does_not_imply_member_domain :
    ¬ ((∃ x : ℝ, Function.IsFixedPt id x) →
      ∃ x ∈ (∅ : Set ℝ), Function.IsFixedPt id x) := by
  intro h
  rcases h ⟨0, rfl⟩ with ⟨x, hx, _⟩
  exact hx

-- Binder-scope mutation: one point cannot be fixed by every self-map.
theorem fixed_point_cannot_precede_map_binder :
    ¬ (∃ x : Bool, ∀ f : Bool → Bool, Function.IsFixedPt f x) := by
  rintro ⟨x, hx⟩
  exact (Bool.not_eq_self x).mp (hx fun y ↦ !y)

-- Invariance mutation: a continuous map need not fix a point of a compact convex set it leaves.
theorem interval_rejects_removed_mapsTo :
    ¬ (∃ x ∈ Set.Icc (0 : ℝ) 1, Function.IsFixedPt (fun y : ℝ ↦ y + 2) x) := by
  simp [Function.IsFixedPt]

set_option pp.universes true in
#print TychonoffFixedPointTarget

set_option pp.universes true in
#print ambient_subtype_fixed_point_iff

end AwesomeTheorems.THM_M_0317
