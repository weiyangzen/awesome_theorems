import Mathlib.Dynamics.Newton

/-!
# THM-M-1440 discovery-only intake probe

These checks authenticate pinned polynomial Newton-map, root/fixed-point, and nilpotent interfaces.
They do not select a canonical analytic convergence proposition or prove THM-M-1440.
-/

#check Polynomial.newtonMap
#check Polynomial.newtonMap_apply
#check Polynomial.newtonMap_apply_of_isUnit
#check Polynomial.newtonMap_apply_of_not_isUnit
#check Polynomial.isFixedPt_newtonMap_of_aeval_eq_zero
#check Polynomial.isFixedPt_newtonMap_of_isUnit_iff
#check Polynomial.isNilpotent_iterate_newtonMap_sub_of_isNilpotent
#check Polynomial.aeval_pow_two_pow_dvd_aeval_iterate_newtonMap
#check Polynomial.existsUnique_nilpotent_sub_and_aeval_eq_zero
