import Statement

/-!
# THM-M-1084 obligation interfaces

This file checks only the final composition boundary. The two package premises remain open proof
obligations; neither is a global assumption or a claimed theorem.
-/

noncomputable section

open MeasureTheory Set

namespace Stage1Instances.THM_M_1084

universe u v

/-- The integrability half of the exact target, exposed as a proof-package interface. -/
def SupremumIntegrabilityPackage : Prop :=
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
      Integrable (basedSupremum X t0) mu

/-- The numerical inequality half of the exact target, with every original premise retained. -/
def EntropyInequalityPackage : Prop :=
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
      ∫ omega, basedSupremum X t0 omega ∂mu ≤ 12 * entropyIntegral T

/-- Checked child-to-parent composition. It is conditional and proves no package premise. -/
theorem root_of_integrability_and_entropy_packages
    (hIntegrable : SupremumIntegrabilityPackage.{u, v})
    (hBound : EntropyInequalityPackage.{u, v}) :
    DudleyEntropyBoundTarget.{u, v} := by
  intro T _ _ Omega _ mu X t0 dense hGaussian hCentered hCanonical hTotallyBounded
    hSeparating hEntropyIntegrable
  exact ⟨
    hIntegrable T Omega mu X t0 dense hGaussian hCentered hCanonical hTotallyBounded
      hSeparating hEntropyIntegrable,
    hBound T Omega mu X t0 dense hGaussian hCentered hCanonical hTotallyBounded
      hSeparating hEntropyIntegrable⟩

#check root_of_integrability_and_entropy_packages
#print axioms root_of_integrability_and_entropy_packages

end Stage1Instances.THM_M_1084
