import Statement
import AtlasFourierSeries
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-0347 validation probe

This module deliberately does not import `Proof.lean`. It independently
rebuilds the two definition transports and the final composition from the
vendored Fejer theorem to the exact frozen target.
-/

namespace Stage1Instances.THM_M_0347.Validation

open Filter Topology
open scoped BigOperators

open Stage1Instances.THM_M_0347

/-- Independent replay of the frozen partial-sum transport. -/
theorem reconstructedPartialSum {T : Real} [Fact (0 < T)]
    (f : C(AddCircle T, Complex)) (n : Nat) (x : AddCircle T) :
    symmetricFourierPartialSum f n x =
      FourierSeries.partialFourierSum (fun y => f y) n x := by
  simp [symmetricFourierPartialSum, FourierSeries.partialFourierSum]

/-- Independent replay of the frozen Cesaro-mean transport. -/
theorem reconstructedMean {T : Real} [Fact (0 < T)]
    (f : C(AddCircle T, Complex)) (n : Nat) (x : AddCircle T) :
    fejerMean f n x = FourierSeries.cesaroFourierMean (fun y => f y) n x := by
  simp only [fejerMean, ContinuousMap.sum_apply, ContinuousMap.smul_apply,
    FourierSeries.cesaroFourierMean, Finset.smul_sum, reconstructedPartialSum]
  push_cast
  rfl

/-- Independently composed inhabitant of the unchanged frozen target. -/
theorem reconstructedFejerTheorem : FejerTheoremTarget := by
  intro T _ f
  rw [ContinuousMap.tendsto_iff_tendstoUniformly]
  simpa only [reconstructedMean] using fejer_uniform_convergence f

#check reconstructedFejerTheorem
assert_no_sorry FourierSeries.fejer_kernel_properties
assert_no_sorry FourierSeries.cesaroMean_eq_fejer_convolution
assert_no_sorry fejerKernel_eq_ofReal
assert_no_sorry integral_norm_fejerKernel
assert_no_sorry cesaroMean_uniform_bound
assert_no_sorry fejer_uniform_convergence
assert_no_sorry reconstructedPartialSum
assert_no_sorry reconstructedMean
assert_no_sorry reconstructedFejerTheorem
#print sorries FourierSeries.fejer_kernel_properties
#print sorries FourierSeries.cesaroMean_eq_fejer_convolution
#print sorries fejerKernel_eq_ofReal
#print sorries integral_norm_fejerKernel
#print sorries cesaroMean_uniform_bound
#print sorries fejer_uniform_convergence
#print sorries reconstructedPartialSum
#print sorries reconstructedMean
#print sorries reconstructedFejerTheorem

end Stage1Instances.THM_M_0347.Validation

#print axioms FourierSeries.fejer_kernel_properties
#print axioms FourierSeries.cesaroMean_eq_fejer_convolution
#print axioms fejerKernel_eq_ofReal
#print axioms integral_norm_fejerKernel
#print axioms cesaroMean_uniform_bound
#print axioms fejer_uniform_convergence
#print axioms Stage1Instances.THM_M_0347.Validation.reconstructedPartialSum
#print axioms Stage1Instances.THM_M_0347.Validation.reconstructedMean
#print axioms Stage1Instances.THM_M_0347.Validation.reconstructedFejerTheorem
