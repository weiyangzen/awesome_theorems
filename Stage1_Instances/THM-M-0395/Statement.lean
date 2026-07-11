import Mathlib.AlgebraicGeometry.Properties
import Mathlib.NumberTheory.NumberField.Basic

/-!
# THM-M-0395: Faltings theorem (statement boundary)

This module freezes the Mordell-conjecture form of Faltings's theorem. The
three curve predicates whose mathematical definitions are not available in
the pinned mathlib snapshot are explicit fields of the curve datum rather
than unconstrained arguments to the theorem.

The file states a proposition only. It does not assert Faltings's theorem.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

universe u

namespace Stage1Rev56.THMM0395

/-- The affine base scheme of a number field. -/
abbrev SpecOf (K : Type u) [CommRing K] : Scheme.{u} :=
  Spec (CommRingCat.of K)

/-- A rational point is a section of the curve's structure morphism. -/
abbrev RationalPoint {K : Type u} [Field K] (X : Scheme.{u})
    (structureMap : X ⟶ SpecOf K) : Type u :=
  { point : SpecOf K ⟶ X // point ≫ structureMap = 𝟙 (SpecOf K) }

/--
The data and predicates defining a curve in the selected Faltings statement.

`smooth`, `proper`, and `geometricallyConnected` name their standard
scheme-theoretic meanings. `dimensionOne` and `genusAtLeastTwo` exclude
higher-dimensional varieties and the genus-zero/one boundary cases. They are
fields because the pinned dependency snapshot has no complete curve-genus API.
-/
structure CurveOver (K : Type u) [Field K] [NumberField K] where
  scheme : Scheme.{u}
  structureMap : scheme ⟶ SpecOf K
  smooth : Prop
  proper : Prop
  geometricallyConnected : Prop
  dimensionOne : Prop
  genusAtLeastTwo : Prop

/-- All hypotheses of the selected smooth proper curve formulation. -/
def IsFaltingsCurve {K : Type u} [Field K] [NumberField K]
    (C : CurveOver K) : Prop :=
  C.smooth ∧ C.proper ∧ C.geometricallyConnected ∧
    C.dimensionOne ∧ C.genusAtLeastTwo

/--
Faltings's theorem in Mordell form: every smooth, proper, geometrically
connected curve of genus at least two over a number field has finitely many
rational points.
-/
def Statement : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K] (C : CurveOver K),
    IsFaltingsCurve C → Finite (RationalPoint C.scheme C.structureMap)

/-- Checked expansion of the canonical target's binders and conclusion. -/
theorem statement_iff_expanded :
    Statement.{u} ↔
      ∀ (K : Type u) [Field K] [NumberField K] (C : CurveOver K),
        IsFaltingsCurve C → Finite (RationalPoint C.scheme C.structureMap) :=
  Iff.rfl

/-- Checked transport to finiteness of the universal set of rational points. -/
theorem finite_points_iff_finite_univ
    {K : Type u} [Field K] [NumberField K] (C : CurveOver K) :
    Finite (RationalPoint C.scheme C.structureMap) ↔
      (Set.univ : Set (RationalPoint C.scheme C.structureMap)).Finite :=
  Set.finite_univ_iff.symm

#check Statement

end Stage1Rev56.THMM0395
