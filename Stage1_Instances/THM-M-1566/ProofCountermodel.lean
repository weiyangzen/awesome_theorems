import Statement

/-!
# THM-M-1566 proof-phase countermodel

The frozen target ranges over every implementation of its abstract analytic
API.  In particular, it permits an implementation whose solution type is
empty while all of the stated input assumptions are inhabited.  This module
kernel-checks that obstruction; it does not add an assumed proof body.
-/

namespace Stage1Instances.THMM1566

open MeasureTheory

/-- An admissible abstract API with no possible solution. -/
def emptySolutionAPI : GIPCorollary59API Unit where
  HolderBesov := fun _ => Unit
  BoundedSmoothFunction := fun _ => Unit
  SchwartzFunction := Unit
  SpatialDistribution := Unit
  Solution := Empty
  isSpatialWhiteNoiseOnTorus2 := fun _ => True
  hasIntegralOne := fun _ => True
  mollifiedNoise := fun _ _ _ => ()
  renormalizationConstant := fun _ _ _ => 0
  solvesLimitEquation := fun _ _ _ _ => True
  solvesRenormalizedEquation := fun _ _ _ _ _ => True
  dataMeasurableRandomTime := fun _ _ _ => True
  stoppedHolderDistance := fun _ _ _ _ _ => 0

/-- The numerical and white-noise premises of the frozen data structure remain
consistent for the empty-solution API. -/
noncomputable def emptySolutionData : GIPCorollary59Data Unit emptySolutionAPI where
  alpha := 3 / 4
  beta := 3 / 4
  alpha_gt_two_thirds := by norm_num
  alpha_lt_one := by norm_num
  beta_gt := by norm_num
  beta_le_alpha := le_rfl
  nonlinearity := ()
  initialCondition := ()
  whiteNoise := ()
  whiteNoise_on_torus2 := trivial

/-- The universally quantified frozen target is refuted by the admissible API
whose `Solution` field is `Empty`. -/
theorem not_GIPCorollary59Target : ¬ GIPCorollary59Target.{0} := by
  intro target
  obtain ⟨u, _hu, _unique⟩ :=
    target Unit inferInstance (Measure.dirac ()) inferInstance
      emptySolutionAPI emptySolutionData
  exact u.elim

#print axioms not_GIPCorollary59Target

end Stage1Instances.THMM1566
