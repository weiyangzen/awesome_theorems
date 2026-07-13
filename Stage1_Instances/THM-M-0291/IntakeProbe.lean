import Mathlib.Analysis.Asymptotics.SpecificAsymptotics
import Mathlib.Analysis.Fourier.AddCircle

/-!
# THM-M-0291 discovery-only intake probe

These checks authenticate pinned APIs for stating the periodic Fourier/Cesaro theorem family and
two nearby, non-equivalent convergence results. They do not freeze a source-faithful target, prove
Fejer's theorem, or transfer any evidence from the duplicate target THM-M-0347.
-/

#check AddCircle
#check AddCircle.haarAddCircle
#check fourier
#check fourierCoeff
#check ContinuousMap
#check TendstoUniformly
#check hasSum_fourier_series_of_summable
#check Filter.Tendsto.cesaro_smul
