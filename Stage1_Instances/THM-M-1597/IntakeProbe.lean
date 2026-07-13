import Mathlib.Data.Nat.ModEq
import Mathlib.Data.Nat.Totient
import Mathlib.NumberTheory.PowModTotient
import Mathlib.Data.ZMod.Basic

/-!
# THM-M-1597 discovery-only intake probe

These checks authenticate adjacent pinned modular-arithmetic APIs that could support a future
source-selected RSA correctness statement. They do not select that statement, define RSA, prove
round-trip correctness, or establish any security property.
-/

#check Nat.ModEq
#check Nat.ModEq.pow
#check Nat.ModEq.pow_totient
#check Nat.pow_totient_mod_eq_one
#check Nat.pow_add_mul_totient_mod_eq
#check Nat.totient_mul
#check Nat.totient_prime
#check Nat.modEq_and_modEq_iff_modEq_mul
#check ZMod.chineseRemainder

#print axioms Nat.ModEq.pow_totient
#print axioms Nat.modEq_and_modEq_iff_modEq_mul
