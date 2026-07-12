import Mathlib.Analysis.Convex.KreinMilman

/-!
# THM-M-0322: exact Krein-Milman statement

This module freezes and tests the statement boundary only. The checked wrapper
identifies the target with the pinned mathlib declaration; it adds no new proof
of the Krein-Milman theorem.
-/

namespace Stage1Instances.THM_M_0322

open Set

universe u

/-- The exact target selected at intake for the Krein-Milman theorem. -/
def KreinMilmanTarget : Prop :=
  forall (E : Type u) [AddCommGroup E] [Module Real E] [TopologicalSpace E]
    [T2Space E] [IsTopologicalAddGroup E] [ContinuousSMul Real E]
    [LocallyConvexSpace Real E] (s : Set E),
      IsCompact s ->
      Convex Real s ->
      closure (convexHull Real (s.extremePoints Real)) = s

/-- The pinned mathlib declaration has exactly the frozen target. -/
theorem kreinMilmanTarget_of_pinned : KreinMilmanTarget := by
  intro E _ _ _ _ _ _ _ s hscomp hconv
  exact closure_convexHull_extremePoints hscomp hconv

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedCompactness : Prop :=
  forall (E : Type u) [AddCommGroup E] [Module Real E] [TopologicalSpace E]
    [T2Space E] [IsTopologicalAddGroup E] [ContinuousSMul Real E]
    [LocallyConvexSpace Real E] (s : Set E),
      Convex Real s ->
      closure (convexHull Real (s.extremePoints Real)) = s

def mutationChangedDomainToReal : Prop :=
  forall (s : Set Real),
    IsCompact s ->
    Convex Real s ->
    closure (convexHull Real (s.extremePoints Real)) = s

def mutationChangedBinderScope : Prop :=
  forall (E : Type u) [AddCommGroup E] [Module Real E] [TopologicalSpace E]
    [T2Space E] [IsTopologicalAddGroup E] [ContinuousSMul Real E]
    [LocallyConvexSpace Real E],
      (forall s : Set E, IsCompact s) ->
      forall s : Set E,
        Convex Real s ->
        closure (convexHull Real (s.extremePoints Real)) = s

def mutationNonemptyBoundary : Prop :=
  forall (E : Type u) [AddCommGroup E] [Module Real E] [TopologicalSpace E]
    [T2Space E] [IsTopologicalAddGroup E] [ContinuousSMul Real E]
    [LocallyConvexSpace Real E] (s : Set E),
      s.Nonempty ->
      IsCompact s ->
      Convex Real s ->
      closure (convexHull Real (s.extremePoints Real)) = s

/-- The empty set is deliberately in scope; no nonemptiness premise is needed. -/
theorem empty_boundary
    (E : Type u) [AddCommGroup E] [Module Real E] [TopologicalSpace E]
    [T2Space E] [IsTopologicalAddGroup E] [ContinuousSMul Real E]
    [LocallyConvexSpace Real E] :
    closure (convexHull Real ((∅ : Set E).extremePoints Real)) = (∅ : Set E) := by
  exact closure_convexHull_extremePoints isCompact_empty convex_empty

end Stage1Instances.THM_M_0322

set_option pp.explicit true in
#print Stage1Instances.THM_M_0322.KreinMilmanTarget
