import Mathlib.MeasureTheory.Measure.Typeclasses.Probability

/-!
# THM-M-0982: exact continuity-of-probability statement

This module freezes and tests the statement boundary only. It does not claim
proof or provenance credit for the continuity theorems.
-/

noncomputable section

open Filter MeasureTheory Set Topology

universe u

namespace Stage1Instances.THM_M_0982

/-- Continuity from below for an increasing sequence of measurable events. -/
def ContinuityFromBelowTarget : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (A : Nat → Set Omega),
      (∀ n, MeasurableSet (A n)) →
      Monotone A →
      Tendsto (fun n : Nat => P (A n)) atTop (nhds (P (⋃ n, A n)))

/-- Continuity from above for a decreasing sequence of measurable events. -/
def ContinuityFromAboveTarget : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (A : Nat → Set Omega),
      (∀ n, MeasurableSet (A n)) →
      Antitone A →
      Tendsto (fun n : Nat => P (A n)) atTop (nhds (P (⋂ n, A n)))

/-- The canonical target: both monotone continuity laws for probability. -/
def ProbabilityContinuityTarget : Prop :=
  ContinuityFromBelowTarget.{u} ∧ ContinuityFromAboveTarget.{u}

/-- A direct local copy of the historical candidate's null-measurable form. -/
def HistoricalNullMeasurableShape : Prop :=
  ContinuityFromBelowTarget.{u} ∧
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (A : Nat → Set Omega),
      (∀ n, NullMeasurableSet (A n) P) →
      Antitone A →
      Tendsto (fun n : Nat => P (A n)) atTop (nhds (P (⋂ n, A n)))

/-- Checked transport from the canonical event statement to the broader
historical null-measurable encoding. Only this implication is credited. -/
theorem probabilityContinuityTarget_implies_historicalShape :
    ProbabilityContinuityTarget.{u} → HistoricalNullMeasurableShape.{u} := by
  rintro ⟨hbelow, habove⟩
  refine ⟨hbelow, ?_⟩
  intro Omega _ P _ A hnull hanti
  have hfinite : ∃ n, P (A n) ≠ ⊤ := ⟨0, measure_ne_top P (A 0)⟩
  simpa [Function.comp_def] using
    (tendsto_measure_iInter_atTop (μ := P) hnull hanti hfinite)

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedMeasurability : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (A : Nat → Set Omega),
      Antitone A →
      Tendsto (fun n : Nat => P (A n)) atTop (nhds (P (⋂ n, A n)))

def mutationChangedMeasureDomain : Prop :=
  ∀ (P : Measure Nat) [IsProbabilityMeasure P]
    (A : Nat → Set Nat),
      (∀ n, MeasurableSet (A n)) →
      Monotone A →
      Tendsto (fun n : Nat => P (A n)) atTop (nhds (P (⋃ n, A n)))

def mutationChangedBinderScope : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P],
      (∀ A : Nat → Set Omega, ∀ n, MeasurableSet (A n)) →
      ∀ A : Nat → Set Omega,
        Monotone A →
        Tendsto (fun n : Nat => P (A n)) atTop (nhds (P (⋃ n, A n)))

def mutationStrictMonotonicity : Prop :=
  ∀ (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P]
    (A : Nat → Set Omega),
      (∀ n, MeasurableSet (A n)) →
      (∀ n, A n ⊂ A (n + 1)) →
      Tendsto (fun n : Nat => P (A n)) atTop (nhds (P (⋃ n, A n)))

/-- Constant event sequences, including empty and universal events, stay in scope. -/
theorem constant_sequence_boundary (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) (S : Set Omega) :
    Tendsto (fun _n : Nat => P S) atTop (nhds (P S)) :=
  tendsto_const_nhds

/-- The union boundary of the constantly empty event sequence is empty. -/
theorem empty_union_boundary (Omega : Type u) :
    (⋃ _n : Nat, (∅ : Set Omega)) = ∅ := by simp

/-- The intersection boundary of the constantly universal event sequence is universal. -/
theorem universal_intersection_boundary (Omega : Type u) :
    (⋂ _n : Nat, (Set.univ : Set Omega)) = Set.univ := by simp

end Stage1Instances.THM_M_0982

set_option pp.explicit true in
#print Stage1Instances.THM_M_0982.ProbabilityContinuityTarget
