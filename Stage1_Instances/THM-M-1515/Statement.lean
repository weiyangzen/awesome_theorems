import Mathlib.Analysis.Calculus.Deriv.Basic
import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.Analysis.Normed.Module.FiniteDimension

/-!
# THM-M-1515: exact finite-dimensional Noether statement

This module freezes the statement boundary only. It does not prove Noether's
theorem. The selected variant has a time-independent Lagrangian, a vertical
one-parameter infinitesimal symmetry, and a configuration-dependent boundary
term.
-/

noncomputable section

namespace Stage1Instances.THM_M_1515

universe u

variable (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]

/-- Data occurring in the selected finite-dimensional form of Noether's first
theorem. `generator` is the infinitesimal generator of the selected
one-parameter transformation; `boundary` is its quasi-invariance term. -/
structure NoetherData where
  lagrangian : E → E → ℝ
  generator : E → E
  boundary : E → ℝ

/-- Classical velocity of a curve in the configuration vector space. -/
def velocity (q : ℝ → E) (t : ℝ) : E :=
  deriv q t

/-- Partial Frechet derivative of the Lagrangian in its position argument. -/
def positionDerivative (D : NoetherData E) (x v : E) : E →L[ℝ] ℝ :=
  fderiv ℝ (fun y : E => D.lagrangian y v) x

/-- Partial Frechet derivative of the Lagrangian in its velocity argument. -/
def velocityDerivative (D : NoetherData E) (x v : E) : E →L[ℝ] ℝ :=
  fderiv ℝ (fun w : E => D.lagrangian x w) v

/-- The coordinate Euler-Lagrange equation along a curve. The derivative of
the momentum covector equals the position derivative of the Lagrangian. -/
def IsEulerLagrange (D : NoetherData E) (q : ℝ → E) : Prop :=
  ∀ t : ℝ,
    HasDerivAt
      (fun s : ℝ => velocityDerivative E D (q s) (velocity E q s))
      (positionDerivative E D (q t) (velocity E q t)) t

/-- Infinitesimal quasi-invariance of the Lagrangian. The right side is the
total time derivative of the boundary term along a state with velocity `v`. -/
def IsVariationalSymmetry (D : NoetherData E) : Prop :=
  ∀ x v : E,
    positionDerivative E D x v (D.generator x) +
        velocityDerivative E D x v (fderiv ℝ D.generator x v) =
      fderiv ℝ D.boundary x v

/-- Regularity assumptions that make the derivatives in the theorem carry
their intended analytic meaning rather than the fallback value of `fderiv`. -/
def IsRegularFor (D : NoetherData E) (q : ℝ → E) : Prop :=
  Differentiable ℝ (Function.uncurry D.lagrangian) ∧
    Differentiable ℝ D.generator ∧
      Differentiable ℝ D.boundary ∧ ContDiff ℝ 2 q

/-- Momentum paired with the infinitesimal generator, adjusted by the
quasi-invariance boundary term. -/
def noetherCharge (D : NoetherData E) (q : ℝ → E) (t : ℝ) : ℝ :=
  velocityDerivative E D (q t) (velocity E q t) (D.generator (q t)) -
    D.boundary (q t)

/-- The exact target selected at intake: the Noether charge has zero derivative
along every sufficiently regular Euler-Lagrange trajectory. -/
def NoetherFirstTheoremTarget : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E] (D : NoetherData E) (q : ℝ → E),
      IsRegularFor E D q →
        IsVariationalSymmetry E D →
          IsEulerLagrange E D q →
            ∀ t : ℝ, HasDerivAt (noetherCharge E D q) 0 t

/-- Direct expansion used to check the frozen binder and implication order. -/
def ExpandedTargetShape : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E] (D : NoetherData E) (q : ℝ → E),
      IsRegularFor E D q →
        IsVariationalSymmetry E D →
          IsEulerLagrange E D q →
            ∀ t : ℝ, HasDerivAt (noetherCharge E D q) 0 t

theorem target_iff_expanded :
    NoetherFirstTheoremTarget.{u} ↔ ExpandedTargetShape.{u} :=
  Iff.rfl

-- Structural mutations: these elaborate but are deliberately not the target.
def mutationStrictSymmetryOnly : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E] (D : NoetherData E) (q : ℝ → E),
      D.boundary = 0 → IsRegularFor E D q → IsVariationalSymmetry E D →
        IsEulerLagrange E D q → ∀ t, HasDerivAt (noetherCharge E D q) 0 t

def mutationRemovedEulerLagrange : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E] (D : NoetherData E) (q : ℝ → E),
      IsRegularFor E D q → IsVariationalSymmetry E D →
        ∀ t, HasDerivAt (noetherCharge E D q) 0 t

def mutationInfiniteDimensional : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    (D : NoetherData E) (q : ℝ → E),
      IsRegularFor E D q → IsVariationalSymmetry E D →
        IsEulerLagrange E D q → ∀ t, HasDerivAt (noetherCharge E D q) 0 t

def mutationConservedByDerivFallback : Prop :=
  ∀ (E : Type u) [NormedAddCommGroup E] [NormedSpace ℝ E]
    [FiniteDimensional ℝ E] (D : NoetherData E) (q : ℝ → E),
      IsRegularFor E D q → IsVariationalSymmetry E D →
        IsEulerLagrange E D q → ∀ t, deriv (noetherCharge E D q) t = 0

end Stage1Instances.THM_M_1515

set_option pp.explicit true in
#print Stage1Instances.THM_M_1515.NoetherFirstTheoremTarget
