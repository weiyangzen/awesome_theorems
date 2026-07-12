import Mathlib.MeasureTheory.Integral.BoundedContinuousFunction

/-!
# THM-M-1026 canonical statement

This file freezes the law-level, one-dimensional generalized central limit theorem:
the nondegenerate probability laws which attract normalized convolution powers are
exactly the nondegenerate stable laws. It states, but does not prove, that result.
-/

noncomputable section

open Filter MeasureTheory Set Topology
open scoped MeasureTheory

namespace Stage1Instances.THM_M_1026

/-- The `n`-fold additive convolution, with zeroth power the mass at zero. -/
def convPow (mu : Measure Real) : Nat -> Measure Real
  | 0 => Measure.dirac 0
  | n + 1 => convPow mu n ∗ mu

/-- Push a law forward by the affine normalization `(x - b) / a`. -/
def normalizedLaw (mu : Measure Real) (a b : Real) : Measure Real :=
  mu.map fun x => (x - b) / a

/-- Weak convergence of finite Borel measures, tested on bounded continuous real functions. -/
def WeaklyConverges (mu : Nat -> Measure Real) (nu : Measure Real) : Prop :=
  forall f : BoundedContinuousFunction Real Real,
    Tendsto (fun n => ∫ x, f x ∂(mu n)) atTop
      (nhds (∫ x, f x ∂nu))

/-- A Borel measure is a probability law. -/
def IsProbabilityLaw (mu : Measure Real) : Prop := mu univ = 1

/-- A law is nondegenerate when it is not concentrated at one point. -/
def IsNondegenerate (mu : Measure Real) : Prop :=
  forall x : Real, mu ≠ Measure.dirac x

/-- A nondegenerate probability law is stable when every convolution power is an
affine rescaling of that same law. The positive scale rules out a reflected convention. -/
def IsStableLaw (nu : Measure Real) : Prop :=
  IsProbabilityLaw nu ∧ IsNondegenerate nu ∧
    forall n : Nat, 2 <= n ->
      exists a b : Real, 0 < a ∧ normalizedLaw (convPow nu n) a b = nu

/-- `mu` is in the domain of attraction of `nu` when normalized convolution powers
of `mu` converge weakly to `nu`, using positive scales. -/
def InDomainOfAttraction (mu nu : Measure Real) : Prop :=
  exists a b : Nat -> Real, (forall n, 0 < a n) ∧
    WeaklyConverges (fun n => normalizedLaw (convPow mu n) (a n) (b n)) nu

/-- Exact selected generalized central limit theorem: a nondegenerate probability law
is stable exactly when it has a nonempty domain of attraction. -/
def GeneralizedCentralLimitTheorem : Prop :=
  forall nu : Measure Real,
    IsProbabilityLaw nu -> IsNondegenerate nu ->
      (IsStableLaw nu ↔
        exists mu : Measure Real, IsProbabilityLaw mu ∧ InDomainOfAttraction mu nu)

/-- Public target frozen by the statement phase. -/
abbrev Statement : Prop := GeneralizedCentralLimitTheorem

/-- Fully expanded source shape used for a checked definitional transport. -/
def ExpandedSourceShape : Prop :=
  forall nu : Measure Real,
    nu univ = 1 -> (forall x : Real, nu ≠ Measure.dirac x) ->
      ((nu univ = 1 ∧ (forall x : Real, nu ≠ Measure.dirac x) ∧
          forall n : Nat, 2 <= n -> exists a b : Real, 0 < a ∧
            normalizedLaw (convPow nu n) a b = nu) ↔
        exists mu : Measure Real, mu univ = 1 ∧
          exists a b : Nat -> Real, (forall n, 0 < a n) ∧
            WeaklyConverges
              (fun n => normalizedLaw (convPow mu n) (a n) (b n)) nu)

theorem statement_iff_expanded : Statement ↔ ExpandedSourceShape := by
  rfl

-- Deliberately different structural mutations for statement-boundary checks.
def MutationAllowsDegenerateLimit : Prop :=
  forall nu : Measure Real, IsProbabilityLaw nu ->
    (IsStableLaw nu ↔ exists mu, IsProbabilityLaw mu ∧ InDomainOfAttraction mu nu)

def MutationAllowsZeroScale : Prop :=
  forall nu : Measure Real, IsProbabilityLaw nu -> IsNondegenerate nu ->
    (IsStableLaw nu ↔ exists mu : Measure Real, IsProbabilityLaw mu ∧
      exists a b : Nat -> Real,
        WeaklyConverges (fun n => normalizedLaw (convPow mu n) (a n) (b n)) nu)

def MutationGaussianOnly : Prop :=
  forall mu : Measure Real, IsProbabilityLaw mu ->
    exists a b : Nat -> Real, WeaklyConverges
      (fun n => normalizedLaw (convPow mu n) (a n) (b n)) (Measure.dirac 0)

def MutationNecessityOnly : Prop :=
  forall nu : Measure Real, IsProbabilityLaw nu -> IsNondegenerate nu ->
    (exists mu, IsProbabilityLaw mu ∧ InDomainOfAttraction mu nu) -> IsStableLaw nu

end Stage1Instances.THM_M_1026

set_option pp.explicit true in
#print Stage1Instances.THM_M_1026.GeneralizedCentralLimitTheorem
set_option pp.explicit true in
#print Stage1Instances.THM_M_1026.ExpandedSourceShape
set_option pp.explicit true in
#print Stage1Instances.THM_M_1026.MutationAllowsDegenerateLimit
set_option pp.explicit true in
#print Stage1Instances.THM_M_1026.MutationAllowsZeroScale
set_option pp.explicit true in
#print Stage1Instances.THM_M_1026.MutationGaussianOnly
set_option pp.explicit true in
#print Stage1Instances.THM_M_1026.MutationNecessityOnly
