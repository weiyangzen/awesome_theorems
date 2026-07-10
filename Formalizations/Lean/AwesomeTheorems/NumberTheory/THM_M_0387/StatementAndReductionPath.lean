import Mathlib.NumberTheory.FLT.Four

namespace AwesomeTheorems.NumberTheory.THM_M_0387

/-- The exact natural-number statement selected as the repository's FLT root. -/
def fermatLastTheoremRootStatement : Prop :=
  FermatLastTheorem

/-- The family which remains after the checked exponent-four reduction. -/
def OddPrimeExponentClosure : Prop :=
  ∀ p : ℕ, Nat.Prime p → Odd p → FermatLastTheoremFor p

/-- The primitive natural-number formulation used by the coprime reduction. -/
def FermatLastTheoremForCoprime (n : ℕ) : Prop :=
  ∀ a b c : ℕ, a ≠ 0 → b ≠ 0 → c ≠ 0 →
    ({a, b, c} : Finset ℕ).gcd id = 1 → a ^ n + b ^ n ≠ c ^ n

/-- The selected root is definitionally the mathlib natural-number statement. -/
theorem fermatLastTheoremRootStatement_iff :
    fermatLastTheoremRootStatement ↔ FermatLastTheorem :=
  Iff.rfl

/-- The unrestricted and primitive natural-number formulations are equivalent. -/
theorem fermatLastTheoremFor_iff_coprime {n : ℕ} :
    FermatLastTheoremFor n ↔ FermatLastTheoremForCoprime n := by
  constructor
  · intro h a b c ha hb hc _
    exact h a b c ha hb hc
  · exact fermatLastTheoremWith_of_fermatLastTheoremWith_coprime

/-- Checked transport between the natural-number and integer formulations. -/
theorem fermatLastTheoremFor_iff_integer {n : ℕ} :
    FermatLastTheoremFor n ↔ FermatLastTheoremWith ℤ n :=
  fermatLastTheoremFor_iff_int

/-- Checked transport between the natural-number and rational formulations. -/
theorem fermatLastTheoremFor_iff_rational {n : ℕ} :
    FermatLastTheoremFor n ↔ FermatLastTheoremWith ℚ n :=
  fermatLastTheoremFor_iff_rat

/-- Exponent divisibility transports a checked fixed-exponent result upward. -/
theorem fltOfDivisorPath {m n : ℕ} (hdiv : m ∣ n) (hm : FermatLastTheoremFor m) :
    FermatLastTheoremFor n :=
  FermatLastTheoremFor.mono hdiv hm

/-- The exact checked assembly edge from all odd-prime exponents to the root. -/
theorem fermatLastTheoremRootOfOddPrimesPath
    (hodd : OddPrimeExponentClosure) : fermatLastTheoremRootStatement :=
  FermatLastTheorem.of_odd_primes hodd

/-- The exponent-zero boundary lies outside FLT but is vacuously true. -/
theorem fltExponentZeroPath : FermatLastTheoremFor 0 :=
  fermatLastTheoremFor_zero

/-- The exponent-one boundary lies outside FLT and is false. -/
theorem notFltExponentOnePath : ¬ FermatLastTheoremFor 1 :=
  not_fermatLastTheoremFor_one

/-- The exponent-two boundary lies outside FLT and is false. -/
theorem notFltExponentTwoPath : ¬ FermatLastTheoremFor 2 :=
  not_fermatLastTheoremFor_two

end AwesomeTheorems.NumberTheory.THM_M_0387
