import Mathlib.Analysis.Normed.Module.FiniteDimension
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Dynamics.Ergodic.Ergodic
import Mathlib.LinearAlgebra.Dimension.Finrank
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# THM-M-1056: exact Oseledets statement

This module freezes the finite-dimensional, real, invertible, ergodic cocycle
variant selected at intake. It contains no proof of the multiplicative ergodic
theorem.
-/

open Filter Function MeasureTheory
open scoped BigOperators ENNReal NNReal Topology

namespace Stage1Instances.THM_M_1056

universe u v

/-- The forward action of a one-step invertible linear cocycle on a vector. -/
def cocycleVector {Omega : Type u} {E : Type v} [NormedAddCommGroup E]
    [NormedSpace Real E] (T : Omega -> Omega)
    (A : Omega -> E ≃L[Real] E) : Nat -> Omega -> E -> E
  | 0, _omega, x => x
  | n + 1, omega, x => A (T^[n] omega) (cocycleVector T A n omega x)

/-- The positive part of the logarithm, used in the two integrability hypotheses. -/
noncomputable def logPlus (x : Real) : Real := max (Real.log x) 0

/-- A measurable family of complementary projections encoding a measurable
direct-sum splitting. -/
structure LyapunovSplitting {Omega : Type u} {E : Type v}
    [MeasurableSpace Omega] [NormedAddCommGroup E] [NormedSpace Real E]
    (T : Omega -> Omega) (A : Omega -> E ≃L[Real] E) (mu : Measure Omega) where
  count : Nat
  count_pos : 0 < count
  exponent : Fin count -> Real
  exponent_strict : StrictAnti exponent
  projection : Omega -> Fin count -> E →L[Real] E
  projection_measurable : forall i, StronglyMeasurable (fun eta => projection eta i)
  projection_idempotent : ∀ᵐ eta ∂mu, forall i,
    (projection eta i).comp (projection eta i) = projection eta i
  projection_disjoint : ∀ᵐ eta ∂mu, forall i j, i ≠ j ->
    (projection eta i).comp (projection eta j) = 0
  projection_sum : ∀ᵐ eta ∂mu, (∑ i, projection eta i) =
    ContinuousLinearMap.id Real E
  projection_nonzero : ∀ᵐ eta ∂mu, forall i, projection eta i ≠ 0
  equivariant : ∀ᵐ eta ∂mu, forall i,
    (A eta).toContinuousLinearMap.comp (projection eta i) =
      (projection (T eta) i).comp (A eta).toContinuousLinearMap
  growth : ∀ᵐ eta ∂mu, forall i x, x ≠ 0 -> projection eta i x = x ->
    Tendsto (fun n : Nat => (Real.log (norm (cocycleVector T A n eta x))) / n)
      atTop (nhds (exponent i))

/-- Exact target: the classical finite-dimensional real invertible Oseledets
theorem over an invertible ergodic probability-preserving base.

Measurable complementary projections represent the measurable direct-sum
Lyapunov subspaces. The conclusion is pointwise on one conull set, so its
growth clause applies simultaneously to every nonzero vector in every fiber. -/
def OseledetsMultiplicativeErgodicTarget : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (E : Type v) [NormedAddCommGroup E] [NormedSpace Real E]
    [FiniteDimensional Real E] [MeasurableSpace E] [BorelSpace E]
    (hE : 0 < Module.finrank Real E)
    (T : Omega ≃ᵐ Omega) (hT : Ergodic T mu)
    (A : Omega -> E ≃L[Real] E),
      StronglyMeasurable (fun omega => (A omega).toContinuousLinearMap) ->
      Integrable (fun omega => logPlus (norm (A omega).toContinuousLinearMap)) mu ->
      Integrable (fun omega => logPlus (norm (A omega).symm.toContinuousLinearMap)) mu ->
      Nonempty (LyapunovSplitting T A mu)

-- Separately elaborated mutations. Their printed expressions are compared by
-- the statement validator; none is credited as an alternate target.
def mutationRemovedInverseIntegrability : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (E : Type v) [NormedAddCommGroup E] [NormedSpace Real E]
    [FiniteDimensional Real E] [MeasurableSpace E] [BorelSpace E]
    (hE : 0 < Module.finrank Real E)
    (T : Omega ≃ᵐ Omega) (hT : Ergodic T mu)
    (A : Omega -> E ≃L[Real] E),
      StronglyMeasurable (fun omega => (A omega).toContinuousLinearMap) ->
      Integrable (fun omega => logPlus (norm (A omega).toContinuousLinearMap)) mu ->
      Nonempty (LyapunovSplitting T A mu)

def mutationChangedDomainToComplex : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (E : Type v) [NormedAddCommGroup E] [NormedSpace Complex E]
    [FiniteDimensional Complex E] [MeasurableSpace E] [BorelSpace E], True

def mutationChangedBinderScope : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (E : Type v) [NormedAddCommGroup E] [NormedSpace Real E]
    [FiniteDimensional Real E] [MeasurableSpace E] [BorelSpace E]
    (hE : 0 < Module.finrank Real E) (T : Omega ≃ᵐ Omega) (hT : Ergodic T mu),
      forall A : Omega -> E ≃L[Real] E,
      StronglyMeasurable (fun omega => (A omega).toContinuousLinearMap) ->
      (Integrable (fun omega => logPlus (norm (A omega).toContinuousLinearMap)) mu /\
       Integrable (fun omega => logPlus (norm (A omega).symm.toContinuousLinearMap)) mu) ->
      Nonempty (LyapunovSplitting T A mu)

/-- Boundary mutation admitting the excluded zero-dimensional fiber. -/
def mutationAllowsZeroDimension : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (E : Type v) [NormedAddCommGroup E] [NormedSpace Real E]
    [FiniteDimensional Real E] [MeasurableSpace E] [BorelSpace E]
    (T : Omega ≃ᵐ Omega) (hT : Ergodic T mu)
    (A : Omega -> E ≃L[Real] E),
      StronglyMeasurable (fun omega => (A omega).toContinuousLinearMap) ->
      Integrable (fun omega => logPlus (norm (A omega).toContinuousLinearMap)) mu ->
      Integrable (fun omega => logPlus (norm (A omega).symm.toContinuousLinearMap)) mu ->
      Nonempty (LyapunovSplitting T A mu)

end Stage1Instances.THM_M_1056

set_option pp.explicit true in
#print Stage1Instances.THM_M_1056.OseledetsMultiplicativeErgodicTarget
