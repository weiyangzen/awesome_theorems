import Mathlib.ModelTheory.Satisfiability

/-!
# THM-M-0698: exact first-order compactness statement

This module freezes and tests the statement boundary only. It does not claim
proof credit for the compactness theorem imported from mathlib.
-/

namespace Stage1Instances.THM_M_0698

open FirstOrder

universe u v

/-- The exact semantic compactness target selected at intake. -/
def FirstOrderCompactnessTarget : Prop :=
  forall {L : FirstOrder.Language.{u, v}} {T : L.Theory},
    T.IsSatisfiable <-> T.IsFinitelySatisfiable

/-- Checked identity with the exact type of the pinned mathlib declaration. -/
theorem firstOrderCompactnessTarget_iff_pinnedMathlibType :
    FirstOrderCompactnessTarget.{u, v} <->
      (forall {L : FirstOrder.Language.{u, v}} {T : L.Theory},
        T.IsSatisfiable <-> T.IsFinitelySatisfiable) := by
  rfl

/-- Direct expansion of finite satisfiability into finite subtheories. -/
def ExpandedFiniteSubtheoryShape : Prop :=
  forall {L : FirstOrder.Language.{u, v}} {T : L.Theory},
    T.IsSatisfiable <->
      forall T0 : Finset L.Sentence,
        (T0 : L.Theory) ⊆ T ->
          FirstOrder.Language.Theory.IsSatisfiable (T0 : L.Theory)

/-- Checked identity between the canonical API predicate and its direct expansion. -/
theorem firstOrderCompactnessTarget_iff_expandedFiniteSubtheoryShape :
    FirstOrderCompactnessTarget.{u, v} <-> ExpandedFiniteSubtheoryShape.{u, v} := by
  simp only [FirstOrderCompactnessTarget, ExpandedFiniteSubtheoryShape,
    FirstOrder.Language.Theory.IsFinitelySatisfiable]

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedContainmentHypothesis : Prop :=
  forall {L : FirstOrder.Language.{u, v}} {T : L.Theory},
    T.IsSatisfiable <->
      forall T0 : Finset L.Sentence,
        FirstOrder.Language.Theory.IsSatisfiable (T0 : L.Theory)

def mutationChangedFiniteDomain : Prop :=
  forall {L : FirstOrder.Language.{u, v}} {T : L.Theory},
    T.IsSatisfiable <->
      forall T0 : L.Theory, T0.Finite -> T0 ⊆ T -> T0.IsSatisfiable

def mutationChangedBinderScope : Prop :=
  forall {L : FirstOrder.Language.{u, v}} {T : L.Theory},
    T.IsSatisfiable <->
      (forall T0 : Finset L.Sentence, (T0 : L.Theory) ⊆ T) ->
        forall T0 : Finset L.Sentence,
          FirstOrder.Language.Theory.IsSatisfiable (T0 : L.Theory)

def mutationExcludesEmptySubtheory : Prop :=
  forall {L : FirstOrder.Language.{u, v}} {T : L.Theory},
    T.IsSatisfiable <->
      forall T0 : Finset L.Sentence,
        T0.Nonempty -> (T0 : L.Theory) ⊆ T ->
          FirstOrder.Language.Theory.IsSatisfiable (T0 : L.Theory)

end Stage1Instances.THM_M_0698

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0698.FirstOrderCompactnessTarget
