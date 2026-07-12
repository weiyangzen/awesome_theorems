import Mathlib.Data.Real.Basic

/-!
# THM-M-1111: Tao--Vu Four Moment Theorem statement

This module freezes the quantifier structure of Theorem 15 in arXiv:0906.0510v10.
The analytic notions are parameters of an explicit semantic interface so that the
statement does not pretend that mathlib already supplies a random-Hermitian-matrix
and ordered-eigenvalue API with the conventions of the paper.  No proof of the
theorem is supplied here.
-/

namespace Stage1Instances.THM_M_1111

/-- Semantic operations needed to state the source theorem.  Later phases must
implement these fields with measure-theoretic random Hermitian matrices; none of
the fields carries proof credit. -/
structure FourMomentSemantics where
  Ensemble : Nat → Type
  Observable : Nat → Type
  obeysC0 : {n : Nat} → (C C' : ℝ) → Ensemble n → Prop
  offDiagonalMatch : {n : Nat} → Ensemble n → Ensemble n →
    (i j order : Nat) → Prop
  diagonalMatch : {n : Nat} → Ensemble n → Ensemble n →
    (i order : Nat) → Prop
  smooth : {k : Nat} → Observable k → Prop
  derivativeBound : {k : Nat} → Observable k → Nat → ℝ → Prop
  expectedEigenvalueStatistic : {n k : Nat} →
    Ensemble n → Observable k → (Fin k → Fin n) → ℝ
  powerBound : Nat → ℝ → ℝ

/-- The exact four-moment (not the weaker three-moment) branch of Tao and Vu,
Theorem 15.  `C` and `C'` are the uniform Condition C0 constants; consequently
the threshold may depend on them, as well as on `ε` and `k`, but not on the two
ensembles, observable, or eigenvalue indices. -/
def TaoVuFourMomentTarget (S : FourMomentSemantics) : Prop :=
  ∃ c0 : ℝ, 0 < c0 ∧
    ∀ ε : ℝ, 0 < ε → ε < 1 →
    ∀ k : Nat, 1 ≤ k →
    ∀ C C' : ℝ, 0 < C → 0 < C' →
    ∃ N : Nat, ∀ n : Nat, N ≤ n →
    ∀ M M' : S.Ensemble n,
      S.obeysC0 C C' M → S.obeysC0 C C' M' →
      (∀ i j : Nat, i < j → j < n → S.offDiagonalMatch M M' i j 4) →
      (∀ i : Nat, i < n → S.diagonalMatch M M' i 2) →
      ∀ G : S.Observable k,
        S.smooth G →
        (∀ derivativeOrder : Nat, derivativeOrder ≤ 5 →
          S.derivativeBound G derivativeOrder (S.powerBound n c0)) →
        ∀ indices : Fin k → Fin n,
          (∀ r s : Fin k, r < s → (indices r).val < (indices s).val) →
          (∀ r : Fin k,
            ε * (n : ℝ) ≤ ((indices r : Fin n) : Nat) ∧
            (((indices r : Fin n) : Nat) : ℝ) ≤ (1 - ε) * (n : ℝ)) →
          |S.expectedEigenvalueStatistic M G indices -
              S.expectedEigenvalueStatistic M' G indices| ≤ S.powerBound n (-c0)

-- Structural mutations are elaborated separately and rejected by the checker.
def mutationOffDiagonalOrderThree (S : FourMomentSemantics) : Prop :=
  ∃ c0 : ℝ, 0 < c0 ∧ ∀ n : Nat, ∀ M M' : S.Ensemble n,
    (∀ i j : Nat, i < j → j < n → S.offDiagonalMatch M M' i j 3) → True

def mutationNoBulkRestriction (S : FourMomentSemantics) : Prop :=
  ∃ c0 : ℝ, 0 < c0 ∧ ∀ n k : Nat, ∀ M M' : S.Ensemble n,
    ∀ G : S.Observable k, ∀ indices : Fin k → Fin n,
      |S.expectedEigenvalueStatistic M G indices -
          S.expectedEigenvalueStatistic M' G indices| ≤ S.powerBound n (-c0)

def mutationDiagonalOrderFour (S : FourMomentSemantics) : Prop :=
  ∀ n : Nat, ∀ M M' : S.Ensemble n,
    ∀ i : Nat, i < n → S.diagonalMatch M M' i 4

end Stage1Instances.THM_M_1111

set_option pp.explicit true in
#print Stage1Instances.THM_M_1111.TaoVuFourMomentTarget
