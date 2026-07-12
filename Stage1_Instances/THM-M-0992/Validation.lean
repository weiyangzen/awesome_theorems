import Statement

/-!
# THM-M-0992 independent validation probe

This module independently transcribes the frozen target and applies the pinned
mathlib theorem without importing `Proof.lean` or `ObligationTree.lean`. It is
a same-workspace validation probe, not a distinct-runner attestation.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal ProbabilityTheory

namespace Stage1Instances.THM_M_0992.Validation

universe u

/-- Independent exact-type replay of the selected probability-space form of
Chebyshev's inequality. -/
theorem independentlyReconstructedTarget :
    forall (Omega : Type u) [MeasurableSpace Omega]
      (P : Measure Omega) [IsProbabilityMeasure P] (X : Omega -> Real),
        MemLp X 2 P ->
          forall r : Real, 0 < r ->
            P {omega | r <= |X omega - P[X]|} <=
              ENNReal.ofReal (variance X P / r ^ 2) := by
  intro Omega _ P _ X hX r hr
  exact ProbabilityTheory.meas_ge_le_variance_div_sq (μ := P) hX hr

/-- The independent transcription is definitionally the frozen target. -/
theorem independentTarget_iff_frozenTarget :
    ChebyshevTarget.{u} <->
      (forall (Omega : Type u) [MeasurableSpace Omega]
        (P : Measure Omega) [IsProbabilityMeasure P] (X : Omega -> Real),
          MemLp X 2 P ->
            forall r : Real, 0 < r ->
              P {omega | r <= |X omega - P[X]|} <=
                ENNReal.ofReal (variance X P / r ^ 2)) := by
  rfl

#print axioms independentlyReconstructedTarget
#print axioms independentTarget_iff_frozenTarget
#print axioms ProbabilityTheory.meas_ge_le_variance_div_sq

end Stage1Instances.THM_M_0992.Validation
