import Proof
import Mathlib.Util.AssertNoSorry
import Mathlib.Util.PrintSorries

/-!
# THM-M-1246 kernel-facing proof audit

This module asks Lean itself to traverse the exact statement transport,
composition boundary, analytic terminal, and public root for `sorryAx`. It also
prints their complete axiom closures for the validation runner.
-/

open Stage1Instances.THM_M_1246
open Stage1Instances.THM_M_1246.ObligationTree
open Stage1Instances.THM_M_1246.Proof

assert_no_sorry hardyInequalityTarget_iff_expanded
assert_no_sorry root_of_hardyTerminal
assert_no_sorry hardyTerminal
assert_no_sorry hardyInequality

#print sorries hardyInequalityTarget_iff_expanded
#print sorries root_of_hardyTerminal
#print sorries hardyTerminal
#print sorries hardyInequality

#print axioms hardyInequalityTarget_iff_expanded
#print axioms root_of_hardyTerminal
#print axioms hardyTerminal
#print axioms hardyInequality
