import Mathlib.LinearAlgebra.AffineSpace.AffineMap
import Mathlib.NumberTheory.ArithmeticFunction.VonMangoldt
import Mathlib.NumberTheory.LSeries.PrimesInAP
import Mathlib.NumberTheory.PrimeCounting

-- Discovery-only checks for substrate adjacent to a future exact statement.
#check Nat.Prime
#check Nat.primeCounting
#check Nat.tendsto_primeCounting
#check ArithmeticFunction.vonMangoldt
#check ArithmeticFunction.vonMangoldt_apply_prime
#check ArithmeticFunction.vonMangoldt_sum
#check AffineMap
#check LinearMap

#print axioms Nat.tendsto_primeCounting
#print axioms ArithmeticFunction.vonMangoldt_apply_prime
#print axioms ArithmeticFunction.vonMangoldt_sum
