import Statement
import AtlasFourierSeries

/-!
# THM-M-0347 exact proof wrapper

This module checks that the frozen symmetric sums and Cesaro convention are
exactly the ones used by the pinned ATLAS proof, then transports its uniform
Fejer convergence theorem to the unchanged target from `Statement.lean`.
-/

namespace Stage1Instances.THM_M_0347

open Filter Topology
open scoped BigOperators

/-- The frozen bundled partial sum agrees pointwise with the ATLAS definition. -/
theorem symmetricFourierPartialSum_apply {T : Real} [Fact (0 < T)]
    (f : C(AddCircle T, Complex)) (n : Nat) (x : AddCircle T) :
    symmetricFourierPartialSum f n x =
      FourierSeries.partialFourierSum (⇑f) n x := by
  simp [symmetricFourierPartialSum, FourierSeries.partialFourierSum]

/-- The frozen mean agrees pointwise with the ATLAS Cesaro-Fourier mean. -/
theorem fejerMean_apply {T : Real} [Fact (0 < T)]
    (f : C(AddCircle T, Complex)) (n : Nat) (x : AddCircle T) :
    fejerMean f n x = FourierSeries.cesaroFourierMean (⇑f) n x := by
  simp only [fejerMean, ContinuousMap.sum_apply, ContinuousMap.smul_apply,
    FourierSeries.cesaroFourierMean, Finset.smul_sum,
    symmetricFourierPartialSum_apply]
  push_cast
  rfl

/-- Exact premise-free inhabitant of the unchanged frozen Fejer target. -/
theorem fejerTheorem : FejerTheoremTarget := by
  intro T _ f
  rw [ContinuousMap.tendsto_iff_tendstoUniformly]
  simpa only [fejerMean_apply] using fejer_uniform_convergence f

end Stage1Instances.THM_M_0347

#print axioms Stage1Instances.THM_M_0347.symmetricFourierPartialSum_apply
#print axioms Stage1Instances.THM_M_0347.fejerMean_apply
#print axioms Stage1Instances.THM_M_0347.fejerTheorem
