import Mathlib.Algebra.Category.ModuleCat.Monoidal.Basic
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Category.ModuleCat.Colimits
import Mathlib.Algebra.Category.ModuleCat.Projective
import Mathlib.Algebra.Homology.ShortComplex.ShortExact
import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.CategoryTheory.Monoidal.Tor
import Mathlib.RingTheory.PrincipalIdealDomain

/-!
# Kernel-visible support-anchor probe for THM-M-0005

This probe checks only the declarations that the anchor audit found in pinned mathlib. None of
them states the Kunneth formula or the Eilenberg-Zilber comparison.
-/

#check AlgebraicTopology.singularChainComplexFunctor
#check AlgebraicTopology.singularHomologyFunctor
#check CategoryTheory.Tor
#check CategoryTheory.isZero_Tor_succ_of_projective
#check CategoryTheory.ShortComplex.ShortExact
#check CategoryTheory.ShortComplex.ShortExact.map
#check CategoryTheory.ShortComplex.ShortExact.splittingOfProjective

#print axioms AlgebraicTopology.singularHomologyFunctor
#print axioms CategoryTheory.Tor
#print axioms CategoryTheory.isZero_Tor_succ_of_projective
#print axioms CategoryTheory.ShortComplex.ShortExact.map
