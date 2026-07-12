import Stage1_Instances.«THM-M-1227».Statement

/-!
# THM-M-1227 proof execution

This module closes only the frozen `M1227-B-ZERO` obligation. It deliberately does not assert the
general Leray-Hopf existence theorem: the five-node root cut set recorded by the frozen obligation
registry has no repo-local or pinned terminal proof body.
-/

namespace Stage1.THM_M_1227

/-- The identically zero velocity and gradient satisfy all six frozen solution conditions. -/
theorem zero_isLerayHopfSolution (nu : Real) :
    IsLerayHopfSolution nu (fun _ => 0) (fun _ _ => 0) (fun _ _ => 0) := by
  apply isLerayHopfSolution_compose
  · simp [IsWeakGradient, spatialPartial]
  · simp [sqNorm, dot, gradSqNorm]
  · simp
  · intro phi _
    simp [dot]
  · simp [sqNorm, dot]
  · intro t _
    simp [sqNorm, dot, gradSqNorm]

#print axioms zero_isLerayHopfSolution

end Stage1.THM_M_1227
