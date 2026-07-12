import Mathlib.Analysis.InnerProductSpace.Laplacian
import Mathlib.MeasureTheory.Integral.IntegralEqImproper

/-!
# THM-M-1247: pinned anchor probes

The declarations below are locally available analytic substrate. None states
the sharp multidimensional Rellich inequality frozen in `Statement.lean`.
-/

namespace Stage1Instances.THM_M_1247.AnchorAudit

def auditedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

#check Laplacian.laplacian
#check InnerProductSpace.laplacian_eq_iteratedFDeriv_stdOrthonormalBasis
#check fderiv_of_notMem_tsupport
#check HasCompactSupport.fderiv
#check HasCompactSupport.fderiv_apply
#check HasCompactSupport.integral_Ioi_deriv_eq
#check HasCompactSupport.integral_Iic_deriv_eq

end Stage1Instances.THM_M_1247.AnchorAudit
