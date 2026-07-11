import Mathlib.CategoryTheory.Yoneda

/-!
# THM-M-0081 anchor audit

This file elaborates the theorem-level mathlib candidates used by the canonical statement.  It is
an audit surface only: it neither declares the canonical theorem nor assigns proof credit.
-/

open CategoryTheory

#check @Yoneda.fullyFaithful
#check @Functor.FullyFaithful.preimageIso
#check @Functor.mapIso
#check @yonedaEquiv
#check @yonedaLemma

#print axioms Yoneda.fullyFaithful
#print axioms Functor.FullyFaithful.preimageIso
#print axioms Functor.mapIso
#print axioms yonedaEquiv
#print axioms yonedaLemma
