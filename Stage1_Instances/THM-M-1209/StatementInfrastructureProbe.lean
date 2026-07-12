import Mathlib.Analysis.InnerProductSpace.Adjoint
import Mathlib.MeasureTheory.Function.LpSeminorm.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# THM-M-1209 statement infrastructure probe

This is not a statement of the Keel-Tao theorem. It checks only that several
interfaces necessarily mentioned by any faithful encoding of Theorem 1.2 are
available in the pinned environment. In particular, it does not invent an
interpolation-space model or replace the source's mixed norms by a single
`eLpNorm`.
-/

#check ContinuousLinearMap.adjoint
#check MeasureTheory.eLpNorm
#check MeasureTheory.integral
#check MeasureTheory.Measure.restrict
#check Set.Iio
