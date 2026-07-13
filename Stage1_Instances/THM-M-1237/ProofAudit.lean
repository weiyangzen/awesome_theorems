import «Proof»
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-! Kernel-facing placeholder and axiom probes for the proof-phase declarations. -/

open Stage1Rev56.THMM1237
open Stage1Rev56.THMM1237.ObligationTree
open Stage1Rev56.THMM1237.Proof

assert_no_sorry statement_iff_expanded
assert_no_sorry root_compose
assert_no_sorry representativeFamily
assert_no_sorry not_valueEstimateFamily

#print sorries statement_iff_expanded
#print sorries root_compose
#print sorries representativeFamily
#print sorries not_valueEstimateFamily

#print axioms statement_iff_expanded
#print axioms root_compose
#print axioms representativeFamily
#print axioms not_valueEstimateFamily
