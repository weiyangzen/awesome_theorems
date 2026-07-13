import Mathlib.Analysis.SpecialFunctions.Gamma.BohrMollerup

/-!
# THM-M-0243 discovery-only intake probe

These checks authenticate the exact-topic interfaces present in the pinned mathlib revision. They
do not select a primary-source edition, freeze the canonical Lean target, audit terminal proof-body
provenance, or give the theorem any proof credit.
-/

#check Real.Gamma
#check Real.convexOn_log_Gamma
#check Real.Gamma_add_one
#check Real.Gamma_one
#check Real.Gamma_pos_of_pos
#check Real.eq_Gamma_of_log_convex

#print axioms Real.convexOn_log_Gamma
#print axioms Real.eq_Gamma_of_log_convex
