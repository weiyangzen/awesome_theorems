import Mathlib.AlgebraicTopology.FundamentalGroupoid.FundamentalGroup
import Mathlib.CategoryTheory.Limits.Shapes.Pullback.Square

/-!
# THM-M-0526 anchor surface

This module checks the pinned mathlib declarations that can support the frozen
target.  None of them states Seifert-van Kampen or closes the target.
-/

#check FundamentalGroup
#check FundamentalGroup.map
#check FundamentalGroup.mapOfEq
#check FundamentalGroupoid.map
#check FundamentalGroupoid.map_comp
#check CategoryTheory.Square.IsPushout

#print axioms FundamentalGroup.map
#print axioms FundamentalGroupoid.map_comp
#print axioms CategoryTheory.Square.IsPushout
