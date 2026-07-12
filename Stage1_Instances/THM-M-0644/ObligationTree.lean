import Mathlib.ModelTheory.Satisfiability

/-!
Conditional composition certificate for the frozen compactness architecture. The two directions
remain explicit inputs here; this phase freezes their dependency structure and does not claim a
new proof of compactness.
-/

namespace Stage1.THM_M_0644.ObligationTree

open FirstOrder

universe u v

def RestrictionDirection : Prop :=
  forall {L : Language.{u, v}} {T : L.Theory},
    T.IsSatisfiable -> T.IsFinitelySatisfiable

def UltraproductDirection : Prop :=
  forall {L : Language.{u, v}} {T : L.Theory},
    T.IsFinitelySatisfiable -> T.IsSatisfiable

/-- The checked parent composition consumes both frozen direction obligations. -/
theorem root_of_directions
    (forward : RestrictionDirection.{u, v})
    (backward : UltraproductDirection.{u, v}) :
    forall {L : Language.{u, v}} {T : L.Theory},
      T.IsSatisfiable <-> T.IsFinitelySatisfiable := by
  intro L T
  exact ⟨forward, backward⟩

#check root_of_directions
#print axioms root_of_directions

end Stage1.THM_M_0644.ObligationTree
