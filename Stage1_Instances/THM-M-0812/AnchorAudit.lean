import Mathlib.Combinatorics.Hall.Basic
import Mathlib.Combinatorics.SimpleGraph.Bipartite
import Mathlib.Combinatorics.SimpleGraph.Hall
import Mathlib.Combinatorics.SimpleGraph.Matching
import Mathlib.Combinatorics.SimpleGraph.VertexCover
import Mathlib.Data.Finite.Card
import Mathlib.Data.Set.Card
import Mathlib.Util.AssertNoSorry

/-!
# THM-M-0812 immutable anchor probe

This module repeats the frozen two-sorted finite-incidence target and checks the closest
manifest-pinned mathlib interfaces. It deliberately declares no inhabitant of `ExactTarget`:
the pinned library has matching, vertex-cover, and Hall infrastructure, but no Konig
matching-cover equality or maximum-matching-number interface.
-/

set_option autoImplicit false

namespace Stage1Instances.THM_M_0812

universe uL uR uE

/-- Audit copy of the frozen edge-matching predicate. -/
def IsEdgeMatching {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R) (M : Set E) : Prop :=
  Set.InjOn left M /\ Set.InjOn right M

/-- Audit copy of the frozen two-sided vertex-cover predicate. -/
def IsBipartiteVertexCover {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R) (CLeft : Set L) (CRight : Set R) : Prop :=
  forall e : E, left e ∈ CLeft \/ right e ∈ CRight

/-- Audit copy of the attained maximum matching number predicate. -/
def HasMatchingNumber {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R) (k : Nat) : Prop :=
  (exists M : Set E, IsEdgeMatching left right M /\ M.ncard = k) /\
    forall M : Set E, IsEdgeMatching left right M -> M.ncard <= k

/-- Audit copy of the attained minimum vertex-cover number predicate. -/
def HasVertexCoverNumber {L : Type uL} {R : Type uR} {E : Type uE}
    (left : E -> L) (right : E -> R) (k : Nat) : Prop :=
  (exists CLeft : Set L, exists CRight : Set R,
      IsBipartiteVertexCover left right CLeft CRight /\
        CLeft.ncard + CRight.ncard = k) /\
    forall (CLeft : Set L) (CRight : Set R),
      IsBipartiteVertexCover left right CLeft CRight ->
        k <= CLeft.ncard + CRight.ncard

/-- Literal audit copy of the statement phase's canonical proposition. -/
def ExactTarget : Prop :=
  forall (L : Type uL) (R : Type uR) (E : Type uE)
    [Finite L] [Finite R] [Finite E]
    (left : E -> L) (right : E -> R),
      exists k : Nat,
        HasMatchingNumber left right k /\
          HasVertexCoverNumber left right k

-- The closest pinned simple-graph representation interfaces.
#check SimpleGraph.IsBipartiteWith
#check SimpleGraph.IsBipartite
#check SimpleGraph.Subgraph.IsMatching
#check SimpleGraph.Subgraph.IsMatching.toEdge
#check SimpleGraph.IsVertexCover
#check SimpleGraph.vertexCoverNum

-- Proof-bearing extrema/Hall support, not a proof of the target.
#check SimpleGraph.vertexCoverNum_exists
#check SimpleGraph.exists_isMatching_of_forall_ncard_le
#check SimpleGraph.exists_isPerfectMatching_of_forall_ncard_le
#check Finset.all_card_le_biUnion_card_iff_exists_injective

-- Adjacent declarations do not have the root's type.
#check_failure (SimpleGraph.vertexCoverNum_exists : ExactTarget.{uL, uR, uE})
#check_failure
  (SimpleGraph.exists_isMatching_of_forall_ncard_le : ExactTarget.{uL, uR, uE})

#print sorries SimpleGraph.vertexCoverNum_exists
#print sorries SimpleGraph.exists_isMatching_of_forall_ncard_le
#print sorries SimpleGraph.exists_isPerfectMatching_of_forall_ncard_le
#print sorries Finset.all_card_le_biUnion_card_iff_exists_injective
#print axioms SimpleGraph.vertexCoverNum_exists
#print axioms SimpleGraph.exists_isMatching_of_forall_ncard_le
#print axioms SimpleGraph.exists_isPerfectMatching_of_forall_ncard_le
#print axioms Finset.all_card_le_biUnion_card_iff_exists_injective

end Stage1Instances.THM_M_0812

set_option pp.explicit true in
set_option pp.universes true in
#print Stage1Instances.THM_M_0812.ExactTarget
