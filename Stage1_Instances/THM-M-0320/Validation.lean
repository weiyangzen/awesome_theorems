import Statement
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-0320 differential validation

This module imports neither `Proof` nor `ObligationTree`. It independently
rechecks the closed-graph bridge and the final conditional composition against
the unchanged canonical statement. The closed-graph Kakutani core remains an
explicit premise here, so this is a useful no-import differential check rather
than a second proof of the exact root or an independent release attestation.
-/

namespace Stage1Instances.THM_M_0320.Validation

open Filter Set

abbrev E (n : Nat) := EuclideanSpace Real (Fin n)

/-- An independently restated graph convention for differential checking. -/
def CorrespondenceGraph {n : Nat} (K : Set (E n))
    (F : E n -> Set (E n)) : Set (E n × E n) :=
  {p | p.1 ∈ K ∧ p.2 ∈ F p.1}

/-- The closed-graph core interface restated without importing the proof
architecture module. This proposition is only a premise of the differential
composition theorem below. -/
def ClosedGraphKakutaniCore : Prop :=
  forall (n : Nat) (K : Set (E n)) (F : E n -> Set (E n)),
    K.Nonempty -> IsCompact K -> Convex Real K ->
    (forall x, x ∈ K -> (F x).Nonempty) ->
    (forall x, x ∈ K -> IsClosed (F x)) ->
    (forall x, x ∈ K -> Convex Real (F x)) ->
    (forall x, x ∈ K -> F x ⊆ K) ->
    IsClosed (CorrespondenceGraph K F) ->
    exists x, x ∈ K ∧ x ∈ F x

/-- Independent replay of the Euclidean compactness transport. -/
theorem compact_of_closed_bounded {n : Nat} {K : Set (E n)}
    (hclosed : IsClosed K) (hbounded : Bornology.IsBounded K) : IsCompact K :=
  Metric.isCompact_of_isClosed_isBounded hclosed hbounded

/-- Independent replay of the upper-hemicontinuity-to-closed-graph bridge. -/
theorem upperHemicontinuity_closedGraph
    (n : Nat) (K : Set (E n)) (F : E n -> Set (E n))
    (hK : IsClosed K)
    (hF : forall x, x ∈ K -> IsClosed (F x))
    (hupper : UpperHemicontinuousOn F K) :
    IsClosed (CorrespondenceGraph K F) := by
  apply IsSeqClosed.isClosed
  intro u p hu hp
  have hx_tendsto : Tendsto (fun i => (u i).1) atTop (nhds p.1) :=
    (continuous_fst.tendsto p).comp hp
  have hy_tendsto : Tendsto (fun i => (u i).2) atTop (nhds p.2) :=
    (continuous_snd.tendsto p).comp hp
  have hx_mem : p.1 ∈ K :=
    hK.mem_of_tendsto hx_tendsto (Eventually.of_forall fun i => (hu i).1)
  have hsubtype_tendsto :
      Tendsto (fun i => (⟨(u i).1, (hu i).1⟩ : K)) atTop
        (nhds ⟨p.1, hx_mem⟩) :=
    tendsto_subtype_rng.mpr hx_tendsto
  have hupper_restrict : UpperHemicontinuous (K.restrict F) :=
    upperHemicontinuousOn_iff_restrict.mpr hupper
  refine ⟨hx_mem, ?_⟩
  exact (hupper_restrict.upperHemicontinuousAt ⟨p.1, hx_mem⟩).mem_of_tendsto
    (hF p.1 hx_mem) hsubtype_tendsto
    (Frequently.of_forall fun i => (hu i).2) hy_tendsto

/-- Independent conditional recomposition of the exact canonical target. The
core argument is intentionally visible and receives no proof credit. -/
theorem kakutaniFixedPoint_conditional
    (core : ClosedGraphKakutaniCore) : KakutaniFixedPointTarget := by
  intro n K F hne hclosed hbounded hconv hnonempty hvalueClosed hvalueConvex
    hmaps hupper
  exact core n K F hne (compact_of_closed_bounded hclosed hbounded) hconv
    hnonempty hvalueClosed hvalueConvex hmaps
    (upperHemicontinuity_closedGraph n K F hclosed hvalueClosed hupper)

end Stage1Instances.THM_M_0320.Validation

assert_no_sorry Stage1Instances.THM_M_0320.Validation.compact_of_closed_bounded
assert_no_sorry Stage1Instances.THM_M_0320.Validation.upperHemicontinuity_closedGraph
assert_no_sorry Stage1Instances.THM_M_0320.Validation.kakutaniFixedPoint_conditional
#print sorries Stage1Instances.THM_M_0320.Validation.compact_of_closed_bounded
#print sorries Stage1Instances.THM_M_0320.Validation.upperHemicontinuity_closedGraph
#print sorries Stage1Instances.THM_M_0320.Validation.kakutaniFixedPoint_conditional
#print axioms Stage1Instances.THM_M_0320.Validation.compact_of_closed_bounded
#print axioms Stage1Instances.THM_M_0320.Validation.upperHemicontinuity_closedGraph
#print axioms Stage1Instances.THM_M_0320.Validation.kakutaniFixedPoint_conditional
