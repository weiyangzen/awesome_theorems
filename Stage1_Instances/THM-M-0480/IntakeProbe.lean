import Mathlib.NumberTheory.Chebyshev

/-!
# THM-M-0480 discovery-only intake probe

These checks authenticate pinned prime-counting, asymptotic-equivalence, and Chebyshev interfaces
adjacent to the catalog claim. They do not select a canonical prime number theorem statement,
declare that theorem, inspect a terminal proof body, or supply proof credit.
-/

#check Nat.primeCounting
#check Nat.tendsto_primeCounting
#check Asymptotics.IsEquivalent
#check Asymptotics.isEquivalent_iff_tendsto_one
#check Real.log
#check Filter.atTop
#check Chebyshev.theta
#check Chebyshev.psi
#check Chebyshev.primeCounting_eq_theta_div_log_add_integral
#check Chebyshev.integral_theta_div_log_sq_isLittleO
#check Chebyshev.primeCounting_sub_theta_div_log_isBigO
#check Chebyshev.eventually_primeCounting_le

#print axioms Chebyshev.primeCounting_eq_theta_div_log_add_integral
#print axioms Chebyshev.integral_theta_div_log_sq_isLittleO
#print axioms Chebyshev.eventually_primeCounting_le
