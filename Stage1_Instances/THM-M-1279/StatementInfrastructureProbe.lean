import Mathlib.MeasureTheory.Constructions.HaarToSphere
import Mathlib.MeasureTheory.Integral.Lebesgue.Basic

/-!
# THM-M-1279 statement infrastructure probe

This file checks only pinned mathlib surfaces relevant to a future encoding of
Beckner's sphere inequality. It is not the canonical theorem statement: the
intake has not fixed a source-exact endpoint formula, operator normalization,
or sharpness clause.
-/

open Metric MeasureTheory

#check sphere
#check Measure.toSphere
#check MeasureTheory.integral
#check MeasureTheory.lintegral
#check Real.exp
#check EuclideanSpace

