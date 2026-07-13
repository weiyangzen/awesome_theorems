import Statement
import Mathlib.RingTheory.Polynomial.Basic
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0025 differential validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It checks the exact frozen
root through a separately written wrapper over the pinned mathlib terminal declaration. This is
same-worker corroboration, not a second proof body or independent-runner evidence.
-/

namespace Stage1Instances.THM_M_0025.Validation

universe u

/-- A separately written exact-type route from the pinned terminal theorem to the frozen target. -/
theorem differentialHilbertBasisTheorem :
    Stage1Instances.THM_M_0025.HilbertBasisTheoremTarget.{u} := by
  intro R _ _
  exact Polynomial.isNoetherianRing

assert_no_sorry Polynomial.isNoetherianRing
assert_no_sorry differentialHilbertBasisTheorem

#print sorries Polynomial.isNoetherianRing
#print sorries differentialHilbertBasisTheorem
#print axioms Polynomial.isNoetherianRing
#print axioms differentialHilbertBasisTheorem

end Stage1Instances.THM_M_0025.Validation
