import Mathlib.RepresentationTheory.Maschke

/-!
# THM-M-0067 discovery-only intake probe

These checks authenticate pinned Maschke and semisimple-representation interfaces. They do not
choose an exact meaning of the catalog's phrase "completely reducible", define a canonical target,
establish a source transport, or claim proof credit for the theorem root.
-/

#check Representation
#check Representation.IsSemisimpleRepresentation
#check Representation.isSemisimpleRepresentation_iff_isSemisimpleModule_asModule
#check LinearMap.equivariantProjection_condition
#check MonoidAlgebra.exists_leftInverse_of_injective
#check MonoidAlgebra.Submodule.exists_isCompl

section

open scoped MonoidAlgebra

variable {k G V : Type*} [Group G] [Field k] [Finite G]
  [NeZero (Nat.card G : k)] [AddCommGroup V] [Module k V]
variable (rho : Representation k G V)

#synth Representation.IsSemisimpleRepresentation rho

end


#print axioms LinearMap.equivariantProjection_condition
#print axioms MonoidAlgebra.exists_leftInverse_of_injective
#print axioms MonoidAlgebra.Submodule.exists_isCompl
#print axioms MonoidAlgebra.Submodule.instIsSemisimpleRepresentation
#print axioms Representation.isSemisimpleRepresentation_iff_isSemisimpleModule_asModule
