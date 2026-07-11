import «Stage1_Instances».«THM-M-0394».Statement

/-!
# THM-M-0394 obligation-tree composition harness

This module checks only the logical split used by the frozen architecture.  It
does not prove either substantive branch of Siegel's theorem.
-/

noncomputable section

open Stage1Rev56.THMM0394

universe u v

namespace Stage1Rev56.THMM0394.ObligationTree

/-- The positive-genus branch, kept as an explicit proof obligation. -/
def PositiveGenusBranch : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K]
    (S : FinitePrimeSet K) (C : CurveModel.{u, v} K),
    IsSiegelCurve C → 0 < C.genus → (integralPointSet S C).Finite

/-- The genus-zero, at-least-three-boundary-points branch. -/
def GenusZeroBranch : Prop :=
  ∀ (K : Type u) [Field K] [NumberField K]
    (S : FinitePrimeSet K) (C : CurveModel.{u, v} K),
    IsSiegelCurve C → C.genus = 0 → 3 ≤ C.boundaryPoints.card →
      (integralPointSet S C).Finite

/--
Checked child-to-parent composition: exact closure of the two mathematical
branches would yield the canonical statement.  The branch hypotheses remain
open and therefore this theorem supplies no proof of `Statement` by itself.
-/
theorem branch_composition
    (positive : PositiveGenusBranch.{u, v})
    (genusZero : GenusZeroBranch.{u, v}) : Statement.{u, v} := by
  intro K _ _ S C hC
  rcases hC.2.2.2.2 with hPositive | hZero
  · exact positive K S C hC hPositive
  · exact genusZero K S C hC hZero.1 hZero.2

#check branch_composition

end Stage1Rev56.THMM0394.ObligationTree
