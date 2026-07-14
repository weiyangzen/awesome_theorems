import GaussianMGFBridge
import CoveringNets

/-!
# THM-M-1084 validation probes

This module independently composes the already implemented Gaussian-MGF and finite-cover bodies.
It deliberately does not state or prove either terminal Dudley package or the canonical root.
-/

noncomputable section

open MeasureTheory Set

namespace Stage1Instances.THM_M_1084.Validation

universe u v

/-- Differential reconstruction of the implemented Gaussian-MGF package. -/
theorem independentlyReconstructedGaussianIncrementMGFPackage :
    Proof.GaussianIncrementMGFPackage.{u, v} := by
  intro T _ _ Omega _ mu X hGaussian hCentered hCanonical s t
  have h := Proof.hasSubgaussianMGF_of_hasGaussianLaw_of_integral_eq_zero
    (Proof.increment_hasGaussianLaw hGaussian s t) (by
      rw [integral_sub (Proof.coordinate_integrable hGaussian s)
        (Proof.coordinate_integrable hGaussian t), hCentered, hCentered, sub_self])
  have hnonneg : 0 <= ∫ omega, (X s omega - X t omega) ^ 2 ∂mu :=
    integral_nonneg fun _ => sq_nonneg _
  have hparam : Real.toNNReal (∫ omega, (X s omega - X t omega) ^ 2 ∂mu) =
      Real.toNNReal (dist s t ^ 2) := by
    congr 1
    rw [hCanonical, canonicalDist, Real.sq_sqrt hnonneg]
  rw [← hparam]
  exact h

/-- Differential reconstruction of the positivity consequence of the finite-cover implementation. -/
theorem independentlyReconstructedCoveringNumberPos
    {T : Type u} [PseudoMetricSpace T] [Nonempty T]
    (hTotallyBounded : TotallyBounded (univ : Set T))
    {epsilon : Real} (hepsilon : 0 < epsilon) :
    0 < coveringNumber (T := T) epsilon := by
  obtain ⟨centers, hcard, hcover⟩ :=
    Proof.exists_minimal_openBallCover hTotallyBounded hepsilon
  rw [← hcard]
  apply Finset.card_pos.mpr
  obtain ⟨c, hc, -⟩ := hcover (Classical.choice inferInstance)
  exact ⟨c, hc⟩

#print sorries independentlyReconstructedGaussianIncrementMGFPackage
#print axioms independentlyReconstructedGaussianIncrementMGFPackage
#print sorries independentlyReconstructedCoveringNumberPos
#print axioms independentlyReconstructedCoveringNumberPos

end Stage1Instances.THM_M_1084.Validation
