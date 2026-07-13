import Mathlib.Data.Fintype.BigOperators
import Mathlib.Data.Fintype.EquivFin
import Mathlib.Data.Matrix.Basic

/-!
# THM-M-0903 discovery-only intake probe

These checks authenticate pinned finite-matrix, finite-cardinality, bijection, and product
interfaces adjacent to a possible source-selected orthogonal-Latin-square encoding. They do not
define Latin squares or orthogonality, select one reading of Euler's conjecture, or prove the
Bose-Shrikhande-Parker target.
-/

#check Matrix
#check Fin
#check Fintype.card
#check Fintype.equivFin
#check Function.Bijective
#check Equiv.ofBijective
#check Prod
#check (Matrix (Fin 3) (Fin 3) (Fin 3))
#check (fun (A B : Matrix (Fin 3) (Fin 3) (Fin 3)) i j => (A i j, B i j))
