import Statement

/-!
# THM-M-1271 conditional root composition

This file checks the final composition boundary of the frozen obligation tree.
The two substantive packages remain explicit hypotheses; consequently this is
not a proof of the mountain-pass theorem.
-/

namespace Stage1Instances.THM_M_1271

universe u

/-- The geometric package: every admissible path crosses the positive barrier. -/
def MountainPassBarrierPackage : Prop :=
  forall (X : Type u) [NormedAddCommGroup X] [NormedSpace Real X] [CompleteSpace X]
    (Phi : X -> Real) (rho alpha : Real) (e : X),
    ContDiff Real 1 Phi -> Phi 0 = 0 -> 0 < rho -> 0 < alpha ->
    (forall x : X, norm x = rho -> alpha <= Phi x) -> rho < norm e -> Phi e <= 0 ->
    alpha <= MountainPassLevel Phi e

/-- The analytic package: minimax plus Palais-Smale compactness produces a
critical point at the exact minimax value. -/
def MountainPassCriticalPackage : Prop :=
  forall (X : Type u) [NormedAddCommGroup X] [NormedSpace Real X] [CompleteSpace X]
    (Phi : X -> Real) (rho alpha : Real) (e : X),
    ContDiff Real 1 Phi -> PalaisSmale Phi -> Phi 0 = 0 -> 0 < rho -> 0 < alpha ->
    (forall x : X, norm x = rho -> alpha <= Phi x) -> rho < norm e -> Phi e <= 0 ->
    exists x : X, fderiv Real Phi x = 0 /\ Phi x = MountainPassLevel Phi e

/-- Kernel-checked composition of the geometric and analytic packages into the
exact canonical target. No package implementation is asserted here. -/
theorem root_of_barrier_and_critical_packages
    (barrier : MountainPassBarrierPackage.{u})
    (critical : MountainPassCriticalPackage.{u}) :
    MountainPassTarget.{u} := by
  intro X _group _space _complete Phi rho alpha e hC1 hPS hzero hrho halpha hsphere he hout
  obtain ⟨x, hxcrit, hxvalue⟩ :=
    critical X Phi rho alpha e hC1 hPS hzero hrho halpha hsphere he hout
  exact ⟨x, hxcrit, hxvalue,
    barrier X Phi rho alpha e hC1 hzero hrho halpha hsphere he hout⟩

#print axioms root_of_barrier_and_critical_packages

end Stage1Instances.THM_M_1271
