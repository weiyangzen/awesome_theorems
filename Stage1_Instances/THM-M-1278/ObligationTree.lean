import Mathlib

open MeasureTheory Metric
open scoped Manifold MeasureTheory RealInnerProductSpace

noncomputable section

namespace Stage1Instances.THM_M_1278_Obligations

abbrev Sphere2 := sphere (0 : EuclideanSpace ℝ (Fin 3)) 1

instance : MeasurableSpace Sphere2 := borel Sphere2
instance : BorelSpace Sphere2 := ⟨rfl⟩

structure SmoothSphereFunction where
  extension : EuclideanSpace ℝ (Fin 3) → ℝ
  smooth_extension : ContDiff ℝ (⊤ : WithTop ℕ∞) extension

instance : CoeFun SmoothSphereFunction (fun _ => Sphere2 → ℝ) :=
  ⟨fun u x => u.extension x⟩

def sphereArea : Measure Sphere2 := Measure.hausdorffMeasure 2

def tangentialGradient (u : SmoothSphereFunction) (x : Sphere2) :
    EuclideanSpace ℝ (Fin 3) :=
  gradient u.extension (x : EuclideanSpace ℝ (Fin 3)) -
    (inner ℝ (gradient u.extension (x : EuclideanSpace ℝ (Fin 3)))
      (x : EuclideanSpace ℝ (Fin 3))) • (x : EuclideanSpace ℝ (Fin 3))

def dirichletEnergy (u : SmoothSphereFunction) : ℝ :=
  ∫ x, ‖tangentialGradient u x‖ ^ 2 ∂sphereArea

def mean (u : SmoothSphereFunction) : ℝ :=
  (1 / (4 * Real.pi)) * ∫ x, u x ∂sphereArea

def normalizedExpIntegral (u : SmoothSphereFunction) : ℝ :=
  (1 / (4 * Real.pi)) * ∫ x, Real.exp (u x) ∂sphereArea

/-- The exact root interface, repeated here so this architecture module is independently checked. -/
def Root : Prop :=
  ∀ u : SmoothSphereFunction,
    Real.log (normalizedExpIntegral u) ≤ mean u +
      (1 / (16 * Real.pi)) * dirichletEnergy u

/-- The central sharp analytic estimate after subtracting the spherical mean. -/
def SharpZeroMeanEstimate : Prop :=
  ∀ u : SmoothSphereFunction, mean u = 0 →
    Real.log (normalizedExpIntegral u) ≤
      (1 / (16 * Real.pi)) * dirichletEnergy u

/-- The normalization interface needed to transport the sharp estimate back to the root. -/
def MeanShiftTransport : Prop :=
  ∀ u : SmoothSphereFunction, ∃ v : SmoothSphereFunction,
    mean v = 0 ∧ dirichletEnergy v = dirichletEnergy u ∧
      Real.log (normalizedExpIntegral u) =
        mean u + Real.log (normalizedExpIntegral v)

/-- Exact child-to-parent composition; it consumes both semantic children. -/
theorem compose_root (hsharp : SharpZeroMeanEstimate)
    (hshift : MeanShiftTransport) : Root := by
  intro u
  obtain ⟨v, hvmean, hvenergy, hvlog⟩ := hshift u
  rw [hvlog]
  rw [← hvenergy]
  exact add_le_add_right (hsharp v hvmean) (mean u)

#check Root
#check SharpZeroMeanEstimate
#check MeanShiftTransport
#check compose_root

end Stage1Instances.THM_M_1278_Obligations
