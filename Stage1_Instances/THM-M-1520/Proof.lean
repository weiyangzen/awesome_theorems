import Statement

/-!
# THM-M-1520 proof execution

This module contains the kernel-checked proof bodies obtained for boundary branches of the frozen
obligation tree. It deliberately does not declare the exact root: the positive-dimensional analytic
bridge remains unavailable in the pinned dependency closure.
-/

open MeasureTheory

namespace Stage1.THM_M_1520

/-- The time-zero map preserves volume. This closes the `t = 0` part of `M1520-S-BOUNDARY`
directly from the frozen flow identity hypothesis. -/
theorem timeZero_measurePreserving
    {n : Nat} {Phi : Real -> PhaseSpace n -> PhaseSpace n}
    (hzero : forall z, Phi 0 z = z) :
    MeasurePreserving (Phi 0) volume volume := by
  have hPhi : Phi 0 = id := funext hzero
  simpa only [hPhi] using (MeasurePreserving.id (μ := volume))

/-- Every map of the zero-dimensional phase space to itself is the identity, so every time map
preserves volume. This closes the `n = 0` part of `M1520-S-BOUNDARY` without analytic assumptions. -/
theorem zeroDimension_measurePreserving
    (Phi : Real -> PhaseSpace 0 -> PhaseSpace 0) (t : Real) :
    MeasurePreserving (Phi t) volume volume := by
  have phase_ext (x y : PhaseSpace 0) : x = y := by
    apply WithLp.ofLp_injective
    apply Prod.ext
    · ext i
      exact Fin.elim0 i
    · ext i
      exact Fin.elim0 i
  have hPhi : Phi t = id := funext fun z => phase_ext (Phi t z) z
  simpa only [hPhi] using (MeasurePreserving.id (μ := volume))

#print axioms timeZero_measurePreserving
#print axioms zeroDimension_measurePreserving

end Stage1.THM_M_1520
