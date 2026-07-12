import Mathlib.MeasureTheory.Function.ConvergenceInDistribution
import Mathlib.Analysis.Calculus.FDeriv.Defs

/-!
# THM-M-1016 canonical statement

This module freezes the finite-dimensional Frechet-derivative form of the delta method. It
declares proposition-valued statement and mutation probes; it does not prove the proposition.
-/

noncomputable section

open Filter MeasureTheory
open scoped Topology

namespace Stage1Instances.THM_M_1016

universe u v w

/-- The finite-dimensional delta method for a positive real scaling sequence. -/
def StatementShape : Prop :=
  forall (Omega : Type u) (Omega' : Type v)
    [MeasurableSpace Omega] [MeasurableSpace Omega']
    (mu : Measure Omega) (mu' : Measure Omega')
    [IsProbabilityMeasure mu] [IsProbabilityMeasure mu']
    (E : Type w) (F : Type*)
    [NormedAddCommGroup E] [NormedSpace Real E] [FiniteDimensional Real E]
    [MeasurableSpace E] [BorelSpace E]
    [NormedAddCommGroup F] [NormedSpace Real F] [FiniteDimensional Real F]
    [MeasurableSpace F] [BorelSpace F]
    (X : Nat -> Omega -> E) (Z : Omega' -> E) (theta : E)
    (r : Nat -> Real) (hr_pos : forall n, 0 < r n) (hr_inf : Tendsto r atTop atTop)
    (g : E -> F) (g' : E →L[ℝ] F) (hg_meas : Measurable g)
    (hg_diff : HasFDerivAt g g' theta),
    TendstoInDistribution
        (fun n omega => r n • (X n omega - theta)) atTop Z (fun _ => mu) mu' ->
      TendstoInDistribution
        (fun n omega => r n • (g (X n omega) - g theta)) atTop
        (fun omega => g' (Z omega)) (fun _ => mu) mu'

/-- Removed-hypothesis mutation: omit divergence of the scaling sequence. -/
def MutationNoScalingLimit : Prop :=
  forall (Omega : Type u) (Omega' : Type v)
    [MeasurableSpace Omega] [MeasurableSpace Omega']
    (mu : Measure Omega) (mu' : Measure Omega')
    [IsProbabilityMeasure mu] [IsProbabilityMeasure mu']
    (E : Type w) (F : Type*)
    [NormedAddCommGroup E] [NormedSpace Real E] [FiniteDimensional Real E]
    [MeasurableSpace E] [BorelSpace E]
    [NormedAddCommGroup F] [NormedSpace Real F] [FiniteDimensional Real F]
    [MeasurableSpace F] [BorelSpace F]
    (X : Nat -> Omega -> E) (Z : Omega' -> E) (theta : E)
    (r : Nat -> Real) (hr_pos : forall n, 0 < r n)
    (g : E -> F) (g' : E →L[ℝ] F) (hg_meas : Measurable g)
    (hg_diff : HasFDerivAt g g' theta),
    TendstoInDistribution
        (fun n omega => r n • (X n omega - theta)) atTop Z (fun _ => mu) mu' ->
      TendstoInDistribution
        (fun n omega => r n • (g (X n omega) - g theta)) atTop
        (fun omega => g' (Z omega)) (fun _ => mu) mu'

/-- Changed-domain mutation: restrict both vector spaces to the real line. -/
def MutationRealDomain : Prop :=
  forall (Omega : Type u) (Omega' : Type v)
    [MeasurableSpace Omega] [MeasurableSpace Omega']
    (mu : Measure Omega) (mu' : Measure Omega')
    [IsProbabilityMeasure mu] [IsProbabilityMeasure mu']
    (X : Nat -> Omega -> Real) (Z : Omega' -> Real) (theta : Real)
    (r : Nat -> Real) (hr_pos : forall n, 0 < r n) (hr_inf : Tendsto r atTop atTop)
    (g : Real -> Real) (g' : Real →L[ℝ] Real) (hg_meas : Measurable g)
    (hg_diff : HasFDerivAt g g' theta),
    TendstoInDistribution
        (fun n omega => r n * (X n omega - theta)) atTop Z (fun _ => mu) mu' ->
      TendstoInDistribution
        (fun n omega => r n * (g (X n omega) - g theta)) atTop
        (fun omega => g' (Z omega)) (fun _ => mu) mu'

/-- Binder-scope mutation: allow a different centering point at every index. -/
def MutationVaryingCenter : Prop :=
  forall (Omega : Type u) (Omega' : Type v)
    [MeasurableSpace Omega] [MeasurableSpace Omega']
    (mu : Measure Omega) (mu' : Measure Omega')
    [IsProbabilityMeasure mu] [IsProbabilityMeasure mu']
    (E : Type w) (F : Type*)
    [NormedAddCommGroup E] [NormedSpace Real E] [FiniteDimensional Real E]
    [MeasurableSpace E] [BorelSpace E]
    [NormedAddCommGroup F] [NormedSpace Real F] [FiniteDimensional Real F]
    [MeasurableSpace F] [BorelSpace F]
    (X : Nat -> Omega -> E) (Z : Omega' -> E) (theta : Nat -> E)
    (r : Nat -> Real) (hr_pos : forall n, 0 < r n) (hr_inf : Tendsto r atTop atTop)
    (g : E -> F) (g' : E →L[ℝ] F) (hg_meas : Measurable g)
    (hg_diff : forall n, HasFDerivAt g g' (theta n)),
    TendstoInDistribution
        (fun n omega => r n • (X n omega - theta n)) atTop Z (fun _ => mu) mu' ->
      TendstoInDistribution
        (fun n omega => r n • (g (X n omega) - g (theta n))) atTop
        (fun omega => g' (Z omega)) (fun _ => mu) mu'

/-- Boundary mutation: permit the identically-zero scaling sequence. -/
def MutationZeroScaling : Prop :=
  forall (Omega : Type u) (Omega' : Type v)
    [MeasurableSpace Omega] [MeasurableSpace Omega']
    (mu : Measure Omega) (mu' : Measure Omega')
    [IsProbabilityMeasure mu] [IsProbabilityMeasure mu']
    (E : Type w) (F : Type*)
    [NormedAddCommGroup E] [NormedSpace Real E] [FiniteDimensional Real E]
    [MeasurableSpace E] [BorelSpace E]
    [NormedAddCommGroup F] [NormedSpace Real F] [FiniteDimensional Real F]
    [MeasurableSpace F] [BorelSpace F]
    (X : Nat -> Omega -> E) (Z : Omega' -> E) (theta : E)
    (g : E -> F) (g' : E →L[ℝ] F) (hg_meas : Measurable g)
    (hg_diff : HasFDerivAt g g' theta),
    TendstoInDistribution
        (fun (_ : Nat) (_ : Omega) => (0 : E)) atTop Z (fun _ => mu) mu' ->
      TendstoInDistribution
        (fun (_ : Nat) (_ : Omega) => (0 : F)) atTop
        (fun omega => g' (Z omega)) (fun _ => mu) mu'

#check StatementShape
#print StatementShape
#print MutationNoScalingLimit
#print MutationRealDomain
#print MutationVaryingCenter
#print MutationZeroScaling

end Stage1Instances.THM_M_1016
