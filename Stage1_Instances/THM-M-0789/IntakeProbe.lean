import Mathlib.Order.Filter.Ultrafilter.Basic
import Mathlib.Order.Filter.CardinalInter
import Mathlib.SetTheory.Cardinal.Regular

#check Cardinal
#check Cardinal.mk
#check Ultrafilter
#check Ultrafilter.toFilter
#check CardinalInterFilter
#check Cardinal.IsInaccessible

-- Candidate shape only: this is not the canonical target.
#check fun (alpha : Type*) (kappa : Cardinal) (u : Ultrafilter alpha) =>
  Cardinal.mk alpha = kappa /\ CardinalInterFilter (u : Filter alpha) kappa
