import Mathlib.Analysis.Fourier.AddCircle

/-!
# THM-M-0290 discovery-only intake probe

These checks authenticate pinned interfaces adjacent to a possible periodic Carleson-Hunt
encoding. This file deliberately declares no canonical target or proof. In particular,
`hasSum_fourier_series_L2` is only an L2-topology statement, not almost-everywhere convergence.
-/

#check AddCircle
#check AddCircle.haarAddCircle
#check fourier
#check fourierCoeff
#check fourierLp
#check MeasureTheory.MemLp
#check MeasureTheory.Lp
#check Filter.Tendsto
#check hasSum_fourier_series_L2
