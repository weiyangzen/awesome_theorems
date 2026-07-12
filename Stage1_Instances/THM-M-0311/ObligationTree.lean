import Mathlib.MeasureTheory.Function.LpSpace.Complete

/-!
# THM-M-0311 obligation-tree composition probe

This module checks only the typed decomposition and recomposition of the frozen target. The two
scalar premises are intentionally parameters: admitting the pinned mathlib bodies belongs to the
proof phase.
-/

namespace Stage1Instances.THM_M_0311

open MeasureTheory
open scoped ENNReal

universe u

def ObligationTreeTarget : Prop :=
  forall (alpha : Type u) [MeasurableSpace alpha] (mu : Measure alpha),
    CompleteSpace (Lp Real (2 : ENNReal) mu) /\
      CompleteSpace (Lp Complex (2 : ENNReal) mu)

def RealL2Complete : Prop :=
  forall (alpha : Type u) [MeasurableSpace alpha] (mu : Measure alpha),
    CompleteSpace (Lp Real (2 : ENNReal) mu)

def ComplexL2Complete : Prop :=
  forall (alpha : Type u) [MeasurableSpace alpha] (mu : Measure alpha),
    CompleteSpace (Lp Complex (2 : ENNReal) mu)

/-- Checked child-to-parent composition; this does not discharge either scalar premise. -/
theorem obligationTreeTarget_of_scalar_children
    (hReal : RealL2Complete.{u}) (hComplex : ComplexL2Complete.{u}) :
    ObligationTreeTarget.{u} := by
  intro alpha _ mu
  exact ⟨hReal alpha mu, hComplex alpha mu⟩

end Stage1Instances.THM_M_0311

#check MeasureTheory.Lp.completeSpace_lp_of_cauchy_complete_eLpNorm
#check MeasureTheory.Lp.cauchy_complete_eLpNorm
#check MeasureTheory.Lp.instCompleteSpace
#print axioms Stage1Instances.THM_M_0311.obligationTreeTarget_of_scalar_children
