import Mathlib.Data.Complex.Basic
import Mathlib.Data.Nat.Prime.Basic

/-!
# THM-M-0405: Bilu-Hanrot-Voutier statement

This file freezes the `n > 30` primitive-divisor theorem for Lucas and Lehmer
pairs.  It states the target only; it does not assert or prove the theorem.
-/

namespace Stage1.THM_M_0405

/-- The source condition that `alpha / beta` is not a root of unity. -/
def RatioNotRootOfUnity (alpha beta : ℂ) : Prop :=
  ∀ k : Nat, 0 < k → (alpha / beta) ^ k ≠ 1

/--
A Lucas pair, including its integer Lucas sequence.  The two integer
invariants are `alpha + beta` and `alpha * beta`; `term_spec` is the defining
identity `(alpha - beta) U_n = alpha^n - beta^n`.
-/
structure LucasPair where
  alpha : ℂ
  beta : ℂ
  sum : Int
  product : Int
  sum_eq : alpha + beta = sum
  product_eq : alpha * beta = product
  coprime : Nat.Coprime sum.natAbs product.natAbs
  sum_ne_zero : sum ≠ 0
  product_ne_zero : product ≠ 0
  ratio_not_root_of_unity : RatioNotRootOfUnity alpha beta
  term : Nat → Int
  term_spec : ∀ n : Nat,
    (term n : ℂ) * (alpha - beta) = alpha ^ n - beta ^ n

namespace LucasPair

/-- `(alpha - beta)^2`, expressed through the integral pair invariants. -/
def discriminant (L : LucasPair) : Int :=
  L.sum ^ 2 - 4 * L.product

/--
A primitive divisor of the `n`-th Lucas number: a prime divisor of that term
which divides neither the pair discriminant nor an earlier positive term.
-/
def IsPrimitiveDivisor (L : LucasPair) (p n : Nat) : Prop :=
  p.Prime ∧
    p ∣ (L.term n).natAbs ∧
    ¬ p ∣ L.discriminant.natAbs ∧
    ∀ m : Nat, 0 < m → m < n → ¬ p ∣ (L.term m).natAbs

end LucasPair

/--
A Lehmer pair, including its integer Lehmer sequence.  For odd indices the
defining denominator is `alpha - beta`; for even indices it is
`alpha^2 - beta^2`.
-/
structure LehmerPair where
  alpha : ℂ
  beta : ℂ
  sumSquare : Int
  product : Int
  sumSquare_eq : (alpha + beta) ^ 2 = sumSquare
  product_eq : alpha * beta = product
  coprime : Nat.Coprime sumSquare.natAbs product.natAbs
  sumSquare_ne_zero : sumSquare ≠ 0
  product_ne_zero : product ≠ 0
  ratio_not_root_of_unity : RatioNotRootOfUnity alpha beta
  term : Nat → Int
  term_spec_odd : ∀ n : Nat, n % 2 = 1 →
    (term n : ℂ) * (alpha - beta) = alpha ^ n - beta ^ n
  term_spec_even : ∀ n : Nat, n % 2 = 0 →
    (term n : ℂ) * (alpha ^ 2 - beta ^ 2) = alpha ^ n - beta ^ n

namespace LehmerPair

/-- `(alpha - beta)^2`, expressed through the integral pair invariants. -/
def discriminant (L : LehmerPair) : Int :=
  L.sumSquare - 4 * L.product

/-- `(alpha^2 - beta^2)^2` in terms of the integral pair invariants. -/
def squaredEvenDenominator (L : LehmerPair) : Int :=
  L.sumSquare * L.discriminant

/--
A primitive divisor of the `n`-th Lehmer number: a prime divisor of that term
which divides neither `(alpha^2 - beta^2)^2` nor an earlier positive term.
-/
def IsPrimitiveDivisor (L : LehmerPair) (p n : Nat) : Prop :=
  p.Prime ∧
    p ∣ (L.term n).natAbs ∧
    ¬ p ∣ L.squaredEvenDenominator.natAbs ∧
    ∀ m : Nat, 0 < m → m < n → ¬ p ∣ (L.term m).natAbs

end LehmerPair

/-- Exact normalized target for the Bilu-Hanrot-Voutier theorem. -/
def Statement : Prop :=
  (∀ (L : LucasPair) (n : Nat), 30 < n →
      ∃ p : Nat, L.IsPrimitiveDivisor p n) ∧
  (∀ (L : LehmerPair) (n : Nat), 30 < n →
      ∃ p : Nat, L.IsPrimitiveDivisor p n)

#check Statement

end Stage1.THM_M_0405
