import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.MeasureTheory.Function.LpSeminorm.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# THM-M-0382 statement infrastructure probe

This file is not a statement of the Keel-Tao theorem. It checks only pinned
interfaces that any faithful encoding of the abstract endpoint theorem is
expected to need. In particular, it does not invent the source's interpolation
spaces or replace its mixed norms with a single `eLpNorm`.
-/

#check ContinuousLinearMap.adjoint
#check MeasureTheory.eLpNorm
#check MeasureTheory.integral
#check MeasureTheory.Measure.restrict
#check Set.Iio
