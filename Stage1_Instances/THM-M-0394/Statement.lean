import Mathlib.AlgebraicGeometry.Geometrically.Integral
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth
import Mathlib.AlgebraicGeometry.Properties
import Mathlib.NumberTheory.NumberField.Basic
import Mathlib.RingTheory.DedekindDomain.SInteger

/-!
# THM-M-0394: Siegel's theorem (canonical statement)

This module freezes the number-field, affine-curve form of Siegel's theorem.
The pinned library does not yet provide curve genus, geometric boundary, or
integral-model APIs, so those parts of the selected object model are explicit
data with named semantic compatibility predicates. The proposition is stated
but not asserted or proved here.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

universe u v

namespace Stage1Rev56.THMM0394

/-- The base scheme of a number field. -/
abbrev SpecOf (K : Type u) [CommRing K] : Scheme.{u} :=
  Spec (CommRingCat.of K)

/-- A `K`-rational point, represented as a section of the structure map. -/
abbrev RationalPoint {K : Type u} [Field K] (X : Scheme.{u})
    (structureMap : X ⟶ SpecOf K) : Type u :=
  { point : SpecOf K ⟶ X // point ≫ structureMap = 𝟙 (SpecOf K) }

/--
The curve, compactification, boundary, and affine-coordinate data used by the
selected formulation of Siegel's theorem.

The concrete mathlib predicates are used for affineness, smoothness,
geometric integrality, properness, and the open immersion into the completion.
The three compatibility fields name exactly the unavailable interfaces:
dimension/genus, geometric complement, and affine coordinates.
-/
structure CurveModel (K : Type u) [Field K] [NumberField K] where
  curve : Scheme.{u}
  completion : Scheme.{u}
  structureMap : curve ⟶ SpecOf K
  completionStructureMap : completion ⟶ SpecOf K
  intoCompletion : curve ⟶ completion
  map_commutes : intoCompletion ≫ completionStructureMap = structureMap
  affine : IsAffine curve
  smooth : Smooth structureMap
  geometricallyIntegral : GeometricallyIntegral structureMap
  completionSmooth : Smooth completionStructureMap
  completionProper : IsProper completionStructureMap
  dimensionOne : Prop
  genus : Nat
  genusModelsCompletion : Prop
  geometricBoundaryPoint : Type v
  boundaryPoints : Finset geometricBoundaryPoint
  boundaryModelsComplement : Prop
  coordinateCount : Nat
  coordinate : RationalPoint curve structureMap → Fin coordinateCount → K
  coordinatesModelAffineEmbedding : Prop

/-- The finite primes at which denominators are allowed. -/
abbrev FinitePrimeSet (K : Type u) [Field K] [NumberField K] :=
  Finset (IsDedekindDomain.HeightOneSpectrum (NumberField.RingOfIntegers K))

/-- A rational point is integral outside `S` when every selected affine
coordinate lies in the ring of `S`-integers. Infinite places are implicit, as
usual in the finite-prime description of `S`-integers. -/
def IsSIntegral {K : Type u} [Field K] [NumberField K]
    (S : FinitePrimeSet K) (C : CurveModel.{u, v} K)
    (P : RationalPoint C.curve C.structureMap) : Prop :=
  ∀ i, C.coordinate P i ∈
    (S : Set (IsDedekindDomain.HeightOneSpectrum
      (NumberField.RingOfIntegers K))).integer K

/-- The set of rational points integral outside `S` in the frozen model. -/
def integralPointSet {K : Type u} [Field K] [NumberField K]
    (S : FinitePrimeSet K) (C : CurveModel.{u, v} K) :
    Set (RationalPoint C.curve C.structureMap) :=
  {P | IsSIntegral S C P}

/-- The normalized geometric hypotheses on the chosen affine curve model. -/
def IsSiegelCurve {K : Type u} [Field K] [NumberField K]
    (C : CurveModel.{u, v} K) : Prop :=
  C.dimensionOne ∧ C.genusModelsCompletion ∧ C.boundaryModelsComplement ∧
    C.coordinatesModelAffineEmbedding ∧
      (0 < C.genus ∨
        (C.genus = 0 ∧ 3 ≤ C.boundaryPoints.card))

/--
Siegel's theorem: for a number field, a finite set of finite primes, and a
smooth geometrically integral affine curve whose smooth projective completion
has positive genus or at least three geometric boundary points in genus zero,
the points integral outside that finite set are finite.
-/
def Statement : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K]
    (S : FinitePrimeSet K) (C : CurveModel.{u, v} K),
    IsSiegelCurve C → (integralPointSet S C).Finite

/-- Exact expansion fixture for the ordered binders and conclusion. -/
theorem statement_iff_expanded :
    Statement.{u, v} ↔
      ∀ (K : Type u) [Field K] [NumberField K]
        (S : FinitePrimeSet K) (C : CurveModel.{u, v} K),
        IsSiegelCurve C → (integralPointSet S C).Finite :=
  Iff.rfl

/-- Checked expansion of membership in the integral-point set. -/
theorem mem_integralPointSet_iff
    {K : Type u} [Field K] [NumberField K]
    (S : FinitePrimeSet K) (C : CurveModel.{u, v} K)
    (P : RationalPoint C.curve C.structureMap) :
    P ∈ integralPointSet S C ↔
      ∀ i, C.coordinate P i ∈
        (S : Set (IsDedekindDomain.HeightOneSpectrum
          (NumberField.RingOfIntegers K))).integer K :=
  Iff.rfl

#check Statement

end Stage1Rev56.THMM0394
