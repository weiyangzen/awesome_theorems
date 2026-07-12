import Statement

/-!
# THM-M-0322 checked obligation composition

This module checks the final two-inclusion composition chosen by the frozen
architecture. The reverse inclusion remains an explicit premise here; its
proof body is owned by the later proof phase.
-/

namespace Stage1Instances.THM_M_0322

open Set

universe u

/-- The closed convex hull of the extreme points is contained in the compact
convex set. This is the elementary inclusion in the pinned proof. -/
theorem hullExtreme_subset
    (E : Type u) [AddCommGroup E] [Module Real E] [TopologicalSpace E]
    [T2Space E] [IsTopologicalAddGroup E] [ContinuousSMul Real E]
    [LocallyConvexSpace Real E] (s : Set E)
    (hscomp : IsCompact s) (hconv : Convex Real s) :
    closure (convexHull Real (s.extremePoints Real)) ⊆ s := by
  exact closure_minimal (convexHull_min extremePoints_subset hconv) hscomp.isClosed

/-- Exact parent composition from the two directional packages. This consumes
both children and introduces no mathematical premise besides their outputs. -/
theorem root_of_inclusions
    (E : Type u) [AddCommGroup E] [Module Real E] [TopologicalSpace E]
    [T2Space E] [IsTopologicalAddGroup E] [ContinuousSMul Real E]
    [LocallyConvexSpace Real E] (s : Set E)
    (hscomp : IsCompact s) (hconv : Convex Real s)
    (forward : closure (convexHull Real (s.extremePoints Real)) ⊆ s)
    (reverse : s ⊆ closure (convexHull Real (s.extremePoints Real))) :
    closure (convexHull Real (s.extremePoints Real)) = s := by
  exact Set.Subset.antisymm forward reverse

#print axioms hullExtreme_subset
#print axioms root_of_inclusions

end Stage1Instances.THM_M_0322
