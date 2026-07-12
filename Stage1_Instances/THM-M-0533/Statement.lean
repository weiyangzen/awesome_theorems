import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.Algebra.Category.Grp.Biproducts
import Mathlib.Algebra.Category.Grp.Colimits
import Mathlib.Algebra.Category.Grp.Abelian
import Mathlib.Algebra.Homology.ShortComplex.Exact
import Mathlib.Algebra.Homology.ShortComplex.Abelian
import Mathlib.Topology.Category.TopCat.Opens

/-!
The exact formal target for the ordinary integral Mayer-Vietoris sequence of an
open cover, following Hatcher, *Algebraic Topology* (2002), p. 149.  `U` and `V`
are open subsets of `X`, and `hcover` says that they cover `X`.

The connecting morphisms are data because pinned mathlib does not yet construct
them for singular homology.  Exactness is the conclusion, never an input.
-/

open CategoryTheory CategoryTheory.Limits
open TopologicalSpace

namespace AwesomeTheorems.THM_M_0533

universe u

noncomputable section

abbrev IntegralCoefficients : AddCommGrpCat.{u} :=
  AddCommGrpCat.of (ULift.{u} ℤ)

abbrev HFunctor (n : ℕ) : TopCat.{u} ⥤ AddCommGrpCat.{u} :=
  (AlgebraicTopology.singularHomologyFunctor AddCommGrpCat.{u} n).obj
    IntegralCoefficients

abbrev H (n : ℕ) (Y : TopCat.{u}) : AddCommGrpCat.{u} :=
  (HFunctor n).obj Y

abbrev OpenSpace {X : TopCat.{u}} (U : Opens X) : TopCat.{u} :=
  (Opens.toTopCat X).obj U

abbrev interLeft {X : TopCat.{u}} (U V : Opens X) : OpenSpace (U ⊓ V) ⟶ OpenSpace U :=
  (Opens.toTopCat X).map (Opens.infLELeft U V)

abbrev interRight {X : TopCat.{u}} (U V : Opens X) : OpenSpace (U ⊓ V) ⟶ OpenSpace V :=
  (Opens.toTopCat X).map (Opens.infLERight U V)

abbrev firstMap {X : TopCat.{u}} (U V : Opens X) (n : ℕ) :
    H n (OpenSpace (U ⊓ V)) ⟶ H n (OpenSpace U) ⊞ H n (OpenSpace V) :=
  biprod.lift
    ((HFunctor n).map (interLeft U V))
    (-((HFunctor n).map (interRight U V)))

