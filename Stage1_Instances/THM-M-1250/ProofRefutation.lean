import Statement
import ProofBlocker
import Counterexample

/-!
# THM-M-1250: proof-phase impossibility certificate

The exact frozen characterization is refuted by a compactly supported smooth
Schwartz map that is not analytic. This file connects that countertheorem to
the forward package required by the frozen obligation tree. It does not prove
the positive Schwartz-space characterization.
-/

/-- Local exact spelling of the forward package frozen in the obligation tree. -/
def Stage1Instances.THM_M_1250.RefutedForwardPackage : Prop :=
  forall (n : Nat) (f : Stage1Instances.THM_M_1250.EuclideanDomain n -> Complex)
    (phi : SchwartzMap (Stage1Instances.THM_M_1250.EuclideanDomain n) Complex),
    (phi : Stage1Instances.THM_M_1250.EuclideanDomain n -> Complex) = f ->
      Stage1Instances.THM_M_1250.IsSchwartzFunction f

/-- The forward package required by the frozen positive proof route cannot
exist. -/
theorem Stage1Instances.THM_M_1250.not_refutedForwardPackage :
    Not Stage1Instances.THM_M_1250.RefutedForwardPackage := by
  intro forward
  exact Stage1Instances.THM_M_1250.Counterexample.not_schwartzSpaceCharacterization
    (by
      intro n f
      constructor
      · rintro ⟨phi, hphi⟩
        exact forward n f phi hphi
      · exact Stage1Instances.THM_M_1250.reversePackage_from_frozen_conditions n f)

#check Stage1Instances.THM_M_1250.not_refutedForwardPackage
#print axioms Stage1Instances.THM_M_1250.not_refutedForwardPackage
