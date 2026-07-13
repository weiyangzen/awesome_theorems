import Mathlib.Combinatorics.SetFamily.KruskalKatona

/-!
# THM-M-0822 anchor-audit probe

This module checks the pinned mathlib Erdős-Ko-Rado terminal theorem and a
literal wrapper for the universal-bound component of the frozen target. The
full maximum target also requires attainment; the audit checker composes this
wrapper with the statement module's checked star witness in a temporary Lean
module. This file is candidate evidence only, not an accepted proof-phase
declaration.
-/

namespace Stage1Instances.THM_M_0822_AnchorAudit

/-- The universal-bound component of the frozen maximum-value target. -/
def UpperBoundTarget : Prop :=
  ∀ (n r : Nat), 1 ≤ r → r ≤ n / 2 →
    ∀ A : Finset (Finset (Fin n)),
      (A : Set (Finset (Fin n))).Intersecting →
      (A : Set (Finset (Fin n))).Sized r →
      A.card ≤ (n - 1).choose (r - 1)

/-- Exact wrapper from the pinned mathlib upper-bound theorem. -/
theorem upperBound_of_pinnedMathlib : UpperBoundTarget := by
  intro n r _hr hhalf A hIntersecting hSized
  exact Finset.erdos_ko_rado hIntersecting hSized hhalf

#check Finset.erdos_ko_rado
#check Finset.kruskal_katona_lovasz_form
#check Finset.iterated_kk
#check Finset.kruskal_katona

#print axioms Finset.erdos_ko_rado
#print axioms upperBound_of_pinnedMathlib

set_option pp.explicit true in
set_option pp.universes true in
#print UpperBoundTarget

end Stage1Instances.THM_M_0822_AnchorAudit
