import Mathlib.Algebra.BigOperators.Group.Finset.Basic

/-!
# THM-M-1466 discovery-only intake probe

These checks authenticate pinned finite-sum interfaces that could support a later source-selected
finite-volume conservation statement, especially reindexing and cancellation of oriented internal
face fluxes. They do not define a mesh, numerical flux, discrete update, canonical convergence
theorem, or proof of THM-M-1466.
-/

#check Finset.sum
#check Finset.sum_bij
#check Finset.sum_equiv
#check Finset.sum_attach
#check Finset.sum_union
#check Finset.sum_disjUnion
#check Finset.sum_add_distrib
#check Finset.sum_sub_distrib

#print axioms Finset.sum_bij
#print axioms Finset.sum_union
