import Statement

/-! Checked composition surface for the frozen THM-M-0088 obligation tree. -/

open CategoryTheory

universe v u

namespace Stage1Instances.THM_M_0088

/-- Supplying an inverse to `yoneda.map` and both inverse laws constructs exactly the frozen root. -/
def yonedaEmbedding_of_inverseLaws (C : Type u) [Category.{v} C]
    (preimage : {X Y : C} -> (yoneda.obj X ⟶ yoneda.obj Y) -> (X ⟶ Y))
    (map_preimage : forall {X Y : C} (f : yoneda.obj X ⟶ yoneda.obj Y),
      yoneda.map (preimage f) = f)
    (preimage_map : forall {X Y : C} (f : X ⟶ Y),
      preimage (yoneda.map f) = f) : YonedaEmbeddingTarget C where
  preimage := preimage
  map_preimage := map_preimage
  preimage_map := preimage_map

end Stage1Instances.THM_M_0088

#check Stage1Instances.THM_M_0088.yonedaEmbedding_of_inverseLaws
#print axioms Stage1Instances.THM_M_0088.yonedaEmbedding_of_inverseLaws
