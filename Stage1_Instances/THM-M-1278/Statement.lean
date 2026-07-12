import Mathlib.Geometry.Manifold.Instances.Sphere
import Mathlib.Analysis.Calculus.Gradient.Basic
import Mathlib.MeasureTheory.Measure.Hausdorff
import Mathlib.MeasureTheory.Integral.Bochner.Basic

open MeasureTheory Metric
open scoped Manifold MeasureTheory RealInnerProductSpace

noncomputable section

namespace Stage1Instances.THM_M_1278

/-- The standard unit two-sphere, realized in three-dimensional Euclidean space. -/
abbrev Sphere2 := sphere (0 : EuclideanSpace ℝ (Fin 3)) 1

instance : MeasurableSpace Sphere2 := borel Sphere2
instance : BorelSpace Sphere2 := ⟨rfl⟩

/-- Surface area on the unit sphere, as two-dimensional Hausdorff measure. -/
def sphereArea : Measure Sphere2 := Measure.hausdorffMeasure 2

/-- A concrete smooth encoding of a function on the sphere by a smooth ambient extension. -/
structure SmoothSphereFunction where
  extension : EuclideanSpace ℝ (Fin 3) → ℝ
  smooth_extension : ContDiff ℝ (⊤ : WithTop ℕ∞) extension

instance : CoeFun SmoothSphereFunction (fun _ => Sphere2 → ℝ) :=
  ⟨fun u x => u.extension x⟩

/-- The tangential gradient of an ambient representative on the unit sphere. -/
def tangentialGradient (u : SmoothSphereFunction) (x : Sphere2) :
    EuclideanSpace ℝ (Fin 3) :=
  gradient u.extension (x : EuclideanSpace ℝ (Fin 3)) -
    (inner ℝ (gradient u.extension (x : EuclideanSpace ℝ (Fin 3)))
      (x : EuclideanSpace ℝ (Fin 3))) • (x : EuclideanSpace ℝ (Fin 3))

/-- The Dirichlet energy of the represented sphere function. -/
def dirichletEnergy (u : SmoothSphereFunction) : ℝ :=
  ∫ x, ‖tangentialGradient u x‖ ^ 2 ∂sphereArea

/-- The sharp Onofri inequality on the standard unit two-sphere, in unnormalized area form. -/
def OnofriInequality : Prop :=
  ∀ u : SmoothSphereFunction,
    Real.log ((1 / (4 * Real.pi)) * ∫ x, Real.exp (u x) ∂sphereArea) ≤
      (1 / (4 * Real.pi)) * ∫ x, u x ∂sphereArea +
        (1 / (16 * Real.pi)) * dirichletEnergy u

/-- A zero-mean normalization of the same target shape, kept distinct for mutation testing. -/
def MutationZeroMeanOnly : Prop :=
  ∀ u : SmoothSphereFunction,
    (∫ x, u x ∂sphereArea) = 0 →
      Real.log ((1 / (4 * Real.pi)) * ∫ x, Real.exp (u x) ∂sphereArea) ≤
        (1 / (16 * Real.pi)) * dirichletEnergy u

/-- A non-sharp coefficient mutation. -/
def MutationEnergyCoefficient : Prop :=
  ∀ u : SmoothSphereFunction,
    Real.log ((1 / (4 * Real.pi)) * ∫ x, Real.exp (u x) ∂sphereArea) ≤
      (1 / (4 * Real.pi)) * ∫ x, u x ∂sphereArea +
        (1 / (8 * Real.pi)) * dirichletEnergy u

#check OnofriInequality
#check tangentialGradient
#check sphereArea

set_option pp.explicit true in
#print OnofriInequality

set_option pp.explicit true in
#print MutationZeroMeanOnly

set_option pp.explicit true in
#print MutationEnergyCoefficient

end Stage1Instances.THM_M_1278
