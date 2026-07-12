import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Topology.CWComplex.Classical.Basic

/-!
# THM-M-0539 statement-gate probe

This module checks the two pinned interfaces needed by any faithful cellular
homology statement: the skeletal filtration of a CW complex and singular
chains/homology.  It deliberately does not declare a canonical target.  The
pinned library has no relative singular-homology object for consecutive
skeleta and no cellular chain complex or cellular comparison map, so writing
the comparison as a Lean proposition would require inventing that missing
construction or accepting it as an input.
-/

open CategoryTheory

#check Topology.CWComplex
#check Topology.CWComplex.cell
#check Topology.CWComplex.skeletonLT
#check AlgebraicTopology.singularChainComplexFunctor
#check AlgebraicTopology.singularHomologyFunctor
#check ChainComplex

