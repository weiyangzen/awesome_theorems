import Mathlib.MeasureTheory.Function.ConvergenceInDistribution
import Mathlib.Analysis.Calculus.FDeriv.Basic

/-!
# THM-M-1016 anchor-audit probe

This file checks the pinned mathlib interfaces nearest to the frozen finite-dimensional delta
method.  None of these declarations proves the Taylor-remainder step, so this module deliberately
does not assert the canonical target.
-/

noncomputable section

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1016.AnchorAudit

#check TendstoInDistribution
#check TendstoInDistribution.continuous_comp
#check tendstoInDistribution_of_tendstoInMeasure_sub
#check TendstoInMeasure
#check HasFDerivAt
#check HasFDerivAt.continuousAt

end Stage1Instances.THM_M_1016.AnchorAudit
