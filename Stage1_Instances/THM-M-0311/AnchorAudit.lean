import Mathlib.MeasureTheory.Function.LpSpace.Complete

/-!
# THM-M-0311 mathlib anchor audit

This module checks that the pinned mathlib completeness instance closes the exact frozen target.
It is an anchor-phase probe, not the proof-phase integration artifact.
-/

namespace Stage1Instances.THM_M_0311

open MeasureTheory
open scoped ENNReal

universe u

/-- Audit copy of the frozen target; `check_anchor_audit.py` checks it against `Statement.lean`. -/
def AnchorAuditTarget : Prop :=
  forall (α : Type u) [MeasurableSpace α] (μ : Measure α),
    CompleteSpace (Lp ℝ (2 : ℝ≥0∞) μ) ∧
      CompleteSpace (Lp ℂ (2 : ℝ≥0∞) μ)

/-- Exact candidate closure supplied by pinned mathlib's `MeasureTheory.Lp.instCompleteSpace`. -/
theorem rieszFischerTarget_of_pinned_mathlib : AnchorAuditTarget.{u} := by
  intro _ _ _
  constructor <;> infer_instance

end Stage1Instances.THM_M_0311

#check MeasureTheory.Lp.instCompleteSpace
#check Stage1Instances.THM_M_0311.rieszFischerTarget_of_pinned_mathlib
#print axioms MeasureTheory.Lp.instCompleteSpace
#print axioms Stage1Instances.THM_M_0311.rieszFischerTarget_of_pinned_mathlib
