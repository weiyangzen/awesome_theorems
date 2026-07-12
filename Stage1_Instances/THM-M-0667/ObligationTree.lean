import Statement

/-!
# THM-M-0667 conditional obligation composition

This module checks the reduction from the domination package to the exact
canonical target. The domination package remains an explicit hypothesis, so
this architecture module does not claim the root proof.
-/

namespace Stage1Instances.THM_M_0667

open Nat

/-- The substantive package proved by structural induction over the unary
primitive-recursive function constructors. -/
def DominationPackage : Prop :=
  forall (f : Nat -> Nat), Nat.Primrec f ->
    exists m, forall n, f n < ack m n

/-- Checked child-to-parent composition: binary primitive recursiveness gives
primitive recursiveness of the diagonal, which contradicts domination at its
own witnessing level. -/
theorem root_of_domination (dominate : DominationPackage) :
    AckermannNondefinabilityTarget := by
  intro hbinary
  have hdiag : Primrec (fun n : Nat => ack n n) :=
    hbinary.comp Primrec.id Primrec.id
  have hdiagNat : Nat.Primrec (fun n : Nat => ack n n) :=
    Primrec.nat_iff.mp hdiag
  obtain ⟨m, hm⟩ := dominate _ hdiagNat
  exact (hm m).false

#print axioms root_of_domination

end Stage1Instances.THM_M_0667
