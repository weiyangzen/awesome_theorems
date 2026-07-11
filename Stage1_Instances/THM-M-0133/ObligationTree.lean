import Mathlib.NumberTheory.FLT.Four

/-! Conditional root composition for the frozen THM-M-0133 architecture. -/

namespace Stage1Instances.THM_M_0133.ObligationTree

def Root : Prop :=
  forall n : Nat, 3 <= n ->
    forall a b c : Nat, Ne a 0 -> Ne b 0 -> Ne c 0 ->
      Ne (a ^ n + b ^ n) (c ^ n)

/-- The pinned mathlib assembly consumes the still-open all-odd-prime branch.
This checks composition only and does not prove that branch. -/
theorem root_compose
    (oddPrimeCases : forall p, Nat.Prime p -> Odd p -> FermatLastTheoremFor p) :
    Root := by
  simpa [Root, FermatLastTheorem, FermatLastTheoremFor, FermatLastTheoremWith] using
    FermatLastTheorem.of_odd_primes oddPrimeCases

theorem root_exact_type :
    Root =
      (forall n : Nat, 3 <= n ->
        forall a b c : Nat, Ne a 0 -> Ne b 0 -> Ne c 0 ->
          Ne (a ^ n + b ^ n) (c ^ n)) :=
  rfl

#print root_compose
#print axioms root_compose

end Stage1Instances.THM_M_0133.ObligationTree
