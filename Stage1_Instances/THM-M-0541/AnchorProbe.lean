import Mathlib.AlgebraicTopology.AlternatingFaceMapComplex
import Mathlib.AlgebraicTopology.SimplicialComplex.Basic
import Mathlib.Algebra.Homology.ShortComplex.HomologicalComplex

/-!
Pinned-candidate probe for `S56-M-0541-ANCHOR_AUDIT`.

These checks establish that the adjacent mathlib declarations elaborate in the pinned
environment. They deliberately do not claim that a simplicial object has been constructed from an
`AbstractSimplicialComplex`, or that any declaration has the exact dossier target type.
-/

#check AbstractSimplicialComplex
#check AlgebraicTopology.AlternatingFaceMapComplex.objD
#check AlgebraicTopology.AlternatingFaceMapComplex.d_squared
#check AlgebraicTopology.AlternatingFaceMapComplex.obj
#check AlgebraicTopology.alternatingFaceMapComplex
#check HomologicalComplex.homologyFunctor

#print axioms AlgebraicTopology.AlternatingFaceMapComplex.d_squared
#print axioms AlgebraicTopology.AlternatingFaceMapComplex.obj
#print axioms AlgebraicTopology.alternatingFaceMapComplex
