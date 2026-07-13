import Mathlib.Combinatorics.Nullstellensatz

/-!
# THM-M-0930 discovery-only intake probe

These commands authenticate pinned multivariate-polynomial and Combinatorial Nullstellensatz
interfaces. They do not select the catalog's exact root, establish source-to-Lean transport, or
prove a THM-M-0930 target.
-/

#check MvPolynomial
#check MvPolynomial.eval
#check MvPolynomial.coeff
#check MvPolynomial.totalDegree
#check MvPolynomial.eq_zero_of_eval_zero_at_prod_finset
#check MvPolynomial.combinatorial_nullstellensatz_exists_linearCombination
#check MvPolynomial.combinatorial_nullstellensatz_exists_eval_nonzero

#print axioms MvPolynomial.eq_zero_of_eval_zero_at_prod_finset
#print axioms MvPolynomial.combinatorial_nullstellensatz_exists_linearCombination
#print axioms MvPolynomial.combinatorial_nullstellensatz_exists_eval_nonzero
