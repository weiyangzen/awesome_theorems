import Mathlib.Algebra.Lie.CartanExists
import Mathlib.Algebra.Lie.Classical
import Mathlib.Algebra.Lie.Semisimple.Basic
import Mathlib.Algebra.Lie.Weights.RootSystem
import Mathlib.Data.Matrix.Cartan

/-!
# THM-M-0092 discovery-only intake probe

These checks authenticate adjacent pinned semisimple-Lie-algebra, Cartan-subalgebra, root-system,
classical-algebra, Cartan-matrix, and representation APIs. They do not select a canonical meaning
of the catalog label or prove a classification or representation theorem.
-/

#check LieAlgebra.IsSemisimple
#check LieAlgebra.IsSemisimple.isSimple_of_isAtom
#check LieAlgebra.IsSemisimple.instHasTrivialRadical
#check LieAlgebra.exists_isCartanSubalgebra_engel
#check LieAlgebra.IsKilling.rootSystem
#check LieAlgebra.SpecialLinear.sl
#check CartanMatrix.A
#check CartanMatrix.E₈
#check LieModule.IsIrreducible
