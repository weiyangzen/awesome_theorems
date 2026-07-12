import Mathlib.Algebra.Module.Projective
import Mathlib.RingTheory.MvPolynomial.Basic

/-!
# THM-M-0033 discovery-only intake probe

These checks authenticate the pinned projective/free-module and polynomial-ring interfaces that a
future exact statement may use. They do not state Serre's conjecture, identify a source-faithful
encoding, or provide proof credit for the missing projective-to-free implication.
-/

#check Module.Projective
#check Module.projective_def
#check Module.Free
#check Module.Finite
#check Module.finite_def
#check Module.Projective.of_free
#check MvPolynomial
