import Mathlib.Algebra.MonoidAlgebra.Basic
import Mathlib.Algebra.Lie.Character
import Mathlib.Algebra.Lie.Loop
import Mathlib.Algebra.Lie.Weights.Basic
import Mathlib.LinearAlgebra.RootSystem.WeylGroup
import Mathlib.RingTheory.HahnSeries.Basic

/-!
# THM-M-0137 statement boundary probe

The repository source record says only "Kac-Peterson character formula" and "characters of
affine Lie algebras". It does not select an exact mathematical proposition. This module therefore
checks only the pinned interfaces common to the unresolved candidate interpretations. It
deliberately declares no canonical target, transport, or mutation fixture.
-/

namespace Stage1Instances.THM_M_0137

#check AddMonoidAlgebra
#check HahnSeries
#check LieAlgebra.loopAlgebra
#check LieAlgebra.LieCharacter
#check LieModule.weightSpace
#check RootPairing.weylGroup

end Stage1Instances.THM_M_0137
