import Statement
import Proof

/-! Exact canonical-target check for the THM-M-1268 proof phase. -/

namespace Stage1Instances.THM_M_1268

universe u

/-- The proof-phase body inhabits the exact declaration frozen by the
statement phase, not merely a broadened or substituted proposition. -/
theorem weakLowerSemicontinuity : WeakLowerSemicontinuityTarget.{u} :=
  Proof.weakLowerSemicontinuity

#print axioms weakLowerSemicontinuity

end Stage1Instances.THM_M_1268
