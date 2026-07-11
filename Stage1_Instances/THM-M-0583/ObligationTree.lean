import Mathlib.Geometry.Manifold.PoincareConjecture

/-!
# THM-M-0583 obligation-tree interface

This file checks only the logical interfaces used by the frozen architecture.
The deep four-dimensional topology premise remains explicit and open.
-/

noncomputable section

open Metric ContinuousMap
open scoped Manifold

namespace Stage1Instances.THM_M_0583.ObligationTree

universe u

abbrev FourModel := EuclideanSpace Real (Fin 4)
abbrev FourSphere := sphere (0 : EuclideanSpace Real (Fin 5)) 1

/-- The terminal mathematical obligation before adapting it to the dossier name. -/
def FreedmanTopologicalCore : Prop :=
  forall (M : Type u) [TopologicalSpace M] [T2Space M] [CompactSpace M]
    [ChartedSpace FourModel M],
      M ≃ₕ FourSphere -> Nonempty (M ≃ₜ FourSphere)

/-- The exact root, repeated here so this module has no generated local import. -/
def CanonicalRoot : Prop :=
  forall (M : Type u) [TopologicalSpace M] [T2Space M] [CompactSpace M]
    [ChartedSpace FourModel M],
      M ≃ₕ FourSphere -> Nonempty (M ≃ₜ FourSphere)

/-- Checked composition: an implementation of the deep core closes the exact root. -/
theorem canonicalRoot_of_freedmanTopologicalCore
    (core : FreedmanTopologicalCore.{u}) : CanonicalRoot.{u} :=
  core

/-- The adapter neither weakens nor strengthens the terminal mathematical claim. -/
theorem freedmanTopologicalCore_iff_canonicalRoot :
    FreedmanTopologicalCore.{u} ↔ CanonicalRoot.{u} :=
  Iff.rfl

#check canonicalRoot_of_freedmanTopologicalCore
#print axioms canonicalRoot_of_freedmanTopologicalCore

end Stage1Instances.THM_M_0583.ObligationTree
