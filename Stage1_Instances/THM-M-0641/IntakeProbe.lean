import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Dynamics.FixedPoints.Basic
import Mathlib.LinearAlgebra.Trace

/-!
Discovery-only checks for APIs adjacent to the ambiguous THM-M-0641 catalog wording.

These declarations expose singular homology, linear trace, and fixed-point vocabulary. They do not
define a Lefschetz number, select a class of spaces, state the Lefschetz fixed-point theorem, or
supply source-fidelity or proof credit.
-/

#check AlgebraicTopology.singularChainComplexFunctor
#check AlgebraicTopology.singularHomologyFunctor
#check TopCat.toSSet
#check LinearMap.trace
#check Function.IsFixedPt
#check Function.fixedPoints
