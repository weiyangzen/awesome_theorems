import Mathlib.Analysis.InnerProductSpace.Basic
import Mathlib.LinearAlgebra.LinearPMap

/-!
# THM-M-1524 anchor-audit probes

These probes check the pinned mathlib interfaces used by the frozen target and
by the audited external proof architecture. They are not a proof of the target.
-/

open scoped ComplexConjugate

#check LinearPMap
#check LinearPMap.domain
#check LinearPMap.toFun
#check Dense
#check Submodule
#check inner_mul_inner_self_le
#check norm_inner_le_norm
#check inner_self_eq_norm_sq
#check inner_sub_left
#check inner_sub_right

universe u

namespace Stage1Instances.THM_M_1524.AnchorAudit

variable {H : Type u} [NormedAddCommGroup H] [InnerProductSpace ℂ H]

/-- The exact Cauchy-Schwarz inequality needed at the analytic leaf. -/
theorem centered_cauchy_schwarz (x y : H) :
    ‖inner ℂ x y‖ ≤ ‖x‖ * ‖y‖ :=
  norm_inner_le_norm x y

end Stage1Instances.THM_M_1524.AnchorAudit

#print axioms Stage1Instances.THM_M_1524.AnchorAudit.centered_cauchy_schwarz
