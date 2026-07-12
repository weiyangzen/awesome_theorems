import Mathlib.MeasureTheory.Integral.IntervalIntegral.Basic
import Mathlib.Probability.Distributions.Gaussian.HasGaussianLaw.Basic
import Mathlib.Topology.MetricSpace.Bounded

/-!
# THM-M-1084: Dudley's entropy bound statement

This module freezes the statement boundary. It defines open-ball covering numbers explicitly and
states the constant-12, diameter-over-two form of Dudley's bound for a centered, sample-separable
real Gaussian process. It does not contain a proof of the bound.
-/

noncomputable section

open MeasureTheory Set

namespace Stage1Instances.THM_M_1084

universe u v

/-- A finite family of open `epsilon`-balls covering the whole index space. -/
def IsOpenBallCover {T : Type u} [PseudoMetricSpace T] (epsilon : ℝ)
    (centers : Finset T) : Prop :=
  ∀ t : T, ∃ c ∈ centers, dist t c < epsilon

/-- The least cardinality of an open `epsilon`-ball cover. The surrounding target assumes total
boundedness; hence the defining set is nonempty for every positive `epsilon`. -/
def coveringNumber {T : Type u} [PseudoMetricSpace T] (epsilon : ℝ) : ℕ :=
  sInf {n : ℕ | ∃ centers : Finset T, centers.card = n ∧ IsOpenBallCover epsilon centers}

/-- The entropy integral in the constant-12 normalization. -/
def entropyIntegral (T : Type u) [PseudoMetricSpace T] : ℝ :=
  ∫ epsilon in (0 : ℝ)..Metric.diam (univ : Set T) / 2,
    Real.sqrt (Real.log (coveringNumber (T := T) epsilon : ℝ))

/-- Every finite linear combination of the coordinates has a real Gaussian law. -/
def IsRealGaussianProcess {T : Type u} {Omega : Type v} [MeasurableSpace Omega]
    (mu : Measure Omega) (X : T → Omega → ℝ) : Prop :=
  ∀ (s : Finset T) (a : T → ℝ),
    ProbabilityTheory.HasGaussianLaw (fun omega ↦ ∑ t ∈ s, a t * X t omega) mu

/-- The canonical increment pseudometric induced by a real process. -/
def canonicalDist {T : Type u} {Omega : Type v} [MeasurableSpace Omega]
    (mu : Measure Omega) (X : T → Omega → ℝ) (s t : T) : ℝ :=
  Real.sqrt (∫ omega, (X s omega - X t omega) ^ 2 ∂mu)

/-- The samplewise based supremum. -/
def basedSupremum {T : Type u} {Omega : Type v} (X : T → Omega → ℝ) (t0 : T)
    (omega : Omega) : ℝ :=
  sSup (range fun t : T ↦ X t omega - X t0 omega)

/-- A sequence realizes the sample supremum, the explicit separability condition used here. -/
def IsSampleSeparatingSequence {T : Type u} [TopologicalSpace T] {Omega : Type v}
    (X : T → Omega → ℝ)
    (t0 : T) (dense : ℕ → T) : Prop :=
  DenseRange dense ∧ ∀ omega,
    basedSupremum X t0 omega = sSup (range fun n : ℕ ↦ X (dense n) omega - X t0 omega)

/-- Dudley's entropy bound in the open-ball, constant-12 normalization. -/
def DudleyEntropyBoundTarget : Prop :=
  ∀ (T : Type u) [PseudoMetricSpace T] [Nonempty T]
    (Omega : Type v) [MeasurableSpace Omega] (mu : Measure Omega)
    (X : T → Omega → ℝ) (t0 : T) (dense : ℕ → T),
      IsRealGaussianProcess mu X →
      (∀ t, ∫ omega, X t omega ∂mu = 0) →
      (∀ s t, dist s t = canonicalDist mu X s t) →
      TotallyBounded (univ : Set T) →
      IsSampleSeparatingSequence X t0 dense →
      IntegrableOn
        (fun epsilon ↦ Real.sqrt (Real.log (coveringNumber (T := T) epsilon : ℝ)))
        (Icc 0 (Metric.diam (univ : Set T) / 2)) →
      Integrable (basedSupremum X t0) mu ∧
        ∫ omega, basedSupremum X t0 omega ∂mu ≤ 12 * entropyIntegral T

