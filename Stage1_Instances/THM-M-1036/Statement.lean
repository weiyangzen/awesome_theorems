import Mathlib.Probability.Process.Adapted
import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic

/-!
# THM-M-1036: source-normalized SDE existence and uniqueness target

This module freezes the finite-dimensional, finite-horizon strong-solution
statement.  `itoIntegral` is an explicit semantic boundary because the pinned
mathlib revision has no general Ito-integral API.  No existence or uniqueness
proof is supplied here.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal NNReal

namespace Stage1Instances.THM_M_1036

universe u

abbrev State (n : Nat) := Fin n -> Real
abbrev Noise (m : Nat) := Fin m -> Real
abbrev Diffusion (n m : Nat) := Fin n -> Fin m -> Real
abbrev Process (Ω : Type u) (n : Nat) := Real -> Ω -> State n

/-- Data and hypotheses of the global-Lipschitz finite-horizon Ito SDE. -/
structure Problem (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω)
    (n m : Nat) where
  horizon : Real
  horizon_pos : 0 < horizon
  filtration : Filtration Real (inferInstance : MeasurableSpace Ω)
  brownian : Process Ω m
  initial : Ω -> State n
  drift : Real -> State n -> State n
  diffusion : Real -> State n -> Diffusion n m
  drift_measurable : Measurable fun z : Real × State n => drift z.1 z.2
  diffusion_measurable : Measurable fun z : Real × State n => diffusion z.1 z.2
  lipschitzConstant : Real
  lipschitzConstant_nonneg : 0 <= lipschitzConstant
  globalLipschitz :
    ∀ t, t ∈ Set.Icc (0 : Real) horizon -> ∀ x y,
      ‖drift t x - drift t y‖ + ‖diffusion t x - diffusion t y‖ <=
        lipschitzConstant * ‖x - y‖
  growthConstant : Real
  growthConstant_nonneg : 0 <= growthConstant
  linearGrowth :
    ∀ t, t ∈ Set.Icc (0 : Real) horizon -> ∀ x,
      ‖drift t x‖ + ‖diffusion t x‖ <= growthConstant * (1 + ‖x‖)
  initial_sq_integrable : Integrable (fun ω => ‖initial ω‖ ^ 2) P
  initial_measurable : Measurable[filtration 0] initial
  brownian_gaussian : ProbabilityTheory.IsGaussianProcess brownian P
  brownian_adapted : Adapted filtration brownian
  brownian_continuous : ∀ ω, Continuous fun t => brownian t ω
  brownian_starts_zero : brownian 0 =ᵐ[P] fun _ => 0
  brownian_independent_increments :
    ∀ ⦃s t u v : Real⦄, 0 <= s -> s <= t -> t <= u -> u <= v ->
      ProbabilityTheory.IndepFun
        (fun ω => brownian t ω - brownian s ω)
        (fun ω => brownian v ω - brownian u ω) P
  brownian_covariance :
    ∀ i j s t, 0 <= s -> 0 <= t ->
      (∫ ω, brownian s ω i * brownian t ω j ∂P) =
        if i = j then min s t else 0
  initial_independent_of_future_increments :
    ∀ t, 0 <= t -> ProbabilityTheory.Indep
      (MeasurableSpace.comap initial inferInstance)
      (⨆ s ∈ Set.Ici t, MeasurableSpace.comap
        (fun ω => brownian s ω - brownian t ω) inferInstance) P

/--
Semantic interpretation of the two integrals in the source SDE.  Keeping this
boundary explicit prevents the unavailable Ito integral from being disguised
as a repo-local construction.
-/
structure IntegralSemantics {Ω : Type u} [MeasurableSpace Ω] {P : Measure Ω}
    {n m : Nat} (D : Problem Ω P n m) where
  timeIntegral : (Real -> Ω -> State n) -> Real -> Ω -> State n
  itoIntegral : (Real -> Ω -> Diffusion n m) -> Process Ω m -> Real -> Ω -> State n
  standard_time_integral : Prop
  standard_ito_integral : Prop

/-- A continuous adapted strong solution of the integral SDE on `[0,T]`. -/
structure StrongSolution {Ω : Type u} [MeasurableSpace Ω] {P : Measure Ω}
    {n m : Nat} (D : Problem Ω P n m) (I : IntegralSemantics D) where
  process : Process Ω n
  adapted : Adapted D.filtration process
  continuous_paths : ∀ ω, ContinuousOn (fun t => process t ω) (Set.Icc 0 D.horizon)
  expected_time_square_integrable :
    IntegrableOn (fun t => ∫ ω, ‖process t ω‖ ^ 2 ∂P) (Set.Icc 0 D.horizon)
  integral_equation : ∀ t ∈ Set.Icc (0 : Real) D.horizon,
    process t =ᵐ[P] fun ω =>
      D.initial ω + I.timeIntegral (fun s ω' => D.drift s (process s ω')) t ω +
        I.itoIntegral (fun s ω' => D.diffusion s (process s ω')) D.brownian t ω

/-- Equality convention used by the source theorem: indistinguishability on the horizon. -/
def Indistinguishable {Ω : Type u} [MeasurableSpace Ω] {P : Measure Ω}
    {n m : Nat} {D : Problem Ω P n m} {I : IntegralSemantics D}
    (X Y : StrongSolution D I) : Prop :=
  ∀ᵐ ω ∂P, ∀ t ∈ Set.Icc (0 : Real) D.horizon, X.process t ω = Y.process t ω

/--
Canonical target: under the displayed global-Lipschitz, linear-growth and
square-integrability hypotheses, there is a strong solution and any two strong
solutions are indistinguishable.  The standard-Ito interpretation of `I` is a
foundation boundary to be discharged by a later pinned integration layer.
-/
def SdeExistenceUniquenessTarget : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    (n m : Nat) (D : Problem Ω P n m) (I : IntegralSemantics D),
    I.standard_time_integral -> I.standard_ito_integral ->
      Nonempty (StrongSolution D I) ∧
      ∀ X Y : StrongSolution D I, Indistinguishable X Y

-- Separately elaborated mutations checked by `check_statement.py`.
def mutationRemovedUniqueness : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    (n m : Nat) (D : Problem Ω P n m) (I : IntegralSemantics D),
    Nonempty (StrongSolution D I)

def mutationChangedUniquenessToFixedTime : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    (n m : Nat) (D : Problem Ω P n m) (I : IntegralSemantics D),
    Nonempty (StrongSolution D I) ∧ ∀ X Y : StrongSolution D I,
      ∀ t ∈ Set.Icc (0 : Real) D.horizon, X.process t =ᵐ[P] Y.process t

def mutationAllowsZeroHorizon : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
    (n m : Nat) (D : Problem Ω P n m) (I : IntegralSemantics D),
    0 <= D.horizon -> Nonempty (StrongSolution D I) ∧
      ∀ X Y : StrongSolution D I, Indistinguishable X Y

end Stage1Instances.THM_M_1036

set_option pp.explicit true in
#print Stage1Instances.THM_M_1036.SdeExistenceUniquenessTarget
