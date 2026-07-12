import Statement

/-!
# THM-M-1245 conditional obligation composition

This module checks the last bridge from the audited scalar mathlib estimate to
the frozen root.  The terminal estimate remains an explicit premise: supplying
its named proof body belongs to the proof phase.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1245

/-- The exact per-function estimate exposed by the audited terminal anchor. -/
def AuditedTerminalEstimate : Prop :=
  forall (n : Nat) (p q : NNReal),
    0 < n ->
    1 <= p ->
    (q : Real)⁻¹ = (p : Real)⁻¹ - (n : Real)⁻¹ ->
    forall u : EuclideanSpace Real (Fin n) -> Real,
      ContDiff Real 1 u ->
      HasCompactSupport u ->
      eLpNorm u q volume <=
        MeasureTheory.eLpNormLESNormFDerivOfEqInnerConst
            (volume : Measure (EuclideanSpace Real (Fin n))) p *
          eLpNorm (fderiv Real u) p volume

/-- Checked composition: the terminal anchor's uniform explicit constant is a
valid witness for the existential constant in the canonical target. -/
theorem root_of_audited_terminal_estimate
    (terminal : AuditedTerminalEstimate) : SobolevInequalityTarget := by
  intro n p q hn hp hpq
  refine ⟨MeasureTheory.eLpNormLESNormFDerivOfEqInnerConst
      (volume : Measure (EuclideanSpace Real (Fin n))) p, ?_⟩
  intro u hu hcu
  exact terminal n p q hn hp hpq u hu hcu

#print axioms root_of_audited_terminal_estimate

end Stage1Instances.THM_M_1245
