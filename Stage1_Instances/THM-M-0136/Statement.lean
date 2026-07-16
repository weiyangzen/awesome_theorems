import Mathlib.Algebra.Lie.SerreConstruction

/-!
# THM-M-0136 statement boundary probe

The repository record names Kac-Moody algebras and gives only the broad gloss
"classification of infinite-dimensional Lie algebras". It does not select one
mathematical proposition. This module therefore checks only mathlib's pinned
Serre-construction interface, which is common to several unresolved readings.

It deliberately declares no canonical target, alternate transport, or mutation
fixture. In particular, it does not promote the explicitly provisional legacy
matrix-recovery candidate into the requested theorem.
-/

namespace Stage1Instances.THM_M_0136

#check Matrix.ToLieAlgebra
#check CartanMatrix.Generators
#check CartanMatrix.Relations.toIdeal

end Stage1Instances.THM_M_0136
