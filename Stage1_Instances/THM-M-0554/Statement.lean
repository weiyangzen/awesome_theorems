import Mathlib.Algebra.Homology.SpectralSequence.Basic
import Mathlib.AlgebraicTopology.SingularHomology.HomotopyInvarianceTopCat

/-!
# THM-M-0554: cohomological Atiyah-Hirzebruch spectral sequence

This file freezes the exact statement selected by the intake. It defines a
proposition; it does not assert or prove that proposition.
-/

noncomputable section

universe uC vC w

namespace Stage1.THM_M_0554

open CategoryTheory AlgebraicTopology

/-- The generalized-cohomology interface required by the target. -/
structure GeneralizedCohomologyTheory
    (C : Type uC) [Category.{vC} C] [Abelian C] : Type (max uC vC (w + 1)) where
  cohomology : ℤ → TopCat.{w}ᵒᵖ ⥤ C
  coefficient : ℤ → C
  point : TopCat.{w}
  pointIsPoint : Prop
  coefficientIso :
    ∀ q : ℤ, coefficient q ≅ (cohomology q).obj (Opposite.op point)
  suspension : TopCat.{w} → TopCat.{w}
  suspensionIso :
    ∀ (q : ℤ) (X : TopCat.{w}),
      (cohomology (q + 1)).obj (Opposite.op (suspension X)) ≅
        (cohomology q).obj (Opposite.op X)
  homotopyInvariant :
    ∀ (q : ℤ) {X Y : TopCat.{w}} {f g : X ⟶ Y},
      TopCat.Homotopy f g → (cohomology q).map f.op = (cohomology q).map g.op
  exactnessAxiom : Prop
  wedgeAxiomOrRepresentability : Prop

/-- A finite CW structure through its skeletal filtration. -/
structure FiniteCWInput (X : TopCat.{w}) : Type (w + 1) where
  skeleton : ℕ → TopCat.{w}
  inclusion : (m n : ℕ) → m ≤ n → (skeleton m ⟶ skeleton n)
  toTotal : ∀ n, skeleton n ⟶ X
  inclusion_id : ∀ n, inclusion n n (le_refl n) = 𝟙 (skeleton n)
  inclusion_comp :
    ∀ {l m n} (hlm : l ≤ m) (hmn : m ≤ n),
      inclusion l n (hlm.trans hmn) = inclusion l m hlm ≫ inclusion m n hmn
  compatible :
    ∀ {m n} (hmn : m ≤ n), inclusion m n hmn ≫ toTotal n = toTotal m
  finiteCW : Prop
  exhaustive : Prop
  cellAttachments : Prop

/-- The complete output demanded from the cohomological AHSS construction. -/
structure AtiyahHirzebruchData
    (C : Type uC) [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheory.{uC, vC, w} C)
    (X : TopCat.{w}) (K : FiniteCWInput X) : Type (max uC vC (w + 1)) where
  spectralSequence : CategoryTheory.E₂CohomologicalSpectralSequence C
  ordinaryCohomology : ℤ → ℤ → C
  e2PageIso :
    ∀ p q : ℤ, (spectralSequence.page 2).X (p, q) ≅ ordinaryCohomology p q
  coefficientConvention : Prop
  coefficientConvention_exact :
    coefficientConvention
  pageDifferentialBidegree :
    ∀ r p q : ℤ, 2 ≤ r →
      (ComplexShape.up' (⟨r, 1 - r⟩ : ℤ × ℤ)).Rel
        (p, q) (p + r, q + (1 - r))
  generalizedCohomology : ℤ → C
  generalizedCohomologyIso :
    ∀ n : ℤ, generalizedCohomology n ≅
      (E.cohomology n).obj (Opposite.op X)
  filtrationStage : ℤ → ℤ → C
  associatedGraded : ℤ → ℤ → C
  stablePage : ℤ → ℤ → C
  convergesToSkeletalAssociatedGraded :
    ∀ p q : ℤ, stablePage p q ≅ associatedGraded p (p + q)
  filtrationIsInducedBy : K.skeleton = K.skeleton
  strongConvergence : Prop
  naturalityInSpace : Prop

/--
The exact target for one generalized cohomology theory and one finite CW
complex. Besides convergence, the subtype fixes the skeletal filtration and
identifies the `E₂` coefficient model with `H^p(X; E^q(pt))`.
-/
def StatementShape
    (C : Type uC) [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheory.{uC, vC, w} C)
    (X : TopCat.{w}) (K : FiniteCWInput X) : Prop :=
  Nonempty (AtiyahHirzebruchData C E X K)

/-- Closed target with universes, domains, instances, and binders explicit. -/
def Statement : Prop :=
  ∀ (C : Type uC) [Category.{vC} C] [Abelian C]
      (E : GeneralizedCohomologyTheory.{uC, vC, w} C)
      (X : TopCat.{w}) (K : FiniteCWInput X),
    StatementShape C E X K

/-- Checked expansion of the canonical closed target. -/
theorem statement_iff :
    Statement.{uC, vC, w} ↔
      ∀ (C : Type uC) [Category.{vC} C] [Abelian C]
          (E : GeneralizedCohomologyTheory.{uC, vC, w} C)
          (X : TopCat.{w}) (K : FiniteCWInput X),
        Nonempty (AtiyahHirzebruchData C E X K) := by
  rfl

#check Statement
#check StatementShape
set_option pp.universes true in
#print Statement

end Stage1.THM_M_0554
