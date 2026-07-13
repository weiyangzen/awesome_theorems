import Statement
import Mathlib.NumberTheory.Wilson
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0476 differential validation reconstruction

This module imports the frozen statement but neither `Proof` nor `ObligationTree`. It reconstructs
the exact forward Wilson target from mathlib's stronger primality characterization. This is an
implementation-diverse same-worker check, not an independent-runner attestation.
-/

namespace Stage1Instances.THM_M_0476.Validation

open Stage1Instances.THM_M_0476

/-- The exact frozen target recovered through the stronger pinned Wilson equivalence. -/
theorem wilsonTheorem_via_primeCharacterization : WilsonTheoremTarget := by
  intro p hp
  exact (Nat.prime_iff_fac_equiv_neg_one hp.ne_one).mp hp

assert_no_sorry Nat.prime_iff_fac_equiv_neg_one
assert_no_sorry wilsonTheorem_via_primeCharacterization

#print sorries Nat.prime_iff_fac_equiv_neg_one
#print sorries wilsonTheorem_via_primeCharacterization

#print axioms Nat.prime_iff_fac_equiv_neg_one
#print axioms wilsonTheorem_via_primeCharacterization

end Stage1Instances.THM_M_0476.Validation
