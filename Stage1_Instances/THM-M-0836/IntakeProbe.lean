import Mathlib.Combinatorics.SimpleGraph.Coloring
import Mathlib.Combinatorics.SimpleGraph.DegreeSum

#check SimpleGraph.Coloring
#check SimpleGraph.Colorable
#check SimpleGraph.Coloring.valid
#check SimpleGraph.Colorable.mono
#check SimpleGraph.chromaticNumber
#check SimpleGraph.chromaticNumber_le_iff_colorable
#check SimpleGraph.degree
#check SimpleGraph.sum_degrees_eq_twice_card_edges

example : (⊥ : SimpleGraph (Fin 3)).Colorable 4 := by
  exact (SimpleGraph.colorable_of_fintype (⊥ : SimpleGraph (Fin 3))).mono (by decide)
