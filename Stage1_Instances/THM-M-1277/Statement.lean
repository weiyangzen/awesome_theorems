import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Geometry.Euclidean.Volume.Measure
import Mathlib.MeasureTheory.Function.LpSeminorm.Basic
import Mathlib.MeasureTheory.Integral.Lebesgue.Basic

/-!
Exact statement surface for the sharp two-dimensional Moser-Trudinger inequality.

`ZeroBoundarySobolev` spells out `W₀¹,²` by completion of smooth functions
compactly supported in the domain.  Keeping the weak gradient as part of the
predicate avoids choosing a representative-dependent derivative operation.
-/

noncomputable section

open MeasureTheory Filter
open scoped ENNReal Topology

namespace Stage1Rev56.THMM1277

abbrev Plane := EuclideanSpace ℝ (Fin 2)
abbrev ScalarField := Plane → ℝ
abbrev VectorField := Plane → Plane

def basisVector (i : Fin 2) : Plane :=
  EuclideanSpace.single i 1

def classicalGradient (u : ScalarField) (x : Plane) : Plane :=
  (WithLp.equiv 2 (Fin 2 → ℝ)).symm (fun i => fderiv ℝ u x (basisVector i))

def SmoothCompactIn (Omega : Set Plane) (u : ScalarField) : Prop :=
  ContDiff ℝ ⊤ u ∧ HasCompactSupport u ∧ Function.support u ⊆ Omega

/-- Membership in `W₀¹,²(Omega)`, together with a selected weak gradient. -/
def ZeroBoundarySobolev
    (Omega : Set Plane) (u : ScalarField) (g : VectorField) : Prop :=
  AEStronglyMeasurable u volume ∧ AEStronglyMeasurable g volume ∧
    ∃ phi : ℕ → ScalarField,
      (∀ n, SmoothCompactIn Omega (phi n)) ∧
      Tendsto (fun n => eLpNorm (u - phi n) 2 volume) atTop (nhds 0) ∧
      Tendsto
        (fun n => eLpNorm (g - classicalGradient (phi n)) 2 volume)
        atTop (nhds 0)

def GradientEnergy (g : VectorField) : ℝ≥0∞ :=
  ∫⁻ x, ENNReal.ofReal ‖g x‖ ^ 2 ∂volume

def ExponentialIntegral (Omega : Set Plane) (alpha : ℝ) (u : ScalarField) : ℝ≥0∞ :=
  ∫⁻ x in Omega, ENNReal.ofReal (Real.exp (alpha * u x ^ 2)) ∂volume

def Admissible (Omega : Set Plane) (u : ScalarField) : Prop :=
  ∃ g : VectorField, ZeroBoundarySobolev Omega u g ∧ GradientEnergy g ≤ 1

/-- The endpoint bound at `4 * pi` and failure of every supercritical bound. -/
def Statement : Prop :=
  ∀ Omega : Set Plane, IsOpen Omega → Omega.Nonempty → Bornology.IsBounded Omega →
    (∃ C : ℝ≥0∞, C < ⊤ ∧
      ∀ u : ScalarField, Admissible Omega u →
        ExponentialIntegral Omega (4 * Real.pi) u ≤ C) ∧
    (∀ alpha : ℝ, 4 * Real.pi < alpha →
      ∀ C : ℝ≥0∞, C < ⊤ →
        ∃ u : ScalarField, Admissible Omega u ∧
          C < ExponentialIntegral Omega alpha u)

#check Statement

end Stage1Rev56.THMM1277
