import Mathlib.Algebra.LinearRecurrence
import Mathlib.Data.Nat.Fib.Basic

/-!
# THM-M-0924 discovery-only intake probe

These commands authenticate pinned generic recurrence and Fibonacci interfaces that could support
a future Lucas-number encoding. They do not define Lucas numbers, select a canonical proposition,
declare the THM-M-0924 target, or grant source or proof credit.
-/

#check LinearRecurrence
#check LinearRecurrence.IsSolution
#check LinearRecurrence.mkSol
#check LinearRecurrence.is_sol_mkSol
#check LinearRecurrence.mkSol_eq_init
#check LinearRecurrence.eq_mk_of_is_sol_of_eq_init'
#check LinearRecurrence.sol_eq_of_eq_init
#check Nat.fib
#check Nat.fib_zero
#check Nat.fib_one
#check Nat.fib_add_two

#print axioms LinearRecurrence.is_sol_mkSol
#print axioms LinearRecurrence.eq_mk_of_is_sol_of_eq_init'
#print axioms LinearRecurrence.sol_eq_of_eq_init
#print axioms Nat.fib_add_two
