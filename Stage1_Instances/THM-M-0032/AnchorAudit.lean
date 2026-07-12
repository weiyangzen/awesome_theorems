import Mathlib.RingTheory.PrincipalIdealDomain
import Mathlib.RingTheory.PrincipalIdealDomainOfPrime
import Mathlib.RingTheory.RegularLocalRing.Defs
import Mathlib.RingTheory.UniqueFactorizationDomain.Kaplansky

/-!
# THM-M-0032 pinned anchor probes

This module checks the mathlib interfaces retained by the anchor audit.  They supply the regular
local-ring definition and general routes into unique factorization, but no declaration connects
those two endpoints.  In particular, the PID-to-regular instance has the reverse direction from
the frozen target.
-/

namespace Stage1Instances.THM_M_0032_AnchorAudit

universe u

/-- A literal audit-local copy of the already frozen target; this is a proposition, not a proof. -/
def ExactTarget : Prop :=
  forall (R : Type u) [CommRing R] [IsRegularLocalRing R],
    UniqueFactorizationMonoid R

#check IsRegularLocalRing
#check isRegularLocalRing_iff
#check IsRegularLocalRing.iff_finrank_cotangentSpace
#check IsRegularLocalRing.of_ringEquiv
#check UniqueFactorizationMonoid.iff_exists_prime_mem_of_isPrime
#check IsPrincipalIdealRing.of_prime_ne_bot
#check PrincipalIdealRing.to_uniqueFactorizationMonoid

section MissingBridge

variable (R : Type u) [CommRing R] [IsRegularLocalRing R]

-- The pinned environment must not silently gain the target as a typeclass instance.
#check_failure (inferInstance : UniqueFactorizationMonoid R)

end MissingBridge

set_option pp.universes true in
set_option pp.explicit true in
#print ExactTarget

end Stage1Instances.THM_M_0032_AnchorAudit
