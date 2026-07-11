import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Geometry.Euclidean.Volume.Measure
import Mathlib.MeasureTheory.Function.LpSpace.Basic
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
The statement node for THM-M-1234.  This selects the whole-plane, unforced,
finite-energy form of the two-dimensional Yudovich existence theorem.  The
weak momentum equation is pressure-free because it is tested only against
divergence-free vector fields.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal

namespace Stage1Rev56.THMM1234

abbrev Plane := EuclideanSpace ℝ (Fin 2)
abbrev StaticVelocity := Plane → Plane
abbrev StaticVorticity := Plane → ℝ
abbrev Velocity := ℝ → Plane → Plane
abbrev Vorticity := ℝ → Plane → ℝ

def unitVector (i : Fin 2) : Plane :=
  EuclideanSpace.single i 1

def dot (v w : Plane) : ℝ :=
  ∑ i, v i * w i

def spatialDerivative (f : Plane → ℝ) (j : Fin 2) (x : Plane) : ℝ :=
  fderiv ℝ f x (unitVector j)

def SmoothCompactScalarTest (ψ : Plane → ℝ) : Prop :=
  ContDiff ℝ ⊤ ψ ∧ HasCompactSupport ψ

def SmoothCompactSpacetimeScalarTest (ψ : ℝ → Plane → ℝ) : Prop :=
  ContDiff ℝ ⊤ (Function.uncurry ψ) ∧ HasCompactSupport (Function.uncurry ψ)

def SmoothCompactSpacetimeVectorTest (φ : ℝ → Plane → Plane) : Prop :=
  ContDiff ℝ ⊤ (Function.uncurry φ) ∧ HasCompactSupport (Function.uncurry φ)

def WeaklyDivergenceFree (u : StaticVelocity) : Prop :=
  ∀ ψ : Plane → ℝ, SmoothCompactScalarTest ψ →
    (∫ x, ∑ i : Fin 2, u x i * spatialDerivative ψ i x) = 0

def WeakCurl (u : StaticVelocity) (ω : StaticVorticity) : Prop :=
  ∀ ψ : Plane → ℝ, SmoothCompactScalarTest ψ →
    (∫ x, ω x * ψ x) =
      ∫ x, u x 1 * spatialDerivative ψ 0 x -
        u x 0 * spatialDerivative ψ 1 x

def DivergenceFreeTest (φ : ℝ → Plane → Plane) : Prop :=
  ∀ t x,
    ∑ i : Fin 2, spatialDerivative (fun y => φ t y i) i x = 0

def WeakMomentumEquation (u₀ : StaticVelocity) (u : Velocity) : Prop :=
  ∀ φ : ℝ → Plane → Plane,
    SmoothCompactSpacetimeVectorTest φ → DivergenceFreeTest φ →
      (∫ t in Set.Ici (0 : ℝ), ∫ x,
        (∑ i : Fin 2, u t x i * deriv (fun s => φ s x i) t) +
          ∑ i : Fin 2, ∑ j : Fin 2,
            u t x i * u t x j *
              spatialDerivative (fun y => φ t y i) j x) +
        ∫ x, dot (u₀ x) (φ 0 x) = 0

structure InitialData (u₀ : StaticVelocity) (ω₀ : StaticVorticity) : Prop where
  velocityMeasurable : AEStronglyMeasurable u₀ volume
  vorticityMeasurable : AEStronglyMeasurable ω₀ volume
  finiteEnergy : MemLp u₀ 2 volume
  boundedVorticity : MemLp ω₀ ⊤ volume
  divergenceFree : WeaklyDivergenceFree u₀
  vorticityIsCurl : WeakCurl u₀ ω₀

structure GlobalWeakSolution
    (u₀ : StaticVelocity) (ω₀ : StaticVorticity) : Type where
  velocity : Velocity
  vorticity : Vorticity
  velocityMeasurable : ∀ t : ℝ, 0 ≤ t → AEStronglyMeasurable (velocity t) volume
  vorticityMeasurable : ∀ t : ℝ, 0 ≤ t → AEStronglyMeasurable (vorticity t) volume
  finiteEnergy : ∀ t : ℝ, 0 ≤ t → MemLp (velocity t) 2 volume
  boundedVorticity : ∀ t : ℝ, 0 ≤ t → MemLp (vorticity t) ⊤ volume
  divergenceFree : ∀ t : ℝ, 0 ≤ t → WeaklyDivergenceFree (velocity t)
  vorticityIsCurl : ∀ t : ℝ, 0 ≤ t → WeakCurl (velocity t) (vorticity t)
  momentumEquation : WeakMomentumEquation u₀ velocity
  initialVorticityTrace :
    ∀ ψ : Plane → ℝ, SmoothCompactScalarTest ψ →
      Filter.Tendsto
        (fun t => ∫ x, vorticity t x * ψ x)
        (nhdsWithin 0 (Set.Ioi 0))
        (nhds (∫ x, ω₀ x * ψ x))

def Statement : Prop :=
  ∀ (u₀ : StaticVelocity) (ω₀ : StaticVorticity),
    InitialData u₀ ω₀ → Nonempty (GlobalWeakSolution u₀ ω₀)

theorem statement_iff_expanded :
    Statement ↔
      ∀ (u₀ : StaticVelocity) (ω₀ : StaticVorticity),
        InitialData u₀ ω₀ → Nonempty (GlobalWeakSolution u₀ ω₀) :=
  Iff.rfl

-- Structural mutation checks: none of these altered targets is definitionally
-- the canonical proposition.
example : True := by
  fail_if_success
    exact (Iff.rfl : Statement ↔
      ∀ (u₀ : StaticVelocity) (ω₀ : StaticVorticity),
        Nonempty (GlobalWeakSolution u₀ ω₀))
  trivial

example : True := by
  fail_if_success
    exact (Iff.rfl : Statement ↔
      ∀ (u₀ : (Fin 2 → ℝ) → (Fin 2 → ℝ)) (ω₀ : (Fin 2 → ℝ) → ℝ),
        InitialData u₀ ω₀ → Nonempty (GlobalWeakSolution u₀ ω₀))
  trivial

example : True := by
  fail_if_success
    exact (Iff.rfl : Statement ↔
      ∀ u₀ : StaticVelocity,
        InitialData u₀ 0 → ∀ ω₀ : StaticVorticity,
          Nonempty (GlobalWeakSolution u₀ ω₀))
  trivial

example : True := by
  fail_if_success
    exact (Iff.rfl : Statement ↔
      ∀ (u₀ : StaticVelocity) (ω₀ : StaticVorticity),
        InitialData u₀ ω₀ →
          Nonempty (GlobalWeakSolution u₀ ω₀) ∧ u₀ ≠ 0)
  trivial

#check Statement
#print Statement

end Stage1Rev56.THMM1234
