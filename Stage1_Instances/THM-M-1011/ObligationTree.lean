import Statement
import Mathlib.MeasureTheory.Measure.Prokhorov

/-!
# THM-M-1011 conditional obligation composition

The frozen statement uses a `PseudoMetricSpace` without a separation instance.
This module checks both available directions and makes that missing premise
explicit.  It does not prove that the premise follows from the frozen context.
-/

open MeasureTheory Set Topology

namespace Stage1Instances.THM_M_1011.ObligationTree

universe u

/-- The compact-closure to uniform-tightness direction matches the frozen
statement without an additional separation premise. -/
theorem compact_to_tight
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] [CompleteSpace X]
    (S : Set (ProbabilityMeasure X)) (h : IsCompact (closure S)) :
    IsUniformlyTight S := by
  exact isTightMeasureSet_of_isCompact_closure h

/-- The pinned tightness-to-compactness anchor composes only after a `T2Space`
dictionary is supplied explicitly. -/
theorem tight_to_compact_of_t2
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] [CompleteSpace X]
    (separation : T2Space X) (S : Set (ProbabilityMeasure X))
    (h : IsUniformlyTight S) : IsCompact (closure S) := by
  letI : T2Space X := separation
  exact isCompact_closure_of_isTightMeasureSet h

/-- Checked child-to-parent composition.  The extra separation child is open;
therefore this theorem is conditional evidence, not root closure. -/
theorem canonical_of_t2
    (X : Type u) [MeasurableSpace X] [PseudoMetricSpace X] [BorelSpace X]
    [SecondCountableTopology X] [CompleteSpace X]
    (separation : T2Space X) : CanonicalStatement X := by
  intro S
  constructor
  · exact tight_to_compact_of_t2 X separation S
  · exact compact_to_tight X S

#check compact_to_tight
#check tight_to_compact_of_t2
#check canonical_of_t2
#print axioms canonical_of_t2

end Stage1Instances.THM_M_1011.ObligationTree
