import Mathlib.Analysis.Distribution.TemperedDistribution
import Mathlib.RingTheory.MvPolynomial.Basic

/-!
# THM-M-1255 conditional obligation composition

This module checks only the interfaces and final composition selected by the
frozen obligation architecture. The two substantive packages remain explicit
premises; no Malgrange-Ehrenpreis proof is asserted here.
-/

noncomputable section

namespace Stage1Instances.THM_M_1255

universe u

open scoped SchwartzMap

-- The statement interface is repeated because this standalone validation file
-- is elaborated directly rather than through a generated local `.olean`.
abbrev Space (ι : Type u) [Fintype ι] : Type u := EuclideanSpace ℝ ι
abbrev TemperedDist (ι : Type u) [Fintype ι] : Type u := 𝓢'(Space ι, ℂ)
abbrev OperatorEnd (ι : Type u) [Fintype ι] : Type u := Module.End ℂ (TemperedDist ι)

def deltaZero (ι : Type u) [Fintype ι] : TemperedDist ι :=
  TemperedDistribution.delta (0 : Space ι)

def coordinateDirection (ι : Type u) [Fintype ι] [DecidableEq ι] (i : ι) : Space ι :=
  EuclideanSpace.single i (1 : ℝ)

def coordinateDerivative
    (ι : Type u) [Fintype ι] [DecidableEq ι] (i : ι) : OperatorEnd ι :=
  LineDeriv.lineDerivOpCLM ℂ (TemperedDist ι) (coordinateDirection ι i)

structure PolynomialDifferentialAction
    (ι : Type u) [Fintype ι] [DecidableEq ι] : Type u where
  toAlgHom : MvPolynomial ι ℂ →ₐ[ℂ] OperatorEnd ι
  map_X : ∀ i : ι, toAlgHom (MvPolynomial.X i) = coordinateDerivative ι i

def MalgrangeEhrenpreisTarget : Prop :=
  ∀ (ι : Type u) [Fintype ι] [DecidableEq ι],
    ∃ A : PolynomialDifferentialAction ι,
      ∀ (P : MvPolynomial ι ℂ), P ≠ 0 →
        ∃ E : TemperedDist ι, A.toAlgHom P E = deltaZero ι

/-- A coherent choice of the polynomial differential action in every finite
coordinate dimension. -/
structure PolynomialActionPackage : Type (u + 1) where
  action : forall (ι : Type u) [Fintype ι] [DecidableEq ι],
    PolynomialDifferentialAction ι

/-- Fundamental solutions for every nonzero symbol, relative to the chosen
action package. -/
def FundamentalSolutionsFor (actions : PolynomialActionPackage.{u}) : Prop :=
  forall (ι : Type u) [Fintype ι] [DecidableEq ι]
    (P : MvPolynomial ι ℂ), P ≠ 0 ->
      exists E : TemperedDist ι,
        (actions.action ι).toAlgHom P E = deltaZero ι

/-- Kernel-checked conditional composition into the exact frozen root. -/
theorem root_of_action_and_fundamental_packages
    (actions : PolynomialActionPackage.{u})
    (solutions : FundamentalSolutionsFor actions) :
    MalgrangeEhrenpreisTarget.{u} := by
  intro ι _fintype _decidableEq
  refine ⟨actions.action ι, ?_⟩
  intro P hP
  exact solutions ι P hP

#print axioms root_of_action_and_fundamental_packages

end Stage1Instances.THM_M_1255
