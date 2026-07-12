import Mathlib.Algebra.Module.Projective
import Mathlib.LinearAlgebra.FiniteDimensional.Defs
import Mathlib.LinearAlgebra.Finsupp.VectorSpace
import Mathlib.RingTheory.MvPolynomial.Basic

/-!
# THM-M-0034 discovery-only intake probe

These checks authenticate adjacent pinned projective-module, free-module, finite-module, and
polynomial-ring interfaces. They neither state Quillen-Suslin nor turn the easy implication from
free to projective into its converse.
-/

#check Module.Projective
#check Module.Free
#check Module.Finite
#check Module.Projective.of_free
#check Module.projective_def
#check Polynomial
#check Polynomial.toFinsuppIsoLinear
#check Polynomial.instFree
#check MvPolynomial
#check MvPolynomial.basisMonomials

#print axioms Module.Projective.of_free
