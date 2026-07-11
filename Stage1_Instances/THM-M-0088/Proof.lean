import ObligationTree

/-! Proof bodies for the frozen THM-M-0088 Yoneda-embedding obligations. -/

open CategoryTheory

universe v u

namespace Stage1Instances.THM_M_0088

/-- The frozen preimage construction: evaluate at the source object and its identity. -/
def yonedaPreimage (C : Type u) [Category.{v} C] {X Y : C}
    (f : yoneda.obj X ⟶ yoneda.obj Y) : X ⟶ Y :=
  f.app (Opposite.op X) (𝟙 X)

/-- Naturality recovers every component from the identity component. -/
theorem yonedaPreimage_component (C : Type u) [Category.{v} C] {X Y Z : C}
    (f : yoneda.obj X ⟶ yoneda.obj Y) (g : Z ⟶ X) :
    g ≫ yonedaPreimage C f = f.app (Opposite.op Z) g := by
  simpa [yonedaPreimage] using Yoneda.naturality f g (𝟙 X)

/-- Mapping the selected preimage recovers the original natural transformation. -/
theorem yoneda_map_preimage (C : Type u) [Category.{v} C] {X Y : C}
    (f : yoneda.obj X ⟶ yoneda.obj Y) :
    yoneda.map (yonedaPreimage C f) = f := by
  ext Z g
  exact yonedaPreimage_component C f g

/-- Evaluating the image of a morphism at the identity recovers that morphism. -/
theorem yoneda_preimage_map (C : Type u) [Category.{v} C] {X Y : C} (f : X ⟶ Y) :
    yonedaPreimage C (yoneda.map f) = f := by
  simp [yonedaPreimage]

/-- The exact frozen root, assembled only from the checked local obligation bodies above. -/
def yonedaEmbedding (C : Type u) [Category.{v} C] : YonedaEmbeddingTarget C :=
  yonedaEmbedding_of_inverseLaws C
    (fun f => yonedaPreimage C f)
    (yoneda_map_preimage C)
    (yoneda_preimage_map C)

end Stage1Instances.THM_M_0088

#check Stage1Instances.THM_M_0088.yonedaEmbedding
#print axioms Stage1Instances.THM_M_0088.yonedaPreimage_component
#print axioms Stage1Instances.THM_M_0088.yoneda_map_preimage
#print axioms Stage1Instances.THM_M_0088.yoneda_preimage_map
#print axioms Stage1Instances.THM_M_0088.yonedaEmbedding
