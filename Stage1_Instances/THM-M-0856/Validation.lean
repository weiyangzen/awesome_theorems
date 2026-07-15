import Statement
import Mathlib.Combinatorics.SimpleGraph.Tutte
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

set_option autoImplicit false

/-!
# THM-M-0856 same-worker differential validation

This module deliberately imports neither `Proof` nor `ObligationTree`. It reconstructs the exact
frozen target directly from the manifest-pinned mathlib terminal theorem. Running it in this
worker supplies differential corroboration, not a second proof body or independent-runner evidence.
-/

namespace Stage1Instances.THM_M_0856.Validation

universe u

open SimpleGraph
open Stage1Instances.THM_M_0856

/-- A separately written exact-target route from the pinned terminal theorem. -/
theorem tutteOneFactor_differential : TutteOneFactorTarget.{u} := by
  intro V G _
  simpa only [OddComponentCondition, SimpleGraph.IsTutteViolator, not_lt] using
    (SimpleGraph.tutte (G := G))

assert_no_sorry SimpleGraph.tutte
assert_no_sorry tutteOneFactor_differential

#print sorries SimpleGraph.tutte
#print sorries tutteOneFactor_differential

#print axioms SimpleGraph.tutte
#print axioms tutteOneFactor_differential

end Stage1Instances.THM_M_0856.Validation
