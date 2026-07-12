import Mathlib.MeasureTheory.Measure.LevyConvergence

/-!
# THM-M-1012: pinned mathlib anchor check

This file checks that the exact known-limit target frozen by the statement node
is supplied by the pinned mathlib declaration. It is audit evidence, not a
release or theorem-completion claim.
-/

noncomputable section

open Filter MeasureTheory
open scoped Topology RealInnerProductSpace

namespace Stage1Instances.THM_M_1012.AnchorAudit

universe u

/-- Exact-type wrapper around the pinned mathlib Levy convergence theorem. -/
theorem pinned_mathlib_candidate
    (E : Type u) [NormedAddCommGroup E] [InnerProductSpace Real E]
    [FiniteDimensional Real E] [MeasurableSpace E] [BorelSpace E]
    (mu : Nat -> ProbabilityMeasure E) (mu0 : ProbabilityMeasure E) :
    Tendsto mu atTop (nhds mu0) <->
      forall t : E,
        Tendsto (fun n : Nat => charFun ((mu n : ProbabilityMeasure E) : Measure E) t) atTop
          (nhds (charFun ((mu0 : ProbabilityMeasure E) : Measure E) t)) := by
  exact ProbabilityMeasure.tendsto_iff_tendsto_charFun

end Stage1Instances.THM_M_1012.AnchorAudit

#check MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun
#print axioms MeasureTheory.ProbabilityMeasure.tendsto_iff_tendsto_charFun
#print axioms Stage1Instances.THM_M_1012.AnchorAudit.pinned_mathlib_candidate
