import Mathlib.Dynamics.Ergodic.Conservative

/-!
The exact rev-5.6 statement gate for THM-M-1521. This file intentionally
contains only the canonical target, statement transports, structural mutations,
and boundary checks. It does not claim proof or release closure.
-/

noncomputable section

open Filter Set

namespace Stage1Instances.THM_M_1521

universe u

def SetRecurrenceConclusion {alpha : Type u} [MeasurableSpace alpha]
    (f : alpha -> alpha) (mu : MeasureTheory.Measure alpha) : Prop :=
  forall s : Set alpha,
    MeasureTheory.NullMeasurableSet s mu ->
      ∀ᵐ x ∂mu,
        x ∈ s -> ∃ᶠ n in atTop, f^[n] x ∈ s

/--
The intake-selected measure-theoretic Poincare recurrence target: a self-map
preserving a finite measure returns almost every point of every null-measurable
set to that set infinitely often.
-/
def PoincareRecurrenceTarget (alpha : Type u) [MeasurableSpace alpha] : Prop :=
  forall (f : alpha -> alpha) (mu : MeasureTheory.Measure alpha),
    MeasureTheory.IsFiniteMeasure mu ->
      MeasureTheory.MeasurePreserving f mu mu ->
        SetRecurrenceConclusion f mu

/-- Direct expansion of the historical candidate, retained only for statement transport. -/
def PinnedCandidateSourceShape (alpha : Type u) [MeasurableSpace alpha] : Prop :=
  forall (f : alpha -> alpha) (mu : MeasureTheory.Measure alpha),
    MeasureTheory.IsFiniteMeasure mu ->
      MeasureTheory.MeasurePreserving f mu mu ->
        forall s : Set alpha,
          MeasureTheory.NullMeasurableSet s mu ->
            ∀ᵐ x ∂mu,
              x ∈ s -> ∃ᶠ n in atTop, f^[n] x ∈ s

theorem poincareRecurrenceTarget_iff_pinnedCandidateSourceShape
    (alpha : Type u) [MeasurableSpace alpha] :
    PoincareRecurrenceTarget alpha <-> PinnedCandidateSourceShape alpha := by
  rfl

/-- The conservative-system alternate is stronger than the finite-preserving target. -/
def ConservativeRecurrenceTarget (alpha : Type u) [MeasurableSpace alpha] : Prop :=
  forall (f : alpha -> alpha) (mu : MeasureTheory.Measure alpha),
    MeasureTheory.Conservative f mu -> SetRecurrenceConclusion f mu

theorem poincareRecurrenceTarget_of_conservativeRecurrenceTarget
    {alpha : Type u} [MeasurableSpace alpha]
    (h : ConservativeRecurrenceTarget alpha) : PoincareRecurrenceTarget alpha := by
  intro f mu hFinite hf
  letI : MeasureTheory.IsFiniteMeasure mu := hFinite
  exact h f mu hf.conservative

/- Structural mutations. The validator requires every printed expression to
be distinct from the canonical target before later proof evidence is inspected. -/

def mutationRemovedFiniteMeasure
    (alpha : Type u) [MeasurableSpace alpha] : Prop :=
  forall (f : alpha -> alpha) (mu : MeasureTheory.Measure alpha),
    MeasureTheory.MeasurePreserving f mu mu -> SetRecurrenceConclusion f mu

def mutationChangedDomain : Prop :=
  PoincareRecurrenceTarget Nat

def mutationChangedBinderScope
    (alpha : Type u) [MeasurableSpace alpha] : Prop :=
  forall (f : alpha -> alpha) (mu : MeasureTheory.Measure alpha),
    MeasureTheory.IsFiniteMeasure mu ->
      MeasureTheory.MeasurePreserving f mu mu ->
        ∀ᵐ x ∂mu,
          forall s : Set alpha,
            MeasureTheory.NullMeasurableSet s mu ->
              x ∈ s -> ∃ᶠ n in atTop, f^[n] x ∈ s

def mutationExcludedNullSetBoundary
    (alpha : Type u) [MeasurableSpace alpha] : Prop :=
  forall (f : alpha -> alpha) (mu : MeasureTheory.Measure alpha),
    MeasureTheory.IsFiniteMeasure mu ->
      MeasureTheory.MeasurePreserving f mu mu ->
        forall s : Set alpha,
          MeasureTheory.NullMeasurableSet s mu -> mu s ≠ 0 ->
            ∀ᵐ x ∂mu,
              x ∈ s -> ∃ᶠ n in atTop, f^[n] x ∈ s

/-- The empty-set case is deliberately retained; its implication is vacuous. -/
theorem emptySetBoundary {alpha : Type u} [MeasurableSpace alpha]
    (f : alpha -> alpha) (mu : MeasureTheory.Measure alpha) :
    (∀ᵐ x ∂mu,
      x ∈ (∅ : Set alpha) -> ∃ᶠ n in atTop, f^[n] x ∈ (∅ : Set alpha)) := by
  simp

set_option pp.explicit true in
#print Stage1Instances.THM_M_1521.PoincareRecurrenceTarget

end Stage1Instances.THM_M_1521
