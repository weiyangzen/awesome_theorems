import Mathlib.Probability.StrongLaw

/-!
# THM-M-0983 conditional obligation composition

This module checks the interfaces and final composition selected by the frozen
obligation architecture. The three package arguments remain explicit, so this
is not a proof-node closure claim.
-/

noncomputable section

open MeasureTheory Filter Finset
open scoped BigOperators MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THM_M_0983_Obligations

universe u

def empiricalFrequency {Omega : Type u} (X : Nat -> Omega -> Real)
    (n : Nat) (omega : Omega) : Real :=
  (∑ i ∈ range n, X i omega) / (n : Real)

def Target : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (X : Nat -> Omega -> Real) (p : Real),
      Integrable (X 0) mu ->
      ProbabilityTheory.iIndepFun X mu ->
      (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
      (forall i, ∀ᵐ omega ∂mu, X i omega = 0 \/ X i omega = 1) ->
      mu[X 0] = p ->
      ∀ᵐ omega ∂mu,
        Tendsto (fun n : Nat => empiricalFrequency X n omega) atTop (nhds p)

/-- Family independence supplies the pairwise premise of the pinned theorem. -/
def PairwiseProjectionPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega)
    (X : Nat -> Omega -> Real),
    ProbabilityTheory.iIndepFun X mu ->
    Pairwise (Function.onFun (fun f g => f ⟂ᵢ[mu] g) X)

/-- Exact analytic output supplied by the pinned mathlib strong law. -/
def StrongLawPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega)
    (X : Nat -> Omega -> Real),
    Integrable (X 0) mu ->
    Pairwise (Function.onFun (fun f g => f ⟂ᵢ[mu] g) X) ->
    (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
    ∀ᵐ omega ∂mu,
      Tendsto (fun n : Nat => empiricalFrequency X n omega)
        atTop (nhds (mu[X 0]))

/-- Transport the analytic limit along the frozen expectation equation. -/
def ExpectationTransportPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega)
    (X : Nat -> Omega -> Real) (p : Real),
    mu[X 0] = p ->
    (∀ᵐ omega ∂mu,
      Tendsto (fun n : Nat => empiricalFrequency X n omega)
        atTop (nhds (mu[X 0]))) ->
    ∀ᵐ omega ∂mu,
      Tendsto (fun n : Nat => empiricalFrequency X n omega) atTop (nhds p)

/-- Checked composition of the three substantive interfaces into the root. -/
theorem root_of_packages
    (pairwiseProjection : PairwiseProjectionPackage.{u})
    (strongLaw : StrongLawPackage.{u})
    (expectationTransport : ExpectationTransportPackage.{u}) : Target.{u} := by
  intro Omega _ mu _ X p hint hindep hident _hBernoulli hexpect
  exact expectationTransport Omega mu X p hexpect
    (strongLaw Omega mu X hint (pairwiseProjection Omega mu X hindep) hident)

#print axioms root_of_packages

end Stage1Instances.THM_M_0983_Obligations
