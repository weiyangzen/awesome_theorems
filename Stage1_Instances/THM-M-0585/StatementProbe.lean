import Mathlib.LinearAlgebra.CliffordAlgebra.SpinGroup

/-!
Pinned-environment substrate probe for the THM-M-0585 statement gate.

This module checks only mathlib's algebraic spin-group API. It does not define a Spin-c structure,
a four-manifold gauge configuration, a Dirac operator, the Seiberg-Witten equations, a moduli
space, or an invariant, and therefore is not a candidate statement of Seiberg-Witten theory.
-/

#check lipschitzGroup
#check pinGroup
#check spinGroup
#check spinGroup.toUnits
