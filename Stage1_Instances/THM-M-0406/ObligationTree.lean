import Statement

/-!
# THM-M-0406 checked obligation interfaces

This module names the exact degeneracy conclusion and checks both directions
between the planned proof engine and the canonical target. The engine remains
an explicit premise: these adapters do not prove Corvaja--Zannier Theorem 1.
-/

set_option autoImplicit false

noncomputable section

namespace Stage1Instances.THMM0406

universe u v

variable {k : Type u} [Field k] [NumberField k]

/-- Exact conclusion delivered by the geometric/arithmetic proof engine. -/
def IntegralPointsLieOnProperCurve
    (X : SurfaceData.{v}) (P : IntegralPointData (k := k) X) : Prop :=
  ∃ C : X.curve, X.isCurveOnAffineOpen C ∧ X.isProperCurve C ∧
    ∀ x : X.point, P.isKRationalPoint x -> P.isSIntegralPoint x ->
      X.pointLiesOnCurve x C

/-- Planned central engine, with exactly the canonical binders and premises. -/
def SurfaceDegeneracyEngine : Prop :=
  ∀ (X : SurfaceData.{v}) (P : IntegralPointData (k := k) X),
    X.isGeometricallyIrreducibleNonsingularSurface ->
    X.isAffineOpenInProjectiveSurface ->
    X.boundaryIsProjectiveComplement ->
    ∀ (weight : X.boundaryDivisor -> Nat) (c : Nat),
      HasTheoremOneBoundary X weight c -> IntegralPointsLieOnProperCurve X P

/-- Checked engine-to-root composition. The engine premise is still open. -/
theorem corvajaZannierTheoremOne_of_engine
    (h : SurfaceDegeneracyEngine.{u, v} (k := k)) :
    CorvajaZannierTheoremOne.{u, v} (k := k) := by
  exact h

/-- The canonical root exposes precisely the planned proof engine. -/
theorem engine_of_corvajaZannierTheoremOne
    (h : CorvajaZannierTheoremOne.{u, v} (k := k)) :
    SurfaceDegeneracyEngine.{u, v} (k := k) := by
  exact h

#print axioms corvajaZannierTheoremOne_of_engine
#print axioms engine_of_corvajaZannierTheoremOne

end Stage1Instances.THMM0406
