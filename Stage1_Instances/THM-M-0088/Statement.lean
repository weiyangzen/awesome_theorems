import Mathlib.CategoryTheory.Yoneda

/-!
The exact statement surface for THM-M-0088.  This file deliberately declares
the target type and transports only; it does not supply an inhabitant of the
target and therefore does not claim proof credit.
-/

open CategoryTheory

universe v u

namespace Stage1Instances.THM_M_0088

/-- The canonical Yoneda-embedding target, retaining the fully-faithful data. -/
def YonedaEmbeddingTarget (C : Type u) [Category.{v} C] : Type (max u v) :=
  (yoneda (C := C)).FullyFaithful

/-- Mutation: retains faithfulness but removes fullness. -/
def MutationFaithfulOnly (C : Type u) [Category.{v} C] : Prop :=
  (yoneda (C := C)).Faithful

/-- Mutation: changes the variance and source category to the co-Yoneda embedding. -/
def MutationCoyoneda (C : Type u) [Category.{v} C] : Type (max u v) :=
  (coyoneda (C := C)).FullyFaithful

/-- Mutation: raises the presheaf codomain universe instead of retaining `Type v`. -/
def MutationUniverseRaised (C : Type u) [Category.{v} C] : Type (max u v) :=
  (uliftYoneda.{u} (C := C)).FullyFaithful

/-- The historical proposition is exactly existence of the canonical target data. -/
theorem nonemptyTarget_iff_historicalShape (C : Type u) [Category.{v} C] :
    Nonempty (YonedaEmbeddingTarget C) ↔
      Nonempty ((yoneda (C := C)).FullyFaithful) :=
  Iff.rfl

/-- Expanding the local target introduces no alternate encoding. -/
theorem target_eq_expanded (C : Type u) [Category.{v} C] :
    YonedaEmbeddingTarget C = (yoneda (C := C)).FullyFaithful :=
  rfl

end Stage1Instances.THM_M_0088

set_option pp.universes true in
set_option pp.explicit true in
#check Stage1Instances.THM_M_0088.YonedaEmbeddingTarget

set_option pp.universes true in
set_option pp.explicit true in
#check Stage1Instances.THM_M_0088.nonemptyTarget_iff_historicalShape

set_option pp.universes true in
set_option pp.explicit true in
#check CategoryTheory.Yoneda.fullyFaithful

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THM_M_0088.YonedaEmbeddingTarget
