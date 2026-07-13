import Mathlib.Data.Int.GCD

/-!
# THM-M-0473 discovery-only intake probe

These checks authenticate the pinned extended-gcd APIs and two candidate existential wrappers.
They do not select the catalog's missing domain conventions, freeze a canonical target, or audit a
proof body for rev-5.6 proof credit.
-/

#check Nat.gcd
#check Nat.gcdA
#check Nat.gcdB
#check Nat.gcd_eq_gcd_ab
#check Int.gcd
#check Int.gcdA
#check Int.gcdB
#check Int.gcd_eq_gcd_ab

#print axioms Nat.gcd_eq_gcd_ab
#print axioms Int.gcd_eq_gcd_ab

example (a b : Nat) :
    ∃ x y : Int, (Nat.gcd a b : Int) = (a : Int) * x + (b : Int) * y := by
  exact ⟨a.gcdA b, a.gcdB b, Nat.gcd_eq_gcd_ab a b⟩

example (a b : Int) :
    ∃ x y : Int, (Int.gcd a b : Int) = a * x + b * y := by
  exact ⟨Int.gcdA a b, Int.gcdB a b, Int.gcd_eq_gcd_ab a b⟩

example :
    ∃ x y : Int, (Int.gcd (0 : Int) 0 : Int) = (0 : Int) * x + 0 * y := by
  exact ⟨Int.gcdA 0 0, Int.gcdB 0 0, Int.gcd_eq_gcd_ab 0 0⟩
