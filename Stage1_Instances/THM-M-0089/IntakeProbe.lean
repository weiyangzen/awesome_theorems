import Mathlib.Analysis.InnerProductSpace.l2Space
import Mathlib.MeasureTheory.Function.ContinuousMapDense
import Mathlib.MeasureTheory.Measure.Haar.Basic
import Mathlib.RepresentationTheory.FDRep

/-!
# THM-M-0089 discovery-only intake probe

These checks authenticate adjacent pinned representation, Haar-measure, continuous-to-Lp density,
and Hilbert-basis APIs. They do not define matrix coefficients, select a Peter-Weyl formulation, or
prove THM-M-0089.
-/

#check Representation
#check FDRep
#check FDRep.ρ
#check MeasureTheory.Measure.haar
#check ContinuousMap.toLp
#check ContinuousMap.toLp_denseRange
#check HilbertBasis
#check HilbertBasis.dense_span
