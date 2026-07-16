import Mathlib.GroupTheory.Coxeter.Length
import Mathlib.LinearAlgebra.RootSystem.WeylGroup
import Mathlib.RingTheory.HahnSeries.Basic

/-!
# THM-M-0135 statement boundary probe

The repository source record names the family of Macdonald identities for affine root systems,
but it does not select one numbered identity or its conventions. This module therefore checks only
the pinned interfaces needed to encode the unresolved denominator-product candidates. It
deliberately declares no canonical target, transport, or mutation fixture.
-/

namespace Stage1Instances.THM_M_0135

#check AddMonoidAlgebra
#check HahnSeries
#check CoxeterSystem.length_mul_mod_two
#check RootPairing.weylGroup

end Stage1Instances.THM_M_0135
