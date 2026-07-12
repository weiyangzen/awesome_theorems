import Mathlib.Analysis.Calculus.Deriv.Add
import Mathlib.Analysis.Calculus.Deriv.Comp
import Mathlib.Analysis.Calculus.Deriv.Mul
import Mathlib.Analysis.Calculus.FDeriv.CompCLM

/-!
# THM-M-1515 immutable anchor-audit probes

These declarations check calculus substrate in the pinned mathlib snapshot.
They do not state or prove the frozen Noether target.
-/

namespace Stage1Instances.THM_M_1515.AnchorAudit

def auditedMathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

def candidateClassification : List String := [
  "HasDerivAt.sub: charge subtraction rule; substrate only",
  "HasDerivAt.clm_apply: derivative of a varying covector applied to a varying vector; substrate only",
  "HasFDerivAt.clm_apply: Frechet analogue of covector application; substrate only",
  "DifferentiableAt.hasFDerivAt: canonical fderiv witness; substrate only"
]

#check HasDerivAt.sub
#check HasDerivAt.clm_apply
#check HasFDerivAt.clm_apply
#check DifferentiableAt.hasFDerivAt
#check HasDerivAt.comp_hasFDerivAt
#check HasDerivAt.comp
#check fderiv
#check deriv

end Stage1Instances.THM_M_1515.AnchorAudit
