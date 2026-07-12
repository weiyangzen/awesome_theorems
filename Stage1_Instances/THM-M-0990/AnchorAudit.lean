import Mathlib.Probability.CentralLimitTheorem

/-!
# THM-M-0990 pinned mathlib anchor audit

This file checks the declarations found by the rev-5.6 anchor search. None is a
terminal Lyapunov triangular-array central limit theorem: the available CLT
requires one sequence of identically distributed variables.
-/

open Filter MeasureTheory ProbabilityTheory
open scoped Real Topology ProbabilityTheory

#check @ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum_sub
#check @ProbabilityTheory.tendstoInDistribution_inv_sqrt_mul_sum
#check @ProbabilityTheory.tendsto_charFun_inv_sqrt_mul_pow
#check @ProbabilityTheory.iIndepFun.charFun_map_fun_finset_sum_eq_prod
#check @MeasureTheory.taylor_charFun_two
#check @ProbabilityMeasure.tendsto_iff_tendsto_charFun

namespace Stage1Instances.THM_M_0990.AnchorAudit

/-- Machine-readable boundary: the checked terminal mathlib CLT has an
identical-distribution hypothesis, unlike the frozen triangular-array target. -/
def terminalMathlibAnchorIsIidOnly : Bool := true

/-- The audit does not represent the checked anchors as terminal proof credit. -/
theorem noTerminalProofCredit : terminalMathlibAnchorIsIidOnly = true := rfl

end Stage1Instances.THM_M_0990.AnchorAudit
