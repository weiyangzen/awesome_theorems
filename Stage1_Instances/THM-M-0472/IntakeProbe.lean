import Init.Data.Nat.Gcd

/-!
# THM-M-0472 discovery-only intake probe

This file checks pinned interfaces adjacent to the Euclidean algorithm and its correctness
boundary. It does not select a source-exact target or claim proof credit.
-/

#check Nat.gcd
#check Nat.gcd_zero_left
#check Nat.gcd_def
#check Nat.gcd_rec
#check Nat.gcd.induction
#check Nat.gcd_dvd_left
#check Nat.gcd_dvd_right
#check Nat.dvd_gcd
#check Nat.gcd_eq_iff
#print axioms Nat.gcd_rec
#print axioms Nat.gcd_eq_iff

example (m n : Nat) : Nat.gcd m n = Nat.gcd (n % m) m :=
  Nat.gcd_rec m n

example (m n : Nat) : Nat.gcd m n ∣ m ∧ Nat.gcd m n ∣ n :=
  ⟨Nat.gcd_dvd_left m n, Nat.gcd_dvd_right m n⟩

example (m n d : Nat) (hdm : d ∣ m) (hdn : d ∣ n) : d ∣ Nat.gcd m n :=
  Nat.dvd_gcd hdm hdn

example (m n g : Nat) :
    Nat.gcd m n = g ↔ g ∣ m ∧ g ∣ n ∧ ∀ d, d ∣ m → d ∣ n → d ∣ g :=
  Nat.gcd_eq_iff

example (n : Nat) : Nat.gcd 0 n = n :=
  Nat.gcd_zero_left n

example : Nat.gcd 48 18 = 6 := by decide
