import ObligationTree
import Birkhoff

/-!
# THM-M-1522 proof execution

This module packages the ported pointwise theorem at the two interfaces frozen
by `ObligationTree.lean`, then composes those bodies into the exact canonical
target. It also checks the port's direct exact-root theorem independently.
-/

open Filter MeasureTheory

namespace Stage1Instances.THM_M_1522

universe u

/-- The ported general Birkhoff theorem, with its invariant conditional
expectation and integral identity, realizes the frozen pointwise package. -/
theorem generalPointwiseLimitPackage : GeneralPointwiseLimitPackage.{u} := by
  intro X _ mu _ T f hT hf
  let g : X -> Real := mu[f | MeasurableSpace.invariants T]
  refine ⟨g, ErgodicTheory.tendsto_birkhoffAverage_ae hT.toMeasurePreserving hf, ?_⟩
  refine ⟨integrable_condExp, ?_, integral_condExp (MeasurableSpace.invariants_le T)⟩
  have hcomp : g ∘ T =ᵐ[mu] g :=
    ErgodicTheory.condExp_invariants_comp_self hT.toMeasurePreserving hT.measurable hf
  simpa only [Function.comp_apply] using hcomp

/-- An integrable invariant limit is a.e. constant under ergodicity; equality
of integrals and probability normalization identify that constant. -/
theorem ergodicInvariantLimitIdentification :
    ErgodicInvariantLimitIdentification.{u} := by
  intro X _ mu _ T f g hT _ hdata
  obtain ⟨hg, hginvariant, hintegral⟩ := hdata
  obtain ⟨c, hc⟩ := hT.ae_eq_const_of_ae_eq_comp_ae hg.1 <| by
    simpa only [Function.comp_apply] using hginvariant
  have hgc : integral mu g = c := by
    calc
      integral mu g = integral mu (Function.const X c) := integral_congr_ae hc
      _ = c := integral_eq_const (Eventually.of_forall fun _ => rfl)
  filter_upwards [hc] with x hx
  exact hx.trans (hgc.symm.trans hintegral)

/-- Exact root obtained through the child-to-parent composition fixed before
proof search. -/
theorem birkhoffPointwiseErgodicViaFrozenComposition :
    BirkhoffPointwiseErgodicTarget.{u} :=
  root_of_pointwise_and_identification
    generalPointwiseLimitPackage ergodicInvariantLimitIdentification

/-- Independent exact-type adapter to the port's terminal ergodic corollary. -/
theorem birkhoffPointwiseErgodicDirect :
    BirkhoffPointwiseErgodicTarget.{u} := by
  intro X _ mu _ T f hT hf
  exact ErgodicTheory.tendsto_birkhoffAverage_ae_integral hT hf

#check generalPointwiseLimitPackage
#check ergodicInvariantLimitIdentification
#check birkhoffPointwiseErgodicViaFrozenComposition
#check birkhoffPointwiseErgodicDirect
#print sorries ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg
#print sorries ErgodicTheory.tendsto_birkhoffAverage_ae
#print sorries ErgodicTheory.tendsto_birkhoffAverage_ae_integral
#print sorries generalPointwiseLimitPackage
#print sorries ergodicInvariantLimitIdentification
#print sorries birkhoffPointwiseErgodicViaFrozenComposition
#print sorries birkhoffPointwiseErgodicDirect
#print axioms ErgodicTheory.setIntegral_birkhoffSum_pos_nonneg
#print axioms ErgodicTheory.tendsto_birkhoffAverage_ae
#print axioms ErgodicTheory.tendsto_birkhoffAverage_ae_integral
#print axioms generalPointwiseLimitPackage
#print axioms ergodicInvariantLimitIdentification
#print axioms birkhoffPointwiseErgodicViaFrozenComposition
#print axioms birkhoffPointwiseErgodicDirect

end Stage1Instances.THM_M_1522
