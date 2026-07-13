import Mathlib.Analysis.SpecialFunctions.Elliptic.Weierstrass

/-!
# THM-M-0238 discovery-only intake probe

These checks authenticate pinned output-side Weierstrass infrastructure adjacent to
elliptic-integral inversion. They neither define a selected elliptic integral nor state that the
checked function is its inverse.
-/

#check PeriodPair
#check PeriodPair.weierstrassP
#check PeriodPair.deriv_weierstrassP
#check PeriodPair.weierstrassP_add_coe
#check PeriodPair.periodic_weierstrassP
#check PeriodPair.meromorphic_weierstrassP
#check PeriodPair.order_weierstrassP
#check PeriodPair.derivWeierstrassP_sq

#print axioms PeriodPair.deriv_weierstrassP
#print axioms PeriodPair.periodic_weierstrassP
#print axioms PeriodPair.meromorphic_weierstrassP
#print axioms PeriodPair.derivWeierstrassP_sq
