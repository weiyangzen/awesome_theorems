import Mathlib.Combinatorics.SimpleGraph.Coloring

/-!
# THM-M-0838 discovery-only intake probe

These checks authenticate pinned simple-graph coloring interfaces and a parameterized schema for
later transport work. `Planar` is deliberately an argument: pinned mathlib does not supply the
source's real-plane map model or an accepted planar-graph bridge. This file states no theorem and
proves no instance of the Four Color Theorem.
-/

#check SimpleGraph.Coloring
#check SimpleGraph.Colorable
#check SimpleGraph.chromaticNumber_le_iff_colorable

universe u

/- A schema used only to check the type of a possible graph-level transport target. -/
def FourColorSchema {V : Type u} (Planar : SimpleGraph V -> Prop) : Prop :=
  forall G : SimpleGraph V, Planar G -> G.Colorable 4
