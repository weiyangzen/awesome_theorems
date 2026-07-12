import Mathlib.MeasureTheory.Function.LpSpace.Complete

/-!
# THM-M-0311: exact Riesz-Fischer statement

This module freezes the repository's "completeness of L2 spaces" formulation. It states the
real- and complex-scalar cases over an arbitrary measure, including the almost-everywhere quotient
built into `MeasureTheory.Lp`. It does not prove the target.
-/

namespace Stage1Instances.THM_M_0311

open MeasureTheory
open scoped ENNReal

universe u

/-- The exact completeness target selected for the repository's Riesz-Fischer entry. -/
def RieszFischerTarget : Prop :=
  forall (α : Type u) [MeasurableSpace α] (μ : Measure α),
    CompleteSpace (Lp ℝ (2 : ℝ≥0∞) μ) ∧
      CompleteSpace (Lp ℂ (2 : ℝ≥0∞) μ)

/-- Direct expansion used as a checked alternate encoding. -/
def DirectL2Completeness : Prop :=
  forall (α : Type u) [MeasurableSpace α] (μ : Measure α),
    CompleteSpace (MeasureTheory.Lp ℝ (2 : ENNReal) μ) ∧
      CompleteSpace (MeasureTheory.Lp ℂ (2 : ENNReal) μ)

/-- The notation-level and fully qualified encodings are definitionally identical. -/
theorem rieszFischerTarget_iff_direct :
    RieszFischerTarget.{u} ↔ DirectL2Completeness.{u} :=
  Iff.rfl

-- Separately printed structural mutations used by `check_statement.py`.
def mutationRemovedComplexCase : Prop :=
  forall (α : Type u) [MeasurableSpace α] (μ : Measure α),
    CompleteSpace (Lp ℝ (2 : ℝ≥0∞) μ)

def mutationChangedDomain : Prop :=
  forall (μ : Measure Bool),
    CompleteSpace (Lp ℝ (2 : ℝ≥0∞) μ) ∧
      CompleteSpace (Lp ℂ (2 : ℝ≥0∞) μ)

def mutationChangedBinderScope : Prop :=
  forall (α : Type u) [MeasurableSpace α],
    ∃ μ : Measure α,
      CompleteSpace (Lp ℝ (2 : ℝ≥0∞) μ) ∧
        CompleteSpace (Lp ℂ (2 : ℝ≥0∞) μ)

def mutationFiniteMeasureOnly : Prop :=
  forall (α : Type u) [MeasurableSpace α] (μ : Measure α),
    IsFiniteMeasure μ →
      CompleteSpace (Lp ℝ (2 : ℝ≥0∞) μ) ∧
        CompleteSpace (Lp ℂ (2 : ℝ≥0∞) μ)

/-- The zero measure and empty carrier are retained by the canonical binder domain. -/
example :
    CompleteSpace (Lp ℝ (2 : ℝ≥0∞) (0 : Measure Empty)) ∧
      CompleteSpace (Lp ℂ (2 : ℝ≥0∞) (0 : Measure Empty)) := by
  constructor <;> infer_instance

/-- Infinite measures are not excluded; counting measure on `Nat` exercises that boundary. -/
example :
    CompleteSpace (Lp ℝ (2 : ℝ≥0∞) (Measure.count : Measure Nat)) ∧
      CompleteSpace (Lp ℂ (2 : ℝ≥0∞) (Measure.count : Measure Nat)) := by
  constructor <;> infer_instance

end Stage1Instances.THM_M_0311

set_option pp.explicit true in
#print Stage1Instances.THM_M_0311.RieszFischerTarget
