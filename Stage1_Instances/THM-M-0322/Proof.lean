import ObligationTree

/-!
# THM-M-0322 proof-phase closure

The exact frozen target is discharged by the Krein-Milman proof in the pinned
mathlib revision.  The local declarations also expose the reverse inclusion
and the frozen two-inclusion composition, so neither direction is hidden in a
changed statement or an extra premise.
-/

namespace Stage1Instances.THM_M_0322

open Set

universe u

/-- The nontrivial inclusion, obtained from the pinned exact Krein-Milman body. -/
theorem hullExtreme_superset
    (E : Type u) [AddCommGroup E] [Module Real E] [TopologicalSpace E]
    [T2Space E] [IsTopologicalAddGroup E] [ContinuousSMul Real E]
    [LocallyConvexSpace Real E] (s : Set E)
    (hscomp : IsCompact s) (hconv : Convex Real s) :
    s ⊆ closure (convexHull Real (s.extremePoints Real)) := by
  rw [closure_convexHull_extremePoints hscomp hconv]

/-- Unconditional proof of the exact target frozen in `Statement.lean`. -/
theorem kreinMilmanTarget_proof : KreinMilmanTarget := by
  intro E _ _ _ _ _ _ _ s hscomp hconv
  exact root_of_inclusions E s hscomp hconv
    (hullExtreme_subset E s hscomp hconv)
    (hullExtreme_superset E s hscomp hconv)

#print axioms hullExtreme_superset
#print axioms kreinMilmanTarget_proof

end Stage1Instances.THM_M_0322
