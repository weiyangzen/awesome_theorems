import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Analysis.Convex.Basic
import Mathlib.Topology.Order.Compact

/-!
# THM-M-0318 proof bodies

This module implements the compact-limit half of the frozen Schauder proof
architecture.  The finite-dimensional approximation half remains open.
-/

namespace Stage1Instances.THM_M_0318

universe u

def HasApproximateFixedPoints
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (K : Set E) (f : E → E) : Prop :=
  ∀ ε : ℝ, 0 < ε → ∃ x : E, x ∈ K ∧ dist (f x) x < ε

def CompactLimitEngine : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (K : Set E) (f : E → E),
      IsCompact K → ContinuousOn f K → HasApproximateFixedPoints E K f →
        ∃ x : E, x ∈ K ∧ f x = x

/-- The displacement function attains its minimum on `K`; approximate fixed
points force that minimum to be zero.  This closes the compactness and
continuity half of the frozen proof architecture without a sequence choice. -/
theorem compactLimitEngine : CompactLimitEngine.{u} := by
  intro E _ _ K f hcompact hcont happrox
  have hne : K.Nonempty := by
    obtain ⟨x, hx, _⟩ := happrox 1 zero_lt_one
    exact ⟨x, hx⟩
  obtain ⟨x, hxK, hxMin⟩ := hcompact.exists_isMinOn
    hne (fun y hy => (hcont y hy).dist continuousWithinAt_id)
  have hxZero : dist (f x) x = 0 := by
    apply le_antisymm
    · by_contra hnot
      have hxPos : 0 < dist (f x) x := lt_of_not_ge hnot
      obtain ⟨y, hyK, hy⟩ := happrox (dist (f x) x) hxPos
      exact (not_lt_of_ge (hxMin hyK)) hy
    · exact dist_nonneg
  exact ⟨x, hxK, dist_eq_zero.mp hxZero⟩

end Stage1Instances.THM_M_0318

set_option pp.explicit true in
#check Stage1Instances.THM_M_0318.compactLimitEngine

set_option pp.universes true in
#print axioms Stage1Instances.THM_M_0318.compactLimitEngine
