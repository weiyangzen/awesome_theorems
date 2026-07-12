import Mathlib.Analysis.Calculus.ContDiff.Defs

/-!
# THM-M-0168 anchor-audit probes

These probes check the pinned calculus surface used by the exact statement.
They deliberately do not assert Bernstein's theorem.
-/

namespace Stage1Instances.THM_M_0168.AnchorAudit

#check ContDiff
#check fderiv
#check ContDiff.differentiable
#check contDiff_succ_iff_fderiv
#check contDiff_infty_iff_fderiv

end Stage1Instances.THM_M_0168.AnchorAudit
