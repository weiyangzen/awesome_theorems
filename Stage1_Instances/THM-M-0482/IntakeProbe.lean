import Mathlib.NumberTheory.Chebyshev

/-!
Discovery-only checks for pinned Chebyshev-function and prime-counting interfaces adjacent to the
catalog target. No declaration below selects or proves a source-identical two-sided estimate.
-/

#check Nat.primeCounting
#check Chebyshev.theta
#check Chebyshev.psi
#check Chebyshev.theta_le_log4_mul_x
#check Chebyshev.psi_le
#check Chebyshev.psi_le_const_mul_self
#check Chebyshev.primeCounting_eq_theta_div_log_add_integral
#check Chebyshev.eventually_primeCounting_le

#print axioms Chebyshev.theta_le_log4_mul_x
#print axioms Chebyshev.psi_le_const_mul_self
#print axioms Chebyshev.eventually_primeCounting_le
