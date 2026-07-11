import AwesomeTheorems.NumberTheory.THM_M_0387.StatementAndReductionPath
import AwesomeTheorems.NumberTheory.THM_M_0387.FLT3Path
import AwesomeTheorems.NumberTheory.THM_M_0387.FLT4Path
import AwesomeTheorems.NumberTheory.THM_M_0387.RegularPrimesPath

/-!
# THM-M-0387 proof-phase admissions

This module admits only proof bodies available in the pinned dependency closure.
The final theorem is deliberately conditional on the complete odd-prime branch;
that premise is the unresolved machine frontier rather than a hidden assumption.
-/

namespace Stage1Instances.THM_M_0387

/-- The frozen `Statement.lean` target, repeated transparently because the
dossier directory is intentionally outside the Lake library source tree. -/
def ProofTarget : Prop :=
  ∀ n : Nat, 3 ≤ n →
    ∀ a b c : Nat, a ≠ 0 → b ≠ 0 → c ≠ 0 →
      a ^ n + b ^ n ≠ c ^ n

/-- Checked transport from the frozen target to mathlib's canonical FLT statement. -/
theorem fermatLastTheoremTarget_iff_mathlib :
    ProofTarget ↔ FermatLastTheorem :=
  Iff.rfl

/-- Pinned mathlib proof body for exponent three. -/
theorem exponentThree : FermatLastTheoremFor 3 :=
  fermatLastTheoremThree

/-- Pinned mathlib proof body for exponent four. -/
theorem exponentFour : FermatLastTheoremFor 4 :=
  fermatLastTheoremFour

/-- Pinned `flt-regular` proof body for a regular prime exponent. -/
theorem regularPrimeExponent {p : Nat} [Fact p.Prime]
    (hreg : IsRegularPrime p) (hodd : p ≠ 2) : FermatLastTheoremFor p :=
  flt_regular hreg hodd

/-- Exact root composition after supplying every odd-prime exponent case. -/
theorem target_of_odd_prime_exponents
    (hodd : ∀ p : Nat, Nat.Prime p → Odd p → FermatLastTheoremFor p) :
    ProofTarget :=
  fermatLastTheoremTarget_iff_mathlib.mpr
    (FermatLastTheorem.of_odd_primes hodd)

end Stage1Instances.THM_M_0387

#print axioms Stage1Instances.THM_M_0387.fermatLastTheoremTarget_iff_mathlib
#print axioms Stage1Instances.THM_M_0387.exponentThree
#print axioms Stage1Instances.THM_M_0387.exponentFour
#print axioms Stage1Instances.THM_M_0387.regularPrimeExponent
#print axioms Stage1Instances.THM_M_0387.target_of_odd_prime_exponents
