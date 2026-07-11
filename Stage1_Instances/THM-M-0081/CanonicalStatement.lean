import Mathlib.CategoryTheory.Yoneda

/-!
# THM-M-0081 canonical statement

The repository claim "an object is uniquely determined by its representable functor" is read with
"uniquely" meaning up to categorical isomorphism.  Both sides use `Nonempty` because the claim is
existential and does not select an isomorphism.
-/

open CategoryTheory

universe v u

namespace Stage1Instances.THM_M_0081

/--
In any locally small category, two objects have naturally isomorphic contravariant representable
functors if and only if the objects themselves are isomorphic.
-/
def CanonicalTarget (C : Type u) [Category.{v} C] (X Y : C) : Prop :=
  Nonempty (yoneda.obj X ≅ yoneda.obj Y) ↔ Nonempty (X ≅ Y)

#check CanonicalTarget

end Stage1Instances.THM_M_0081
