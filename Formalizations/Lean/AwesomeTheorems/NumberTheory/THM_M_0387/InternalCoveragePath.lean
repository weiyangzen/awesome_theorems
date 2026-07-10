import Mathlib.NumberTheory.FLT.Three
import Mathlib.NumberTheory.FLT.Four
import FltRegular.FltRegular

namespace AwesomeTheorems.NumberTheory.THM_M_0387

/-!
Checked aliases for high-risk internal proof-tree endpoints. Each declaration
keeps its imported proof body in mathlib or the pinned `flt-regular` package;
the aliases make the exact local validation boundary explicit.
-/

theorem flt4MinimalWitnessPath {a b c : ℤ} (h : Fermat42 a b c) :
    ∃ a0 b0 c0, Fermat42.Minimal a0 b0 c0 :=
  Fermat42.exists_minimal h

theorem flt4CoprimeMinimalPath {a b c : ℤ} (h : Fermat42.Minimal a b c) :
    IsCoprime a b :=
  Fermat42.coprime_of_minimal h

theorem flt4OddMinimalPath {a b c : ℤ} (h : Fermat42 a b c) :
    ∃ a0 b0 c0, Fermat42.Minimal a0 b0 c0 ∧ a0 % 2 = 1 :=
  Fermat42.exists_odd_minimal h

theorem flt4PositiveOddMinimalPath {a b c : ℤ} (h : Fermat42 a b c) :
    ∃ a0 b0 c0, Fermat42.Minimal a0 b0 c0 ∧ a0 % 2 = 1 ∧ 0 < c0 :=
  Fermat42.exists_pos_odd_minimal h

theorem flt4CoprimeSquareSumPath {r s : ℤ} (h : IsCoprime s r) :
    IsCoprime (r ^ 2 + s ^ 2) r :=
  Int.isCoprime_of_sq_sum h

theorem flt4CoprimeSquareSumSymmPath {r s : ℤ} (h : IsCoprime r s) :
    IsCoprime (r ^ 2 + s ^ 2) (r * s) :=
  Int.isCoprime_of_sq_sum' h

theorem flt4NoMinimalPath {a b c : ℤ} (h : Fermat42.Minimal a b c)
    (ha2 : a % 2 = 1) (hc : 0 < c) : False :=
  Fermat42.not_minimal h ha2 hc

theorem flt4BridgeTerminalPath {a b c : ℤ} (ha : a ≠ 0) (hb : b ≠ 0) :
    a ^ 4 + b ^ 4 ≠ c ^ 2 :=
  not_fermat_42 ha hb

theorem regularPrimePrimitivePath {a b c : ℤ} {n : ℕ}
    (h : a ^ n + b ^ n = c ^ n) (hprod : a * b * c ≠ 0) :
    (a / ({a, b, c} : Finset ℤ).gcd id) ^ n +
        (b / ({a, b, c} : Finset ℤ).gcd id) ^ n =
        (c / ({a, b, c} : Finset ℤ).gcd id) ^ n ∧
      ({a / ({a, b, c} : Finset ℤ).gcd id,
          b / ({a, b, c} : Finset ℤ).gcd id,
          c / ({a, b, c} : Finset ℤ).gcd id} : Finset ℤ).gcd id = 1 ∧
      a / ({a, b, c} : Finset ℤ).gcd id *
          (b / ({a, b, c} : Finset ℤ).gcd id) *
          (c / ({a, b, c} : Finset ℤ).gcd id) ≠ 0 :=
  FltRegular.MayAssume.coprime h hprod

theorem regularPrimeDivisibilityPath {p : ℕ} {a b c : ℤ}
    (hpri : p.Prime) (hp : p ≠ 3) (h : a ^ p + b ^ p = c ^ p)
    (hab : a ≡ b [ZMOD p]) (hbc : b ≡ -c [ZMOD p]) : (p : ℤ) ∣ c :=
  FltRegular.p_dvd_c_of_ab_of_anegc hpri hp h hab hbc

theorem regularPrimeNoncongruencePath {p : ℕ} {a b c : ℤ}
    (hpri : p.Prime) (hp5 : 5 ≤ p) (hprod : a * b * c ≠ 0)
    (h : a ^ p + b ^ p = c ^ p) (hgcd : ({a, b, c} : Finset ℤ).gcd id = 1)
    (caseI : ¬(p : ℤ) ∣ a * b * c) :
    ∃ x y z, x ^ p + y ^ p = z ^ p ∧ ({x, y, z} : Finset ℤ).gcd id = 1 ∧
      ¬x ≡ y [ZMOD p] ∧ x * y * z ≠ 0 ∧ ¬(p : ℤ) ∣ x * y * z :=
  FltRegular.a_not_cong_b hpri hp5 hprod h hgcd caseI

theorem regularPrimeCaseIPath {a b c : ℤ} {p : ℕ} [Fact p.Prime]
    (hreg : IsRegularPrime p) (caseI : ¬(p : ℤ) ∣ a * b * c) :
    a ^ p + b ^ p ≠ c ^ p :=
  FltRegular.caseI hreg caseI

theorem regularPrimeCaseIIPath {a b c : ℤ} {p : ℕ} [Fact p.Prime]
    (hreg : IsRegularPrime p) (hodd : p ≠ 2) (hprod : a * b * c ≠ 0)
    (hgcd : ({a, b, c} : Finset ℤ).gcd id = 1)
    (caseII : (p : ℤ) ∣ a * b * c) : a ^ p + b ^ p ≠ c ^ p :=
  FltRegular.caseII hreg hodd hprod hgcd caseII

end AwesomeTheorems.NumberTheory.THM_M_0387
