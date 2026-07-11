import Mathlib.NumberTheory.Height.NumberField

/-!
# THM-M-0396: Baker-Matveev lower bound (statement boundary)

This module freezes the standard real, multiplicative form of Matveev's
explicit lower bound for a nonzero linear form in logarithms. It states a
proposition only and does not assert the theorem.
-/

noncomputable section

open scoped BigOperators

namespace Stage1Rev56.THMM0396

universe u

/-- The real value of the algebraic product occurring in the selected theorem. -/
def algebraicProduct {K : Type*} [Field K] {n : Nat}
    (embedding : K →+* Real) (alpha : Fin n → K) (coeff : Fin n → Int) : Real :=
  ∏ i, embedding (alpha i) ^ coeff i

/-- `Λ = α₁^b₁ ... αₙ^bₙ - 1` in the standard multiplicative formulation. -/
def linearFormValue {K : Type*} [Field K] {n : Nat}
    (embedding : K →+* Real) (alpha : Fin n → K) (coeff : Fin n → Int) : Real :=
  algebraicProduct embedding alpha coeff - 1

/-- The explicit positive quantity in the selected Matveev bound. -/
def exponentBound (n : Nat) (D B : Real) (A : Fin n → Real) : Real :=
  (14 / 10 : Real) * 30 ^ (n + 3) * (n : Real) ^ (9 / 2 : Real) * D ^ 2 *
    (1 + Real.log D) * (1 + Real.log (n * B)) * ∏ i, A i

/--
The selected exact target.

Here `K` is a number field of degree `D`, all `alpha i` are positive in the
chosen real embedding, `A i` majorizes the normalized logarithmic height and
the absolute logarithm, and `B` majorizes the nonzero integer coefficients.
For a nonzero multiplicative linear form, its logarithmic absolute value is
strictly greater than the negative explicit Matveev quantity.
-/
def Statement : Prop :=
  ∀ (n : Nat),
    1 ≤ n →
    ∀ (K : Type u) [Field K] [NumberField K]
      (embedding : K →+* Real) (alpha : Fin n → K) (coeff : Fin n → Int)
      (A : Fin n → Real) (B : Real),
      (∀ i, 0 < embedding (alpha i)) →
      (∀ i, max (Height.logHeight₁ (alpha i))
          |Real.log (embedding (alpha i))| ≤ A i) →
      (∀ i, (16 / 100 : Real) ≤ A i) →
      (1 : Real) ≤ B →
      (∀ i, (Int.natAbs (coeff i) : Real) ≤ B) →
      linearFormValue embedding alpha coeff ≠ 0 →
      -exponentBound n (Module.finrank Rat K : Real) B A <
        Real.log |linearFormValue embedding alpha coeff|

/-- Checked expansion of every binder, hypothesis, and the conclusion. -/
theorem statement_iff_expanded :
    Statement.{u} ↔
      ∀ (n : Nat),
        1 ≤ n →
        ∀ (K : Type u) [Field K] [NumberField K]
          (embedding : K →+* Real) (alpha : Fin n → K) (coeff : Fin n → Int)
          (A : Fin n → Real) (B : Real),
          (∀ i, 0 < embedding (alpha i)) →
          (∀ i, max (Height.logHeight₁ (alpha i))
              |Real.log (embedding (alpha i))| ≤ A i) →
          (∀ i, (16 / 100 : Real) ≤ A i) →
          (1 : Real) ≤ B →
          (∀ i, (Int.natAbs (coeff i) : Real) ≤ B) →
          linearFormValue embedding alpha coeff ≠ 0 →
          -exponentBound n (Module.finrank Rat K : Real) B A <
            Real.log |linearFormValue embedding alpha coeff| := by
  simp only [Statement]

/-- Boundary check: zero coefficients force the excluded zero linear form. -/
theorem linearFormValue_eq_zero_of_coeff_zero {K : Type*} [Field K] {n : Nat}
    (embedding : K →+* Real) (alpha : Fin n → K)
    (coeff : Fin n → Int) (hcoeff : ∀ i, coeff i = 0) :
    linearFormValue embedding alpha coeff = 0 := by
  simp [linearFormValue, algebraicProduct, hcoeff]

#check Statement

end Stage1Rev56.THMM0396
