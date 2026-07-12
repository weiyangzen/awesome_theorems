import Mathlib.Analysis.Fourier.FourierTransform
import Mathlib.Analysis.Fourier.LpSpace
import Mathlib.MeasureTheory.Function.LpSeminorm.Basic
import Mathlib.MeasureTheory.Measure.Restrict
import Mathlib.Topology.MetricSpace.Pseudo.Defs

open MeasureTheory

-- Intake-only vocabulary checks; these do not select or prove a restriction theorem.
#check FourierTransform.fourier
#check MeasureTheory.Lp.fourierTransformₗᵢ
#check MemLp
#check eLpNorm
#check Metric.sphere
#check Measure.restrict
