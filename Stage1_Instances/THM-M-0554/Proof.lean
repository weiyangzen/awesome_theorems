import Statement

/-!
# THM-M-0554 conditional proof composition

This file checks how the four frozen output branches recompose into the
literal target. It does not construct any branch and therefore is not a proof
of the Atiyah-Hirzebruch spectral sequence.
-/

noncomputable section

universe uC vC w

namespace Stage1.THM_M_0554.Proof

open CategoryTheory AlgebraicTopology
open Stage1.THM_M_0554

/-- Data supplied by the frozen `E2` branch. -/
structure E2Branch
    (C : Type uC) [Category.{vC} C] [Abelian C] where
  spectralSequence : CategoryTheory.E₂CohomologicalSpectralSequence C
  ordinaryCohomology : ℤ → ℤ → C
  e2PageIso :
    ∀ p q : ℤ, (spectralSequence.page 2).X (p, q) ≅ ordinaryCohomology p q
  coefficientConvention : Prop
  coefficientConvention_exact : coefficientConvention

/-- Data supplied by the frozen differential branch. -/
structure DifferentialBranch : Type where
  pageDifferentialBidegree :
    ∀ r p q : ℤ, 2 ≤ r →
      (ComplexShape.up' (⟨r, 1 - r⟩ : ℤ × ℤ)).Rel
        (p, q) (p + r, q + (1 - r))

/-- Data supplied by the frozen convergence branch. -/
structure ConvergenceBranch
    (C : Type uC) [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheory.{uC, vC, w} C)
    (X : TopCat.{w}) (K : FiniteCWInput X) where
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

/-- Data supplied by the frozen naturality branch. -/
structure NaturalityBranch : Type where
  naturalityInSpace : Prop

/-- Conditional child-to-parent composition. Every field of the literal
output is consumed from one of the four explicit branch packages. -/
def dataOfBranches
    (C : Type uC) [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheory.{uC, vC, w} C)
    (X : TopCat.{w}) (K : FiniteCWInput X)
    (e2 : E2Branch C)
    (differential : DifferentialBranch)
    (convergence : ConvergenceBranch C E X K)
    (naturality : NaturalityBranch) :
    AtiyahHirzebruchData C E X K where
  spectralSequence := e2.spectralSequence
  ordinaryCohomology := e2.ordinaryCohomology
  e2PageIso := e2.e2PageIso
  coefficientConvention := e2.coefficientConvention
  coefficientConvention_exact := e2.coefficientConvention_exact
  pageDifferentialBidegree := differential.pageDifferentialBidegree
  generalizedCohomology := convergence.generalizedCohomology
  generalizedCohomologyIso := convergence.generalizedCohomologyIso
  filtrationStage := convergence.filtrationStage
  associatedGraded := convergence.associatedGraded
  stablePage := convergence.stablePage
  convergesToSkeletalAssociatedGraded :=
    convergence.convergesToSkeletalAssociatedGraded
  filtrationIsInducedBy := convergence.filtrationIsInducedBy
  strongConvergence := convergence.strongConvergence
  naturalityInSpace := naturality.naturalityInSpace

/-- Package a conditionally recomposed data record as the frozen local target. -/
theorem statementShapeOfBranches
    (C : Type uC) [Category.{vC} C] [Abelian C]
    (E : GeneralizedCohomologyTheory.{uC, vC, w} C)
    (X : TopCat.{w}) (K : FiniteCWInput X)
    (e2 : E2Branch C)
    (differential : DifferentialBranch)
    (convergence : ConvergenceBranch C E X K)
    (naturality : NaturalityBranch) :
    StatementShape C E X K :=
  ⟨dataOfBranches C E X K e2 differential convergence naturality⟩

/-- Exact conditional root composition. The four branch families remain an
explicit premise and are not asserted in this module. -/
theorem statementOfBranchFamily
    (branches :
      ∀ (C : Type uC) [Category.{vC} C] [Abelian C]
        (E : GeneralizedCohomologyTheory.{uC, vC, w} C)
        (X : TopCat.{w}) (K : FiniteCWInput X),
        E2Branch C × DifferentialBranch ×
          ConvergenceBranch C E X K × NaturalityBranch) :
    Statement.{uC, vC, w} := by
  intro C _ _ E X K
  obtain ⟨e2, differential, convergence, naturality⟩ := branches C E X K
  exact statementShapeOfBranches C E X K e2 differential convergence naturality

#print axioms dataOfBranches
#print axioms statementShapeOfBranches
#print axioms statementOfBranchFamily
#print sorries dataOfBranches
#print sorries statementShapeOfBranches
#print sorries statementOfBranchFamily

end Stage1.THM_M_0554.Proof
