import Mathlib.Algebra.Lie.Basis
import Mathlib.Algebra.Lie.SerreConstruction
import Mathlib.LinearAlgebra.RootSystem.GeckConstruction.Basis

/-!
# THM-M-0096 discovery-only intake probe

These checks authenticate adjacent pinned Cartan, root-system, Serre-construction, and Lie-algebra
basis APIs. They do not define a Chevalley basis, select an integral-basis theorem, construct a
Chevalley basis for an arbitrary semisimple Lie algebra, or prove THM-M-0096.
-/

#check LieAlgebra.Basis
#check LieAlgebra.Basis.cartanMatrix_base_eq
#check RootPairing.IsCrystallographic
#check RootPairing.GeckConstruction.lieAlgebra
#check RootPairing.GeckConstruction.isSl2Triple
#check RootPairing.GeckConstruction.basis
#check RootPairing.GeckConstruction.equivRootSystem
#check Matrix.ToLieAlgebra
#check CartanMatrix.Relations.toIdeal
