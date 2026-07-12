import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Hermitian
import Mathlib.MeasureTheory.Integral.Bochner.Basic
import Mathlib.Probability.Independence.Basic

/-!
# THM-M-1111 formal-anchor audit

These declarations are checked substrate for a future implementation of the
semantic interface in `Statement.lean`.  None states or proves the Tao--Vu
Four Moment Theorem.
-/

namespace Stage1Instances.THM_M_1111.AnchorAudit

structure Candidate where
  source : String
  immutableRevision : String
  moduleName : String
  relationToTarget : String
  repoLocalChecked : Bool
  terminalExactProof : Bool
  machineClass : String

def pinnedMathlib : Candidate where
  source := "https://github.com/leanprover-community/mathlib4"
  immutableRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  moduleName := "Mathlib.Data.Matrix.Basic; Mathlib.LinearAlgebra.Matrix.Hermitian; Mathlib.MeasureTheory.Integral.Bochner.Basic; Mathlib.Probability.Independence.Basic"
  relationToTarget :=
    "matrix, Hermitian, expectation/integration, and independence substrate only; no Wigner ensemble, ordered random-matrix eigenvalue statistic, moment-matching, Condition C0, or Four Moment terminal theorem"
  repoLocalChecked := true
  terminalExactProof := false
  machineClass := "M3 support only; not M0-W"

def repoLocalStatement : Candidate where
  source := "Stage1_Instances/THM-M-1111/Statement.lean"
  immutableRevision := "cd7d0c47c19a08d85f4314833fd1e5a339230a3c"
  moduleName := "Stage1Instances.THM_M_1111"
  relationToTarget :=
    "exact proposition over an explicit unimplemented semantic interface; no proof body"
  repoLocalChecked := true
  terminalExactProof := false
  machineClass := "M3 exact statement/interface; not M0-L"

def candidates : List Candidate := [repoLocalStatement, pinnedMathlib]

theorem noRetainedCandidateClaimsTerminalProof :
    candidates.all (fun c => !c.terminalExactProof) = true := by
  rfl

def anchorAuditPermitsTheoremCompletion : Bool := false

theorem anchorAuditPermitsTheoremCompletion_eq_false :
    anchorAuditPermitsTheoremCompletion = false := by
  rfl

#check Matrix
#check Matrix.IsHermitian
#check MeasureTheory.integral
#check ProbabilityTheory.iIndepFun
#check noRetainedCandidateClaimsTerminalProof
#check anchorAuditPermitsTheoremCompletion_eq_false

end Stage1Instances.THM_M_1111.AnchorAudit
