import Mathlib.Analysis.Normed.Module.Basic
import Mathlib.Analysis.Convex.Basic

/-!
# THM-M-0318 obligation composition harness

This file checks only the interfaces and composition of the frozen Schauder
architecture.  Its hypotheses are deliberately abstract: it is not a proof of
Schauder's theorem and supplies no machine credit to an open leaf.
-/

namespace Stage1Instances.THM_M_0318

universe u

/-- Re-elaboration of the frozen root inside the standalone composition
harness. `check_obligation_tree.py` verifies this binder text against
`Statement.lean`; it is not a substitute theorem. -/
def ExactSchauderTarget : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (K : Set E) (f : E → E),
      K.Nonempty → IsCompact K → Convex ℝ K →
        ContinuousOn f K → Set.MapsTo f K K →
          ∃ x : E, x ∈ K ∧ f x = x

/-- The analytic output required from the finite-dimensional approximation
and Brouwer branches. -/
def HasApproximateFixedPoints
    (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (K : Set E) (f : E → E) : Prop :=
  ∀ ε : ℝ, 0 < ε → ∃ x : E, x ∈ K ∧ dist (f x) x < ε

/-- Typed interface for the construction/Brouwer half of the proof. -/
def ApproximationEngine : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (K : Set E) (f : E → E),
      K.Nonempty → IsCompact K → Convex ℝ K → ContinuousOn f K →
        Set.MapsTo f K K → HasApproximateFixedPoints E K f

/-- Typed interface for the compactness/continuity limit half of the proof. -/
def CompactLimitEngine : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (K : Set E) (f : E → E),
      IsCompact K → ContinuousOn f K → HasApproximateFixedPoints E K f →
        ∃ x : E, x ∈ K ∧ f x = x

/-- Checked parent composition: the two open mathematical engines together
yield exactly the statement frozen in `Statement.lean`. -/
theorem compose_schauder
    (hApprox : ApproximationEngine.{u})
    (hLimit : CompactLimitEngine.{u}) :
    ExactSchauderTarget.{u} := by
  intro E _ _ K f hne hcompact hconv hcont hmap
  exact hLimit E K f hcompact hcont
    (hApprox E K f hne hcompact hconv hcont hmap)

end Stage1Instances.THM_M_0318

set_option pp.explicit true in
#check Stage1Instances.THM_M_0318.compose_schauder
