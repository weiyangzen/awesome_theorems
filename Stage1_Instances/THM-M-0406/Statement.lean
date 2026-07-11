import Mathlib.AlgebraicGeometry.Scheme
import Mathlib.NumberTheory.NumberField.Completion.FinitePlace

/-!
# THM-M-0406: Corvaja--Zannier Theorem 1 statement

This module freezes Theorem 1 of Corvaja and Zannier, *On integral points on
surfaces* (2004), pages 706--707. Mathlib does not presently expose the needed
divisor intersection theory or `S`-integral surface-point API, so those
source-level notions are explicit typed parameters. They are not hypotheses
asserting the result: the target still concludes the existence of a proper
curve containing every `S`-integral `k`-point.
-/

set_option autoImplicit false

noncomputable section

open AlgebraicGeometry

namespace Stage1Instances.THMM0406

universe u v

variable {k : Type u} [Field k] [NumberField k]

/-- Source-level data in Corvaja--Zannier Theorem 1. -/
structure SurfaceData where
  projectiveSurface : Scheme.{v}
  affineOpen : Scheme.{v}
  boundaryDivisor : Type v
  point : Type v
  curve : Type v
  isGeometricallyIrreducibleNonsingularSurface : Prop
  isAffineOpenInProjectiveSurface : Prop
  boundaryComponents : Finset boundaryDivisor
  boundaryIsProjectiveComplement : Prop
  isDistinctIrreducibleBoundaryComponent : boundaryDivisor -> Prop
  threeSharePoint : boundaryDivisor -> boundaryDivisor -> boundaryDivisor -> Prop
  intersectionNumber : boundaryDivisor -> boundaryDivisor -> Nat
  isCurveOnAffineOpen : curve -> Prop
  isProperCurve : curve -> Prop
  pointLiesOnCurve : point -> curve -> Prop

/-- The finite place set and the selected `S`-integral rational points. -/
structure IntegralPointData (X : SurfaceData.{v}) where
  S : Set (NumberField.FinitePlace k)
  S_finite : S.Finite
  isKRationalPoint : X.point -> Prop
  isSIntegralPoint : X.point -> Prop

/-- Exact hypotheses on the boundary divisors from Theorem 1. -/
def HasTheoremOneBoundary
    (X : SurfaceData.{v})
    (weight : X.boundaryDivisor -> Nat) (c : Nat) : Prop :=
  X.boundaryComponents.card >= 4 ∧
    (∀ D ∈ X.boundaryComponents, X.isDistinctIrreducibleBoundaryComponent D) ∧
    (∀ D₁ ∈ X.boundaryComponents, ∀ D₂ ∈ X.boundaryComponents,
      ∀ D₃ ∈ X.boundaryComponents,
        D₁ ≠ D₂ -> D₁ ≠ D₃ -> D₂ ≠ D₃ ->
          ¬X.threeSharePoint D₁ D₂ D₃) ∧
    (∀ D ∈ X.boundaryComponents, 0 < weight D) ∧
    0 < c ∧
    ∀ D₁ ∈ X.boundaryComponents, ∀ D₂ ∈ X.boundaryComponents,
      D₁ ≠ D₂ -> weight D₁ * weight D₂ * X.intersectionNumber D₁ D₂ = c

/--
Corvaja--Zannier Theorem 1: under the stated intersection condition, all
`S`-integral `k`-points of the affine surface lie on one proper curve.
-/
def CorvajaZannierTheoremOne : Prop :=
  ∀ (X : SurfaceData.{v}) (P : IntegralPointData (k := k) X),
    X.isGeometricallyIrreducibleNonsingularSurface ->
    X.isAffineOpenInProjectiveSurface ->
    X.boundaryIsProjectiveComplement ->
    ∀ (weight : X.boundaryDivisor -> Nat) (c : Nat),
      HasTheoremOneBoundary X weight c ->
        ∃ C : X.curve, X.isCurveOnAffineOpen C ∧ X.isProperCurve C ∧
          ∀ x : X.point, P.isKRationalPoint x -> P.isSIntegralPoint x ->
            X.pointLiesOnCurve x C

/-- Exact-type fixture preserving the ordered binders of the canonical target. -/
theorem corvajaZannierTheoremOne_exact_type :
    CorvajaZannierTheoremOne.{u, v} (k := k) ↔
      (∀ (X : SurfaceData.{v}) (P : IntegralPointData (k := k) X),
        X.isGeometricallyIrreducibleNonsingularSurface ->
        X.isAffineOpenInProjectiveSurface ->
        X.boundaryIsProjectiveComplement ->
        ∀ (weight : X.boundaryDivisor -> Nat) (c : Nat),
          HasTheoremOneBoundary X weight c ->
            ∃ C : X.curve, X.isCurveOnAffineOpen C ∧ X.isProperCurve C ∧
              ∀ x : X.point, P.isKRationalPoint x -> P.isSIntegralPoint x ->
                X.pointLiesOnCurve x C) :=
  by
    unfold CorvajaZannierTheoremOne
    rfl

end Stage1Instances.THMM0406

set_option pp.universes true in
set_option pp.explicit true in
#print Stage1Instances.THMM0406.CorvajaZannierTheoremOne
