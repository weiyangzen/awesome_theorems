import Mathlib.Algebra.Polynomial.OfFn
import Mathlib.Data.Complex.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic

/-!
# THM-M-1356: exact Routh-Hurwitz statement

This module freezes Barkovsky's finite Hurwitz-matrix formulation for a real
polynomial written in descending coefficient order. It contains no proof of
the Routh-Hurwitz criterion.
-/

namespace Stage1Instances.THM_M_1356

/-- Source coefficient `a_j` of `a_0 z^n + ... + a_n`, with zero extension. -/
def sourceCoefficient {n : Nat} (a : Fin (n + 1) → Real) (j : Nat) : Real :=
  if h : j < n + 1 then a ⟨j, h⟩ else 0

/-- The finite Hurwitz matrix displayed in Barkovsky, Theorem 40.

Rows and columns are zero-based. Entry `(i,j)` is `a_(2*j+1-i)` when that
natural-number subtraction is defined, and is zero otherwise.
-/
def hurwitzMatrix {n : Nat} (a : Fin (n + 1) → Real) :
    Matrix (Fin n) (Fin n) Real :=
  fun i j ↦
    if (i : Nat) ≤ 2 * (j : Nat) + 1 then
      sourceCoefficient a (2 * (j : Nat) + 1 - (i : Nat))
    else 0

/-- The source minor `eta_(k+1)`, i.e. the leading `(k+1) × (k+1)`
principal minor of the finite Hurwitz matrix. -/
def hurwitzMinor {n : Nat} (a : Fin (n + 1) → Real) (k : Fin n) : Real :=
  Matrix.det ((hurwitzMatrix a).submatrix
    (Fin.castLE (Nat.succ_le_of_lt k.isLt))
    (Fin.castLE (Nat.succ_le_of_lt k.isLt)))

/-- The real polynomial corresponding to the source's descending coefficient
vector. -/
noncomputable def realPolynomial {n : Nat} (a : Fin (n + 1) → Real) : Polynomial Real :=
  Polynomial.ofFn (n + 1) fun j : Fin (n + 1) ↦ a ⟨n - (j : Nat), by omega⟩

/-- The descending-to-ascending adapter places `a_0` at degree `n`. -/
theorem realPolynomial_coeff_degree {n : Nat} (a : Fin (n + 1) → Real) :
    (realPolynomial a).coeff n = a 0 := by
  simp [realPolynomial]

/-- A positive source leading coefficient prevents degree drop. -/
theorem realPolynomial_natDegree_eq {n : Nat} (a : Fin (n + 1) → Real)
    (ha : 0 < a 0) : (realPolynomial a).natDegree = n := by
  apply Polynomial.natDegree_eq_of_le_of_coeff_ne_zero
  · exact Nat.le_of_lt_succ (Polynomial.ofFn_natDegree_lt (by omega) _)
  · simpa [realPolynomial] using ne_of_gt ha

/-- The complex polynomial obtained from the source's real polynomial. -/
noncomputable def complexPolynomial {n : Nat} (a : Fin (n + 1) → Real) : Polynomial Complex :=
  Polynomial.map Complex.ofRealHom
    (realPolynomial a)

/-- The source's positive leading coefficient. In this length-`n+1` encoding,
`a 0` is the coefficient of degree `n`, so positivity also prevents degree
drop. -/
noncomputable def IsPositiveDegreeN {n : Nat} (a : Fin (n + 1) → Real) : Prop :=
  0 < a 0

/-- All roots lie in the strict open left half-plane. -/
noncomputable def IsStrictlyStable {n : Nat} (a : Fin (n + 1) → Real) : Prop :=
  ∀ z : Complex, (complexPolynomial a).IsRoot z → z.re < 0

/-- Exact Barkovsky/Hurwitz target: for a positive-degree real polynomial
with positive leading coefficient, strict stability is equivalent to
positivity of every leading principal Hurwitz minor. -/
noncomputable def RouthHurwitzTarget : Prop :=
  ∀ (n : Nat), 0 < n → ∀ a : Fin (n + 1) → Real,
    IsPositiveDegreeN a →
      (IsStrictlyStable a ↔ ∀ k : Fin n, 0 < hurwitzMinor a k)

/-- A source-shaped spelling used to check the selected binder and definition
boundary. -/
noncomputable def ExpandedTarget : Prop :=
  ∀ (n : Nat), 0 < n → ∀ a : Fin (n + 1) → Real,
    0 < a 0 →
      (IsStrictlyStable a ↔ ∀ k : Fin n, 0 < hurwitzMinor a k)

/-- Checked definitional transport to the source-shaped expansion. -/
theorem routhHurwitzTarget_iff_expandedTarget :
    RouthHurwitzTarget ↔ ExpandedTarget :=
  Iff.rfl

-- Structural mutations. Each elaborates but is definitionally distinct from
-- the canonical target; the scoped checker verifies all four distinctions.
noncomputable def mutationRemovedPositiveLeadingCoefficient : Prop :=
  ∀ (n : Nat), 0 < n → ∀ a : Fin (n + 1) → Real,
    IsStrictlyStable a ↔ ∀ k : Fin n, 0 < hurwitzMinor a k

noncomputable def mutationChangedCoefficientDomain : Prop :=
  ∀ (n : Nat), 0 < n → ∀ a : Fin (n + 1) → Rat,
    0 < a 0 →
      ∀ z : Complex,
        (Polynomial.map (Rat.castHom Complex)
          (Polynomial.ofFn (n + 1) fun j : Fin (n + 1) ↦ a ⟨n - (j : Nat), by omega⟩)).IsRoot z →
          z.re < 0

noncomputable def mutationChangedBinderScope : Prop :=
  ∀ (n : Nat), 0 < n →
    (∀ a : Fin (n + 1) → Real, IsPositiveDegreeN a → IsStrictlyStable a) ↔
      ∀ a : Fin (n + 1) → Real, ∀ k : Fin n, 0 < hurwitzMinor a k

noncomputable def mutationAllowsZeroDegree : Prop :=
  ∀ (n : Nat) (a : Fin (n + 1) → Real),
    IsPositiveDegreeN a →
      (IsStrictlyStable a ↔ ∀ k : Fin n, 0 < hurwitzMinor a k)

#check_failure (rfl : RouthHurwitzTarget = mutationRemovedPositiveLeadingCoefficient)
#check_failure (rfl : RouthHurwitzTarget = mutationChangedCoefficientDomain)
#check_failure (rfl : RouthHurwitzTarget = mutationChangedBinderScope)
#check_failure (rfl : RouthHurwitzTarget = mutationAllowsZeroDegree)

end Stage1Instances.THM_M_1356

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_1356.RouthHurwitzTarget