abbrev secondMap {X : TopCat.{u}} (U V : Opens X) (n : ℕ) :
    H n (OpenSpace U) ⊞ H n (OpenSpace V) ⟶ H n X :=
  biprod.desc
    ((HFunctor n).map (Opens.inclusion' U))
    ((HFunctor n).map (Opens.inclusion' V))

/-- One degree of the long Mayer-Vietoris sequence.  Requiring this for every
`n` expresses exactness at all three recurring terms, including degree zero;
the last boundary has codomain `H 0 (U ⊓ V)`. -/
def MayerVietorisDegree {X : TopCat.{u}} (U V : Opens X) (n : ℕ)
    (boundary : H (n + 1) X ⟶ H n (OpenSpace (U ⊓ V)))
    (zeroBoundaryFirst : boundary ≫ firstMap U V n = 0)
    (zeroFirstSecond : firstMap U V n ≫ secondMap U V n = 0)
    (zeroSecondBoundary : secondMap U V (n + 1) ≫ boundary = 0) : Prop :=
  (ShortComplex.mk boundary (firstMap U V n) zeroBoundaryFirst).Exact ∧
    (ShortComplex.mk (firstMap U V n) (secondMap U V n) zeroFirstSecond).Exact ∧
      (ShortComplex.mk (secondMap U V (n + 1)) boundary zeroSecondBoundary).Exact

/-- Canonical target: there are connecting homomorphisms making the integral
singular-homology Mayer-Vietoris sequence exact in every natural degree. -/
def MayerVietorisSequence : Prop :=
  ∀ (X : TopCat.{u}) (U V : Opens X) (_hcover : U ⊔ V = ⊤),
    ∃ boundary : ∀ n : ℕ, H (n + 1) X ⟶ H n (OpenSpace (U ⊓ V)),
      ∃ zeroBoundaryFirst : ∀ n, boundary n ≫ firstMap U V n = 0,
        ∃ zeroFirstSecond : ∀ n, firstMap U V n ≫ secondMap U V n = 0,
          ∃ zeroSecondBoundary : ∀ n, secondMap U V (n + 1) ≫ boundary n = 0,
            (∀ n : ℕ, MayerVietorisDegree U V n (boundary n)
              (zeroBoundaryFirst n) (zeroFirstSecond n) (zeroSecondBoundary n)) ∧
            (ShortComplex.mk (firstMap U V 0) (secondMap U V 0)
              (zeroFirstSecond 0)).Exact ∧
            (ShortComplex.mk (secondMap U V 0)
              (0 : H 0 X ⟶ AddCommGrpCat.of (ULift.{u} PUnit))
              (by simp)).Exact

#check MayerVietorisSequence

/-- A separately written encoding used to check binder scope and the endpoint. -/
def MayerVietorisSequenceAlternate : Prop :=
  ∀ (X : TopCat.{u}) (U V : Opens X), U ⊔ V = ⊤ →
    ∃ boundary : ∀ n : ℕ, H (n + 1) X ⟶ H n (OpenSpace (U ⊓ V)),
      ∃ zeroBoundaryFirst : ∀ n, boundary n ≫ firstMap U V n = 0,
        ∃ zeroFirstSecond : ∀ n, firstMap U V n ≫ secondMap U V n = 0,
          ∃ zeroSecondBoundary : ∀ n, secondMap U V (n + 1) ≫ boundary n = 0,
            (∀ n : ℕ, MayerVietorisDegree U V n (boundary n)
              (zeroBoundaryFirst n) (zeroFirstSecond n) (zeroSecondBoundary n)) ∧
            (ShortComplex.mk (firstMap U V 0) (secondMap U V 0)
              (zeroFirstSecond 0)).Exact ∧
            (ShortComplex.mk (secondMap U V 0)
              (0 : H 0 X ⟶ AddCommGrpCat.of (ULift.{u} PUnit)) (by simp)).Exact

theorem canonical_iff_alternate :
    MayerVietorisSequence.{u} ↔ MayerVietorisSequenceAlternate.{u} := by
  rfl

-- Mutation witnesses: these are distinct propositions, not credited transports.
def MutationRemovedCover : Prop :=
  ∀ (X : TopCat.{u}) (U V : Opens X),
    ∃ boundary : ∀ n : ℕ, H (n + 1) X ⟶ H n (OpenSpace (U ⊓ V)), True

def MutationChangedDomain : Prop :=
  ∀ (X : TopCat.{u}) (U V : Set X), True

def MutationChangedBinderScope : Prop :=
  ∃ X : TopCat.{u}, ∀ U V : Opens X, U ⊔ V = ⊤ → True

def MutationMissingDegreeZeroEndpoint : Prop :=
  ∀ (X : TopCat.{u}) (U V : Opens X), U ⊔ V = ⊤ →
    ∃ boundary : ∀ n : ℕ, H (n + 1) X ⟶ H n (OpenSpace (U ⊓ V)),
      ∀ n : ℕ, ∃ h : boundary n ≫ firstMap U V n = 0,
        (ShortComplex.mk (boundary n) (firstMap U V n) h).Exact

example : True := by
  fail_if_success have : MutationRemovedCover.{u} = MayerVietorisSequence.{u} := rfl
  fail_if_success have : MutationChangedDomain.{u} = MayerVietorisSequence.{u} := rfl
  fail_if_success have : MutationChangedBinderScope.{u} = MayerVietorisSequence.{u} := rfl
  fail_if_success have : MutationMissingDegreeZeroEndpoint.{u} = MayerVietorisSequence.{u} := rfl
  trivial

end

end AwesomeTheorems.THM_M_0533
