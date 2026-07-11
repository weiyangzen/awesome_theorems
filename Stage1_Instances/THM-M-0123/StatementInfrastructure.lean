import Mathlib.AlgebraicGeometry.Geometrically.Basic
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.NumberTheory.NumberField.Basic

/-!
Kernel-checked infrastructure for the THM-M-0123 statement gate.

This module deliberately does not declare the canonical Mordell/Faltings target.  At the pinned
mathlib revision there is no genus invariant for a smooth proper scheme curve, so adding the
remaining `2 <= genus X` hypothesis would require an uninterpreted replacement rather than an exact
formalization.  The declarations below check the part of the target that the pinned APIs express.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

universe u

namespace Stage1Instances.THM_M_0123.StatementInfrastructure

/-- The base scheme used by the target. -/
abbrev SpecOf (K : Type u) [CommRing K] : Scheme.{u} :=
  Spec (CommRingCat.of K)

/-- A rational point as a section of the structure morphism. -/
abbrev RationalPointOver {K : Type u} [Field K] (X : Scheme.{u})
    (structureMap : X ⟶ SpecOf K) : Type u :=
  { point : SpecOf K ⟶ X // point ≫ structureMap = 𝟙 (SpecOf K) }

/-- The native pinned-mathlib portion of the curve hypotheses in Mordell's conjecture. -/
structure CurveBackbone {K : Type u} [Field K] [NumberField K] (X : Scheme.{u})
    (structureMap : X ⟶ SpecOf K) : Prop where
  smoothRelativeDimensionOne : SmoothOfRelativeDimension 1 structureMap
  proper : IsProper structureMap
  geometricallyConnected : geometrically (ConnectedSpace ·) structureMap

end Stage1Instances.THM_M_0123.StatementInfrastructure
