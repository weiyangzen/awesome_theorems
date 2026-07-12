import Mathlib.MeasureTheory.Measure.LevyConvergence
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
# THM-M-1013: Cramer-Wold convergence device

This file freezes the exact finite-dimensional probability-measure statement. It
contains no proof of the Cramer-Wold theorem.
-/

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1013

noncomputable section

/-- The finite-dimensional real coordinate space, including dimension zero. -/
abbrev Vector (d : Nat) := EuclideanSpace Real (Fin d)

/-- The scalar projection with coefficient vector `t`. -/
def projection {d : Nat} (t x : Vector d) : Real := inner Real x t

lemma continuous_projection {d : Nat} (t : Vector d) : Continuous (projection t) := by
  unfold projection
  exact continuous_id.inner continuous_const

/--
The Cramer-Wold convergence device: weak convergence of finite-dimensional
probability measures is equivalent to weak convergence of every scalar linear
pushforward.
-/
def StatementShape : Prop :=
  ∀ (d : Nat) (mu : Nat -> ProbabilityMeasure (Vector d))
      (mu0 : ProbabilityMeasure (Vector d)),
    Tendsto mu atTop (nhds mu0) <->
      ∀ t : Vector d,
        Tendsto
          (fun n => (mu n).map ((continuous_projection t).measurable.aemeasurable))
          atTop
          (nhds (mu0.map ((continuous_projection t).measurable.aemeasurable)))

/-- Checked unfolding of the named canonical statement. -/
theorem canonicalStatement_iff :
    StatementShape <->
      ∀ (d : Nat) (mu : Nat -> ProbabilityMeasure (Vector d))
          (mu0 : ProbabilityMeasure (Vector d)),
        Tendsto mu atTop (nhds mu0) <->
          ∀ t : Vector d,
            Tendsto
              (fun n => (mu n).map ((continuous_projection t).measurable.aemeasurable))
              atTop
              (nhds (mu0.map ((continuous_projection t).measurable.aemeasurable))) :=
  Iff.rfl

/-! Structural mutations used only to check the frozen statement boundary. -/

def MutationReverseOnly : Prop :=
  ∀ (d : Nat) (mu : Nat -> ProbabilityMeasure (Vector d))
      (mu0 : ProbabilityMeasure (Vector d)),
    (∀ t : Vector d,
        Tendsto
          (fun n => (mu n).map ((continuous_projection t).measurable.aemeasurable))
          atTop
          (nhds (mu0.map ((continuous_projection t).measurable.aemeasurable)))) ->
      Tendsto mu atTop (nhds mu0)

def MutationSingleProjection : Prop :=
  ∀ (d : Nat) (mu : Nat -> ProbabilityMeasure (Vector d))
      (mu0 : ProbabilityMeasure (Vector d)) (t : Vector d),
    Tendsto mu atTop (nhds mu0) <->
      Tendsto
        (fun n => (mu n).map ((continuous_projection t).measurable.aemeasurable))
        atTop
        (nhds (mu0.map ((continuous_projection t).measurable.aemeasurable)))

def MutationPositiveDimension : Prop :=
  ∀ (d : Nat), 0 < d ->
    ∀ (mu : Nat -> ProbabilityMeasure (Vector d))
      (mu0 : ProbabilityMeasure (Vector d)),
      Tendsto mu atTop (nhds mu0) <->
        ∀ t : Vector d,
          Tendsto
            (fun n => (mu n).map ((continuous_projection t).measurable.aemeasurable))
            atTop
            (nhds (mu0.map ((continuous_projection t).measurable.aemeasurable)))

#print StatementShape

end

end Stage1Instances.THM_M_1013
