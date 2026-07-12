import Mathlib.Combinatorics.SimpleGraph.Regularity.Lemma

/-!
# THM-M-0843 immutable mathlib anchor

This module checks the exact effective regularity target against the pinned
mathlib theorem. It is anchor-audit evidence, not an accepted proof or release
declaration.
-/

namespace Stage1Instances.THM_M_0843_AnchorAudit

universe u

/-- A literal copy of the frozen statement-phase proposition. -/
def ExactTarget : Prop :=
  ∀ {alpha : Type u} [DecidableEq alpha] [Fintype alpha]
    (G : SimpleGraph alpha) [DecidableRel G.Adj] {epsilon : Real} {l : Nat},
    0 < epsilon ->
    l <= Fintype.card alpha ->
    ∃ P : Finpartition (Finset.univ : Finset alpha),
      P.IsEquipartition /\
      l <= P.parts.card /\
      P.parts.card <= SzemerediRegularity.bound epsilon l /\
      P.IsUniform G epsilon

/-- Exact wrapper over the pinned mathlib terminal theorem. -/
theorem exactTarget_mathlib_candidate : ExactTarget.{u} := by
  intro alpha _ _ G _ epsilon l hEpsilon hCard
  exact szemeredi_regularity G hEpsilon hCard

#check szemeredi_regularity
#print sorries szemeredi_regularity
#print axioms szemeredi_regularity
#print axioms Stage1Instances.THM_M_0843_AnchorAudit.exactTarget_mathlib_candidate

end Stage1Instances.THM_M_0843_AnchorAudit
