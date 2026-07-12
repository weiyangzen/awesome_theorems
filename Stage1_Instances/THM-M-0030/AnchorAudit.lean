import Mathlib.RingTheory.Filtration

/-!
# THM-M-0030 immutable mathlib anchor audit

This module copies the frozen proper-ideal target literally and checks it against the theorem at
the repository's pinned mathlib revision. It is anchor-audit evidence only; acceptance and the
proof, validation, and release phases remain downstream.
-/

namespace Stage1Instances.THM_M_0030_AnchorAudit

universe u

/-- A literal copy of the statement-phase proposition. -/
def ExactTarget : Prop :=
  forall {R : Type u} [CommRing R] [IsNoetherianRing R] [IsLocalRing R]
    (I : Ideal R), I ≠ ⊤ -> (iInf fun n : Nat => I ^ n) = ⊥

/-- Exact audit wrapper over the pinned mathlib terminal theorem. -/
theorem exactTarget_mathlib_candidate : ExactTarget.{u} := by
  intro R _ _ _ I hI
  exact Ideal.iInf_pow_eq_bot_of_isLocalRing I hI

#check Ideal.iInf_pow_eq_bot_of_isLocalRing
#check @Ideal.iInf_pow_eq_bot_of_isLocalRing
#check Ideal.iInf_pow_smul_eq_bot_of_isLocalRing
#check Ideal.iInf_pow_smul_eq_bot_of_le_jacobson
#print Ideal.iInf_pow_eq_bot_of_isLocalRing
#print sorries Ideal.iInf_pow_eq_bot_of_isLocalRing
#print sorries Ideal.iInf_pow_smul_eq_bot_of_isLocalRing
#print sorries Ideal.iInf_pow_smul_eq_bot_of_le_jacobson
#print axioms Ideal.iInf_pow_eq_bot_of_isLocalRing
#print axioms Ideal.iInf_pow_smul_eq_bot_of_isLocalRing
#print axioms Ideal.iInf_pow_smul_eq_bot_of_le_jacobson
#print axioms exactTarget_mathlib_candidate

set_option pp.all true in
#print ExactTarget

end Stage1Instances.THM_M_0030_AnchorAudit
