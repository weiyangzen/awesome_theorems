import Statement

/-!
# THM-M-0982 proof-phase integration

This module closes both branches of the exact target frozen in `Statement.lean`.
The proof bodies are local wrappers around the pinned mathlib continuity
theorems; the measurable-event and probability-finiteness transports remain
explicit in the continuity-from-above branch.
-/

noncomputable section

open Filter MeasureTheory Set Topology

universe u

namespace Stage1Instances.THM_M_0982.Proof

open Stage1Instances.THM_M_0982

/-- Increasing measurable events satisfy continuity from below. The
measurability premise is retained because it is part of the frozen target,
although the pinned mathlib theorem is stronger and does not consume it. -/
theorem continuityFromBelow : ContinuityFromBelowTarget.{u} := by
  intro Omega _ P _ A _ hmono
  simpa [Function.comp_def] using
    (tendsto_measure_iUnion_atTop (μ := P) hmono)

/-- Decreasing measurable events satisfy continuity from above. -/
theorem continuityFromAbove : ContinuityFromAboveTarget.{u} := by
  intro Omega _ P _ A hmeas hanti
  have hnull : ∀ n, NullMeasurableSet (A n) P :=
    fun n => (hmeas n).nullMeasurableSet
  have hfinite : ∃ n, P (A n) ≠ ⊤ :=
    ⟨0, measure_ne_top P (A 0)⟩
  simpa [Function.comp_def] using
    (tendsto_measure_iInter_atTop (μ := P) hnull hanti hfinite)

/-- Placeholder-free closure of the exact frozen conjunction. -/
theorem probabilityContinuity : ProbabilityContinuityTarget.{u} :=
  ⟨continuityFromBelow, continuityFromAbove⟩

#print axioms continuityFromBelow
#print axioms continuityFromAbove
#print axioms probabilityContinuity

end Stage1Instances.THM_M_0982.Proof
