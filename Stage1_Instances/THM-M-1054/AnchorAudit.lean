import Mathlib.Analysis.InnerProductSpace.MeanErgodic
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Function.LpSpace.Basic

/-!
# THM-M-1054: pinned anchor audit

This module checks the pinned mathlib theorem against the exact statement
shape frozen in `Statement.lean`. It is candidate evidence only; the later
proof node owns any repo-local proof credit.
-/

noncomputable section

open Filter MeasureTheory
open scoped ENNReal Topology

namespace Stage1Instances.THM_M_1054.AnchorAudit

universe u

abbrev RealL2 (Omega : Type u) [MeasurableSpace Omega] (mu : Measure Omega) :=
  Lp Real (2 : ENNReal) mu

abbrev Koopman {Omega : Type u} [MeasurableSpace Omega] {mu : Measure Omega}
    (T : Omega -> Omega) (hT : MeasurePreserving T mu mu) :=
  (Lp.compMeasurePreservingₗᵢ Real (E := Real) (p := (2 : ENNReal)) T hT).toContinuousLinearMap

abbrev CesaroAverage {Omega : Type u} [MeasurableSpace Omega] {mu : Measure Omega}
    (T : Omega -> Omega) (hT : MeasurePreserving T mu mu) :
    Nat -> RealL2 Omega mu -> RealL2 Omega mu :=
  birkhoffAverage Real (Koopman T hT) _root_.id

abbrev InvariantProjection {Omega : Type u} [MeasurableSpace Omega]
    {mu : Measure Omega} (T : Omega -> Omega)
    (hT : MeasurePreserving T mu mu) (f : RealL2 Omega mu) : RealL2 Omega mu :=
  ((LinearMap.eqLocus (Koopman T hT) 1).orthogonalProjection (𝕜 := Real) f : RealL2 Omega mu)

/-- Exact-shape feasibility check for the pinned abstract mean-ergodic anchor. -/
theorem mathlibCandidateChecksExactTarget :
    forall (Omega : Type u) [MeasurableSpace Omega]
      (mu : Measure Omega) [IsProbabilityMeasure mu]
      (T : Omega -> Omega) (hT : MeasurePreserving T mu mu)
      (f : RealL2 Omega mu),
        Tendsto (fun n : Nat => CesaroAverage T hT n f) atTop
          (nhds (InvariantProjection T hT f)) := by
  intro Omega _ mu _ T hT f
  cases subsingleton_or_nontrivial (RealL2 Omega mu)
  · have hfun : (fun n : Nat => CesaroAverage T hT n f) =
        fun _ => InvariantProjection T hT f := by
      funext n
      exact Subsingleton.elim _ _
    rw [hfun]
    exact tendsto_const_nhds
  · apply ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection
    exact (Lp.compMeasurePreservingₗᵢ Real (E := Real) (p := (2 : ENNReal)) T hT).norm_toContinuousLinearMap.le

end Stage1Instances.THM_M_1054.AnchorAudit

#check ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection
#check MeasureTheory.Lp.compMeasurePreservingₗᵢ
#print axioms ContinuousLinearMap.tendsto_birkhoffAverage_orthogonalProjection
#print axioms Stage1Instances.THM_M_1054.AnchorAudit.mathlibCandidateChecksExactTarget
