import Mathlib.LinearAlgebra.SymplecticGroup

/-!
Pinned-environment substrate probe for the THM-M-0611 exact-statement blocker.

This checks only mathlib's finite-dimensional matrix symplectic-group API. It does not define a
symplectic manifold, Lagrangian submanifold, Hamiltonian isotopy, pseudoholomorphic strip, Floer
complex, or Floer homology, so it is deliberately not presented as the canonical target.
-/

#check Matrix.J
#check Matrix.symplecticGroup
#check SymplecticGroup.mem_iff
#check SymplecticGroup.symplectic_det
