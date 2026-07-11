import Mathlib.Analysis.Distribution.TemperedDistribution
import Mathlib.RingTheory.MvPolynomial.Basic

/-!
# THM-M-1255: exact Malgrange-Ehrenpreis statement

This module freezes the statement boundary only. It contains no proof of the
Malgrange-Ehrenpreis theorem.
-/

noncomputable section

open scoped SchwartzMap

namespace Stage1Instances.THM_M_1255

universe u

abbrev Space (ι : Type u) [Fintype ι] : Type u :=
  EuclideanSpace ℝ ι

abbrev TemperedDist (ι : Type u) [Fintype ι] : Type u :=
  𝓢'(Space ι, ℂ)

abbrev OperatorEnd (ι : Type u) [Fintype ι] : Type u :=
  Module.End ℂ (TemperedDist ι)

def deltaZero (ι : Type u) [Fintype ι] : TemperedDist ι :=
  TemperedDistribution.delta (0 : Space ι)

def coordinateDirection (ι : Type u) [Fintype ι] [DecidableEq ι] (i : ι) : Space ι :=
  EuclideanSpace.single i (1 : ℝ)

def coordinateDerivative
    (ι : Type u) [Fintype ι] [DecidableEq ι] (i : ι) : OperatorEnd ι :=
  LineDeriv.lineDerivOpCLM ℂ (TemperedDist ι) (coordinateDirection ι i)

/-- A polynomial action is the constant-coefficient differential calculus:
each variable is sent to differentiation in its coordinate direction. -/
structure PolynomialDifferentialAction
    (ι : Type u) [Fintype ι] [DecidableEq ι] : Type u where
  toAlgHom : MvPolynomial ι ℂ →ₐ[ℂ] OperatorEnd ι
  map_X : ∀ i : ι, toAlgHom (MvPolynomial.X i) = coordinateDerivative ι i

/-- Every nonzero constant-coefficient polynomial differential operator on a
finite-dimensional real coordinate space has a complex tempered fundamental
solution. The existentially packaged action prevents the statement from
assuming the still-unconstructed polynomial differential calculus. -/
def MalgrangeEhrenpreisTarget : Prop :=
  ∀ (ι : Type u) [Fintype ι] [DecidableEq ι],
    ∃ A : PolynomialDifferentialAction ι,
      ∀ (P : MvPolynomial ι ℂ), P ≠ 0 →
        ∃ E : TemperedDist ι, A.toAlgHom P E = deltaZero ι

/-- The fixed-action form used by the historical candidate. -/
def FixedActionStatement
    (ι : Type u) [Fintype ι] [DecidableEq ι]
    (A : PolynomialDifferentialAction ι) : Prop :=
  ∀ (P : MvPolynomial ι ℂ), P ≠ 0 →
    ∃ E : TemperedDist ι, A.toAlgHom P E = deltaZero ι

/-- Checked packaging identity between the root and its fixed-action form. -/
theorem target_iff_exists_fixedActionStatement :
    MalgrangeEhrenpreisTarget.{u} ↔
      ∀ (ι : Type u) [Fintype ι] [DecidableEq ι],
        ∃ A : PolynomialDifferentialAction ι, FixedActionStatement ι A :=
  by
    constructor <;> intro h <;> intro ι _ _
    · rcases h ι with ⟨A, hA⟩
      exact ⟨A, hA⟩
    · rcases h ι with ⟨A, hA⟩
      exact ⟨A, hA⟩

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationAllowsZeroPolynomial : Prop :=
  ∀ (ι : Type u) [Fintype ι] [DecidableEq ι],
    ∃ A : PolynomialDifferentialAction ι,
      ∀ P : MvPolynomial ι ℂ,
        ∃ E : TemperedDist ι, A.toAlgHom P E = deltaZero ι

def mutationRealPolynomial : Prop :=
  ∀ (ι : Type u) [Fintype ι] [DecidableEq ι],
    ∀ P : MvPolynomial ι ℝ, P ≠ 0 → True

def mutationAssumesAction : Prop :=
  ∀ (ι : Type u) [Fintype ι] [DecidableEq ι],
    ∀ A : PolynomialDifferentialAction ι,
      ∀ (P : MvPolynomial ι ℂ), P ≠ 0 →
        ∃ E : TemperedDist ι, A.toAlgHom P E = deltaZero ι

def mutationOneDimensional : Prop :=
  ∃ A : PolynomialDifferentialAction (Fin 1),
    ∀ (P : MvPolynomial (Fin 1) ℂ), P ≠ 0 →
      ∃ E : TemperedDist (Fin 1), A.toAlgHom P E = deltaZero (Fin 1)

end Stage1Instances.THM_M_1255

set_option pp.explicit true in
#print Stage1Instances.THM_M_1255.MalgrangeEhrenpreisTarget
