import Mathlib.RingTheory.Polynomial.Basic

/-!
# THM-M-0025 discovery-only intake probe

These checks authenticate the pinned Noetherian-ring definitions and the exact formal candidate
adjacent to the catalog claim. They do not freeze the canonical Lean target, inspect a proof body,
perform the later anchor audit, or grant proof credit.
-/

#check IsNoetherian
#check IsNoetherianRing
#check isNoetherianRing_iff_ideal_fg
#check Polynomial
#check Polynomial.isNoetherianRing
#check @Polynomial.isNoetherianRing
#check MvPolynomial.isNoetherianRing
#print axioms Polynomial.isNoetherianRing
