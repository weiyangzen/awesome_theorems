import Statement

/-!
# THM-M-0118 conditional obligation composition

This file checks the final logical interface of the frozen proof architecture.
The analytic Nakano package is an explicit premise: this module does not prove
that package or the root theorem.
-/

namespace Stage1Instances.THMM0118

universe uX uE uH

/-- Output required from the missing Dolbeault-Hodge and curvature argument. -/
def AnalyticNakanoPackage : Prop :=
  forall (D : NakanoVanishingData.{uX, uE, uH}) (p q : Nat),
    D.compactKahler ->
    D.holomorphicVectorBundle ->
    D.nakanoPositive ->
    D.complexDimension < p + q ->
    Subsingleton (D.Cohomology p q)

/-- Checked composition from the explicit analytic package to the exact root. -/
theorem nakanoVanishingTarget_of_analyticPackage
    (analytic : AnalyticNakanoPackage.{uX, uE, uH}) :
    NakanoVanishingTarget.{uX, uE, uH} := by
  intro D p q hKahler hBundle hPositive hDegree
  exact analytic D p q hKahler hBundle hPositive hDegree

theorem analyticPackage_iff_target :
    AnalyticNakanoPackage.{uX, uE, uH} <->
      NakanoVanishingTarget.{uX, uE, uH} :=
  Iff.rfl

#print axioms nakanoVanishingTarget_of_analyticPackage
#print axioms analyticPackage_iff_target

end Stage1Instances.THMM0118
