import Mathlib.MeasureTheory.Measure.ProbabilityMeasure
import Mathlib.Topology.Order.LiminfLimsup
import Mathlib.Topology.Semicontinuity.Defs
import Mathlib.Analysis.SpecialFunctions.Log.ENNRealLog

/-!
# THM-M-1058 anchor-audit probes

These declarations check the substrate used by the frozen statement against
the repository's pinned mathlib. They deliberately do not assert a large
deviation principle or turn substrate APIs into a terminal theorem candidate.
-/

noncomputable section

open MeasureTheory Filter
open scoped ENNReal Topology

namespace Stage1Instances.THM_M_1058.AnchorAudit

universe u

variable {E : Type u} [TopologicalSpace E] [MeasurableSpace E]

/-- The pinned probability-measure type supplies the measure coercion needed
by the statement. -/
example (mu : ProbabilityMeasure E) (s : Set E) : ENNReal :=
  (mu : Measure E) s

/-- The exact extended logarithm used by the statement has the required zero
boundary convention. -/
theorem ennrealLog_zero : ENNReal.log 0 = (⊥ : EReal) := by
  exact ENNReal.log_zero

/-- The pinned order API elaborates limsup and liminf for the statement's
extended-real sequence. -/
example (f : Nat -> EReal) : EReal := limsup f atTop
example (f : Nat -> EReal) : EReal := liminf f atTop

/-- The rate-function regularity predicate is present at the pinned revision. -/
example (rate : E -> EReal) (h : LowerSemicontinuous rate) :
    LowerSemicontinuous rate := h

end Stage1Instances.THM_M_1058.AnchorAudit

#check MeasureTheory.ProbabilityMeasure
#check Filter.limsup
#check Filter.liminf
#check LowerSemicontinuous
#check ENNReal.log
#check ENNReal.log_zero
