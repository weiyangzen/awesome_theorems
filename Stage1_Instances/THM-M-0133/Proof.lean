import Statement
import Mathlib.NumberTheory.FLT.Four

/-!
# THM-M-0133 proof-phase bodies

This module pins the proof bodies currently available in the local dependency
closure. The exact root theorem remains conditional on the all-odd-prime
family, which is an explicit premise rather than an asserted result.
-/

namespace Stage1Instances.THM_M_0133

/-- Checked identity between the frozen target and mathlib's FLT proposition. -/
theorem proofTarget_iff_mathlib :
    WilesFermatLastTheoremTarget ↔ FermatLastTheorem :=
  Iff.rfl

/-- Pinned mathlib proof body for the exponent-four branch. -/
theorem exponentFour_proof : FermatLastTheoremFor 4 :=
  fermatLastTheoremFour

/-- Exact root composition after every odd-prime exponent case is supplied. -/
theorem exactTarget_of_oddPrimeCases
    (oddPrimeCases : ∀ p : Nat, Nat.Prime p → Odd p → FermatLastTheoremFor p) :
    WilesFermatLastTheoremTarget :=
  proofTarget_iff_mathlib.mpr
    (FermatLastTheorem.of_odd_primes oddPrimeCases)

#print axioms proofTarget_iff_mathlib
#print axioms exponentFour_proof
#print axioms exactTarget_of_oddPrimeCases

end Stage1Instances.THM_M_0133
