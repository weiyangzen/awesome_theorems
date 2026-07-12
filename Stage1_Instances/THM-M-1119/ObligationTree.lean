import Statement

/-!
# THM-M-1119 conditional obligation composition

This module checks only the final composition boundary of the frozen proof
architecture.  The two threshold inequalities remain explicit hypotheses; no
proof of either inequality, and hence no proof of Kesten's theorem, is claimed.
-/

namespace Stage1Instances.THM_M_1119

/-- Output of the subcritical/duality half of the architecture. -/
def SubcriticalThresholdBound : Prop :=
  (1 / 2 : NNReal) ≤ criticalProbability

/-- Output of the supercritical/finite-size half of the architecture. -/
def SupercriticalThresholdBound : Prop :=
  criticalProbability ≤ (1 / 2 : NNReal)

/-- Checked conditional composition of the two exact inequalities into the
canonical equality. Both registered premises are consumed. -/
theorem kestenTarget_of_threshold_bounds
    (subcritical : SubcriticalThresholdBound)
    (supercritical : SupercriticalThresholdBound) : KestenTarget := by
  exact le_antisymm supercritical subcritical

#print axioms kestenTarget_of_threshold_bounds

end Stage1Instances.THM_M_1119
