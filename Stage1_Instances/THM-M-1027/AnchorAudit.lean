import Mathlib.Probability.Distributions.Gaussian.IsGaussianProcess.Basic
import Mathlib.Probability.Distributions.Gaussian.Real
import Mathlib.Probability.Independence.Process.HasIndepIncrements
import Mathlib.Probability.Process.Kolmogorov

/-!
# THM-M-1027 anchor-audit probe

This module checks the relevant declarations available in the pinned local
mathlib closure and a typed contract for the external Brownian construction.
It does not import that external project or prove Wiener-process existence.
-/

noncomputable section

open MeasureTheory ProbabilityTheory
open scoped NNReal

namespace Stage1Instances.THM_M_1027

universe u

/-- Local aliases matching the already-elaborated frozen statement module. -/
abbrev AuditTime := NNReal
abbrev AuditRealProcess (Omega : Type u) := AuditTime -> Omega -> Real

def AuditIncrementVariance (s t : AuditTime) (hst : s <= t) : NNReal :=
  ⟨(t : Real) - (s : Real), sub_nonneg.mpr (by exact_mod_cast hst)⟩

#check ProbabilityTheory.IsGaussianProcess
#check ProbabilityTheory.IsGaussianProcess.aemeasurable
#check ProbabilityTheory.IsGaussianProcess.hasGaussianLaw_eval
#check ProbabilityTheory.HasIndepIncrements
#check ProbabilityTheory.HasIndepIncrements.indepFun_sub_sub
#check ProbabilityTheory.IsKolmogorovProcess
#check ProbabilityTheory.gaussianReal
#check ProbabilityTheory.HasLaw

/--
The exact component interface that an imported continuous Brownian construction
must satisfy to witness the frozen target. The external candidate is expected
to supply these fields, but this structure itself gives no existence proof.
-/
structure ExternalCandidateContract (Omega : Type u) [MeasurableSpace Omega]
    (P : Measure Omega) (W : AuditRealProcess Omega) : Prop where
  probability : IsProbabilityMeasure P
  measurable : forall t : AuditTime, Measurable (W t)
  startsAtZero : Filter.Eventually (fun omega => W 0 omega = 0) (ae P)
  incrementLaw : forall {s t : AuditTime}, (hst : s <= t) ->
    HasLaw (fun omega => W t omega - W s omega)
      (gaussianReal 0 (AuditIncrementVariance s t hst)) P
  independentIncrements : HasIndepIncrements W P
  continuousPaths : forall omega, Continuous (fun t : AuditTime => W t omega)

/-- Checked composition to the direct expansion of the exact frozen root. -/
theorem externalCandidateContract_expands_frozen_root
    {Omega : Type u} [MeasurableSpace Omega] {P : Measure Omega}
    {W : AuditRealProcess Omega} (h : ExternalCandidateContract Omega P W) :
    IsProbabilityMeasure P /\
      (forall t : AuditTime, Measurable (W t)) /\
      Filter.Eventually (fun omega => W 0 omega = 0) (ae P) /\
      (forall {s t : AuditTime}, (hst : s <= t) ->
        HasLaw (fun omega => W t omega - W s omega)
          (gaussianReal 0 (AuditIncrementVariance s t hst)) P) /\
      HasIndepIncrements W P /\
      Filter.Eventually
        (fun omega => Continuous (fun t : AuditTime => W t omega)) (ae P) := by
  exact ⟨h.probability, h.measurable, h.startsAtZero, h.incrementLaw,
    h.independentIncrements, Filter.Eventually.of_forall h.continuousPaths⟩

end Stage1Instances.THM_M_1027
