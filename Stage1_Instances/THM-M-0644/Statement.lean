import Mathlib.ModelTheory.Satisfiability

/-!
Exact statement certificate for first-order compactness. This file freezes only the target and
its encodings; it does not claim the upstream proof or any later rev-5.6 gate.
-/

namespace Stage1.THM_M_0644

open FirstOrder

universe u v

/-- A first-order theory has a model exactly when each finite subtheory has a model. -/
def CompactnessTarget : Prop :=
  ∀ {L : Language.{u, v}} {T : L.Theory}, T.IsSatisfiable ↔ T.IsFinitelySatisfiable

/-- Direct expansion of mathlib's finite-satisfiability predicate. -/
def FinsetExpandedTarget (L : Language.{u, v}) (T : L.Theory) : Prop :=
  T.IsSatisfiable ↔
    ∀ T₀ : Finset L.Sentence, (T₀ : L.Theory) ⊆ T →
      FirstOrder.Language.Theory.IsSatisfiable (T₀ : L.Theory)

/-- The repository wording using finite `Set`s rather than `Finset`s. -/
def FiniteSetTarget (L : Language.{u, v}) (T : L.Theory) : Prop :=
  T.IsSatisfiable ↔
    ∀ T₀ : L.Theory, T₀ ⊆ T → T₀.Finite → T₀.IsSatisfiable

theorem target_iff_finsetExpanded {L : Language.{u, v}} {T : L.Theory} :
    (T.IsSatisfiable ↔ T.IsFinitelySatisfiable) ↔ FinsetExpandedTarget L T := by
  unfold FinsetExpandedTarget FirstOrder.Language.Theory.IsFinitelySatisfiable
  rfl

theorem finiteSet_iff_finset {L : Language.{u, v}} {T : L.Theory} :
    (∀ T₀ : L.Theory, T₀ ⊆ T → T₀.Finite → T₀.IsSatisfiable) ↔
      T.IsFinitelySatisfiable := by
  unfold FirstOrder.Language.Theory.IsFinitelySatisfiable
  constructor
  · intro h T₀ hsub
    exact h (T₀ : L.Theory) hsub T₀.finite_toSet
  · intro h T₀ hsub hfinite
    have heq : (hfinite.toFinset : L.Theory) = T₀ := by
      ext x
      simp
    have hsub' : (hfinite.toFinset : L.Theory) ⊆ T := by
      simpa only [heq] using hsub
    simpa only [heq] using h hfinite.toFinset hsub'

#check CompactnessTarget
#print CompactnessTarget

namespace Mutations

def RemovedContainment : Prop :=
  ∀ {L : Language.{u, v}} {T : L.Theory},
    T.IsSatisfiable ↔ ∀ T₀ : Finset L.Sentence,
      FirstOrder.Language.Theory.IsSatisfiable (T₀ : L.Theory)

def ChangedSentenceDomain : Prop :=
  ∀ {L : Language.{u, v}} {T : L.Theory},
    T.IsSatisfiable ↔ ∀ T₀ : Finset (L.Term (Fin 0)), True

def ChangedBinderScope : Prop :=
  ∀ {L : Language.{u, v}},
    (∀ T : L.Theory, T.IsSatisfiable) ↔ (∀ T : L.Theory, T.IsFinitelySatisfiable)

def ExcludedEmptyTheory : Prop :=
  ∀ {L : Language.{u, v}} {T : L.Theory},
    T.Nonempty → (T.IsSatisfiable ↔ T.IsFinitelySatisfiable)

#check_failure (rfl : CompactnessTarget = RemovedContainment)
#check_failure (rfl : CompactnessTarget = ChangedSentenceDomain)
#check_failure (rfl : CompactnessTarget = ChangedBinderScope)
#check_failure (rfl : CompactnessTarget = ExcludedEmptyTheory)

end Mutations

end Stage1.THM_M_0644
