import Mathlib.MeasureTheory.Measure.Prokhorov

/-!
# THM-M-1011: pinned mathlib anchor audit

This module checks the two mathlib declarations against the unfolded canonical
target. The terminal proof bodies remain in the pinned mathlib dependency.
-/

open MeasureTheory Set Topology

namespace Stage1Instances.THM_M_1011.AnchorAudit

universe u

/-- The strongest direct wrapper supplied by the two pinned mathlib anchors. -/
theorem mathlib_wrapper_with_t2
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] [CompleteSpace X] [T2Space X] :
    forall S : Set (ProbabilityMeasure X),
      IsTightMeasureSet
          ((fun P : ProbabilityMeasure X => (P : Measure X)) '' S) <->
        IsCompact (closure S) := by
  intro S
  constructor
  · exact isCompact_closure_of_isTightMeasureSet
  · exact isTightMeasureSet_of_isCompact_closure

/-- The frozen target does not provide the separation instance required upstream. -/
example
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] [CompleteSpace X] : True := by
  fail_if_success haveI : T2Space X := inferInstance
  trivial

#check isCompact_closure_of_isTightMeasureSet
#check isTightMeasureSet_of_isCompact_closure
#print axioms mathlib_wrapper_with_t2

end Stage1Instances.THM_M_1011.AnchorAudit
