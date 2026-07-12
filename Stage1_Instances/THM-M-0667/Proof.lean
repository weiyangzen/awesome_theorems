import Statement

/-!
# THM-M-0667 proof-phase closure

The exact root is discharged by the theorem already present in the pinned
`Mathlib.Computability.Ackermann` dependency. The local wrapper fixes the
repository target and makes the upstream proof boundary explicit.
-/

namespace Stage1Instances.THM_M_0667

open Nat

/-- The standard two-variable Ackermann-Peter function is not primitive
recursive, via the exact theorem in the pinned mathlib revision. -/
theorem ackermannNondefinability : AckermannNondefinabilityTarget := by
  exact not_primrec₂_ack

#check ackermannNondefinability
#print axioms ackermannNondefinability

end Stage1Instances.THM_M_0667
