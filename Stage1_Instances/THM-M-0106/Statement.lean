import Mathlib.AlgebraicGeometry.AffineSpace

/-!
# THM-M-0106: exact Noether-normalization statement

This module freezes and tests the affine coordinate-ring statement boundary.
It contains no proof of Noether normalization.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

namespace Stage1Instances.THM_M_0106

universe u

/-- Coordinate-ring Noether normalization: a nonzero finite-type algebra over
a field is finite over an injectively embedded polynomial algebra. -/
def AlgebraicNoetherNormalizationTarget : Prop :=
  ∀ (k R : Type u) [Field k] [CommRing R] [Nontrivial R] [Algebra k R]
    [Algebra.FiniteType k R],
    ∃ s : Nat, ∃ g : MvPolynomial (Fin s) k →ₐ[k] R,
      Function.Injective g ∧ g.Finite

/-- The exact public target selected from the intake scope: the algebraic
normalization map together with its induced finite morphism from `Spec R` to
the corresponding affine space. -/
def NoetherNormalizationTarget : Prop :=
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

/-- The historical affine-Spec candidate, restated locally so statement
identity can be checked without importing the legacy proof module. -/
def PinnedAffineSpecCandidateShape : Prop :=
  ∀ (k R : Type u) [Field k] [CommRing R] [Nontrivial R] [Algebra k R]
    [Algebra.FiniteType k R],
    ∃ s : Nat, ∃ g : MvPolynomial (Fin s) k →ₐ[k] R,
      Function.Injective g ∧ g.Finite ∧
        IsFinite (Spec.map (CommRingCat.ofHom g.toRingHom))

/-- The explicit affine-space morphism induced contravariantly by an algebra
map, followed by the standard affine-space identification. -/
def affineSpaceMorphism {k R : Type u} [Field k] [CommRing R] [Algebra k R]
    {s : Nat} (g : MvPolynomial (Fin s) k →ₐ[k] R) :
    Spec (CommRingCat.of R) ⟶
      AlgebraicGeometry.AffineSpace (Fin s) (Spec (CommRingCat.of k)) :=
  Spec.map (CommRingCat.ofHom g.toRingHom) ≫
    (AlgebraicGeometry.AffineSpace.SpecIso (Fin s) (CommRingCat.of k)).inv

/-- Checked transport from the historical affine-Spec encoding to the exact
affine-space target. This proves only equivalence of statement encodings. -/
theorem target_iff_pinnedAffineSpecCandidateShape :
    NoetherNormalizationTarget.{u} ↔ PinnedAffineSpecCandidateShape.{u} := by
  constructor
  · intro h k R _ _ _ _ _
    obtain ⟨s, g, hg, hfinite, _f, _hf, _hfg⟩ := h k R
    refine ⟨s, g, hg, hfinite, ?_⟩
    rw [AlgebraicGeometry.IsFinite.SpecMap_iff]
    exact hfinite
  · intro h k R _ _ _ _ _
    obtain ⟨s, g, hg, hfinite, hspec⟩ := h k R
    refine ⟨s, g, hg, hfinite, affineSpaceMorphism g, ?_, ?_⟩
    · exact MorphismProperty.RespectsIso.postcomp (P := @IsFinite)
        (AlgebraicGeometry.AffineSpace.SpecIso (Fin s) (CommRingCat.of k)).inv
        (Spec.map (CommRingCat.ofHom g.toRingHom)) hspec
    · simp [affineSpaceMorphism]

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedNontrivial : Prop :=
  ∀ (k R : Type u) [Field k] [CommRing R] [Algebra k R]
    [Algebra.FiniteType k R],
    ∃ s : Nat, ∃ g : MvPolynomial (Fin s) k →ₐ[k] R,
      Function.Injective g ∧ g.Finite ∧
        ∃ f : Spec (CommRingCat.of R) ⟶
            AlgebraicGeometry.AffineSpace (Fin s) (Spec (CommRingCat.of k)),
          IsFinite f

def mutationChangedBaseDomain : Prop :=
  ∀ (R : Type u) [CommRing R] [Nontrivial R] [Algebra Rat R]
    [Algebra.FiniteType Rat R],
    ∃ s : Nat, ∃ g : MvPolynomial (Fin s) Rat →ₐ[Rat] R,
      Function.Injective g ∧ g.Finite

def mutationChangedBinderScope : Prop :=
  ∀ (k : Type u) [Field k],
    ∃ s : Nat, ∀ (R : Type u) [CommRing R] [Nontrivial R] [Algebra k R]
      [Algebra.FiniteType k R],
      ∃ g : MvPolynomial (Fin s) k →ₐ[k] R,
        Function.Injective g ∧ g.Finite

def mutationDroppedFiniteMorphism : Prop :=
  AlgebraicNoetherNormalizationTarget.{u}

/-- The variable count is a natural number, so the exact target includes the
zero-variable polynomial algebra boundary. -/
example : Nonempty (Fin 0 → Nat) := ⟨fun i => Fin.elim0 i⟩

end Stage1Instances.THM_M_0106

set_option pp.explicit true in
#print Stage1Instances.THM_M_0106.NoetherNormalizationTarget
