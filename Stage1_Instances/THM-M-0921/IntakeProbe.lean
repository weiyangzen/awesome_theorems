import Mathlib.Combinatorics.Enumerative.DyckWord
import Mathlib.RingTheory.PowerSeries.Catalan

/-!
# THM-M-0921 discovery-only intake probe

These checks authenticate pinned Catalan sequence, formula, generating-series, tree-counting, and
Dyck-word-counting interfaces. They do not select one as the catalog root, define the catalog's
phrase "many combinatorial problems," or prove a new theorem.
-/

#check catalan
#check catalan_zero
#check catalan_succ
#check catalan_eq_centralBinom_div
#check succ_mul_catalan_eq_centralBinom
#check Tree.treesOfNumNodesEq_card_eq_catalan
#check DyckWord.card_dyckWord_semilength_eq_catalan
#check PowerSeries.catalanSeries_sq_mul_X_add_one

#print axioms catalan_eq_centralBinom_div
#print axioms Tree.treesOfNumNodesEq_card_eq_catalan
#print axioms DyckWord.card_dyckWord_semilength_eq_catalan
#print axioms PowerSeries.catalanSeries_sq_mul_X_add_one
