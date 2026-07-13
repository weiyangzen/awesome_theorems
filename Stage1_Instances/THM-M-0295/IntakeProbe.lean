import Mathlib.Analysis.Fourier.FourierTransform
import Mathlib.Analysis.Fourier.LpSpace
import Mathlib.Analysis.Distribution.SchwartzSpace.Fourier

/-!
# THM-M-0295 discovery-only intake probe

These checks authenticate pinned `L1 -> L-infinity` and `L2 -> L2` Fourier endpoint APIs. They do
not select a domain, normalization, exponent interval, conjugate-exponent convention, or canonical
Hausdorff-Young target, and they provide no proof credit for THM-M-0295.
-/

#check Real.Lp.fourierTransform
#check Real.Lp.fourierTransformCLM
#check SchwartzMap.norm_fourier_apply_le_toLp_one
#check SchwartzMap.norm_fourier_Lp_top_leq_toLp_one
#check MeasureTheory.Lp.fourierTransformₗᵢ
#check MeasureTheory.Lp.norm_fourier_eq
