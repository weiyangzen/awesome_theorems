import Mathlib.Analysis.InnerProductSpace.MeanErgodic
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Function.LpSpace.Basic

/-!
# THM-M-1054: exact von Neumann L2 mean-ergodic statement

This module freezes the statement boundary selected at intake. It does not
prove the theorem.
-/

noncomputable section

open Filter MeasureTheory
open scoped ENNReal Topology

namespace Stage1Instances.THM_M_1054

universe u

/-- Real-valued `L^2` observables modulo almost-everywhere equality. -/
abbrev RealL2 (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega) :=
  Lp Real (2 : ENNReal) mu

/-- The Koopman operator induced on real `L^2` by a measure-preserving map. -/
abbrev Koopman {Omega : Type u} [MeasurableSpace Omega] {mu : Measure Omega}
    (T : Omega -> Omega) (hT : MeasurePreserving T mu mu) :=
  (Lp.compMeasurePreservingₗᵢ Real (E := Real) (p := (2 : ENNReal)) T hT).toContinuousLinearMap

/-- The first `n` Koopman iterates, normalized by `n`; at `n = 0` mathlib's
convention gives the zero average. -/
abbrev CesaroAverage {Omega : Type u} [MeasurableSpace Omega] {mu : Measure Omega}
    (T : Omega -> Omega) (hT : MeasurePreserving T mu mu) :
    Nat -> RealL2 Omega mu -> RealL2 Omega mu :=
  birkhoffAverage Real (Koopman T hT) _root_.id

/-- Orthogonal projection onto the closed subspace of Koopman-fixed vectors. -/
abbrev InvariantProjection {Omega : Type u} [MeasurableSpace Omega]
    {mu : Measure Omega} (T : Omega -> Omega)
    (hT : MeasurePreserving T mu mu) (f : RealL2 Omega mu) : RealL2 Omega mu :=
  ((LinearMap.eqLocus (Koopman T hT) 1).orthogonalProjection (𝕜 := Real) f : RealL2 Omega mu)

/-- The exact intake-selected probability-space, real-valued `L^2` form of
von Neumann's mean ergodic theorem. -/
def VonNeumannL2MeanErgodicTarget : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (T : Omega -> Omega) (hT : MeasurePreserving T mu mu)
    (f : RealL2 Omega mu),
      Tendsto (fun n : Nat => CesaroAverage T hT n f) atTop
        (nhds (InvariantProjection T hT f))

/-- A second canonical name for the selected intake shape, used to check that
the public target name introduces no additional assumptions. -/
def ExpandedIntakeShape : Prop :=
  VonNeumannL2MeanErgodicTarget.{u}

theorem target_iff_expandedIntakeShape :
    VonNeumannL2MeanErgodicTarget.{u} <-> ExpandedIntakeShape.{u} := by
  rfl

-- Separately elaborated, deliberately non-equivalent structural mutations.
def mutationRemovedProbabilityHypothesis : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega)
    (T : Omega -> Omega) (hT : MeasurePreserving T mu mu) (f : RealL2 Omega mu),
      Tendsto (fun n : Nat => CesaroAverage T hT n f) atTop
        (nhds (InvariantProjection T hT f))

def mutationChangedAveragesToPositiveLength : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (T : Omega -> Omega) (hT : MeasurePreserving T mu mu) (f : RealL2 Omega mu),
      Tendsto (fun n : Nat => CesaroAverage T hT (n + 1) f) atTop
        (nhds (InvariantProjection T hT f))

def mutationChangedLimitToInput : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (T : Omega -> Omega) (hT : MeasurePreserving T mu mu) (f : RealL2 Omega mu),
      Tendsto (fun n : Nat => CesaroAverage T hT n f) atTop (nhds f)

def mutationExistentialTransformation : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu] (f : RealL2 Omega mu),
      exists (T : Omega -> Omega) (hT : MeasurePreserving T mu mu),
        Tendsto (fun n : Nat => CesaroAverage T hT n f) atTop
          (nhds (InvariantProjection T hT f))

/-- The zero-length average is included and is zero by the pinned definition. -/
theorem zeroLengthAverage {Omega : Type u} [MeasurableSpace Omega]
    {mu : Measure Omega} (T : Omega -> Omega) (hT : MeasurePreserving T mu mu)
    (f : RealL2 Omega mu) : CesaroAverage T hT 0 f = 0 := by
  simp [CesaroAverage, birkhoffAverage]

end Stage1Instances.THM_M_1054

set_option pp.explicit true in
#print Stage1Instances.THM_M_1054.VonNeumannL2MeanErgodicTarget