/-- Direct expansion used to ensure that the theorem name hides no stronger or weaker result. -/
def ExpandedSourceShape : Prop :=
  ∀ (T : Type u) [PseudoMetricSpace T] [Nonempty T]
    (Omega : Type v) [MeasurableSpace Omega] (mu : Measure Omega)
    (X : T → Omega → ℝ) (t0 : T) (dense : ℕ → T),
      IsRealGaussianProcess mu X →
      (∀ t, ∫ omega, X t omega ∂mu = 0) →
      (∀ s t, dist s t = Real.sqrt (∫ omega, (X s omega - X t omega) ^ 2 ∂mu)) →
      TotallyBounded (univ : Set T) →
      (DenseRange dense ∧ ∀ omega,
        sSup (range fun t : T ↦ X t omega - X t0 omega) =
          sSup (range fun n : ℕ ↦ X (dense n) omega - X t0 omega)) →
      IntegrableOn
        (fun epsilon ↦ Real.sqrt (Real.log (coveringNumber (T := T) epsilon : ℝ)))
        (Icc 0 (Metric.diam (univ : Set T) / 2)) →
      Integrable (basedSupremum X t0) mu ∧
        ∫ omega, sSup (range fun t : T ↦ X t omega - X t0 omega) ∂mu ≤
          12 * ∫ epsilon in (0 : ℝ)..Metric.diam (univ : Set T) / 2,
            Real.sqrt (Real.log (coveringNumber (T := T) epsilon : ℝ))

theorem target_iff_expandedSourceShape :
    DudleyEntropyBoundTarget.{u, v} ↔ ExpandedSourceShape.{u, v} := by
  simp only [DudleyEntropyBoundTarget, ExpandedSourceShape, canonicalDist, basedSupremum,
    IsSampleSeparatingSequence, entropyIntegral]

-- Non-equivalent mutations elaborated for statement-boundary inspection.
def mutationRemovedCentering : Prop :=
  ∀ (T : Type u) [PseudoMetricSpace T] [Nonempty T]
    (Omega : Type v) [MeasurableSpace Omega] (mu : Measure Omega)
    (X : T → Omega → ℝ) (t0 : T) (dense : ℕ → T),
      IsRealGaussianProcess mu X →
      (∀ s t, dist s t = canonicalDist mu X s t) →
      TotallyBounded (univ : Set T) → IsSampleSeparatingSequence X t0 dense →
      ∫ omega, basedSupremum X t0 omega ∂mu ≤ 12 * entropyIntegral T

def mutationChangedDomainToFinite : Prop :=
  ∀ (n : ℕ) (Omega : Type v) [MeasurableSpace Omega] (mu : Measure Omega)
    (X : Fin n → Omega → ℝ) (t0 : Fin n),
      IsRealGaussianProcess mu X → True

def mutationChangedBinderScope : Prop :=
  ∀ (T : Type u) [PseudoMetricSpace T] [Nonempty T]
    (Omega : Type v) [MeasurableSpace Omega] (mu : Measure Omega) (t0 : T),
      ∃ X : T → Omega → ℝ, ∃ dense : ℕ → T,
        IsRealGaussianProcess mu X ∧ IsSampleSeparatingSequence X t0 dense

/-- The singleton index type records the zero-diameter boundary without asserting the main bound. -/
theorem singleton_coveringNumber (epsilon : ℝ) (hepsilon : 0 < epsilon) :
    coveringNumber (T := PUnit) epsilon = 1 := by
  apply le_antisymm
  · apply csInf_le
    · exact ⟨0, fun n _ ↦ Nat.zero_le n⟩
    · exact ⟨{PUnit.unit}, by simp [IsOpenBallCover, hepsilon]⟩
  · apply le_csInf
    · exact ⟨1, ⟨{PUnit.unit}, by simp [IsOpenBallCover, hepsilon]⟩⟩
    intro n hn
    rcases hn with ⟨centers, rfl, hcover⟩
    obtain ⟨c, hc, _⟩ := hcover PUnit.unit
    exact Finset.one_le_card.mpr ⟨c, hc⟩

end Stage1Instances.THM_M_1084

set_option pp.explicit true in
#print Stage1Instances.THM_M_1084.DudleyEntropyBoundTarget
