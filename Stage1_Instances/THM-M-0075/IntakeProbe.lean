import Mathlib.LinearAlgebra.LinearIndependent.Basic
import Mathlib.RepresentationTheory.Character
import Mathlib.RepresentationTheory.Induced

/-!
# THM-M-0075 discovery-only intake probe

These checks authenticate pinned character, representation-induction, adjunction, and Dedekind
character-independence APIs. They do not select a canonical target or prove Artin induction or any
linear-independence theorem for induced representation characters.
-/

#check FDRep.character
#check FDRep.char_conj
#check FDRep.char_orthonormal
#check Representation.ind
#check Rep.indFunctor
#check Rep.indResHomEquiv
#check Rep.indResAdjunction
#check linearIndependent_monoidHom
