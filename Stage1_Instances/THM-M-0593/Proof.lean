import ObligationTree
import Mathlib.Topology.MetricSpace.HausdorffDimension
import Mathlib.Analysis.Calculus.ContDiff.RCLike
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

set_option maxHeartbeats 4000000

/-!
# THM-M-0593 partial proof execution

This module closes the zero-codomain and lower-domain-dimension branches of
the frozen Sard architecture. The hard `0 < n` and `n <= m` branch remains an
explicit premise of the final composition theorem.
-/

namespace Stage1Instances.THMM0593

open MeasureTheory Set
open scoped NNReal ENNReal

/-- Every derivative into zero-dimensional Euclidean space is surjective, so
the critical locus is empty. -/
theorem zeroCodomainBranch_proof : ZeroCodomainBranch := by
  intro m f R _hopen _hsmooth
  have hcrit : criticalPointsOn f R = ∅ := by
    ext x
    simp only [criticalPointsOn, mem_setOf_eq, mem_empty_iff_false, iff_false]
    intro hx
    exact hx.2 (Function.surjective_to_subsingleton (fderiv ℝ f x))
  simp [hcrit]

/-- In the dimension-increasing case, local smoothness makes the restriction
to the critical locus locally Lipschitz. Its image has Hausdorff dimension at
most `m < n`, hence zero `n`-dimensional volume. -/
theorem lowDimensionBranch_proof : LowDimensionBranch := by
  intro m n f R hmn hopen hsmooth
  have hlocal : ∀ x ∈ criticalPointsOn f R,
      ∃ C : ℝ≥0, ∃ t ∈ nhdsWithin x (criticalPointsOn f R), LipschitzOnWith C f t := by
    intro x hx
    have hxR : x ∈ R := hx.1
    have hC1 : ContDiffOn ℝ 1 f R := hsmooth.of_le (by simp)
    have hAt : ContDiffAt ℝ 1 f x := hopen.contDiffOn_iff.mp hC1 hxR
    rcases hAt.exists_lipschitzOnWith with ⟨C, t, ht, hLip⟩
    exact ⟨C, t, mem_nhdsWithin_of_mem_nhds ht, hLip⟩
  have hdimImage : dimH (f '' criticalPointsOn f R) ≤ m := by
    calc
      dimH (f '' criticalPointsOn f R) ≤ dimH (criticalPointsOn f R) :=
        dimH_image_le_of_locally_lipschitzOn hlocal
      _ ≤ dimH (univ : Set (EuclideanSpace ℝ (Fin m))) := dimH_mono (subset_univ _)
      _ = m := by simp [Real.dimH_univ_eq_finrank]
  have hdim : dimH (f '' criticalPointsOn f R) < ((n : ℝ≥0) : ℝ≥0∞) :=
    hdimImage.trans_lt (by exact_mod_cast hmn)
  have hzero : (μH[(n : ℝ)] : Measure (EuclideanSpace ℝ (Fin n)))
      (f '' criticalPointsOn f R) = 0 :=
    hausdorffMeasure_of_dimH_lt (d := (n : ℝ≥0)) hdim
  rw [← EuclideanSpace.euclideanHausdorffMeasure_eq_volume n]
  rw [Measure.euclideanHausdorffMeasure_def, Measure.smul_apply]
  change ((Measure.addHaarScalarFactor volume (μH[n])) : ℝ≥0∞) *
    (μH[n] : Measure (EuclideanSpace ℝ (Fin n))) (f '' criticalPointsOn f R) = 0
  rw [hzero]
  simp

/-- Exact-root composition after closing the two elementary dimension
branches. The unproved hard branch stays visible in the theorem type. -/
theorem sardTarget_of_hardDimensionBranch (hard : HardDimensionBranch) : SardTarget :=
  root_of_sard_branches zeroCodomainBranch_proof lowDimensionBranch_proof hard

assert_no_sorry zeroCodomainBranch_proof
assert_no_sorry lowDimensionBranch_proof
assert_no_sorry sardTarget_of_hardDimensionBranch

#print sorries zeroCodomainBranch_proof
#print sorries lowDimensionBranch_proof
#print sorries sardTarget_of_hardDimensionBranch

#print axioms zeroCodomainBranch_proof
#print axioms lowDimensionBranch_proof
#print axioms sardTarget_of_hardDimensionBranch

end Stage1Instances.THMM0593
