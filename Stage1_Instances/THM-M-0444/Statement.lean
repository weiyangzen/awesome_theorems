import Mathlib.FieldTheory.AbsoluteGaloisGroup
import Mathlib.RingTheory.DedekindDomain.SelmerGroup

/-!
# THM-M-0444 statement boundary probe

The repository source record says only "Kolyvagin Euler system" and "construction of an Euler
system". It does not select a source theorem or fix the arithmetic data and normalization needed
to determine one Lean proposition. This module therefore checks only two pinned interfaces adjacent
to the unresolved statement. It deliberately declares no canonical target, transport, or mutation
fixture.
-/

namespace Stage1Instances.THM_M_0444

#check Field.absoluteGaloisGroup
#check IsDedekindDomain.selmerGroup

end Stage1Instances.THM_M_0444
