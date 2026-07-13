import Mathlib.MeasureTheory.Group.ModularCharacter
import Mathlib.RepresentationTheory.Character

/-!
# THM-M-0076 discovery-only intake probe

These checks authenticate the pinned ordinary representation-character API and show that mathlib's
similarly named modular-character API belongs to Haar measure on locally compact groups. They do
not define a Brauer character, select a proposition from the catalog's vague gloss, declare a root
target, or claim proof credit.
-/

#check Representation
#check Representation.character
#check Representation.char_one
#check Representation.char_conj
#check MeasureTheory.Measure.modularCharacterFun
#check MeasureTheory.Measure.modularCharacter
#check MeasureTheory.Measure.modularCharacterFun_map_mul

#print axioms Representation.char_one
#print axioms Representation.char_conj
#print axioms MeasureTheory.Measure.modularCharacterFun_map_mul

section OrdinaryCharacterBoundary

variable {G k V : Type*} [Group G] [Field k] [AddCommGroup V] [Module k V]
  [FiniteDimensional k V]

example (rho : Representation k G V) : rho.character 1 = Module.finrank k V :=
  rho.char_one

example (rho : Representation k G V) (g h : G) :
    rho.character (h * g * h⁻¹) = rho.character g :=
  rho.char_conj g h

end OrdinaryCharacterBoundary
