import Mathlib.RingTheory.NoetherNormalization
import Mathlib.AlgebraicGeometry.AffineSpace

/-!
# THM-M-0106 conditional obligation composition

This module checks the final child-to-root composition of the frozen proof
architecture.  The algebraic Noether-normalization package is an explicit
premise: this file does not claim that package or the root theorem as closed.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

namespace Stage1Instances.THM_M_0106.ObligationTree

universe u

def AlgebraicCore : Prop :=
  ∀ (k R : Type u) [Field k] [CommRing R] [Nontrivial R] [Algebra k R]
    [Algebra.FiniteType k R],
    ∃ s : Nat, ∃ g : MvPolynomial (Fin s) k →ₐ[k] R,
      Function.Injective g ∧ g.Finite

def Root : Prop :=
  ∀ (k R : Type u) [Field k] [CommRing R] [Nontrivial R] [Algebra k R]
    [Algebra.FiniteType k R],
    ∃ s : Nat, ∃ g : MvPolynomial (Fin s) k →ₐ[k] R,
      Function.Injective g ∧ g.Finite ∧
        ∃ f : Spec (CommRingCat.of R) ⟶
            AlgebraicGeometry.AffineSpace (Fin s) (Spec (CommRingCat.of k)),
          IsFinite f ∧
            f ≫ (AlgebraicGeometry.AffineSpace.SpecIso
              (Fin s) (CommRingCat.of k)).hom =
                Spec.map (CommRingCat.ofHom g.toRingHom)

def affineSpaceMorphism {k R : Type u} [Field k] [CommRing R] [Algebra k R]
    {s : Nat} (g : MvPolynomial (Fin s) k →ₐ[k] R) :
    Spec (CommRingCat.of R) ⟶
      AlgebraicGeometry.AffineSpace (Fin s) (Spec (CommRingCat.of k)) :=
  Spec.map (CommRingCat.ofHom g.toRingHom) ≫
    (AlgebraicGeometry.AffineSpace.SpecIso (Fin s) (CommRingCat.of k)).inv

/-- Exact conditional composition certificate.  It consumes the algebraic
child and derives both geometric conjuncts without another mathematical
premise. -/
theorem root_compose (algebraic : AlgebraicCore.{u}) : Root.{u} := by
  intro k R _ _ _ _ _
  obtain ⟨s, g, hg, hfinite⟩ := algebraic k R
  refine ⟨s, g, hg, hfinite, affineSpaceMorphism g, ?_, ?_⟩
  · have hspec : IsFinite (Spec.map (CommRingCat.ofHom g.toRingHom)) := by
      rw [AlgebraicGeometry.IsFinite.SpecMap_iff]
      exact hfinite
    exact MorphismProperty.RespectsIso.postcomp (P := @IsFinite)
      (AlgebraicGeometry.AffineSpace.SpecIso (Fin s) (CommRingCat.of k)).inv
      (Spec.map (CommRingCat.ofHom g.toRingHom)) hspec
  · simp [affineSpaceMorphism]

#check exists_integral_inj_algHom_of_quotient
#check exists_integral_inj_algHom_of_fg
#check exists_finite_inj_algHom_of_fg
#print axioms root_compose

end Stage1Instances.THM_M_0106.ObligationTree
