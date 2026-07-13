import Mathlib.Analysis.InnerProductSpace.LaxMilgram
import Mathlib.Analysis.InnerProductSpace.Projection.Basic
import Mathlib.RingTheory.Polynomial.Basic

/-!
# THM-M-1468 discovery-only intake probe

These checks authenticate pinned coercive-form, best-approximation, and polynomial-degree
interfaces adjacent to a possible future hp finite-element statement. They do not define a mesh,
an h-refinement relation, an hp finite-element space, or a convergence theorem, and they do not
prove THM-M-1468.
-/

#check IsCoercive.continuousLinearEquivOfBilin
#check IsCoercive.continuousLinearEquivOfBilin_apply
#check IsCoercive.unique_continuousLinearEquivOfBilin
#check Submodule.orthogonalProjection
#check Submodule.starProjection_minimal
#check Polynomial.degreeLE
#check Polynomial.degreeLT
#check Polynomial.mem_degreeLE
#check Polynomial.degreeLE_mono
#check Polynomial.degreeLT_mono
#check Polynomial.degreeLT_succ_eq_degreeLE

#print axioms IsCoercive.unique_continuousLinearEquivOfBilin
#print axioms Submodule.starProjection_minimal
#print axioms Polynomial.degreeLT_succ_eq_degreeLE
