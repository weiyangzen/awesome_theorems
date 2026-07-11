import Mathlib.RingTheory.NoetherNormalization
import Mathlib.AlgebraicGeometry.AffineSpace

/-!
# THM-M-0106 anchor audit probes

This module checks that the candidate at the pinned mathlib revision has the
exact algebraic type needed by the frozen target and that the affine-space
bridge composes. It is audit evidence, not an accepted proof or release claim.
-/

noncomputable section

open CategoryTheory AlgebraicGeometry

namespace Stage1Instances.THM_M_0106

universe u

/-- Audit copy of the already frozen expression. `check_anchor_audit.py`
rejects the audit if this expression differs from `Statement.lean`. -/
def FrozenTargetAuditExpression : Prop :=
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

def auditedAffineSpaceMorphism {k R : Type u} [Field k] [CommRing R] [Algebra k R]
    {s : Nat} (g : MvPolynomial (Fin s) k →ₐ[k] R) :
    Spec (CommRingCat.of R) ⟶
      AlgebraicGeometry.AffineSpace (Fin s) (Spec (CommRingCat.of k)) :=
  Spec.map (CommRingCat.ofHom g.toRingHom) ≫
    (AlgebraicGeometry.AffineSpace.SpecIso (Fin s) (CommRingCat.of k)).inv

/-- Exact-type probe for mathlib's finite Noether-normalization candidate. -/
example (k R : Type u) [Field k] [CommRing R] [Nontrivial R] [Algebra k R]
    [Algebra.FiniteType k R] :
    ∃ s : Nat, ∃ g : MvPolynomial (Fin s) k →ₐ[k] R,
      Function.Injective g ∧ g.Finite := by
  exact exists_finite_inj_algHom_of_fg k R

/-- Composition probe showing that the candidate closes the frozen target.
This declaration is deliberately local to the audit dossier. -/
theorem mathlibCandidate_closes_frozenTarget :
    FrozenTargetAuditExpression.{u} := by
  intro k R _ _ _ _ _
  obtain ⟨s, g, hg, hfinite⟩ := exists_finite_inj_algHom_of_fg k R
  refine ⟨s, g, hg, hfinite, auditedAffineSpaceMorphism g, ?_, ?_⟩
  · have hspec : IsFinite (Spec.map (CommRingCat.ofHom g.toRingHom)) := by
      rw [AlgebraicGeometry.IsFinite.SpecMap_iff]
      exact hfinite
    exact MorphismProperty.RespectsIso.postcomp (P := @IsFinite)
      (AlgebraicGeometry.AffineSpace.SpecIso (Fin s) (CommRingCat.of k)).inv
      (Spec.map (CommRingCat.ofHom g.toRingHom)) hspec
  · simp [auditedAffineSpaceMorphism]

end Stage1Instances.THM_M_0106

#check exists_integral_inj_algHom_of_fg
#check exists_finite_inj_algHom_of_fg
#check AlgebraicGeometry.IsFinite.SpecMap_iff
#check Stage1Instances.THM_M_0106.mathlibCandidate_closes_frozenTarget
#print axioms exists_integral_inj_algHom_of_fg
#print axioms exists_finite_inj_algHom_of_fg
#print axioms Stage1Instances.THM_M_0106.mathlibCandidate_closes_frozenTarget
