import Statement
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0484 differential validation probe

This module imports neither `Proof` nor `ObligationTree`. It reconstructs the frozen root through
the checked residue encoding and the two pinned Lucas-Lehmer directions. This is a separately
written same-worker probe, not a distinct proof body or an independent-runner attestation.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0484.Validation

open Stage1Instances.THM_M_0484

/-- Differential reconstruction of the residue form from the pinned correctness directions. -/
theorem differentialResidueCriterion : LucasLehmerResidueTarget := by
  intro p hp
  constructor
  · intro hresidue
    exact lucas_lehmer_sufficiency p (by omega) hresidue
  · intro hprime
    exact lucas_lehmer_necessity p hp hprime

/-- The separately reconstructed residue criterion transported to the exact frozen root. -/
theorem differentialLucasLehmerCriterion : LucasLehmerTestTarget :=
  lucasLehmerTestTarget_iff_residueTarget.mpr differentialResidueCriterion

#check differentialResidueCriterion
#check differentialLucasLehmerCriterion

assert_no_sorry lucas_lehmer_sufficiency
assert_no_sorry lucas_lehmer_necessity
assert_no_sorry differentialResidueCriterion
assert_no_sorry differentialLucasLehmerCriterion

#print sorries lucas_lehmer_sufficiency lucas_lehmer_necessity
  differentialResidueCriterion differentialLucasLehmerCriterion

#print axioms lucas_lehmer_sufficiency
#print axioms lucas_lehmer_necessity
#print axioms differentialResidueCriterion
#print axioms differentialLucasLehmerCriterion

end Stage1Instances.THM_M_0484.Validation
