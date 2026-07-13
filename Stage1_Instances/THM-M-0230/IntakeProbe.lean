import Mathlib.Analysis.Analytic.IsolatedZeros
import Mathlib.Analysis.Analytic.Order
import Mathlib.Analysis.Complex.CanonicalDecomposition
import Mathlib.Analysis.Complex.LocallyUniformLimit
import Mathlib.Analysis.Normed.Module.MultipliableUniformlyOn
import Mathlib.Analysis.SpecialFunctions.Trigonometric.EulerSineProd

/-!
# THM-M-0230 discovery-only intake probe

These checks authenticate pinned APIs for zero orders, isolated zeros, locally uniform products,
finite-support zero/pole extraction, disk factors, and Euler's sine product. They do not define a
Weierstrass primary factor, select the catalog's exact statement, or prove THM-M-0230.
-/

#check analyticOrderAt
#check AnalyticAt.eventually_eq_zero_or_eventually_ne_zero
#check Summable.hasProdLocallyUniformlyOn_nat_one_add
#check TendstoLocallyUniformlyOn.differentiableOn
#check MeromorphicOn.extract_zeros_poles
#check Complex.canonicalFactor
#check Complex.tendsto_euler_sin_prod
#check HasProd
#check tprod

#print axioms MeromorphicOn.extract_zeros_poles
#print axioms Complex.tendsto_euler_sin_prod
