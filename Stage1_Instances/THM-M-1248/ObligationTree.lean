import Statement

/-!
# THM-M-1248 conditional root composition

This module checks the final interface of the frozen obligation tree.  The
analytic package is deliberately an explicit premise: no Caffarelli-Kohn-
Nirenberg estimate is claimed here.
-/

namespace Stage1Instances.THM_M_1248

/-- Output expected from the open analytic subtree, with exactly the public
target's binders and conclusion. -/
def CKNAnalyticPackage : Prop :=
  forall (n : Nat) (p q r alpha beta gamma sigma a : Real),
    AdmissibleParameters n p q r alpha beta gamma sigma a ->
    exists C : Real, 0 < C /\
      forall u : EuclideanSpace Real (Fin n) -> Real,
        ContDiff Real ⊤ u -> HasCompactSupport u ->
        weightedLp r gamma u <=
          C * (weightedDerivativeLp p alpha u) ^ a *
            (weightedLp q beta u) ^ (1 - a)

/-- Exact child-to-root composition.  This consumes rather than constructs
the substantive analytic package. -/
theorem caffarelliKohnNirenbergTarget_of_analyticPackage
    (analytic : CKNAnalyticPackage) : CaffarelliKohnNirenbergTarget := by
  exact analytic

#print axioms caffarelliKohnNirenbergTarget_of_analyticPackage

end Stage1Instances.THM_M_1248
