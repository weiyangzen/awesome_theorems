import Mathlib.Dynamics.BirkhoffSum.Average
import Mathlib.Dynamics.Ergodic.Ergodic
import Mathlib.MeasureTheory.Integral.Bochner.Basic

/-!
# THM-M-1522: Birkhoff pointwise ergodic theorem statement

This module freezes the ergodic probability-space specialization selected at
intake. It elaborates the proposition only and supplies no proof of Birkhoff's
theorem.
-/

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1522

universe u

/-- For an integrable real observable on an ergodic probability-preserving
system, its finite-orbit Cesaro averages converge almost everywhere to its
space integral. `Ergodic T mu` includes measurability and preservation of
`mu`; the probability normalization is kept as an explicit typeclass binder. -/
def BirkhoffPointwiseErgodicTarget : Prop :=
  forall (X : Type u) [MeasurableSpace X] (mu : Measure X)
    [IsProbabilityMeasure mu] (T : X -> X) (f : X -> Real),
      Ergodic T mu ->
        Integrable f mu ->
          ∀ᵐ x ∂mu, Tendsto (fun n : Nat => birkhoffAverage Real T f n x)
            atTop (nhds (integral mu f))

/-- The direct finite-sum encoding of the same Cesaro averages. -/
def ExpandedFiniteSumTarget : Prop :=
  forall (X : Type u) [MeasurableSpace X] (mu : Measure X)
    [IsProbabilityMeasure mu] (T : X -> X) (f : X -> Real),
      Ergodic T mu ->
        Integrable f mu ->
          ∀ᵐ x ∂mu, Tendsto
            (fun n : Nat => (n : Real)⁻¹ *
              Finset.sum (Finset.range n) (fun k => f ((T^[k]) x)))
            atTop (nhds (integral mu f))

/-- Checked statement transport from mathlib's `birkhoffAverage` notation to
the direct finite-sum formula. No pointwise convergence theorem is used. -/
theorem birkhoffTarget_iff_expandedFiniteSumTarget :
    BirkhoffPointwiseErgodicTarget.{u} <-> ExpandedFiniteSumTarget.{u} := by
  simp only [BirkhoffPointwiseErgodicTarget, ExpandedFiniteSumTarget,
    birkhoffAverage, birkhoffSum, smul_eq_mul]

-- Separately elaborated structural mutations used by `check_statement.py`.
def mutationRemovedErgodicity : Prop :=
  forall (X : Type u) [MeasurableSpace X] (mu : Measure X)
    [IsProbabilityMeasure mu] (T : X -> X) (f : X -> Real),
      MeasurePreserving T mu mu -> Integrable f mu ->
        ∀ᵐ x ∂mu, Tendsto (fun n : Nat => birkhoffAverage Real T f n x)
          atTop (nhds (integral mu f))

def mutationRemovedIntegrability : Prop :=
  forall (X : Type u) [MeasurableSpace X] (mu : Measure X)
    [IsProbabilityMeasure mu] (T : X -> X) (f : X -> Real),
      Ergodic T mu ->
        ∀ᵐ x ∂mu, Tendsto (fun n : Nat => birkhoffAverage Real T f n x)
          atTop (nhds (integral mu f))

def mutationRemovedProbabilityNormalization : Prop :=
  forall (X : Type u) [MeasurableSpace X] (mu : Measure X)
    (T : X -> X) (f : X -> Real),
      Ergodic T mu -> Integrable f mu ->
        ∀ᵐ x ∂mu, Tendsto (fun n : Nat => birkhoffAverage Real T f n x)
          atTop (nhds (integral mu f))

def mutationPointwiseEverywhere : Prop :=
  forall (X : Type u) [MeasurableSpace X] (mu : Measure X)
    [IsProbabilityMeasure mu] (T : X -> X) (f : X -> Real),
      Ergodic T mu -> Integrable f mu ->
        forall x, Tendsto (fun n : Nat => birkhoffAverage Real T f n x)
          atTop (nhds (integral mu f))

end Stage1Instances.THM_M_1522

set_option pp.explicit true in
#print Stage1Instances.THM_M_1522.BirkhoffPointwiseErgodicTarget
