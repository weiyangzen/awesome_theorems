import Statement
import Mathlib.LinearAlgebra.Matrix.Charpoly.Basic
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0041 differential validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It checks the exact frozen
root through a separately written wrapper over the pinned mathlib terminal declaration. This is
same-worker corroboration, not a second proof body or independent-runner evidence.
-/

namespace Stage1Instances.THM_M_0041.Validation

universe u v

noncomputable section

/-- A separately written exact-type route from the pinned terminal theorem to the frozen target. -/
theorem differentialCayleyHamilton :
    Stage1Instances.THM_M_0041.CayleyHamiltonTarget.{u, v} := by
  intro R _ n _ _ A
  change Polynomial.aeval A A.charpoly = 0
  exact Matrix.aeval_self_charpoly A

assert_no_sorry Matrix.aeval_self_charpoly
assert_no_sorry differentialCayleyHamilton

#print sorries Matrix.aeval_self_charpoly
#print sorries differentialCayleyHamilton
#print axioms Matrix.aeval_self_charpoly
#print axioms differentialCayleyHamilton

end

end Stage1Instances.THM_M_0041.Validation
