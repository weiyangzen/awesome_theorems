import Mathlib.Topology.ContinuousMap.Weierstrass

/-!
# THM-M-0265 discovery-only intake probe

These checks authenticate direct Weierstrass approximation interfaces in the pinned mathlib
snapshot. They do not select one variant as the catalog root, establish source-statement identity,
or credit a proof body for THM-M-0265.
-/

#check polynomialFunctions_closure_eq_top'
#check polynomialFunctions_closure_eq_top
#check continuousMap_mem_polynomialFunctions_closure
#check exists_polynomial_near_continuousMap
#check exists_polynomial_near_of_continuousOn
#check bernsteinApproximation_uniform

#print axioms polynomialFunctions_closure_eq_top
#print axioms exists_polynomial_near_continuousMap
#print axioms exists_polynomial_near_of_continuousOn
