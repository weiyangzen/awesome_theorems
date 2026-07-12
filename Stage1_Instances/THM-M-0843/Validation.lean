import Statement
import Mathlib.Combinatorics.SimpleGraph.Regularity.Lemma
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0843 differential validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It
checks the exact frozen root through a separately written wrapper over the
pinned mathlib terminal declaration. This is same-worker corroboration, not a
second proof body or independent-runner evidence.
-/

namespace Stage1Instances.THM_M_0843.Validation

universe u

/-- A separately written exact-type route from the pinned terminal theorem to
the frozen regularity target. -/
theorem differentialSzemerediRegularity :
    Stage1Instances.THM_M_0843.SzemerediRegularityTarget.{u} := by
  intro alpha _ _ G _ epsilon l hEpsilon hCard
  exact _root_.szemeredi_regularity G hEpsilon hCard

assert_no_sorry szemeredi_regularity
assert_no_sorry differentialSzemerediRegularity

#print sorries _root_.szemeredi_regularity
#print sorries differentialSzemerediRegularity

#print axioms _root_.szemeredi_regularity
#print axioms differentialSzemerediRegularity

end Stage1Instances.THM_M_0843.Validation
