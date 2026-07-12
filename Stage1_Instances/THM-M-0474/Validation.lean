import Statement
import Mathlib.FieldTheory.Finite.Basic
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0474 differential validation probe

This module imports neither `Proof` nor `ObligationTree`. It reconstructs the exact frozen root
through Euler's totient theorem rather than the proof phase's direct Fermat wrapper. The route is
implementation-diverse local evidence; it is not a distinct-runner attestation.
-/

namespace Stage1Instances.THM_M_0474.Validation

open Stage1Instances.THM_M_0474

/-- Exact frozen target reconstructed through `Nat.ModEq.pow_totient`. -/
theorem fermatLittleTheorem_via_totient : FermatLittleTheoremTarget := by
  intro p a hp ha
  simpa only [Nat.totient_prime hp] using Nat.ModEq.pow_totient ha

assert_no_sorry Nat.ModEq.pow_totient
assert_no_sorry Nat.totient_prime
assert_no_sorry fermatLittleTheorem_via_totient

#print sorries Nat.ModEq.pow_totient
#print sorries Nat.totient_prime
#print sorries fermatLittleTheorem_via_totient

#print axioms Nat.ModEq.pow_totient
#print axioms Nat.totient_prime
#print axioms fermatLittleTheorem_via_totient

end Stage1Instances.THM_M_0474.Validation
