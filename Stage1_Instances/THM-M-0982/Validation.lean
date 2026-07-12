import Proof

/-!
# THM-M-0982 independent validation probe

This module checks the proof-phase declaration at the exact frozen type and
also reconstructs that type directly from the pinned mathlib declarations.
The second declaration deliberately does not call the proof-phase wrapper.
-/

noncomputable section

open Filter MeasureTheory Set Topology

universe u

namespace Stage1Instances.THM_M_0982.Validation

open Stage1Instances.THM_M_0982

/-- Exact-type replay of the proof-phase result. -/
theorem proofReplay : ProbabilityContinuityTarget.{u} :=
  Proof.probabilityContinuity

/-- Separately implemented same-workspace probe for the frozen target. -/
theorem independentReconstruction : ProbabilityContinuityTarget.{u} := by
  constructor
  · intro Omega _ P _ A _ hmono
    simpa [Function.comp_def] using
      (tendsto_measure_iUnion_atTop (μ := P) hmono)
  · intro Omega _ P _ A hmeas hanti
    simpa [Function.comp_def] using
      (tendsto_measure_iInter_atTop (μ := P)
        (fun n => (hmeas n).nullMeasurableSet) hanti
        <| Exists.intro 0 (measure_ne_top P (A 0)))

#print axioms proofReplay
#print axioms independentReconstruction

end Stage1Instances.THM_M_0982.Validation
