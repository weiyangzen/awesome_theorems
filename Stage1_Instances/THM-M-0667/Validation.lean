import Statement

/-!
# THM-M-0667 differential validation probe

This module deliberately imports neither `Proof` nor `ObligationTree`. It
reconstructs the exact frozen root from the pinned domination theorem and the
primitive-recursive encoding bridges rather than invoking the root theorem
used by the proof-phase wrapper.
-/

namespace Stage1Instances.THM_M_0667.Validation

open Nat

/-- A separately written route from the pinned domination theorem to the exact
binary Ackermann non-definability target. -/
theorem independentlyReconstructedRoot : AckermannNondefinabilityTarget := by
  intro hbinary
  have hdiag : Primrec (fun n : Nat => ack n n) :=
    hbinary.comp Primrec.id Primrec.id
  have hdiagNat : Nat.Primrec (fun n : Nat => ack n n) :=
    Primrec.nat_iff.mp hdiag
  obtain ⟨m, hm⟩ := exists_lt_ack_of_nat_primrec hdiagNat
  exact (hm m).false

#check independentlyReconstructedRoot
#print axioms independentlyReconstructedRoot
#print axioms exists_lt_ack_of_nat_primrec

end Stage1Instances.THM_M_0667.Validation
