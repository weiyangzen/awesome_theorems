import Mathlib.Analysis.FunctionalSpaces.SobolevInequality
import Mathlib.MeasureTheory.Function.LpSeminorm.CompareExp
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# THM-M-1248 anchor audit

This file checks the closest declarations found in pinned mathlib.  None has
the weighted Caffarelli-Kohn-Nirenberg target as its conclusion.
-/

namespace Stage1Instances.THM_M_1248.AnchorAudit

/-- Immutable mathlib revision inspected by this audit. -/
def mathlibRevision : String :=
  "8a178386ffc0f5fef0b77738bb5449d50efeea95"

/-- Exact terminal-name search terms used on the pinned mathlib source tree. -/
def terminalSearchTerms : List String :=
  ["Caffarelli", "Kohn", "Nirenberg", "Caffarelli-Kohn-Nirenberg",
   "weighted Sobolev", "weighted interpolation"]

/-- No exact CKN declaration was found in the inspected pinned source tree. -/
def exactMathlibAnchorFound : Bool := false

/-- No exact external Lean 4 declaration was found on the bounded search surfaces. -/
def exactExternalAnchorFound : Bool := false

theorem terminalSearchTerms_length : terminalSearchTerms.length = 6 := rfl
theorem exactMathlibAnchorFound_eq_false : exactMathlibAnchorFound = false := rfl
theorem exactExternalAnchorFound_eq_false : exactExternalAnchorFound = false := rfl

end Stage1Instances.THM_M_1248.AnchorAudit

-- Preserve the elaborated types of the three closest reusable APIs.
#check MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq
#check MeasureTheory.MemLp.mul
#check MeasureTheory.integral_mul_le_Lp_mul_Lq_of_nonneg
