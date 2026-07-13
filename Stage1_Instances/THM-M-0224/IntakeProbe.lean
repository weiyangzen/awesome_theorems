import Mathlib.Analysis.Complex.Liouville

/-!
# THM-M-0224 discovery-only intake probe

These checks authenticate the direct Liouville interfaces in the pinned mathlib snapshot. They do
not select a source-faithful canonical target, establish statement identity, audit terminal proof
bodies, or supply proof credit.
-/

#check Bornology.IsBounded
#check Set.range
#check Function.const
#check Differentiable.apply_eq_apply_of_bounded
#check Differentiable.exists_const_forall_eq_of_bounded
#check Differentiable.exists_eq_const_of_bounded

#print axioms Differentiable.apply_eq_apply_of_bounded
#print axioms Differentiable.exists_const_forall_eq_of_bounded
#print axioms Differentiable.exists_eq_const_of_bounded
