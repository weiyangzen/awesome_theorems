import Mathlib.RingTheory.SimpleModule.WedderburnArtin
import Mathlib.RingTheory.SimpleRing.Field
import Mathlib.Algebra.FreeAlgebra

/-!
# THM-M-0039 discovery-only intake probe

These checks authenticate pinned interfaces adjacent to a possible formalization of Kaplansky's
primitive-PI-algebra theorem. They neither select that theorem as the catalogue root nor supply a
polynomial-identity predicate, target declaration, or proof body.
-/

#check FreeAlgebra
#check FreeAlgebra.ι
#check FreeAlgebra.lift
#check IsSimpleModule
#check FaithfulSMul
#check jacobson_density
#check IsSimpleRing
#check IsSimpleRing.isField_center
#check Module.Finite
#check IsSimpleRing.exists_algEquiv_matrix_divisionRing_finite

#print axioms jacobson_density
#print axioms IsSimpleRing.exists_algEquiv_matrix_divisionRing_finite
