import Mathlib.Algebra.Lie.Weights.RootSystem
import Mathlib.AlgebraicGeometry.Modules.Sheaf
import Mathlib.CategoryTheory.Sites.GlobalSections
import Mathlib.CategoryTheory.Sites.SheafCohomology.Basic
import Mathlib.Geometry.Manifold.Algebra.LieGroup
import Mathlib.RepresentationTheory.Irreducible

/-!
# THM-M-0094 discovery-only intake probe

These checks authenticate pinned sheaf, sheaf-cohomology, Lie-theory, and representation
interfaces adjacent to the Borel-Weil-Bott family. They do not construct a flag variety or
homogeneous line bundle, state the Borel-Weil-Bott theorem, identify a canonical source
proposition, or provide proof credit.
-/

#check CategoryTheory.Sheaf.Γ
#check CategoryTheory.Sheaf.H
#check CategoryTheory.Sheaf.cohomologyFunctor
#check AlgebraicGeometry.Scheme.Modules
#check AlgebraicGeometry.Scheme.Modules.pushforward
#check LieModule.Weight
#check LieAlgebra.IsKilling.rootSystem
#check RootPairing
#check Representation
#check Representation.IsIrreducible
#check LieGroup

#print axioms CategoryTheory.Sheaf.subsingleton_H_of_isZero
#print axioms LieAlgebra.IsKilling.rootSystem
#print axioms Representation.irreducible_iff_isSimpleModule_asModule
