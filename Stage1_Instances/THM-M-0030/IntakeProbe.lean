import Mathlib.RingTheory.Filtration

/-!
# THM-M-0030 discovery-only intake probe

These checks authenticate pinned local/Noetherian ring interfaces and the ideal and finite-module
Krull intersection candidates. They do not freeze the canonical Lean target, audit proof-body
provenance, or grant statement or proof credit.
-/

#check IsNoetherianRing
#check IsLocalRing
#check Ideal
#check Ideal.iInf_pow_eq_bot_of_isLocalRing
#check @Ideal.iInf_pow_eq_bot_of_isLocalRing
#check Ideal.iInf_pow_smul_eq_bot_of_isLocalRing
#check @Ideal.iInf_pow_smul_eq_bot_of_isLocalRing
#check Ideal.iInf_pow_smul_eq_bot_of_le_jacobson
#check Ideal.iInf_pow_eq_bot_of_isDomain
#print axioms Ideal.iInf_pow_eq_bot_of_isLocalRing
