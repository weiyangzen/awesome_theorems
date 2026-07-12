import Mathlib.ModelTheory.Satisfiability

/-!
# THM-M-0644 independent validation probe

This probe does not import the local proof module. It reconstructs the frozen compactness root
directly from the pinned mathlib declaration so that validation checks the terminal dependency and
the root type independently of the proof wrapper.
-/

namespace Stage1.THM_M_0644.Validation

open FirstOrder

universe u v

def Root : Prop :=
  forall {L : Language.{u, v}} {T : L.Theory},
    T.IsSatisfiable <-> T.IsFinitelySatisfiable

theorem independentRoot : Root := by
  intro L T
  exact FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable

theorem independentRootExactType :
    forall {L : Language.{u, v}} {T : L.Theory},
      T.IsSatisfiable <-> T.IsFinitelySatisfiable :=
  independentRoot

#check FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable
#print axioms FirstOrder.Language.Theory.isSatisfiable_iff_isFinitelySatisfiable
#print axioms independentRoot

end Stage1.THM_M_0644.Validation
