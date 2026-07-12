import Mathlib.Probability.StrongLaw

/-!
# THM-M-0984: exact modern strong-law statement

This module freezes and tests the modern iid integrable target selected by the
rev-5.6 intake. It does not prove the strong law or identify this general target
with Borel's narrower historical frequency theorem.
-/

noncomputable section

open Filter Finset Function MeasureTheory
open scoped MeasureTheory ProbabilityTheory Topology

namespace Stage1Instances.THM_M_0984

universe u v

/-- The empirical average of the first `n` random variables. At `n = 0` this is
the zero vector because the sum is empty. -/
def empiricalAverage
    {Omega : Type u} {E : Type v} [NormedAddCommGroup E] [NormedSpace Real E]
    (X : Nat -> Omega -> E) (n : Nat) (omega : Omega) : E :=
  (n : Real)⁻¹ • (∑ i ∈ range n, X i omega)

/-- The exact modern strong-law target frozen at intake: pairwise-independent,
identically distributed, integrable Banach-valued random variables have
empirical averages converging almost everywhere to their Bochner expectation. -/
def StrongLawTarget : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega],
    forall (E : Type v) [NormedAddCommGroup E] [NormedSpace Real E]
      [CompleteSpace E] [MeasurableSpace E] [BorelSpace E],
      forall (mu : Measure Omega) (X : Nat -> Omega -> E),
        Integrable (X 0) mu ->
        Pairwise ((fun Y Z => Y ⟂ᵢ[mu] Z) on X) ->
        (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
        ∀ᵐ omega ∂mu,
          Tendsto (fun n : Nat => empiricalAverage X n omega)
            atTop (nhds (integral mu (X 0)))

/-- A bundled encoding of precisely the hypotheses of `StrongLawTarget`. -/
structure StrongLawData (Omega : Type u) [MeasurableSpace Omega]
    (E : Type v) [NormedAddCommGroup E] [NormedSpace Real E]
    [CompleteSpace E] [MeasurableSpace E] [BorelSpace E] where
  mu : Measure Omega
  X : Nat -> Omega -> E
  integrable_zero : Integrable (X 0) mu
  pairwise_independent : Pairwise ((fun Y Z => Y ⟂ᵢ[mu] Z) on X)
  identically_distributed :
    forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu

/-- Bundled alternate encoding used to ensure binder packaging does not change
the target. -/
def BundledStrongLawTarget : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega],
    forall (E : Type v) [NormedAddCommGroup E] [NormedSpace Real E]
      [CompleteSpace E] [MeasurableSpace E] [BorelSpace E],
      forall D : StrongLawData Omega E,
        ∀ᵐ omega ∂D.mu,
          Tendsto (fun n : Nat => empiricalAverage D.X n omega)
            atTop (nhds (integral D.mu (D.X 0)))

/-- Checked transport between the explicit canonical target and its bundled
encoding. No strong-law proof is used by this packaging equivalence. -/
theorem strongLawTarget_iff_bundled :
    StrongLawTarget.{u, v} <-> BundledStrongLawTarget.{u, v} := by
  constructor
  · intro h Omega _ E _ _ _ _ _ D
    exact h Omega E D.mu D.X D.integrable_zero D.pairwise_independent
      D.identically_distributed
  · intro h Omega _ E _ _ _ _ _ mu X h_integrable h_independent h_identical
    exact h Omega E
      { mu := mu
        X := X
        integrable_zero := h_integrable
        pairwise_independent := h_independent
        identically_distributed := h_identical }

-- Separately elaborated structural mutations checked by `check_statement.py`.
def mutationRemovedIntegrability : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega],
    forall (E : Type v) [NormedAddCommGroup E] [NormedSpace Real E]
      [CompleteSpace E] [MeasurableSpace E] [BorelSpace E],
      forall (mu : Measure Omega) (X : Nat -> Omega -> E),
        Pairwise ((fun Y Z => Y ⟂ᵢ[mu] Z) on X) ->
        (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
        ∀ᵐ omega ∂mu,
          Tendsto (fun n : Nat => empiricalAverage X n omega)
            atTop (nhds (integral mu (X 0)))

def mutationRealCodomain : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega],
    forall (mu : Measure Omega) (X : Nat -> Omega -> Real),
      Integrable (X 0) mu ->
      Pairwise ((fun Y Z => Y ⟂ᵢ[mu] Z) on X) ->
      (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
      ∀ᵐ omega ∂mu,
        Tendsto (fun n : Nat => empiricalAverage X n omega)
          atTop (nhds (integral mu (X 0)))

def mutationJointIndependence : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega],
    forall (E : Type v) [NormedAddCommGroup E] [NormedSpace Real E]
      [CompleteSpace E] [MeasurableSpace E] [BorelSpace E],
      forall (mu : Measure Omega) (X : Nat -> Omega -> E),
        Integrable (X 0) mu ->
        ProbabilityTheory.iIndepFun X mu ->
        (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
        ∀ᵐ omega ∂mu,
          Tendsto (fun n : Nat => empiricalAverage X n omega)
            atTop (nhds (integral mu (X 0)))

def mutationChangedLimit : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega],
    forall (E : Type v) [NormedAddCommGroup E] [NormedSpace Real E]
      [CompleteSpace E] [MeasurableSpace E] [BorelSpace E],
      forall (mu : Measure Omega) (X : Nat -> Omega -> E),
        Integrable (X 0) mu ->
        Pairwise ((fun Y Z => Y ⟂ᵢ[mu] Z) on X) ->
        (forall i, ProbabilityTheory.IdentDistrib (X i) (X 0) mu mu) ->
        ∀ᵐ omega ∂mu,
          Tendsto (fun n : Nat => empiricalAverage X n omega) atTop (nhds 0)

/-- The `n = 0` convention is explicitly the zero vector. -/
theorem empiricalAverage_zero
    {Omega : Type u} {E : Type v} [NormedAddCommGroup E] [NormedSpace Real E]
    (X : Nat -> Omega -> E) (omega : Omega) :
    empiricalAverage X 0 omega = 0 := by
  simp [empiricalAverage]

/-- The degenerate zero sequence satisfies the conclusion for every measure. -/
theorem zero_sequence_boundary
    {Omega : Type u} [MeasurableSpace Omega]
    {E : Type v} [NormedAddCommGroup E] [NormedSpace Real E]
    [CompleteSpace E] [MeasurableSpace E] [BorelSpace E]
    (mu : Measure Omega) :
    ∀ᵐ omega ∂mu,
      Tendsto (fun n : Nat => empiricalAverage (fun _ _ => (0 : E)) n omega)
        atTop (nhds (integral mu (fun _ : Omega => (0 : E)))) := by
  filter_upwards
  intro omega
  simp [empiricalAverage]

end Stage1Instances.THM_M_0984

set_option pp.explicit true in
#print Stage1Instances.THM_M_0984.StrongLawTarget
