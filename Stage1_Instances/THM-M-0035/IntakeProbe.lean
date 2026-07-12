import Mathlib.RingTheory.SimpleModule.Basic

/-!
# THM-M-0035 discovery-only intake probe

These checks authenticate the pinned simple-module and Jacobson-density interfaces relevant to a
future exact statement. They neither identify the catalogue gloss with either formal candidate nor
promote a candidate proof body to the theorem root.
-/

#check IsSimpleModule
#check IsSemisimpleModule
#check Module.End
#check Module.toModuleEnd
#check jacobson_density
#check Module.Finite.toModuleEnd_moduleEnd_surjective
#check LinearIndependent
#check FaithfulSMul

#print axioms jacobson_density
#print axioms Module.Finite.toModuleEnd_moduleEnd_surjective
