import ObligationTree

/-!
# THM-M-1245 proof execution

This module installs the pinned mathlib Gagliardo-Nirenberg-Sobolev estimate
as the terminal proof body and composes it with the frozen existential-witness
bridge.  The resulting declaration has exactly the target frozen in
`Statement.lean`.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1245

/-- Pinned mathlib closure of frozen obligation `M1245-A-TERMINAL`. -/
theorem auditedTerminalEstimate_proof : AuditedTerminalEstimate := by
  intro n p q hn hp hpq u hu hcu
  have hfin : 0 < Module.finrank Real (EuclideanSpace Real (Fin n)) := by
    simpa using hn
  have hconj :
      (q : Real)⁻¹ = (p : Real)⁻¹ -
        (Module.finrank Real (EuclideanSpace Real (Fin n)) : Real)⁻¹ := by
    simpa using hpq
  simpa using
    MeasureTheory.eLpNorm_le_eLpNorm_fderiv_of_eq_inner
      volume hu hcu hp hfin hconj

/-- Exact closure of the frozen root, using the uniform mathlib constant. -/
theorem sobolevInequalityTarget_proof : SobolevInequalityTarget :=
  root_of_audited_terminal_estimate auditedTerminalEstimate_proof

#print axioms auditedTerminalEstimate_proof
#print axioms sobolevInequalityTarget_proof

end Stage1Instances.THM_M_1245
