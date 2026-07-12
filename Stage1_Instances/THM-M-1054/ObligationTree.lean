import Statement

/-!
# THM-M-1054 conditional obligation composition

This module checks the composition boundary selected before proof credit is
observed.  The nontrivial mean-ergodic package is an explicit premise; this
file does not assert that package or the canonical root.
-/

noncomputable section

open Filter MeasureTheory
open scoped ENNReal Topology

namespace Stage1Instances.THM_M_1054

universe u

/-- The precise abstract result still required after the Koopman construction,
contractivity fact, and subsingleton edge case have been separated. -/
def NontrivialMeanErgodicPackage : Prop :=
  forall (Omega : Type u) [MeasurableSpace Omega]
    (mu : Measure Omega) [IsProbabilityMeasure mu]
    (T : Omega -> Omega) (hT : MeasurePreserving T mu mu)
    (f : RealL2 Omega mu) [Nontrivial (RealL2 Omega mu)],
      norm (Koopman T hT) <= 1 ->
        Tendsto (fun n : Nat => CesaroAverage T hT n f) atTop
          (nhds (InvariantProjection T hT f))

/-- Checked child-to-parent composition.  It closes the degenerate L2 branch
and obtains Koopman contractivity from the pinned linear isometry, but leaves
the nontrivial abstract mean-ergodic result as an explicit input. -/
theorem root_of_nontrivialMeanErgodicPackage
    (meanErgodic : NontrivialMeanErgodicPackage.{u}) :
    VonNeumannL2MeanErgodicTarget.{u} := by
  intro Omega _ mu _ T hT f
  cases subsingleton_or_nontrivial (RealL2 Omega mu)
  · have hfun : (fun n : Nat => CesaroAverage T hT n f) =
        fun _ => InvariantProjection T hT f := by
      funext n
      exact Subsingleton.elim _ _
    rw [hfun]
    exact tendsto_const_nhds
  · apply meanErgodic Omega mu T hT f
    exact (Lp.compMeasurePreservingₗᵢ Real (E := Real) (p := (2 : ENNReal)) T hT).norm_toContinuousLinearMap.le

#print axioms root_of_nontrivialMeanErgodicPackage

end Stage1Instances.THM_M_1054
