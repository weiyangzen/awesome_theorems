import Mathlib.Probability.Distributions.Gaussian.Real

/-!
# THM-M-1065 formal-anchor audit

This module records the bounded immutable candidate inventory. The checked mathlib declarations
are supporting interfaces only; none proves the KMT coupling target in `Statement.lean`.
-/

namespace Stage1Instances.THM_M_1065.AnchorAudit

structure Candidate where
  source : String
  immutableRevision : String
  moduleName : String
  declarationNames : List String
  relationToTarget : String
  locallyChecked : Bool
  terminalExactProof : Bool
  machineClass : String

def pinnedMathlib : Candidate where
  source := "https://github.com/leanprover-community/mathlib4"
  immutableRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  moduleName := "Mathlib.Probability.Distributions.Gaussian.Real"
  declarationNames := [
    "ProbabilityTheory.gaussianReal",
    "ProbabilityTheory.HasLaw",
    "ProbabilityTheory.iIndepFun"
  ]
  relationToTarget :=
    "Gaussian laws, laws of random variables, and independence substrate; no KMT coupling or logarithmic-error tail theorem"
  locallyChecked := true
  terminalExactProof := false
  machineClass := "M3 substrate; not M0-W"

def candidates : List Candidate := [pinnedMathlib]

theorem noRetainedCandidateClaimsTerminalProof :
    candidates.all (fun c => !c.terminalExactProof) = true := by
  rfl

def anchorAuditPermitsTheoremCompletion : Bool := false

theorem anchorAuditPermitsTheoremCompletion_eq_false :
    anchorAuditPermitsTheoremCompletion = false := by
  rfl

#check ProbabilityTheory.gaussianReal
#check ProbabilityTheory.HasLaw
#check ProbabilityTheory.iIndepFun
#check noRetainedCandidateClaimsTerminalProof
#check anchorAuditPermitsTheoremCompletion_eq_false

end Stage1Instances.THM_M_1065.AnchorAudit
