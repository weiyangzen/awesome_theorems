import Mathlib.RingTheory.HopfAlgebra.Basic
import Mathlib.LinearAlgebra.Basis.Defs
import Mathlib.LinearAlgebra.RootSystem.CartanMatrix

/-!
Pinned interface probe for the blocked THM-M-0141 statement phase.

The repository source does not identify one exact Lusztig theorem or freeze the
quantum-group, coefficient, integral-form, bar, PBW, and basis conventions. This
file therefore declares no canonical target. It only verifies that the narrow
mathlib substrate named by the blocker is present in the pinned environment.
-/

#check HopfAlgebra.antipode
#check Module.Basis
#check RootPairing
#check RootPairing.Base.cartanMatrix
