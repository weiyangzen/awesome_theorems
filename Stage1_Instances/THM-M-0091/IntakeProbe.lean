import Mathlib.Algebra.Lie.Weights.RootSystem
import Mathlib.Geometry.Manifold.Algebra.LieGroup
import Mathlib.LinearAlgebra.RootSystem.Base
import Mathlib.RepresentationTheory.Character

/-!
# THM-M-0091 discovery-only intake probe

These checks authenticate pinned root, Lie-weight, representation, character-at-identity, and
Lie-group interfaces. They do not state the Weyl dimension product, connect irreducible compact
group representations to highest weights, establish source fidelity, or claim proof credit.
-/

#check RootPairing
#check RootPairing.Base
#check RootPairing.Base.IsPos
#check RootPairing.Base.isPos_of_mem_support
#check LieModule.Weight
#check LieAlgebra.IsKilling.rootSystem
#check LieAlgebra.IsKilling.apply_coroot_eq_cast
#check Representation
#check FDRep
#check FDRep.char_one
#check Representation.char_one
#check LieGroup

#print axioms RootPairing.Base.isPos_of_mem_support
#print axioms LieAlgebra.IsKilling.rootSystem
#print axioms LieAlgebra.IsKilling.apply_coroot_eq_cast
#print axioms FDRep.char_one
#print axioms Representation.char_one
