import Statement

/-!
# THM-M-1036: countermodel to the frozen target

The two standard-semantics fields of `IntegralSemantics` are propositions with
no laws relating them to the corresponding operations.  This module gives those
fields true values while choosing an adversarial `timeIntegral`.  The resulting
integral equation says `x = x + 1`, so no strong solution can exist.

This is kernel-checked evidence that the frozen universal target is false.  It
is not a proof of the intended SDE theorem.
-/

noncomputable section

open MeasureTheory

namespace Stage1Instances.THM_M_1036.Counterexample

abbrev Omega := Unit

instance : MeasurableSpace Omega := inferInstance

def probability : Measure Omega := Measure.dirac ()

instance : IsProbabilityMeasure probability := by
  unfold probability
  infer_instance

def filtration : Filtration Real (inferInstance : MeasurableSpace Omega) :=
  Filtration.const Real (inferInstance : MeasurableSpace Omega) le_rfl

def brownian : Process Omega 0 := 0

def initial : Omega -> State 1 := fun _ => 0

def drift : Real -> State 1 -> State 1 := fun _ x => x

def diffusion : Real -> State 1 -> Diffusion 1 0 := 0

theorem brownian_gaussian : ProbabilityTheory.IsGaussianProcess brownian probability := by
  refine ⟨fun I => ?_⟩
  refine ⟨?_⟩
  rw [probability, Measure.map_dirac]
  infer_instance

def problem : Problem Omega probability 1 0 where
  horizon := 1
  horizon_pos := by norm_num
  filtration := filtration
  brownian := brownian
  initial := initial
  drift := drift
  diffusion := diffusion
  drift_measurable := measurable_snd
  diffusion_measurable := measurable_const
  lipschitzConstant := 1
  lipschitzConstant_nonneg := zero_le_one
  globalLipschitz := by simp [drift, diffusion]
  growthConstant := 1
  growthConstant_nonneg := zero_le_one
  linearGrowth := by
    intro t _ x
    simp only [drift, diffusion, Pi.zero_apply, norm_zero, add_zero, one_mul]
    linarith [norm_nonneg x]
  initial_sq_integrable := by
    simp [initial]
  initial_measurable := measurable_const
  brownian_gaussian := brownian_gaussian
  brownian_adapted := adapted_const filtration 0
  brownian_continuous := fun _ => continuous_const
  brownian_starts_zero := by
    filter_upwards [] with omega
    ext i
    exact Fin.elim0 i
  brownian_independent_increments := by
    intro s t u v _ _ _ _
    simpa [brownian] using
      (ProbabilityTheory.indepFun_const_left (μ := probability)
        (0 : Noise 0) (fun _ : Omega => (0 : Noise 0)))
  brownian_covariance := by simp [brownian]
  initial_independent_of_future_increments := by
    intro t _
    rw [show MeasurableSpace.comap initial inferInstance =
        (⊥ : MeasurableSpace Omega) by
      simpa only [initial] using
        (MeasurableSpace.comap_const (m := inferInstance) (0 : State 1))]
    exact ProbabilityTheory.indep_bot_left _

def semantics : IntegralSemantics problem where
  timeIntegral := fun f _ omega => f 0 omega + fun _ => 1
  itoIntegral := fun _ _ _ _ _ => 0
  standard_time_integral := True
  standard_ito_integral := True

theorem no_strong_solution : Not (Nonempty (StrongSolution problem semantics)) := by
  rintro ⟨X⟩
  have htime : (0 : Real) ∈ Set.Icc 0 problem.horizon := by
    change (0 : Real) ∈ Set.Icc 0 1
    simp
  have heq := X.integral_equation 0 htime
  have hpoint : X.process 0 () =
      problem.initial () + semantics.timeIntegral
        (fun s omega => problem.drift s (X.process s omega)) 0 () +
        semantics.itoIntegral
          (fun s omega => problem.diffusion s (X.process s omega)) problem.brownian 0 () := by
    simpa [probability, MeasureTheory.ae_dirac_eq] using heq
  have hcoord := congrFun hpoint 0
  dsimp [problem, initial, semantics, drift, diffusion, brownian] at hcoord
  linarith

/-- The exact frozen target is refuted by the checked adversarial semantics. -/
theorem not_sdeExistenceUniquenessTarget :
    Not SdeExistenceUniquenessTarget.{0} := by
  intro hroot
  have h := hroot Omega probability 1 0 problem semantics trivial trivial
  exact no_strong_solution h.1

#check no_strong_solution
#check not_sdeExistenceUniquenessTarget
#print axioms no_strong_solution
#print axioms not_sdeExistenceUniquenessTarget

end Stage1Instances.THM_M_1036.Counterexample
