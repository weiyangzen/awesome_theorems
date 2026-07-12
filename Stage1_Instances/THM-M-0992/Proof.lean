import Statement
import ObligationTree

/-!
# THM-M-0992 proof phase

This module fills the frozen machine proof cut with the exact theorem from the
pinned mathlib dependency and checks the child-to-parent composition into the
unchanged statement-phase target.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal ProbabilityTheory

namespace Stage1Instances.THM_M_0992.Proof

open Stage1Instances.THM_M_0992

universe u

/-- The probability-space premise supplies the finite-measure interface used
by the pinned terminal theorem. -/
theorem probabilityMeasure_to_finite
    {Omega : Type u} [MeasurableSpace Omega] (P : Measure Omega)
    [IsProbabilityMeasure P] : IsFiniteMeasure P :=
  inferInstance

/-- Exact finite-measure variance package, implemented by the pinned mathlib
terminal proof body. -/
theorem pinnedVarianceAnchor : VarianceAnchorPackage.{u} := by
  intro Omega _ P _ X hX r hr
  exact ProbabilityTheory.meas_ge_le_variance_div_sq (μ := P) hX hr

/-- Checked composition of the pinned terminal package into the frozen root. -/
theorem assembledChebyshevRoot : ChebyshevTarget.{u} :=
  root_of_varianceAnchorPackage pinnedVarianceAnchor

/-- Placeholder-free proof of the exact proposition frozen in `Statement.lean`. -/
theorem chebyshev_inequality : ChebyshevTarget.{u} :=
  assembledChebyshevRoot

#print axioms probabilityMeasure_to_finite
#print axioms pinnedVarianceAnchor
#print axioms assembledChebyshevRoot
#print axioms chebyshev_inequality

end Stage1Instances.THM_M_0992.Proof
