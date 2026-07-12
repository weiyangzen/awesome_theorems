import Mathlib.Probability.Martingale.Convergence

/-!
# THM-M-1003: pinned anchor probes

These probes check the exact declarations retained by the rev-5.6 anchor
audit. They are partial convergence and generic Vitali infrastructure, not a
proof of the frozen full `L^p` martingale convergence target.
-/

open Filter MeasureTheory
open scoped ENNReal MeasureTheory NNReal Topology

#check Martingale.submartingale
#check Submartingale.ae_tendsto_limitProcess
#check Submartingale.memLp_limitProcess
#check Submartingale.tendsto_eLpNorm_one_limitProcess
#check Martingale.ae_eq_condExp_limitProcess
#check tendsto_Lp_finite_of_tendsto_ae
#check tendsto_Lp_finite_of_tendstoInMeasure
#check tendstoInMeasure_iff_tendsto_Lp_finite
#check UniformIntegrable.memLp_of_ae_tendsto
#check MemLp.mono_exponent

#print axioms Submartingale.ae_tendsto_limitProcess
#print axioms Submartingale.memLp_limitProcess
#print axioms Submartingale.tendsto_eLpNorm_one_limitProcess
#print axioms tendsto_Lp_finite_of_tendsto_ae
