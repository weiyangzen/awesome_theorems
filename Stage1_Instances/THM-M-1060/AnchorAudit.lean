import Mathlib.Analysis.SpecialFunctions.Log.ENNRealLog
import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.Probability.Distributions.Gaussian.Real

/-!
# THM-M-1060 formal-anchor audit

This module makes the negative completion decision machine-readable.  The
audited declarations below are substrate only: none proves the exact
`SchilderTarget` frozen in `Statement.lean`.
-/

namespace Stage1Instances.THM_M_1060.AnchorAudit

/-- A bounded inventory row for a formal candidate or supporting anchor. -/
structure Candidate where
  source : String
  immutableRevision : String
  moduleName : String
  declarationNames : List String
  relationToTarget : String
  repoLocalChecked : Bool
  terminalExactProof : Bool
  machineClass : String

/-- The pinned mathlib supplies Gaussian-measure and analytic substrate, not Schilder's theorem. -/
def pinnedMathlib : Candidate where
  source := "https://github.com/leanprover-community/mathlib4"
  immutableRevision := "8a178386ffc0f5fef0b77738bb5449d50efeea95"
  moduleName := "Mathlib.Probability.Distributions.Gaussian.Real"
  declarationNames := [
    "ProbabilityTheory.gaussianReal",
    "ProbabilityTheory.gaussianReal_map_const_mul",
    "Filter.liminf",
    "Filter.limsup",
    "MeasureTheory.Measure.map"
  ]
  relationToTarget :=
    "substrate for finite-dimensional Wiener laws, scaling, and LDP expressions; no terminal Schilder/LDP declaration"
  repoLocalChecked := true
  terminalExactProof := false
  machineClass := "M3 substrate; not M0-W"

/-- The older repo-local LDP file exposes an assumed-obligations interface, not a Schilder proof. -/
def repoLocalLdpInterface : Candidate where
  source := "Formalizations/Lean/AwesomeTheorems/Stage1/S1_M_250.lean"
  immutableRevision := "205d13cfc35c45883410c569709a91cb34edce16"
  moduleName := "AwesomeTheorems.Stage1.S1_M_250"
  declarationNames := [
    "LargeDeviationPrinciple",
    "LargeDeviationProofObligations",
    "largeDeviationPrinciple_of_obligations"
  ]
  relationToTarget :=
    "generic sequence-indexed interface whose wrapper assumes both analytic bounds; different normalization and no Wiener/rate/goodness proof"
  repoLocalChecked := true
  terminalExactProof := false
  machineClass := "M3 interface; circular for SchilderTarget"

/-- Brownian-motion infrastructure exists externally but contains no Schilder/LDP module or theorem. -/
def externalBrownianInfrastructure : Candidate where
  source := "https://github.com/RemyDegenne/brownian-motion"
  immutableRevision := "91885e6172648ea7f9c6a16b3a7069f92c88e023"
  moduleName := "BrownianMotion.Gaussian.BrownianMotion"
  declarationNames := [
    "ProbabilityTheory.IsBrownian",
    "ProbabilityTheory.IsBrownian_brownian",
    "ProbabilityTheory.hasLaw_brownian_eval"
  ]
  relationToTarget :=
    "Brownian construction infrastructure only; recursive immutable tree has no Schilder, deviation, or Cameron-Martin path/module"
  repoLocalChecked := false
  terminalExactProof := false
  machineClass := "M5 integration-blocked substrate; not M1 or M0-P"

def candidates : List Candidate :=
  [pinnedMathlib, repoLocalLdpInterface, externalBrownianInfrastructure]

/-- No retained candidate is falsely promoted to a terminal exact proof. -/
theorem noRetainedCandidateClaimsTerminalProof :
    candidates.all (fun c => !c.terminalExactProof) = true := by
  rfl

/-- Anchor-only evidence cannot close the exact theorem. -/
def anchorAuditPermitsTheoremCompletion : Bool := false

theorem anchorAuditPermitsTheoremCompletion_eq_false :
    anchorAuditPermitsTheoremCompletion = false := by
  rfl

#check ProbabilityTheory.gaussianReal
#check ProbabilityTheory.gaussianReal_map_const_mul
#check Filter.liminf
#check Filter.limsup
#check MeasureTheory.Measure.map
#check noRetainedCandidateClaimsTerminalProof
#check anchorAuditPermitsTheoremCompletion_eq_false

end Stage1Instances.THM_M_1060.AnchorAudit
