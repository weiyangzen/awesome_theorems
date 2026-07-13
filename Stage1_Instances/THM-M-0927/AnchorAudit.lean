import Mathlib.NumberTheory.Real.GoldenRatio
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0927 immutable anchor probe

This audit-local target is a literal copy of the statement-phase proposition.
The checked adapter changes only the spelling of the two characteristic roots;
it does not change the index domain, Fibonacci definition, codomain, or result.
This module is candidate evidence, not accepted proof-phase or release evidence.
-/

noncomputable section

namespace Stage1Instances.THM_M_0927_AnchorAudit

/-- Literal audit copy of `Stage1Instances.THM_M_0927.BinetFormulaTarget`. -/
def ExactTarget : Prop :=
  forall n : Nat,
    (Nat.fib n : Real) =
      ((1 + Real.sqrt 5) ^ n - (1 - Real.sqrt 5) ^ n) /
        ((2 : Real) ^ n * Real.sqrt 5)

/-- Exact specialization and algebraic transport from pinned mathlib's natural-index
Binet theorem to the frozen DLMF radical spelling. -/
theorem exactTarget_mathlib_candidate : ExactTarget := by
  intro n
  rw [Real.coe_fib_eq n]
  simp only [Real.goldenRatio, Real.goldenConj, div_pow]
  ring

#check Real.coe_fib_eq
#check Real.coe_fib_eq'
#check Real.coe_intFib_eq

#print axioms Real.coe_fib_eq
#print axioms Real.coe_fib_eq'
#print axioms Real.coe_intFib_eq
#print axioms exactTarget_mathlib_candidate

assert_no_sorry Real.coe_fib_eq
assert_no_sorry Real.coe_fib_eq'
assert_no_sorry Real.coe_intFib_eq
assert_no_sorry exactTarget_mathlib_candidate

#print sorries Real.coe_fib_eq
#print sorries Real.coe_fib_eq'
#print sorries Real.coe_intFib_eq
#print sorries exactTarget_mathlib_candidate

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0927_AnchorAudit
