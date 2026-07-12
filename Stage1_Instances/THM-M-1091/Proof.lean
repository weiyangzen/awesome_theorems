import Statement

/-!
# THM-M-1091 proof-phase closure

This module adopts the pinned mathlib kernel-power theorem and closes the exact proposition frozen
in `Statement.lean`. The index swap is explicit: mathlib states the power law in displayed
composition order, while the target names the chronological first step `m`.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal ProbabilityTheory

namespace Stage1Instances.THM_M_1091

universe u

/-- The exact frozen homogeneous discrete-time Chapman-Kolmogorov equation. -/
theorem chapmanKolmogorov : ChapmanKolmogorovTarget.{u} := by
  intro State _ kappa _ m n
  simpa only [add_comm] using Kernel.pow_add kappa n m

/-- The checked statement transport gives the conventional setwise integral equation. -/
theorem chapmanKolmogorov_integral : ChapmanKolmogorovIntegralTarget.{u} :=
  target_iff_integralTarget.mp chapmanKolmogorov

#check chapmanKolmogorov
#check chapmanKolmogorov_integral
#print axioms chapmanKolmogorov
#print axioms chapmanKolmogorov_integral

end Stage1Instances.THM_M_1091
