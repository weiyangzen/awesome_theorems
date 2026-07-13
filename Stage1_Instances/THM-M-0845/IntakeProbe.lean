import Mathlib.Combinatorics.SimpleGraph.Maps
import Mathlib.Data.Fintype.Pi

/-! Discovery-only API checks; this file states no graph-homomorphism-count theorem. -/

#check SimpleGraph.Hom
#check SimpleGraph.Embedding
#check SimpleGraph.Iso
#check SimpleGraph.Hom.comp
#check RelHom.instFintype
#check Fintype.card

open SimpleGraph

universe u v

section

variable {V : Type u} {W : Type v}
variable [Fintype V] [DecidableEq V] [Fintype W]
variable (F : SimpleGraph V) (G : SimpleGraph W)
variable [DecidableRel F.Adj] [DecidableRel G.Adj]

#synth Fintype (F →g G)
#check Fintype.card (F →g G)

end
