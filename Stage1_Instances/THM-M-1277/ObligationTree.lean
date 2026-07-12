import Mathlib.Analysis.Calculus.ContDiff.Defs
import Mathlib.Analysis.Calculus.FDeriv.Basic
import Mathlib.Geometry.Euclidean.Volume.Measure
import Mathlib.MeasureTheory.Function.LpSeminorm.Basic
import Mathlib.MeasureTheory.Integral.Lebesgue.Basic

/-!
Checked logical composition for the frozen THM-M-1277 proof architecture.

The analytic endpoint and sharpness branches remain explicit premises.  This
module checks their exact recomposition into the selected statement; it does
not assert either analytic branch.
-/

noncomputable section

open MeasureTheory
open Filter
open scoped ENNReal

namespace Stage1Rev56.THMM1277

abbrev Plane := EuclideanSpace Real (Fin 2)
abbrev ScalarField := Plane -> Real
abbrev VectorField := Plane -> Plane

def basisVector (i : Fin 2) : Plane :=
  EuclideanSpace.single i 1

def classicalGradient (u : ScalarField) (x : Plane) : Plane :=
  (WithLp.equiv 2 (Fin 2 -> Real)).symm (fun i => fderiv Real u x (basisVector i))

def SmoothCompactIn (Omega : Set Plane) (u : ScalarField) : Prop :=
  ContDiff Real ⊤ u ∧ HasCompactSupport u ∧ Function.support u ⊆ Omega

def ZeroBoundarySobolev
    (Omega : Set Plane) (u : ScalarField) (g : VectorField) : Prop :=
  AEStronglyMeasurable u volume ∧ AEStronglyMeasurable g volume ∧
    ∃ phi : Nat -> ScalarField,
      (forall n, SmoothCompactIn Omega (phi n)) ∧
      Tendsto (fun n => eLpNorm (u - phi n) 2 volume) Filter.atTop (nhds 0) ∧
      Tendsto (fun n => eLpNorm (g - classicalGradient (phi n)) 2 volume)
        Filter.atTop (nhds 0)

def GradientEnergy (g : VectorField) : ENNReal :=
  ∫⁻ x, ENNReal.ofReal ‖g x‖ ^ 2 ∂volume

def ExponentialIntegral (Omega : Set Plane) (alpha : Real) (u : ScalarField) : ENNReal :=
  ∫⁻ x in Omega, ENNReal.ofReal (Real.exp (alpha * u x ^ 2)) ∂volume

def Admissible (Omega : Set Plane) (u : ScalarField) : Prop :=
  ∃ g : VectorField, ZeroBoundarySobolev Omega u g ∧ GradientEnergy g <= 1

def Statement : Prop :=
  forall Omega : Set Plane, IsOpen Omega -> Omega.Nonempty -> Bornology.IsBounded Omega ->
    (∃ C : ENNReal, C < ⊤ ∧
      forall u : ScalarField, Admissible Omega u ->
        ExponentialIntegral Omega (4 * Real.pi) u <= C) ∧
    (forall alpha : Real, 4 * Real.pi < alpha ->
      forall C : ENNReal, C < ⊤ ->
        ∃ u : ScalarField, Admissible Omega u ∧
          C < ExponentialIntegral Omega alpha u)

def EndpointBranch : Prop :=
  forall Omega : Set Plane, IsOpen Omega -> Omega.Nonempty -> Bornology.IsBounded Omega ->
    ∃ C : ENNReal, C < ⊤ ∧
      forall u : ScalarField, Admissible Omega u ->
        ExponentialIntegral Omega (4 * Real.pi) u <= C

def SharpnessBranch : Prop :=
  forall Omega : Set Plane, IsOpen Omega -> Omega.Nonempty -> Bornology.IsBounded Omega ->
    forall alpha : Real, 4 * Real.pi < alpha ->
    forall C : ENNReal, C < ⊤ ->
        ∃ u : ScalarField, Admissible Omega u ∧
          C < ExponentialIntegral Omega alpha u

/-- Exact checked composition of the endpoint and supercritical branches. -/
theorem statement_of_branches
    (endpoint : EndpointBranch) (sharpness : SharpnessBranch) : Statement := by
  intro Omega hopen hne hbounded
  exact ⟨endpoint Omega hopen hne hbounded,
    sharpness Omega hopen hne hbounded⟩

#print axioms statement_of_branches

end Stage1Rev56.THMM1277
