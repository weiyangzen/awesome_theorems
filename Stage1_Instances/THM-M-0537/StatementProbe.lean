import Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvarianceTopCat

/-!
# THM-M-0537 statement boundary probe

This file checks only the singular-homology and homotopy-invariance substrate in the pinned
environment. It deliberately does not declare an Eilenberg-Steenrod axiom package: the repository
source does not select a proposition or fix the data and conventions needed for such a package.
-/

open CategoryTheory

#check AlgebraicTopology.singularChainComplexFunctor
#check AlgebraicTopology.singularHomologyFunctor
#check TopCat.Homotopy.congr_homologyMap_singularChainComplexFunctor
