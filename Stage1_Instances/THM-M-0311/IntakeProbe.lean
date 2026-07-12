import Mathlib.MeasureTheory.Function.LpSpace.Complete

open MeasureTheory
open scoped ENNReal

universe u

variable {α : Type u} [MeasurableSpace α] (μ : Measure α)

#check MeasureTheory.Lp
#check MeasureTheory.Lp.instCompleteSpace

example : CompleteSpace (Lp ℝ (2 : ℝ≥0∞) μ) := by infer_instance

example : CompleteSpace (Lp ℂ (2 : ℝ≥0∞) μ) := by infer_instance
