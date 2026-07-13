import Statement
import Mathlib.Data.Nat.Factors
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0471 differential validation reconstruction

This module imports the frozen statement but neither the proof module nor its obligation-tree
implementation. It reconstructs the exact prime-list root directly from the pinned mathlib API.
This is a same-worker differential check, not an independent-runner attestation.
-/

namespace Stage1Instances.THM_M_0471.Validation

open Stage1Instances.THM_M_0471

/-- A separately written reconstruction of the exact frozen natural-number target. -/
theorem independentlyReconstructedFundamentalTheoremOfArithmetic :
    FundamentalTheoremOfArithmeticTarget := by
  intro n hn
  let factors := Nat.primeFactorsList n
  refine ⟨factors, (Nat.primeFactorsList_ne_nil n).2 hn, ?_, ?_⟩
  · exact
      ⟨fun p hp => Nat.prime_of_mem_primeFactorsList hp,
        Nat.prod_primeFactorsList (Nat.ne_zero_of_lt hn)⟩
  · intro k hk
    exact Nat.primeFactorsList_unique hk.2 hk.1

#check independentlyReconstructedFundamentalTheoremOfArithmetic
assert_no_sorry Nat.primeFactorsList_ne_nil
assert_no_sorry Nat.prime_of_mem_primeFactorsList
assert_no_sorry Nat.prod_primeFactorsList
assert_no_sorry Nat.primeFactorsList_unique
assert_no_sorry independentlyReconstructedFundamentalTheoremOfArithmetic
#print sorries independentlyReconstructedFundamentalTheoremOfArithmetic
#print axioms Nat.primeFactorsList_ne_nil
#print axioms Nat.prime_of_mem_primeFactorsList
#print axioms Nat.prod_primeFactorsList
#print axioms Nat.primeFactorsList_unique
#print axioms independentlyReconstructedFundamentalTheoremOfArithmetic

end Stage1Instances.THM_M_0471.Validation
