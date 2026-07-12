import Statement

/-!
# THM-M-0320 obligation interfaces

These declarations check the composition shape frozen by the obligation
registry.  The closed-graph Kakutani core and the upper-hemicontinuity bridge
remain explicit premises; this file does not prove the root theorem.
-/

namespace Stage1Instances.THM_M_0320

open Set

abbrev E (n : Nat) := EuclideanSpace Real (Fin n)

/-- The graph convention used at the boundary to the audited external proof. -/
def CorrespondenceGraph {n : Nat} (K : Set (E n)) (F : E n -> Set (E n)) :
    Set (E n × E n) :=
  {p | p.1 ∈ K ∧ p.2 ∈ F p.1}

/-- The exact closed-graph core required from a locally integrated Kakutani proof. -/
def ClosedGraphKakutaniCore : Prop :=
  forall (n : Nat) (K : Set (E n)) (F : E n -> Set (E n)),
    K.Nonempty -> IsCompact K -> Convex Real K ->
    (forall x, x ∈ K -> (F x).Nonempty) ->
    (forall x, x ∈ K -> IsClosed (F x)) ->
    (forall x, x ∈ K -> Convex Real (F x)) ->
    (forall x, x ∈ K -> F x ⊆ K) ->
    IsClosed (CorrespondenceGraph K F) ->
    exists x, x ∈ K ∧ x ∈ F x

/-- The regularity transport still needed between mathlib's
`UpperHemicontinuousOn` interface and the closed-graph core. -/
def UpperHemicontinuityClosedGraphBridge : Prop :=
  forall (n : Nat) (K : Set (E n)) (F : E n -> Set (E n)),
    IsClosed K ->
    (forall x, x ∈ K -> IsClosed (F x)) ->
    UpperHemicontinuousOn F K ->
    IsClosed (CorrespondenceGraph K F)

/-- Closed and bounded subsets of the frozen Euclidean domain are compact. -/
theorem compact_of_closed_bounded {n : Nat} {K : Set (E n)}
    (hclosed : IsClosed K) (hbounded : Bornology.IsBounded K) : IsCompact K :=
  Metric.isCompact_of_isClosed_isBounded hclosed hbounded

/-- Checked child-to-parent composition.  Its two package arguments are the
open root cut set; they receive no proof credit merely from this theorem. -/
theorem root_of_closedGraph_packages
    (core : ClosedGraphKakutaniCore)
    (graphBridge : UpperHemicontinuityClosedGraphBridge) :
    KakutaniFixedPointTarget := by
  intro n K F hne hclosed hbounded hconv hnonempty hvalueClosed hvalueConvex
    hmaps hupper
  exact core n K F hne (compact_of_closed_bounded hclosed hbounded) hconv
    hnonempty hvalueClosed hvalueConvex hmaps
    (graphBridge n K F hclosed hvalueClosed hupper)

#print axioms compact_of_closed_bounded
#print axioms root_of_closedGraph_packages

end Stage1Instances.THM_M_0320
