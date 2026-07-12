import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Topology.EMetricSpace.PairReduction
import Mathlib.Topology.MetricSpace.CoveringNumbers

/-!
# THM-M-1084 formal-anchor audit

These probes check the strongest relevant declarations found in the pinned mathlib revision.
They are Gaussian-process and chaining substrate, not a proof of the frozen Dudley target.
-/

namespace Stage1Instances.THM_M_1084.AnchorAudit

/-- A bounded formal-candidate inventory row. -/
structure Candidate where
  source : String
  immutableRevision : String
  moduleName : String
  declarationNames : List String
  relationToTarget : String
  repoLocalChecked : Bool
  terminalExactProof : Bool
  machineClass : String

def pinnedMathlib : Candidate where
  source := "https://github.com/leanprover-community/mathlib4"
  immutableRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  moduleName := "Mathlib.Topology.MetricSpace.CoveringNumbers; Mathlib.Topology.EMetricSpace.PairReduction; Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic"
  declarationNames := [
    "Metric.coveringNumber",
    "Metric.externalCoveringNumber",
    "Metric.coveringNumber_anti",
    "EMetric.pair_reduction",
    "ProbabilityTheory.IsGaussianProcess",
    "ProbabilityTheory.IsGaussianProcess.hasGaussianLaw_fun_sub"
  ]
  relationToTarget :=
    "covering-number, finite pair-reduction, and Gaussian-increment substrate; no entropy-integral expected-supremum theorem"
  repoLocalChecked := true
  terminalExactProof := false
  machineClass := "M3 substrate; not M0-W"

def externalStatLearning : Candidate where
  source := "https://github.com/YuanheZ/lean-stat-learning-theory"
  immutableRevision := "be5d5a8a1a1f46f2ec9502980ff10a39e17e3820"
  moduleName := "SLT.Dudley"
  declarationNames := [
    "dudley_chaining_bound_core",
    "dudley_chaining_bound_countable",
    "dudley"
  ]
  relationToTarget :=
    "proved sub-Gaussian entropy inequality with closed-ball WithTop covering numbers, continuity, and constant 12*sqrt(2)*sigma; not definitionally the frozen centered-Gaussian constant-12 target"
  repoLocalChecked := false
  terminalExactProof := false
  machineClass := "M1 anchor-only near candidate; exact bridge and pinned integration required"

def candidates : List Candidate := [pinnedMathlib, externalStatLearning]

/-- The audit does not promote either retained row to an exact terminal proof. -/
theorem noRetainedCandidateClaimsTerminalProof :
    candidates.all (fun candidate => !candidate.terminalExactProof) = true := by
  rfl

/-- Anchor-only evidence cannot close the exact theorem. -/
def anchorAuditPermitsTheoremCompletion : Bool := false

theorem anchorAuditPermitsTheoremCompletion_eq_false :
    anchorAuditPermitsTheoremCompletion = false := by
  rfl

#check Metric.coveringNumber
#check Metric.externalCoveringNumber
#check Metric.coveringNumber_anti
#check EMetric.pair_reduction
#check ProbabilityTheory.IsGaussianProcess
#check ProbabilityTheory.IsGaussianProcess.hasGaussianLaw_fun_sub
#check noRetainedCandidateClaimsTerminalProof
#check anchorAuditPermitsTheoremCompletion_eq_false

end Stage1Instances.THM_M_1084.AnchorAudit
