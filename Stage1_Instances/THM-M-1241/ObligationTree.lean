import Statement

/-!
# THM-M-1241 conditional obligation composition

This module checks an exhaustive finite-exponent/endpoint split while keeping
both analytic packages as explicit premises. It does not prove either package.
-/

noncomputable section

open MeasureTheory
open scoped ENNReal Topology

namespace Stage1Instances.THM_M_1241

/-- The hypotheses on structural parameters, factored without changing their order. -/
def AdmissibleParameters (n m j : Nat) (q r p : ENNReal) (a : Real) : Prop :=
  0 < n ∧ j < m ∧ 1 <= q ∧ 1 <= r ∧
  reciprocalExponent p =
    (j : Real) / n + a * (reciprocalExponent r - (m : Real) / n) +
      (1 - a) * reciprocalExponent q ∧
  (j : Real) / m <= a ∧ a <= 1 ∧
  (((1 < r ∧ r < (⊤ : ENNReal) ∧
    ∃ z : Int, 0 <= z ∧ (m : Real) - j - n * reciprocalExponent r = z) -> a < 1))

/-- The exact conclusion for fixed structural parameters, including uniformity in `u`. -/
def ParameterConclusion (n m j : Nat) (q r p : ENNReal) (a : Real) : Prop :=
  exists C : NNReal,
    forall u : Space n -> Real,
      ContDiff Real m u ->
      derivativeLpNorm 0 q u < (⊤ : ENNReal) ->
      derivativeLpNorm m r u < (⊤ : ENNReal) ->
      (j = 0 ∧ r < (⊤ : ENNReal) ∧ (r.toReal * m < n) ∧ q = (⊤ : ENNReal) ->
        ZeroOrderExceptionalHypothesis u) ->
      derivativeLpNorm j p u <=
        C * (derivativeLpNorm m r u) ^ a *
          (derivativeLpNorm 0 q u) ^ (1 - a)

/-- The analytic package for finite `q` and `r`. -/
def FiniteExponentPackage : Prop :=
  forall (n m j : Nat) (q r p : ENNReal) (a : Real),
    AdmissibleParameters n m j q r p a -> q < (⊤ : ENNReal) -> r < (⊤ : ENNReal) ->
      ParameterConclusion n m j q r p a

/-- The analytic package for every case where `q` or `r` is infinite. -/
def InfiniteEndpointPackage : Prop :=
  forall (n m j : Nat) (q r p : ENNReal) (a : Real),
    AdmissibleParameters n m j q r p a ->
      ¬ (q < (⊤ : ENNReal) ∧ r < (⊤ : ENNReal)) ->
      ParameterConclusion n m j q r p a

/-- Checked composition of the two exhaustive analytic packages into the exact target. -/
theorem root_of_finite_and_endpoint_packages
    (finite : FiniteExponentPackage) (endpoint : InfiniteEndpointPackage) :
    GagliardoNirenbergTarget := by
  intro n m j q r p a hn hjm hq hr hscale hlo hhi hcritical
  have hadm : AdmissibleParameters n m j q r p a :=
    ⟨hn, hjm, hq, hr, hscale, hlo, hhi, hcritical⟩
  by_cases hfinite : q < (⊤ : ENNReal) ∧ r < (⊤ : ENNReal)
  · exact finite n m j q r p a hadm hfinite.1 hfinite.2
  · exact endpoint n m j q r p a hadm hfinite

#print axioms root_of_finite_and_endpoint_packages

end Stage1Instances.THM_M_1241
