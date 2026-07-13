import Mathlib.NumberTheory.Real.GoldenRatio

/-!
# THM-M-0927 discovery-only intake probe

These checks authenticate the pinned Fibonacci, golden-ratio, and direct Binet-formula interfaces.
They do not choose a source-approved canonical statement, perform the downstream anchor audit, or
grant statement or proof credit.
-/

#check Nat.fib
#check Real.goldenRatio
#check Real.goldenConj
#check Real.coe_fib_eq'
#check Real.coe_fib_eq
#check Real.coe_intFib_eq

#print axioms Real.coe_fib_eq'
#print axioms Real.coe_fib_eq
#print axioms Real.coe_intFib_eq
