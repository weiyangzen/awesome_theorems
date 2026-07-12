import Statement

/-!
# THM-M-0698 conditional obligation composition

This module checks the logical interfaces selected by the frozen obligation
architecture. The difficult finite-satisfiability-to-model direction remains
an explicit premise here; the imported compactness theorem is not invoked.
-/

namespace Stage1Instances.THM_M_0698

open FirstOrder

universe u v

/-- The elementary direction, separated from the compactness construction. -/
def SatisfiableToFinite : Prop :=
  forall {L : FirstOrder.Language.{u, v}} {T : L.Theory},
    T.IsSatisfiable -> T.IsFinitelySatisfiable

/-- The substantive compactness direction delivered by the ultraproduct route. -/
def FiniteToSatisfiable : Prop :=
  forall {L : FirstOrder.Language.{u, v}} {T : L.Theory},
    T.IsFinitelySatisfiable -> T.IsSatisfiable

/-- Monotonicity supplies the forward compactness direction without using compactness. -/
theorem satisfiableToFinite_checked : SatisfiableToFinite.{u, v} := by
  intro L T h
  exact h.isFinitelySatisfiable

/-- Checked parent composition: the two directions yield the exact frozen root. -/
theorem firstOrderCompactness_of_directions
    (forward : SatisfiableToFinite.{u, v})
    (reverse : FiniteToSatisfiable.{u, v}) :
    FirstOrderCompactnessTarget.{u, v} := by
  intro L T
  exact ⟨forward, reverse⟩

#print axioms satisfiableToFinite_checked
#print axioms firstOrderCompactness_of_directions

end Stage1Instances.THM_M_0698
