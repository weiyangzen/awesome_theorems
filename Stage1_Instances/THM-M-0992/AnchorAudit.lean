import Mathlib.Probability.Moments.Variance

/-!
# THM-M-0992: pinned anchor audit

This module independently restates the frozen probability-space target and
checks the direct bridge to the pinned mathlib declaration. It is anchor-audit
evidence only; downstream proof, provenance, and release gates remain open.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal ProbabilityTheory

namespace Stage1Instances.THM_M_0992.AnchorAudit

universe u

/-- Independent copy of the material clauses in the frozen target. -/
def AuditedChebyshevTarget : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsProbabilityMeasure P] (X : Omega -> Real),
      MemLp X 2 P ->
        forall r : Real, 0 < r ->
          P {omega | r <= |X omega - P[X]|} <=
            ENNReal.ofReal (variance X P / r ^ 2)

#check ProbabilityTheory.meas_ge_le_variance_div_sq
#check ProbabilityTheory.meas_ge_le_evariance_div_sq
#check ProbabilityTheory.variance
#check MeasureTheory.MemLp

/-- The pinned mathlib theorem has the exact conclusion and needs only the
finite-measure instance implied by the frozen probability-measure instance. -/
theorem exactTarget_from_pinned_mathlib : AuditedChebyshevTarget.{u} := by
  intro Omega _ P _ X hX r hr
  exact ProbabilityTheory.meas_ge_le_variance_div_sq (μ := P) hX hr

end Stage1Instances.THM_M_0992.AnchorAudit

#print axioms Stage1Instances.THM_M_0992.AnchorAudit.exactTarget_from_pinned_mathlib
