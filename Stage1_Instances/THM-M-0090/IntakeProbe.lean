import Mathlib.Algebra.Lie.Weights.RootSystem
import Mathlib.LinearAlgebra.RootSystem.WeylGroup
import Mathlib.RepresentationTheory.Character

/-!
Pinned discovery-only API probe for `THM-M-0090`.

These declarations expose representation characters, Lie-module weights, a Lie-algebra root
system, and Weyl groups. Their coexistence does not state or prove the Weyl character formula.
-/

#check FDRep.character
#check Representation.character
#check LieModule.weightSpace
#check LieModule.Weight
#check LieAlgebra.IsKilling.rootSystem
#check RootPairing.weylGroup
#check RootPairing.weylGroupToPerm
#check RootPairing.weylGroupRootRep
#check RootPairing.weylGroupCorootRep
