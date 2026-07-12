import Statement

/-!
# THM-M-0992 obligation composition

This module checks the typed boundary between the pinned finite-measure
mathlib anchor and the frozen probability-space target.  The anchor package
remains an explicit premise, so this file freezes composition without claiming
the downstream proof or release gates.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped ENNReal ProbabilityTheory

namespace Stage1Instances.THM_M_0992

universe u

/-- Exact interface exported by the pinned finite-measure variance theorem. -/
def VarianceAnchorPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) [IsFiniteMeasure P] (X : Omega -> Real),
      MemLp X 2 P ->
        forall r : Real, 0 < r ->
          P {omega | r <= |X omega - P[X]|} <=
            ENNReal.ofReal (variance X P / r ^ 2)

/-- Checked child-to-parent composition.  A probability measure supplies the
finite-measure instance required by the exact anchor package. -/
theorem root_of_varianceAnchorPackage
    (anchor : VarianceAnchorPackage.{u}) : ChebyshevTarget.{u} := by
  intro Omega _ P _ X hX r hr
  exact anchor Omega P X hX r hr

#print axioms root_of_varianceAnchorPackage

end Stage1Instances.THM_M_0992
