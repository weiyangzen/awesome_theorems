import Mathlib.Algebra.Homology.SpectralSequence.Basic
import Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvarianceTopCat
import Mathlib.Topology.CWComplex.Classical.Finite

/-!
# THM-M-0554 anchor audit

This file checks the principal substrate found by the bounded anchor search.
None of these declarations constructs the Atiyah-Hirzebruch spectral sequence.
-/

open CategoryTheory AlgebraicTopology
open Topology

#check CategoryTheory.SpectralSequence
#check CategoryTheory.E₂CohomologicalSpectralSequence
#check CategoryTheory.SpectralSequence.pageFunctor
#check CWComplex
#check RelCWComplex.skeleton
#check RelCWComplex.skeleton_mono
#check RelCWComplex.Finite
#check AlgebraicTopology.singularChainComplexFunctor
#check AlgebraicTopology.singularHomologyFunctor
#check TopCat.Homotopy.congr_homologyMap_singularChainComplexFunctor
