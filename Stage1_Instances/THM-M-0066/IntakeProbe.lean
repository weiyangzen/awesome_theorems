import Mathlib.RepresentationTheory.Irreducible
import Mathlib.CategoryTheory.Preadditive.Schur

/-!
# THM-M-0066 discovery-only intake probe

These checks authenticate pinned representation, simple-module, and categorical Schur interfaces.
They do not select the catalog's missing domains and binders, define a canonical target, establish
a source transport, or claim a root proof.
-/

#check Representation
#check Representation.IsIrreducible
#check Representation.IntertwiningMap
#check Representation.IsIrreducible.bijective_or_eq_zero
#check Representation.IntertwiningMap.ofBijective
#check LinearMap.bijective_or_eq_zero
#check CategoryTheory.isIso_of_hom_simple
#check CategoryTheory.isIso_iff_nonzero

#print axioms Representation.IsIrreducible.bijective_or_eq_zero
#print axioms LinearMap.bijective_or_eq_zero
#print axioms CategoryTheory.isIso_iff_nonzero
