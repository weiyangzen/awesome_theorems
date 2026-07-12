import Mathlib.MeasureTheory.Function.ConvergenceInMeasure

/-!
# THM-M-1566 exact statement boundary

This module freezes Corollary 5.9 of Gubinelli--Imkeller--Perkowski as an
abstract, typed interface.  The interface names analytic notions absent from
the pinned dependency closure, but none of its input fields assumes existence,
uniqueness, positivity of the stopping time, or approximation convergence.
This is a statement artifact, not a proof of the corollary.
-/

noncomputable section

open Filter MeasureTheory Set
open scoped Topology

namespace Stage1Instances.THMM1566

/-- Strictly positive regularization parameters. -/
abbrev PositiveEpsilon := {epsilon : Real // 0 < epsilon}

/-- The filter in which a positive regularization parameter tends to zero. -/
def epsilonToZero : Filter PositiveEpsilon :=
  Filter.comap ((↑) : PositiveEpsilon -> Real) (nhdsWithin 0 (Ioi 0))

/--
Typed vocabulary for the generalized two-dimensional parabolic Anderson model
in Corollary 5.9.  These operations specify meanings; they carry no theorem
asserting that a solution or a convergent approximation exists.
-/
structure GIPCorollary59API (Omega : Type*) [MeasurableSpace Omega] where
  HolderBesov : Real -> Type
  BoundedSmoothFunction : Real -> Type
  SchwartzFunction : Type
  SpatialDistribution : Type
  Solution : Type
  isSpatialWhiteNoiseOnTorus2 : SpatialDistribution -> Prop
  hasIntegralOne : SchwartzFunction -> Prop
  mollifiedNoise : SchwartzFunction -> PositiveEpsilon -> SpatialDistribution -> SpatialDistribution
  renormalizationConstant : SchwartzFunction -> PositiveEpsilon -> SpatialDistribution -> Real
  solvesLimitEquation :
    {gamma alpha : Real} -> BoundedSmoothFunction gamma -> HolderBesov alpha ->
      SpatialDistribution -> Solution -> Prop
  solvesRenormalizedEquation :
    {gamma alpha : Real} -> BoundedSmoothFunction gamma -> HolderBesov alpha ->
      SpatialDistribution -> Real -> Solution -> Prop
  dataMeasurableRandomTime : {alpha : Real} -> HolderBesov alpha -> SpatialDistribution ->
    (Omega -> Real) -> Prop
  stoppedHolderDistance : Real -> (Omega -> Real) -> Solution -> Solution -> Omega -> Real

/-- Data and source assumptions appearing before the conclusion of Corollary 5.9. -/
structure GIPCorollary59Data (Omega : Type*) [MeasurableSpace Omega]
    (api : GIPCorollary59API Omega) where
  alpha : Real
  beta : Real
  alpha_gt_two_thirds : (2 : Real) / 3 < alpha
  alpha_lt_one : alpha < 1
  beta_gt : 2 - 2 * alpha < beta
  beta_le_alpha : beta <= alpha
  nonlinearity : api.BoundedSmoothFunction (2 + beta / alpha)
  initialCondition : api.HolderBesov alpha
  whiteNoise : api.SpatialDistribution
  whiteNoise_on_torus2 : api.isSpatialWhiteNoiseOnTorus2 whiteNoise

/--
The convergence characterization of the unique solution.  For every
unit-integral Schwartz mollifier it includes renormalized classical solutions,
a data-measurable almost-surely positive stopping time, and convergence in
probability of the stopped `C^alpha` distance.
-/
def IsCorollary59Solution {Omega : Type*} [MeasurableSpace Omega]
    (mu : Measure Omega) (api : GIPCorollary59API Omega)
    (D : GIPCorollary59Data Omega api) (u : api.Solution) : Prop :=
  api.solvesLimitEquation
      D.nonlinearity D.initialCondition D.whiteNoise u /\
    forall psi : api.SchwartzFunction, api.hasIntegralOne psi ->
      exists (uEpsilon : PositiveEpsilon -> api.Solution) (tau : Omega -> Real),
        (forall epsilon : PositiveEpsilon,
          api.solvesRenormalizedEquation
            D.nonlinearity D.initialCondition
            (api.mollifiedNoise psi epsilon D.whiteNoise)
            (api.renormalizationConstant psi epsilon D.whiteNoise)
            (uEpsilon epsilon)) /\
        api.dataMeasurableRandomTime D.initialCondition D.whiteNoise tau /\
        (∀ᵐ x : Omega ∂mu, 0 < tau x) /\
        TendstoInMeasure mu
          (fun epsilon omega => api.stoppedHolderDistance D.alpha tau (uEpsilon epsilon) u omega)
          epsilonToZero (fun _ => 0)

/-- Exact Lean target selected from the intake candidate: GIP Corollary 5.9. -/
def GIPCorollary59Target : Prop :=
  forall (Omega : Type*) (_m : MeasurableSpace Omega) (mu : Measure Omega),
    IsProbabilityMeasure mu ->
      forall (api : GIPCorollary59API Omega) (D : GIPCorollary59Data Omega api),
        ∃! u : api.Solution, IsCorollary59Solution mu api D u

-- Separately elaborated structural mutations inspected by `check_statement.py`.
def mutationRemovedWhiteNoiseHypothesis : Prop :=
  forall (Omega : Type*) (_m : MeasurableSpace Omega) (mu : Measure Omega),
    IsProbabilityMeasure mu -> forall (api : GIPCorollary59API Omega),
      forall D : GIPCorollary59Data Omega api,
        (¬ api.isSpatialWhiteNoiseOnTorus2 D.whiteNoise) ->
          ∃! u : api.Solution, IsCorollary59Solution mu api D u

def mutationChangedDomainToArbitraryNoise : Prop :=
  forall (Omega : Type*) (_m : MeasurableSpace Omega) (mu : Measure Omega),
    IsProbabilityMeasure mu -> forall (api : GIPCorollary59API Omega),
      forall D : GIPCorollary59Data Omega api,
        ∃! u : api.Solution,
          api.solvesLimitEquation
            D.nonlinearity D.initialCondition D.whiteNoise u

def mutationChangedMollifierBinderScope : Prop :=
  forall (Omega : Type*) (_m : MeasurableSpace Omega) (mu : Measure Omega),
    IsProbabilityMeasure mu -> forall (api : GIPCorollary59API Omega),
      exists psi : api.SchwartzFunction, api.hasIntegralOne psi /\
        forall D : GIPCorollary59Data Omega api,
          ∃! u : api.Solution, IsCorollary59Solution mu api D u

def mutationAllowsZeroStoppingTime : Prop :=
  forall (Omega : Type*) (_m : MeasurableSpace Omega) (mu : Measure Omega),
    IsProbabilityMeasure mu -> forall (api : GIPCorollary59API Omega),
      forall D : GIPCorollary59Data Omega api,
        exists (u : api.Solution) (tau : Omega -> Real),
          IsCorollary59Solution mu api D u /\ (∀ᵐ x : Omega ∂mu, 0 <= tau x)

/-- The strict source interval admits neither endpoint for `alpha`. -/
theorem alpha_boundary_excluded {Omega : Type*} [MeasurableSpace Omega]
    (api : GIPCorollary59API Omega) (D : GIPCorollary59Data Omega api) :
    D.alpha ≠ (2 : Real) / 3 /\ D.alpha ≠ 1 :=
  ⟨D.alpha_gt_two_thirds.ne', D.alpha_lt_one.ne⟩

end Stage1Instances.THMM1566

set_option pp.explicit true in
#print Stage1Instances.THMM1566.GIPCorollary59Target
