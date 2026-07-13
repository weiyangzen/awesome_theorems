import Mathlib.Analysis.Asymptotics.Lemmas
import Mathlib.Analysis.InnerProductSpace.LaxMilgram
import Mathlib.Analysis.InnerProductSpace.Projection.Basic

/-!
# THM-M-1471 discovery-only intake probe

These checks authenticate pinned asymptotic-order, coercive variational, and best-approximation
interfaces adjacent to possible a priori error estimates. They do not select a numerical problem,
discretization, error norm, convergence rate, or canonical theorem, and grant no proof credit.
-/

#check Asymptotics.IsBigO
#check Asymptotics.isBigO_iff
#check Asymptotics.IsBigO.trans_tendsto
#check IsCoercive
#check IsCoercive.continuousLinearEquivOfBilin
#check IsCoercive.unique_continuousLinearEquivOfBilin
#check Submodule.starProjection_minimal

#print axioms Asymptotics.isBigO_iff
#print axioms IsCoercive.unique_continuousLinearEquivOfBilin
#print axioms Submodule.starProjection_minimal
