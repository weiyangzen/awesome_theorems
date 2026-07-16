import Statement

/-!
# THM-M-0110 proof-phase execution

The pinned dependency closure has no premise-free Kodaira-vanishing theorem
for the exact frozen `Sheaf.H` target. This module therefore installs only the
already-frozen, kernel-checked child-to-root composition body. The two actual
root premises, native semantic transport and substantive positive-degree
vanishing, remain explicit arguments.

No declaration here claims to construct either premise or close the root.
-/

namespace Stage1Instances.THMM0110.Proof

universe u

open Stage1Instances.THMM0110

/-- Consumer-owned proof body for the registered final assembly obligation.
It consumes exactly the substantive positive-degree vanishing package and
returns the exact frozen target without adding or changing a premise. -/
theorem kodairaVanishingTarget_of_vanishing
    (vanishing : forall (k : Type u) [Field k] [CharZero k]
      (D : KodairaVanishingData.{u} k),
        D.Hypotheses -> D.VanishingConclusion) :
    KodairaVanishingTarget.{u} := by
  intro k _ _ D hD
  exact vanishing k D hD

#check kodairaVanishingTarget_of_vanishing
#print sorries kodairaVanishingTarget_of_vanishing
#print axioms kodairaVanishingTarget_of_vanishing

end Stage1Instances.THMM0110.Proof
