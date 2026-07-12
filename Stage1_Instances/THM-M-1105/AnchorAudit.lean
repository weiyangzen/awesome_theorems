import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
import Mathlib.Probability.Independence.CharacteristicFunction
import Mathlib.Analysis.Matrix.Spectrum

open MeasureTheory Matrix ProbabilityTheory

namespace Stage1.THM_M_1105.AnchorAudit

-- These are supporting interfaces, not a proof of the Wigner semicircle law.
#check Matrix.IsHermitian.eigenvalues
#check Matrix.IsHermitian.trace_eq_sum_eigenvalues
#check ProbabilityTheory.iIndepFun.charFun_map_sum_eq_prod
#check MeasureTheory.ProbabilityMeasure.tendsto_iff_forall_integral_tendsto

end Stage1.THM_M_1105.AnchorAudit
