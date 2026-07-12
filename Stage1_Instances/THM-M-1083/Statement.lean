import Mathlib.Probability.Process.Kolmogorov
import Mathlib.MeasureTheory.Measure.Typeclasses.Probability
import Mathlib.Topology.MetricSpace.Holder

/-!
# THM-M-1083 canonical statement

This file freezes the compact-interval, real-valued Kolmogorov-Chentsov target. It declares the
proposition only; no proof of the continuity theorem is asserted here.
-/

noncomputable section

open MeasureTheory Set
open scoped ENNReal NNReal

namespace Stage1Instances.THM_M_1083

universe u

/-- The compact time interval used intrinsically as the process index type. -/
abbrev TimeInterval (T : ℝ) := Set.Icc (0 : ℝ) T

/-- A real-valued stochastic process on `[0, T]`. -/
abbrev RealProcess (T : ℝ) (Ω : Type u) := TimeInterval T → Ω → ℝ

/-- Fixed-time almost-everywhere equality, the standard modification relation. -/
def IsModification {T : ℝ} {Ω : Type u} [MeasurableSpace Ω]
    (P : Measure Ω) (X Y : RealProcess T Ω) : Prop :=
  ∀ t, X t =ᵐ[P] Y t

/-- A path has a finite Hölder constant at exponent `gamma` on the intrinsic interval. -/
def HasHolderPath {T : ℝ} {Ω : Type u} (Y : RealProcess T Ω)
    (gamma : ℝ≥0) (ω : Ω) : Prop :=
  ∃ K : ℝ≥0, HolderWith K gamma (fun t => Y t ω)

/--
The compact-interval, real-valued Kolmogorov-Chentsov theorem.

The `lintegral` is the extended nonnegative expectation of the increment moment. Constants and
Hölder exponents use `NNReal` exactly where nonnegativity is structural. The null set for Hölder
regularity may depend on `gamma`, while modification equality is asserted at each fixed time.
-/
def KolmogorovContinuity : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
      (T alpha beta : ℝ) (C : ℝ≥0) (X : RealProcess T Ω),
    0 < T →
    0 < alpha →
    0 < beta →
    (∀ t, Measurable (X t)) →
    (∀ s t,
      ∫⁻ ω, edist (X s ω) (X t ω) ^ alpha ∂P ≤
        (C : ℝ≥0∞) * edist s t ^ (1 + beta)) →
    ∃ Y : RealProcess T Ω,
      IsModification P X Y ∧
        ∀ gamma : ℝ≥0,
          0 < gamma →
          (gamma : ℝ) < beta / alpha →
          ∀ᵐ ω ∂P, HasHolderPath Y gamma ω

/-- Public canonical target for the statement phase. -/
abbrev Statement : Prop := KolmogorovContinuity.{u}

-- Structural mutations fingerprint excluded or altered claims.
def MutationIncludesCriticalExponent : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
      (T alpha beta : ℝ) (C : ℝ≥0) (X : RealProcess T Ω),
    0 < T → 0 < alpha → 0 < beta → (∀ t, Measurable (X t)) →
    (∀ s t, ∫⁻ ω, edist (X s ω) (X t ω) ^ alpha ∂P ≤
      (C : ℝ≥0∞) * edist s t ^ (1 + beta)) →
    ∃ Y : RealProcess T Ω, IsModification P X Y ∧
      ∀ gamma : ℝ≥0, 0 < gamma → (gamma : ℝ) ≤ beta / alpha →
        ∀ᵐ ω ∂P, HasHolderPath Y gamma ω

def MutationContinuityOnly : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
      (T alpha beta : ℝ) (C : ℝ≥0) (X : RealProcess T Ω),
    0 < T → 0 < alpha → 0 < beta → (∀ t, Measurable (X t)) →
    (∀ s t, ∫⁻ ω, edist (X s ω) (X t ω) ^ alpha ∂P ≤
      (C : ℝ≥0∞) * edist s t ^ (1 + beta)) →
    ∃ Y : RealProcess T Ω, IsModification P X Y ∧
      ∀ᵐ ω ∂P, Continuous (fun t => Y t ω)

def MutationSimultaneousModification : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
      (T alpha beta : ℝ) (C : ℝ≥0) (X : RealProcess T Ω),
    0 < T → 0 < alpha → 0 < beta → (∀ t, Measurable (X t)) →
    (∀ s t, ∫⁻ ω, edist (X s ω) (X t ω) ^ alpha ∂P ≤
      (C : ℝ≥0∞) * edist s t ^ (1 + beta)) →
    ∃ Y : RealProcess T Ω,
      (∀ᵐ ω ∂P, ∀ t, X t ω = Y t ω) ∧
        ∀ gamma : ℝ≥0, 0 < gamma → (gamma : ℝ) < beta / alpha →
          ∀ᵐ ω ∂P, HasHolderPath Y gamma ω

def MutationLinearIncrementPower : Prop :=
  ∀ (Ω : Type u) [MeasurableSpace Ω] (P : Measure Ω) [IsProbabilityMeasure P]
      (T alpha beta : ℝ) (C : ℝ≥0) (X : RealProcess T Ω),
    0 < T → 0 < alpha → 0 < beta → (∀ t, Measurable (X t)) →
    (∀ s t, ∫⁻ ω, edist (X s ω) (X t ω) ^ alpha ∂P ≤
      (C : ℝ≥0∞) * edist s t ^ beta) →
    ∃ Y : RealProcess T Ω, IsModification P X Y ∧
      ∀ gamma : ℝ≥0, 0 < gamma → (gamma : ℝ) < beta / alpha →
        ∀ᵐ ω ∂P, HasHolderPath Y gamma ω

#check Statement
#print KolmogorovContinuity
#print MutationIncludesCriticalExponent
#print MutationContinuityOnly
#print MutationSimultaneousModification
#print MutationLinearIncrementPower

end Stage1Instances.THM_M_1083
