import Mathlib.Computability.MyhillNerode

/-!
Pinned-environment discovery probe for the THM-M-0760 intake.

These checks authenticate a strong Myhill-Nerode candidate and its immediate interfaces. This file
does not select the canonical source variant, serialize an expression fingerprint, check a
quotient/range transport or mutations, audit terminal proof provenance, or assign proof credit.
-/

#check Language
#check DFA
#check Language.IsRegular
#check Language.leftQuotient
#check Language.mem_leftQuotient
#check Language.IsRegular.finite_range_leftQuotient
#check Language.toDFA
#check Language.accepts_toDFA
#check Language.IsRegular.of_finite_range_leftQuotient
#check Language.isRegular_iff_finite_range_leftQuotient

#print axioms Language.isRegular_iff_finite_range_leftQuotient
