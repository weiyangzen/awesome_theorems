import Mathlib.Data.Real.Basic

/-!
# THM-M-1228: obligation-tree composition check

This file checks only the child-to-parent logical composition frozen by the
obligation registry.  It deliberately supplies no CKN analytic proof.
-/

namespace Stage1Instances.THMM1228.ObligationTree

/- The harness repeats the already-hashed statement interface because the
source dossier is outside the Lake module root. The structural checker binds
this file to `statement.json`; no duplicate declaration is imported or credited. -/
abbrev HarnessSpaceTime : Type := (Fin 3 -> Real) × Real
abbrev HarnessVelocity : Type := Fin 3 -> Real

structure HarnessSolutionData where
  domain : Set HarnessSpaceTime
  velocity : HarnessSpaceTime -> HarnessVelocity
  pressure : HarnessSpaceTime -> Real
  force : HarnessSpaceTime -> HarnessVelocity

structure HarnessSemantics where
  IsSuitableWeakSolution : HarnessSolutionData -> Prop
  RegularAt : HarnessSolutionData -> HarnessSpaceTime -> Prop
  ParabolicHausdorffOneMeasureZero : Set HarnessSpaceTime -> Prop

def HarnessSingularSet (S : HarnessSemantics) (D : HarnessSolutionData) :
    Set HarnessSpaceTime :=
  {z | z ∈ D.domain ∧ ¬ S.RegularAt D z}

def HarnessTarget (S : HarnessSemantics) : Prop :=
  ∀ D : HarnessSolutionData,
    S.IsSuitableWeakSolution D ->
      S.ParabolicHausdorffOneMeasureZero (HarnessSingularSet S D)

/-- Per-solution terminal conclusion used by the frozen proof tree. -/
def SingularMeasureConclusion (S : HarnessSemantics) (D : HarnessSolutionData) : Prop :=
  S.ParabolicHausdorffOneMeasureZero (HarnessSingularSet S D)

/-- The terminal family composes to the exact canonical root.  The analytic
content is the `perSolution` premise, which remains open for the proof phase. -/
theorem root_compose (S : HarnessSemantics)
    (perSolution : forall D : HarnessSolutionData,
      S.IsSuitableWeakSolution D -> SingularMeasureConclusion S D) :
    HarnessTarget S := by
  intro D hD
  exact perSolution D hD

theorem per_solution_expands (S : HarnessSemantics) (D : HarnessSolutionData) :
    SingularMeasureConclusion S D <->
      S.ParabolicHausdorffOneMeasureZero
        {z | z ∈ D.domain ∧ ¬ S.RegularAt D z} :=
  Iff.rfl

#print axioms root_compose

end Stage1Instances.THMM1228.ObligationTree
