import Mathlib.AlgebraicGeometry.Geometrically.Integral
import Mathlib.AlgebraicGeometry.Morphisms.Proper
import Mathlib.AlgebraicGeometry.Morphisms.Smooth

/-!
# THM-M-0105: Riemann-Roch statement for algebraic curves

This module freezes the classical divisor formula selected at intake. The
pinned snapshot supplies schemes and the geometric curve predicates below, but
not concrete curve-divisor, canonical-divisor, degree, or divisor-sheaf APIs.
Those missing interfaces are represented by typed data plus explicit semantic
compatibility predicates. No field assumes or implies the Riemann-Roch
equality. This file states and mutation-tests the target; it does not prove it.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

universe u v

namespace Stage1Instances.THM_M_0105

/-- The base scheme associated to a commutative ring. -/
abbrev SpecOf (k : Type u) [CommRing k] : Scheme.{u} :=
  Spec (CommRingCat.of k)

/-- A scheme over a field, with its structure morphism. -/
structure CurveOver (k : Type u) [Field k] where
  scheme : Scheme.{u}
  structureMap : scheme ⟶ SpecOf k

namespace CurveOver

variable {k : Type u} [Field k]

/-- The pinned geometric hypotheses for the intake-selected curve scope. -/
def IsSmoothProjectiveGeometricallyIntegral (C : CurveOver.{u} k) : Prop :=
  SmoothOfRelativeDimension 1 C.structureMap ∧
    IsProper C.structureMap ∧ GeometricallyIntegral C.structureMap

end CurveOver

/--
Typed divisor/cohomology data needed for the selected formula. The semantic
predicates require the carrier and operations to model divisors on `C`, a
canonical divisor, degree, and `ell(E) = dim_k H^0(C, O_C(E))`; they do not
contain the desired equality.
-/
structure RiemannRochData (k : Type u) [Field k] (C : CurveOver.{u} k) where
  Divisor : Type v
  sub : Divisor → Divisor → Divisor
  degree : Divisor → Int
  ell : Divisor → Int
  canonicalDivisor : Divisor
  genus : Int
  divisorModelsDivisorsOnCurve : Prop
  subtractionModelsDivisorSubtraction : Prop
  degreeModelsDivisorDegree : Prop
  ellModelsGlobalSectionDimension : Prop
  canonicalDivisorModelsCanonicalDivisor : Prop
  genusModelsCurveGenus : Prop

namespace RiemannRochData

variable {k : Type u} [Field k] {C : CurveOver.{u} k}

/-- All conclusion-free semantic-interface hypotheses of the target. -/
def ModelsCanonicalInvariants (A : RiemannRochData.{u, v} k C) : Prop :=
  A.divisorModelsDivisorsOnCurve ∧
    A.subtractionModelsDivisorSubtraction ∧
      A.degreeModelsDivisorDegree ∧
        A.ellModelsGlobalSectionDimension ∧
          A.canonicalDivisorModelsCanonicalDivisor ∧ A.genusModelsCurveGenus

/-- The classical formula for one divisor. -/
def Formula (A : RiemannRochData.{u, v} k C) (D : A.Divisor) : Prop :=
  A.ell D - A.ell (A.sub A.canonicalDivisor D) =
    A.degree D + 1 - A.genus

end RiemannRochData

/--
The exact normalized target: on every smooth projective geometrically integral
curve over an arbitrary field, every divisor satisfies Riemann-Roch for every
typed realization of the canonical divisor, degree, genus, and `ell` data.
-/
def RiemannRochTarget : Prop :=
  ∀ (k : Type u) [Field k] (C : CurveOver.{u} k)
    (A : RiemannRochData.{u, v} k C),
      C.IsSmoothProjectiveGeometricallyIntegral →
        A.ModelsCanonicalInvariants → ∀ D : A.Divisor, A.Formula D

/-- Checked expansion fixing all ordered binders, hypotheses, and the formula. -/
theorem riemannRochTarget_iff_expanded :
    RiemannRochTarget.{u, v} ↔
      ∀ (k : Type u) [Field k] (C : CurveOver.{u} k)
        (A : RiemannRochData.{u, v} k C),
          SmoothOfRelativeDimension 1 C.structureMap ∧
              IsProper C.structureMap ∧ GeometricallyIntegral C.structureMap →
            A.divisorModelsDivisorsOnCurve ∧
                A.subtractionModelsDivisorSubtraction ∧
                  A.degreeModelsDivisorDegree ∧
                    A.ellModelsGlobalSectionDimension ∧
                      A.canonicalDivisorModelsCanonicalDivisor ∧
                        A.genusModelsCurveGenus →
              ∀ D : A.Divisor,
                A.ell D - A.ell (A.sub A.canonicalDivisor D) =
                  A.degree D + 1 - A.genus :=
  Iff.rfl

/-! Structural mutations elaborate independently and receive no identity credit. -/

def MutationRemovedGeometricIntegrality : Prop :=
  ∀ (k : Type u) [Field k] (C : CurveOver.{u} k)
    (A : RiemannRochData.{u, v} k C),
      SmoothOfRelativeDimension 1 C.structureMap ∧ IsProper C.structureMap →
        A.ModelsCanonicalInvariants → ∀ D : A.Divisor, A.Formula D

def MutationChangedDomainToRational : Prop :=
  ∀ (C : CurveOver.{0} Rat)
    (A : RiemannRochData.{0, v} Rat C),
      C.IsSmoothProjectiveGeometricallyIntegral →
        A.ModelsCanonicalInvariants → ∀ D : A.Divisor, A.Formula D

def MutationChangedDivisorBinderScope : Prop :=
  ∀ (k : Type u) [Field k] (C : CurveOver.{u} k),
    ∃ A : RiemannRochData.{u, v} k C,
      C.IsSmoothProjectiveGeometricallyIntegral →
        A.ModelsCanonicalInvariants → ∃ D : A.Divisor, A.Formula D

def MutationOnlyCanonicalDivisor : Prop :=
  ∀ (k : Type u) [Field k] (C : CurveOver.{u} k)
    (A : RiemannRochData.{u, v} k C),
      C.IsSmoothProjectiveGeometricallyIntegral →
        A.ModelsCanonicalInvariants → A.Formula A.canonicalDivisor

variable
  (hRemoved : MutationRemovedGeometricIntegrality.{u, v})
  (hDomain : MutationChangedDomainToRational.{v})
  (hScope : MutationChangedDivisorBinderScope.{u, v})
  (hBoundary : MutationOnlyCanonicalDivisor.{u, v})

#check_failure (show RiemannRochTarget.{u, v} from hRemoved)
#check_failure (show RiemannRochTarget.{u, v} from hDomain)
#check_failure (show RiemannRochTarget.{u, v} from hScope)
#check_failure (show RiemannRochTarget.{u, v} from hBoundary)

#check riemannRochTarget_iff_expanded
#print axioms riemannRochTarget_iff_expanded

set_option pp.universes true in
set_option pp.explicit true in
#print RiemannRochTarget

end Stage1Instances.THM_M_0105
