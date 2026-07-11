import Mathlib.Algebra.Category.ModuleCat.Monoidal.Basic
import Mathlib.Algebra.Category.ModuleCat.Abelian
import Mathlib.Algebra.Category.ModuleCat.Colimits
import Mathlib.Algebra.Category.ModuleCat.Projective
import Mathlib.Algebra.Homology.ShortComplex.ShortExact
import Mathlib.AlgebraicTopology.SingularHomology.Basic
import Mathlib.CategoryTheory.Monoidal.Tor
import Mathlib.RingTheory.PrincipalIdealDomain

/-!
# Exact statement target for THM-M-0005

This file contains only the canonical proposition for the statement phase.  In particular, the
structure below is not inhabited here: its `shortExact` and naturality fields are proof obligations,
not assumptions hidden in a theorem declaration.
-/

noncomputable section

open AlgebraicTopology CategoryTheory CategoryTheory.Limits
open CategoryTheory.MonoidalCategory

universe u

namespace AwesomeTheorems.Stage1.THM_M_0005

/-- Singular homology in degree `n` with coefficients in a commutative ring `R`. -/
abbrev Homology (R : Type u) [CommRing R] (n : ℕ) (X : TopCat.{u}) : ModuleCat.{u} R :=
  ((singularHomologyFunctor (ModuleCat.{u} R) n).obj (ModuleCat.of R R)).obj X

/-- Pairs of homological degrees contributing to the tensor term in total degree `n`. -/
abbrev TensorDegrees (n : ℕ) := {pq : ℕ × ℕ // pq.1 + pq.2 = n}

/-- Pairs of homological degrees contributing to the `Tor₁` term in total degree `n`. -/
abbrev TorDegrees (n : ℕ) := {pq : ℕ × ℕ // pq.1 + pq.2 + 1 = n}

/-- The direct sum of tensor products in total degree `n`. -/
abbrev TensorTerm (R : Type u) [CommRing R] (X Y : TopCat.{u}) (n : ℕ) : ModuleCat.{u} R :=
  ∐ fun pq : TensorDegrees n ↦ Homology R pq.1.1 X ⊗ Homology R pq.1.2 Y

/-- The direct sum of first `Tor` objects in total degree `n - 1`. -/
abbrev TorTerm (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R]
    (X Y : TopCat.{u}) (n : ℕ) : ModuleCat.{u} R :=
  ∐ fun pq : TorDegrees n ↦ ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
    (Homology R pq.1.1 X)).obj (Homology R pq.1.2 Y)

/-- The middle term, singular homology of the product space. -/
abbrev ProductHomology (R : Type u) [CommRing R] (X Y : TopCat.{u}) (n : ℕ) :
    ModuleCat.{u} R :=
  Homology R n (X ⨯ Y)

/--
The PID-coefficient Kunneth short exact sequences, including naturality in both spaces.

The two naturality equations deliberately quantify the induced maps rather than postulating
unspecified truth-valued "naturality" data.  The component equations pin the maps on the tensor
and `Tor₁` direct sums to the maps induced on homology by `f` and `g`.
-/
structure NaturalKunnethSequence
    (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R] where
  inclusion : ∀ (X Y : TopCat.{u}) (n : ℕ),
    TensorTerm R X Y n ⟶ ProductHomology R X Y n
  projection : ∀ (X Y : TopCat.{u}) (n : ℕ),
    ProductHomology R X Y n ⟶ TorTerm R X Y n
  zero : ∀ (X Y : TopCat.{u}) (n : ℕ), inclusion X Y n ≫ projection X Y n = 0
  shortExact : ∀ (X Y : TopCat.{u}) (n : ℕ),
    (ShortComplex.mk (inclusion X Y n) (projection X Y n) (zero X Y n)).ShortExact
  tensorMap : ∀ {X X' Y Y' : TopCat.{u}} (f : X ⟶ X') (g : Y ⟶ Y') (n : ℕ),
    TensorTerm R X Y n ⟶ TensorTerm R X' Y' n
  torMap : ∀ {X X' Y Y' : TopCat.{u}} (f : X ⟶ X') (g : Y ⟶ Y') (n : ℕ),
    TorTerm R X Y n ⟶ TorTerm R X' Y' n
  tensorMap_component : ∀ {X X' Y Y' : TopCat.{u}} (f : X ⟶ X') (g : Y ⟶ Y')
      (n : ℕ) (pq : TensorDegrees n),
    Sigma.ι (fun pq : TensorDegrees n ↦ Homology R pq.1.1 X ⊗ Homology R pq.1.2 Y) pq ≫
        tensorMap f g n =
      (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.1).obj (ModuleCat.of R R)).map f ⊗ₘ
          ((singularHomologyFunctor (ModuleCat.{u} R) pq.1.2).obj (ModuleCat.of R R)).map g) ≫
        Sigma.ι (fun pq : TensorDegrees n ↦ Homology R pq.1.1 X' ⊗ Homology R pq.1.2 Y') pq
  torMap_component : ∀ {X X' Y Y' : TopCat.{u}} (f : X ⟶ X') (g : Y ⟶ Y')
      (n : ℕ) (pq : TorDegrees n),
    Sigma.ι (fun pq : TorDegrees n ↦ ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
        (Homology R pq.1.1 X)).obj (Homology R pq.1.2 Y)) pq ≫ torMap f g n =
      ((CategoryTheory.Tor (ModuleCat.{u} R) 1).map
          (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.1).obj
            (ModuleCat.of R R)).map f)).app (Homology R pq.1.2 Y) ≫
        ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj (Homology R pq.1.1 X')).map
          (((singularHomologyFunctor (ModuleCat.{u} R) pq.1.2).obj
            (ModuleCat.of R R)).map g) ≫
        Sigma.ι (fun pq : TorDegrees n ↦ ((CategoryTheory.Tor (ModuleCat.{u} R) 1).obj
          (Homology R pq.1.1 X')).obj (Homology R pq.1.2 Y')) pq
  inclusion_natural : ∀ {X X' Y Y' : TopCat.{u}} (f : X ⟶ X') (g : Y ⟶ Y') (n : ℕ),
    tensorMap f g n ≫ inclusion X' Y' n = inclusion X Y n ≫
      ((singularHomologyFunctor (ModuleCat.{u} R) n).obj (ModuleCat.of R R)).map
        (Limits.prod.map f g)
  projection_natural : ∀ {X X' Y Y' : TopCat.{u}} (f : X ⟶ X') (g : Y ⟶ Y') (n : ℕ),
    ((singularHomologyFunctor (ModuleCat.{u} R) n).obj (ModuleCat.of R R)).map
        (Limits.prod.map f g) ≫ projection X' Y' n = projection X Y n ≫ torMap f g n

/-- Exact Lean target for THM-M-0005. -/
def KunnethFormula : Prop :=
  ∀ (R : Type u) [CommRing R] [IsDomain R] [IsPrincipalIdealRing R],
    Nonempty (NaturalKunnethSequence R)

end AwesomeTheorems.Stage1.THM_M_0005
