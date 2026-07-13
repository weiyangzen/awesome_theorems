import ObligationTree

/-!
# THM-M-1278 proof-phase bodies

This module implements the smooth mean-shift construction and proves that it preserves the
tangential gradient and Dirichlet energy. The sphere-area formula, zero-mean calculation,
exponential/logarithmic transport, and sharp Onofri estimate remain open.
-/

open MeasureTheory Metric
open scoped Manifold MeasureTheory RealInnerProductSpace

noncomputable section

namespace Stage1Instances.THM_M_1278_Obligations

/-- Subtract the spherical mean from the ambient smooth representative. -/
def subtractMean (u : SmoothSphereFunction) : SmoothSphereFunction where
  extension := fun x => u.extension x - mean u
  smooth_extension := u.smooth_extension.sub contDiff_const

@[simp]
theorem subtractMean_apply (u : SmoothSphereFunction) (x : Sphere2) :
    subtractMean u x = u x - mean u := rfl

/-- Exact body for the frozen `M1278-N-SUBTRACT-MEAN` construction. -/
theorem exists_subtract_mean (u : SmoothSphereFunction) :
    exists v : SmoothSphereFunction, forall x : Sphere2, v x = u x - mean u := by
  exact ⟨subtractMean u, fun _ => rfl⟩

theorem gradient_subtractMean_extension (u : SmoothSphereFunction)
    (x : EuclideanSpace Real (Fin 3)) :
    gradient (subtractMean u).extension x = gradient u.extension x := by
  unfold gradient subtractMean
  rw [fderiv_sub_const]

theorem tangentialGradient_subtractMean (u : SmoothSphereFunction) (x : Sphere2) :
    tangentialGradient (subtractMean u) x = tangentialGradient u x := by
  simp only [tangentialGradient, gradient_subtractMean_extension]

/-- Exact body for the frozen `M1278-N-ENERGY` invariant, specialized to the selected shift. -/
theorem dirichletEnergy_subtractMean (u : SmoothSphereFunction) :
    dirichletEnergy (subtractMean u) = dirichletEnergy u := by
  simp_rw [dirichletEnergy, tangentialGradient_subtractMean]

#check exists_subtract_mean
#check dirichletEnergy_subtractMean
#print axioms exists_subtract_mean
#print axioms dirichletEnergy_subtractMean

end Stage1Instances.THM_M_1278_Obligations
