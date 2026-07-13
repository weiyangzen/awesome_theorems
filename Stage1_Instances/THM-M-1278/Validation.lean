import ObligationTree

/-!
# THM-M-1278 validation probe

This module independently reconstructs the implemented mean-shift witness and its Dirichlet-energy
invariance. It deliberately does not import `Proof`, and it does not assert the open zero-mean,
exponential-transport, or sharp Onofri obligations.
-/

open MeasureTheory Metric
open scoped Manifold MeasureTheory RealInnerProductSpace

noncomputable section

namespace Stage1Instances.THM_M_1278_Validation

open Stage1Instances.THM_M_1278_Obligations

/-- Independently selected mean-shift representative. -/
def validationSubtractMean (u : SmoothSphereFunction) : SmoothSphereFunction where
  extension := fun x => u.extension x - mean u
  smooth_extension := u.smooth_extension.sub contDiff_const

/-- Independent reconstruction of the frozen mean-subtraction construction interface. -/
theorem independentlyExistsSubtractMean (u : SmoothSphereFunction) :
    exists v : SmoothSphereFunction, forall x : Sphere2, v x = u x - mean u := by
  exact ⟨validationSubtractMean u, fun _ => rfl⟩

theorem gradient_validationSubtractMean (u : SmoothSphereFunction)
    (x : EuclideanSpace Real (Fin 3)) :
    gradient (validationSubtractMean u).extension x = gradient u.extension x := by
  unfold gradient validationSubtractMean
  rw [fderiv_sub_const]

theorem tangentialGradient_validationSubtractMean (u : SmoothSphereFunction) (x : Sphere2) :
    tangentialGradient (validationSubtractMean u) x = tangentialGradient u x := by
  simp only [tangentialGradient, gradient_validationSubtractMean]

/-- Independent reconstruction of energy invariance for the independently selected witness. -/
theorem independentlyDirichletEnergyInvariant (u : SmoothSphereFunction) :
    dirichletEnergy (validationSubtractMean u) = dirichletEnergy u := by
  simp_rw [dirichletEnergy, tangentialGradient_validationSubtractMean]

#print axioms independentlyExistsSubtractMean
#print axioms independentlyDirichletEnergyInvariant

end Stage1Instances.THM_M_1278_Validation
