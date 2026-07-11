import Mathlib.RingTheory.DedekindDomain.Factorization

/-!
# THM-M-0414 obligation-tree composition surface

This module checks the exact two-component decomposition of the frozen target.
The component propositions are explicit premises, so this is architecture evidence
rather than proof-node closure.
-/

noncomputable section

namespace Stage1Instances.THM_M_0414.ObligationTree

universe u

def Root : Prop :=
  forall (R : Type u) [CommRing R] [IsDedekindDomain R],
    UniqueFactorizationMonoid (Ideal R) /\
      forall {I : Ideal R}, I != 0 ->
        ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum R, v.maxPowDividing I = I

def UFMComponent : Prop :=
  forall (R : Type u) [CommRing R] [IsDedekindDomain R],
    UniqueFactorizationMonoid (Ideal R)

def FiniteProductComponent : Prop :=
  forall (R : Type u) [CommRing R] [IsDedekindDomain R] {I : Ideal R}, I != 0 ->
    ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum R, v.maxPowDividing I = I

theorem root_exact_type :
    Root.{u} =
      (forall (R : Type u) [CommRing R] [IsDedekindDomain R],
        UniqueFactorizationMonoid (Ideal R) /\
          forall {I : Ideal R}, I != 0 ->
            ∏ᶠ v : IsDedekindDomain.HeightOneSpectrum R, v.maxPowDividing I = I) :=
  rfl

/-- Checked child-to-parent composition. Its arguments keep both proof bodies open. -/
theorem components_compose
    (hUFM : UFMComponent.{u}) (hProduct : FiniteProductComponent.{u}) : Root.{u} := by
  intro R _ _
  exact ⟨hUFM R, fun hI => hProduct R hI⟩

#check Ideal.uniqueFactorizationMonoid
#check Ideal.finprod_heightOneSpectrum_factorization
#print axioms components_compose

end Stage1Instances.THM_M_0414.ObligationTree
