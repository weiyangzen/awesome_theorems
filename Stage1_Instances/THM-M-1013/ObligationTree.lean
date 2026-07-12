import Mathlib.MeasureTheory.Measure.LevyConvergence
import Mathlib.Analysis.InnerProductSpace.PiL2

/-!
# THM-M-1013 obligation composition

This module checks the child-to-parent composition for the two directions of
the frozen Cramer-Wold biconditional. The direction arguments are deliberately
abstract: constructing them belongs to the proof phase.
-/

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1013.ObligationTree

noncomputable section

abbrev Vector (d : Nat) := EuclideanSpace Real (Fin d)

def projection {d : Nat} (t x : Vector d) : Real := inner Real x t

lemma continuous_projection {d : Nat} (t : Vector d) : Continuous (projection t) := by
  unfold projection
  exact continuous_id.inner continuous_const

def WeakLimit {d : Nat}
    (mu : Nat -> ProbabilityMeasure (Vector d))
    (mu0 : ProbabilityMeasure (Vector d)) : Prop :=
  Tendsto mu atTop (nhds mu0)

def ProjectedLimits {d : Nat} (mu : Nat -> ProbabilityMeasure (Vector d))
    (mu0 : ProbabilityMeasure (Vector d)) : Prop :=
  forall t : Vector d,
    Tendsto
      (fun n => (mu n).map ((continuous_projection t).measurable.aemeasurable))
      atTop
      (nhds (mu0.map ((continuous_projection t).measurable.aemeasurable)))

def ExactTarget : Prop :=
  forall (d : Nat) (mu : Nat -> ProbabilityMeasure (Vector d))
      (mu0 : ProbabilityMeasure (Vector d)),
    WeakLimit (d := d) mu mu0 <-> ProjectedLimits (d := d) mu mu0

/-- Exact composition certificate: both directional children are consumed. -/
theorem compose_directions
    (forward : forall (d : Nat) (mu : Nat -> ProbabilityMeasure (Vector d))
      (mu0 : ProbabilityMeasure (Vector d)),
      WeakLimit (d := d) mu mu0 -> ProjectedLimits (d := d) mu mu0)
    (reverse : forall (d : Nat) (mu : Nat -> ProbabilityMeasure (Vector d))
      (mu0 : ProbabilityMeasure (Vector d)),
      ProjectedLimits (d := d) mu mu0 -> WeakLimit (d := d) mu mu0) :
    ExactTarget := by
  intro d mu mu0
  exact ⟨forward d mu mu0, reverse d mu mu0⟩

/-- The zero-dimensional case remains inside the universally quantified root. -/
theorem zero_dimension_boundary
    (h : ExactTarget) (mu : Nat -> ProbabilityMeasure (Vector 0))
      (mu0 : ProbabilityMeasure (Vector 0)) :
    WeakLimit (d := 0) mu mu0 <-> ProjectedLimits (d := 0) mu mu0 :=
  h 0 mu mu0

#check compose_directions
#check zero_dimension_boundary
#print axioms compose_directions
#print axioms zero_dimension_boundary

end

end Stage1Instances.THM_M_1013.ObligationTree
