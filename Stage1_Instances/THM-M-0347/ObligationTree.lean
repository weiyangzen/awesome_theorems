import Statement

/-!
# THM-M-0347 conditional obligation composition

This module checks the final child-to-root interface selected by the frozen
Fejer proof architecture.  The uniform estimate is an explicit premise; no
proof of that estimate, and hence no proof of Fejer's theorem, is supplied.
-/

namespace Stage1Instances.THM_M_0347.ObligationTree

open Filter Topology

/-- The epsilon form of the still-open uniform approximate-identity estimate. -/
def UniformFejerEstimate : Prop :=
  forall (T : Real) [Fact (0 < T)] (f : C(AddCircle T, Complex)) (eps : Real),
    0 < eps -> exists N : Nat, forall n, N <= n -> dist (fejerMean f n) f < eps

/-- Checked composition from the uniform estimate to the exact frozen target. -/
theorem root_of_uniformFejerEstimate (h : UniformFejerEstimate) :
    FejerTheoremTarget := by
  intro T _ f
  rw [Metric.tendsto_atTop]
  intro eps heps
  exact h T f eps heps

#check UniformFejerEstimate
#check root_of_uniformFejerEstimate
#print axioms root_of_uniformFejerEstimate

end Stage1Instances.THM_M_0347.ObligationTree
