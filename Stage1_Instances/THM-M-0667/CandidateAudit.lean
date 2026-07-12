import Mathlib.Computability.Ackermann

/-!
# THM-M-0667 anchor audit

This file checks the type and foundation surface of the pinned mathlib
candidate. It deliberately creates no repo-local wrapper theorem: proof
integration belongs to the later proof phase.
-/

#check (not_primrec₂_ack : ¬Primrec₂ ack)
#check exists_lt_ack_of_nat_primrec
#check not_nat_primrec_ack_self
#check not_primrec_ack_self
#print axioms not_primrec₂_ack
#print not_primrec₂_ack
