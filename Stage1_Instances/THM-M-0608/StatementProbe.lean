import Mathlib.LinearAlgebra.CliffordAlgebra.SpinGroup

/-!
Pinned-environment substrate probe for the THM-M-0608 exact-statement blocker.

This checks only mathlib's algebraic spin-group API. It does not define a Spin-c structure on a
smooth four-manifold, the Seiberg-Witten equations or moduli space, or a four-manifold invariant,
so it is deliberately not presented as the canonical target.
-/

#check lipschitzGroup
#check pinGroup
#check spinGroup
#check spinGroup.toUnits
