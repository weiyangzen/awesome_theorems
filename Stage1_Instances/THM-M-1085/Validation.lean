import Stage1_Instances.«THM-M-1085».LawReduction

/-!
# THM-M-1085 validation probes

This module independently reconstructs two implemented finite-law transport results. It does not
provide an inhabitant of `LawSlepianTarget` and therefore does not prove Slepian's lemma.
-/

noncomputable section

open MeasureTheory ProbabilityTheory Set

namespace Stage1Instances.THM_M_1085.Validation

universe u v w

/-- Differential reconstruction of lower-orthant transport to the vector's pushforward law. -/
theorem independentlyReconstructedMapBelowAll {I : Type u} [Fintype I]
    {Omega : Type v} [MeasurableSpace Omega] {mu : Measure Omega}
    {X : Omega -> I -> Real} (hX : HasGaussianLaw X mu) (t : Real) :
    mu.map X {x : I -> Real | forall i, x i <= t} =
      mu (Stage1Instances.THM_M_1085.BelowAll X t) := by
  rw [Measure.map_apply_of_aemeasurable hX.aemeasurable
    (Proof.measurableSet_belowAllRange t)]
  rfl

/-- Differential reconstruction of the covariance-order data produced by the frozen hypotheses. -/
theorem independentlyReconstructedCovarianceOrder {I : Type u} [Fintype I]
    {OmegaX : Type v} [MeasurableSpace OmegaX] {muX : Measure OmegaX}
    {OmegaY : Type w} [MeasurableSpace OmegaY] {muY : Measure OmegaY}
    {X : OmegaX -> I -> Real} {Y : OmegaY -> I -> Real}
    (hX : HasGaussianLaw X muX) (hY : HasGaussianLaw Y muY)
    (hdiag : forall i,
      covariance (fun omega => X omega i) (fun omega => X omega i) muX =
        covariance (fun omega => Y omega i) (fun omega => Y omega i) muY)
    (hoff : forall i j, Not (i = j) ->
      covariance (fun omega => X omega i) (fun omega => X omega j) muX <=
        covariance (fun omega => Y omega i) (fun omega => Y omega j) muY) :
    (Proof.covarianceMatrix muX X).PosSemidef /\
      (Proof.covarianceMatrix muY Y).PosSemidef /\
      (forall i, Proof.covarianceMatrix muX X i i = Proof.covarianceMatrix muY Y i i) /\
      (forall i j, Not (i = j) ->
        Proof.covarianceMatrix muX X i j <= Proof.covarianceMatrix muY Y i j) := by
  refine ⟨Proof.covarianceMatrix_posSemidef hX, Proof.covarianceMatrix_posSemidef hY, ?_, ?_⟩
  · intro i
    exact Proof.covarianceMatrix_diag_eq hdiag i
  · intro i j hij
    exact Proof.covarianceMatrix_offdiag_le hoff i j hij

#print sorries Stage1Instances.THM_M_1085.Validation.independentlyReconstructedMapBelowAll
#print axioms Stage1Instances.THM_M_1085.Validation.independentlyReconstructedMapBelowAll
#print sorries Stage1Instances.THM_M_1085.Validation.independentlyReconstructedCovarianceOrder
#print axioms Stage1Instances.THM_M_1085.Validation.independentlyReconstructedCovarianceOrder

end Stage1Instances.THM_M_1085.Validation
